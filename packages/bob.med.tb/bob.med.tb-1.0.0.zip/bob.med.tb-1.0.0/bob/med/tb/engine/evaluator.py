#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Defines functionality for the evaluation of predictions"""

import os

import numpy
import pandas as pd
import matplotlib.pyplot as plt
import re

import torch
from sklearn import metrics
from bob.measure import eer_threshold

from ..utils.measure import base_measures, get_centered_maxf1

import logging

logger = logging.getLogger(__name__)


def posneg(pred, gt, threshold):
    """Calculates true and false positives and negatives"""

    # threshold
    binary_pred = torch.gt(pred, threshold)

    # equals and not-equals
    equals = torch.eq(binary_pred, gt).type(torch.uint8)
    notequals = torch.ne(binary_pred, gt).type(torch.uint8)

    # true positives
    tp_tensor = (gt * binary_pred).type(torch.uint8)

    # false positives
    fp_tensor = torch.eq((binary_pred + tp_tensor), 1).type(torch.uint8)

    # true negatives
    tn_tensor = (equals - tp_tensor).type(torch.uint8)

    # false negatives
    fn_tensor = notequals - fp_tensor.type(torch.uint8)

    return tp_tensor, fp_tensor, tn_tensor, fn_tensor

def sample_measures_for_threshold(pred, gt, threshold):
    """
    Calculates measures on one single sample, for a specific threshold


    Parameters
    ----------

    pred : torch.Tensor
        pixel-wise predictions

    gt : torch.Tensor
        ground-truth (annotations)

    threshold : float
        a particular threshold in which to calculate the performance
        measures


    Returns
    -------

    precision: float

    recall: float

    specificity: float

    accuracy: float

    jaccard: float

    f1_score: float

    """

    tp_tensor, fp_tensor, tn_tensor, fn_tensor = posneg(pred, gt, threshold)

    # calc measures from scalars
    tp_count = torch.sum(tp_tensor).item()
    fp_count = torch.sum(fp_tensor).item()
    tn_count = torch.sum(tn_tensor).item()
    fn_count = torch.sum(fn_tensor).item()
    return base_measures(tp_count, fp_count, tn_count, fn_count)

def run(
    dataset,
    name,
    predictions_folder,
    output_folder=None,
    f1_thresh=None,
    eer_thresh=None,
    steps=1000,
):
    """
    Runs inference and calculates measures


    Parameters
    ---------

    dataset : py:class:`torch.utils.data.Dataset`
        a dataset to iterate on

    name : str
        the local name of this dataset (e.g. ``train``, or ``test``), to be
        used when saving measures files.

    predictions_folder : str
        folder where predictions for the dataset images has been previously
        stored

    output_folder : :py:class:`str`, Optional
        folder where to store results.

    f1_thresh : :py:class:`float`, Optional
        This number should come from
        the training set or a separate validation set.  Using a test set value
        may bias your analysis.  This number is also used to print the a priori
        F1-score on the evaluated set.

    eer_thresh : :py:class:`float`, Optional
        This number should come from
        the training set or a separate validation set.  Using a test set value
        may bias your analysis.  This number is used to print the a priori
        EER.

    steps : :py:class:`float`, Optional
        number of threshold steps to consider when evaluating thresholds.


    Returns
    -------

    f1_threshold : float
        Threshold to achieve the highest possible F1-score for this dataset

    eer_threshold : float
        Threshold achieving Equal Error Rate for this dataset

    """

    predictions_path = os.path.join(predictions_folder, name, "predictions.csv")
    if not os.path.exists(predictions_path):
        predictions_path = predictions_folder

    # Load predictions
    pred_data = pd.read_csv(predictions_path)
    pred = torch.Tensor([eval(re.sub(' +', ' ', x.replace('\n', '')).replace(' ', ',')) for x in pred_data['likelihood'].values]).double()
    gt = torch.Tensor([eval(re.sub(' +', ' ', x.replace('\n', '')).replace(' ', ',')) for x in pred_data['ground_truth'].values]).double()

    if pred.shape[1] == 1 and gt.shape[1] == 1:
        pred = torch.flatten(pred)
        gt = torch.flatten(gt)

    pred_data['likelihood'] = pred
    pred_data['ground_truth'] = gt

    # Multiclass f1 score computation
    if pred.ndim > 1:
        auc = metrics.roc_auc_score(gt, pred)
        logger.info("Evaluating multiclass classification")
        logger.info(f"AUC: {auc}")
        logger.info("F1 and EER are not implemented for multiclass")
        
        return None, None
    
    # Generate measures for each threshold
    step_size = 1.0 / steps
    data = [
        (index, threshold) + sample_measures_for_threshold(pred, gt, threshold)
        for index, threshold in enumerate(numpy.arange(0.0, 1.0, step_size))
    ]

    data_df = pd.DataFrame(
        data,
        columns=(
            "index",
            "threshold",
            "precision",
            "recall",
            "specificity",
            "accuracy",
            "jaccard",
            "f1_score",
        )
    )
    data_df = data_df.set_index("index")

    # Save evaluation csv
    if output_folder is not None:
        fullpath = os.path.join(output_folder, f"{name}.csv")
        logger.info(f"Saving {fullpath}...")
        os.makedirs(os.path.dirname(fullpath), exist_ok=True)
        data_df.to_csv(fullpath)

    # Find max F1 score
    f1_scores = numpy.asarray(data_df["f1_score"])
    thresholds = numpy.asarray(data_df["threshold"])

    maxf1, maxf1_threshold = get_centered_maxf1(
            f1_scores,
            thresholds
        )

    logger.info(
        f"Maximum F1-score of {maxf1:.5f}, achieved at "
        f"threshold {maxf1_threshold:.3f} (chosen *a posteriori*)"
    )

    # Find EER
    neg_gt = pred_data.loc[pred_data.loc[:, 'ground_truth'] == 0, :]
    pos_gt = pred_data.loc[pred_data.loc[:, 'ground_truth'] == 1, :]
    post_eer_threshold = eer_threshold(neg_gt['likelihood'], pos_gt['likelihood'])

    logger.info(
        f"Equal error rate achieved at "
        f"threshold {post_eer_threshold:.3f} (chosen *a posteriori*)"
    )

    # Save score table
    if output_folder is not None:
        fig, axes = plt.subplots(1)
        fig.tight_layout(pad=3.0)

        # Names and bounds
        axes.set_xlabel("Score")
        axes.set_ylabel("Normalized counts")
        axes.set_xlim(0.0, 1.0)

        neg_weights = numpy.ones_like(neg_gt['likelihood']) / len(pred_data['likelihood'])
        pos_weights = numpy.ones_like(pos_gt['likelihood']) / len(pred_data['likelihood'])

        axes.hist(
            [neg_gt['likelihood'], pos_gt['likelihood']], 
            weights=[neg_weights, pos_weights],
            bins=100, color=['tab:blue', 'tab:orange'], 
            label=["Negatives", "Positives"])
        axes.legend(prop={'size': 10}, loc="upper center")
        axes.set_title(f"Score table for {name} subset")

        # we should see some of axes 1 axes
        axes.spines["right"].set_visible(False)
        axes.spines["top"].set_visible(False)
        axes.spines["left"].set_position(("data", -0.015))

        fullpath = os.path.join(output_folder, f"{name}_score_table.pdf")
        fig.savefig(fullpath)

    if f1_thresh is not None and eer_thresh is not None:

        # get the closest possible threshold we have
        index = int(round(steps * f1_thresh))
        f1_a_priori = data_df["f1_score"][index]
        actual_threshold = data_df["threshold"][index]

        logger.info(
            f"F1-score of {f1_a_priori:.5f}, at threshold "
            f"{actual_threshold:.3f} (chosen *a priori*)"
        )

        # Print the a priori EER threshold
        logger.info(
            f"Equal error rate (chosen *a priori*) {eer_thresh:.3f}"
        )
    
    return maxf1_threshold, post_eer_threshold

        # from matplotlib.backends.backend_pdf import PdfPages

        # fname = os.path.join(output_folder, name + ".pdf")
        # os.makedirs(os.path.dirname(fname), exist_ok=True)
        
        # with PdfPages(fname) as pdf:
            
        #     fig, axes = plt.subplots(2, 2, figsize=(12.8, 9.6))
        #     fig.suptitle(f"Subset: {name}", fontsize=16, fontweight='semibold')
        #     axes = axes.flatten()
            
        #     # Tight layout often produces nice results
        #     # but requires the title to be spaced accordingly
        #     fig.tight_layout(pad=3.0)
        #     fig.subplots_adjust(top=0.92)
            
        #     # ------------
        #     # Score table
        #     # ------------

        #     axes[0].set_xlim(0.0, 1.0)
        #     axes[0].hist(
        #         [neg_gt['likelihood'], pos_gt['likelihood']], 
        #         bins=30, color=['tab:blue', 'tab:orange'], 
        #         label=["Negatives", "Positives"])
        #     axes[0].legend(prop={'size': 10})
        #     axes[0].set_title("Score table")

        #     # ----------
        #     # ROC Curve
        #     # ----------

        #     # TPR = 1 - FNR
        #     (line,) = axes[1].plot(
        #         1 - data_df['specificity'], 
        #         data_df['recall'], 
        #         color="#1f77b4"
        #     )
        #     auc = roc_auc_score(neg_gt['likelihood'], pos_gt['likelihood'])
        #     axes[1].set(xlabel='1 - specificity', ylabel='Sensitivity',
        #         title=f'ROC curve (AUC={auc:.4f})')
        #     # axes[1].plot([0, 1], [0, 1], color='tab:orange', linestyle='--')
        #     axes[1].grid(linestyle="--", linewidth=1, color="gray", alpha=0.2)
        #     axes[1].set_xlim([0.0, 1.0])
        #     axes[1].set_ylim([0.0, 1.0])

        #     #  Equal Error Rate threshold
        #     EER = eer(neg_gt['likelihood'], pos_gt['likelihood'])
        #     threshold = eer_threshold(neg_gt['likelihood'], pos_gt['likelihood'])
        #     threshold_index = data_df['threshold'].sub(threshold).abs().idxmin()
        #     # hter_threshold = min_hter_threshold(neg_gt['likelihood'], pos_gt['likelihood'])

        #     # Plot EER
        #     (marker,) = axes[1].plot(
        #         1 - data_df["specificity"][threshold_index],
        #         data_df["recall"][threshold_index],
        #         marker="o",
        #         color="tab:blue",
        #         markersize=8
        #     )

        #     # We should see some of axes 1 axes
        #     axes[1].spines["right"].set_visible(False)
        #     axes[1].spines["top"].set_visible(False)
        #     axes[1].spines["left"].set_position(("data", -0.015))
        #     axes[1].spines["bottom"].set_position(("data", -0.015))

        #     # Legend
        #     label = f"{name} set (EER={EER:.4f})"
        #     axes[1].legend(
        #         [tuple([line, marker])],
        #         [label],
        #         loc="lower right",
        #         fancybox=True,
        #         framealpha=0.7,
        #     )

        #     # -----------------------
        #     # Precision-recall Curve
        #     # -----------------------

        #     (line,) = axes[2].plot(data_df['recall'], data_df['precision'])
        #     prc_auc = metrics.auc(data_df['recall'], data_df['precision'])
        #     axes[2].set(xlabel='Recall', ylabel='Precision',
        #         title=f'Precision-recall curve (AUC={prc_auc:.4f})')
        #     axes[2].grid(linestyle="--", linewidth=1, color="gray", alpha=0.2)
        #     axes[2].set_xlim([0.0, 1.0])
        #     axes[2].set_ylim([0.0, 1.0])
            
        #     # Annotates plot with F1-score iso-lines
        #     axes_right = axes[2].twinx()
        #     f_scores_d = numpy.linspace(0.1, 0.9, num=9)
        #     tick_locs = []
        #     tick_labels = []
        #     for f in f_scores_d:
        #         x = numpy.linspace(0.01, 1)
        #         y = f * x / (2 * x - f)
        #         (l,) = axes_right.plot(x[y >= 0], y[y >= 0], color="green", alpha=0.1)
        #         tick_locs.append(y[-1])
        #         tick_labels.append("%.1f" % f)
        #     axes_right.tick_params(axis="y", which="both", pad=0, right=False, left=False)
        #     axes_right.set_ylabel("iso-F", color="green", alpha=0.3)
        #     axes_right.set_ylim([0.0, 1.0])
        #     axes_right.yaxis.set_label_coords(1.015, 0.97)
        #     axes_right.set_yticks(tick_locs)  # notice these are invisible
        #     for k in axes_right.set_yticklabels(tick_labels):
        #         k.set_color("green")
        #         k.set_alpha(0.3)
        #         k.set_size(8)

        #     # We shouldn't see any of axes_right axes
        #     axes_right.spines["right"].set_visible(False)
        #     axes_right.spines["top"].set_visible(False)
        #     axes_right.spines["left"].set_visible(False)
        #     axes_right.spines["bottom"].set_visible(False)

        #     # Plot F1 score
        #     (marker,) = axes[2].plot(
        #         data_df["recall"][maxf1_index],
        #         data_df["precision"][maxf1_index],
        #         marker="o",
        #         color="tab:blue",
        #         markersize=8
        #     )

        #     # We should see some of axes 2 axes
        #     axes[2].spines["right"].set_visible(False)
        #     axes[2].spines["top"].set_visible(False)
        #     axes[2].spines["left"].set_position(("data", -0.015))
        #     axes[2].spines["bottom"].set_position(("data", -0.015))

        #     # Legend
        #     label = f"{name} set (F1={data_df['f1_score'][maxf1_index]:.4f})"
        #     axes[2].legend(
        #         [tuple([line, marker])],
        #         [label],
        #         loc="lower left",
        #         fancybox=True,
        #         framealpha=0.7,
        #     )

        #     # Mean square error given optimal threshold (computed on train set)
        #     ground_truth = pred_data['ground_truth']
        #     likelihood = pred_data['likelihood']
        #     mse_res = mse(likelihood, ground_truth)
        #     text_mse = f"MSE with a threshold of {threshold:.3f}: {mse_res:.3f}"
        #     axes[3].text(0.5, 0.5, text_mse, horizontalalignment="center",
        #         verticalalignment="center")
        #     axes[3].axis('off')

        #     pdf.savefig()
        #     plt.close(fig)

        #     f1_score = f_score(neg_gt['likelihood'], pos_gt['likelihood'], threshold)

        #     logger.info(
        #         f"Maximum F1-score of {f1_score:.5f}, achieved at "
        #         f"threshold {threshold:.3f} (chosen *a priori*)"
        #     )

        #     return threshold