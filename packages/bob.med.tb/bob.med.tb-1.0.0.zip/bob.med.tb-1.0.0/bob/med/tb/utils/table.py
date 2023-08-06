#!/usr/bin/env python
# coding=utf-8


import tabulate
import numpy as np
import torch
from sklearn.metrics import auc, precision_recall_curve as pr_curve, roc_curve as r_curve, f1_score, accuracy_score
from ..engine.evaluator import posneg
from ..utils.measure import bayesian_measures, base_measures


def performance_table(data, fmt):
    """Tables result comparison in a given format


    Parameters
    ----------

    data : dict
        A dictionary in which keys are strings defining plot labels and values
        are dictionaries with two entries:

        * ``df``: :py:class:`pandas.DataFrame`

          A dataframe that is produced by our predictor engine containing 
          the following columns: ``filename``, ``likelihood``, 
          ``ground_truth``.

        * ``threshold``: :py:class:`list`

          A threshold to compute measures.


    fmt : str
        One of the formats supported by tabulate.


    Returns
    -------

    table : str
        A table in a specific format

    """

    headers = [
        "Dataset",
        "T",
        "F1 (95% CI)",
        "Prec (95% CI)",
        "Recall/Sen (95% CI)",
        "Spec (95% CI)",
        "Acc (95% CI)",
        "AUC (PRC)",
        "AUC (ROC)"
        ]

    table = []
    for k, v in data.items():
        entry = [k, v["threshold"], ]

        df = v["df"]

        gt = torch.tensor(df['ground_truth'].values)
        pred = torch.tensor(df['likelihood'].values)
        threshold = v["threshold"]
        
        tp_tensor, fp_tensor, tn_tensor, fn_tensor = posneg(pred, gt, threshold)

        # calc measures from scalars
        tp_count = torch.sum(tp_tensor).item()
        fp_count = torch.sum(fp_tensor).item()
        tn_count = torch.sum(tn_tensor).item()
        fn_count = torch.sum(fn_tensor).item()

        base_m = base_measures(
                tp_count,
                fp_count,
                tn_count,
                fn_count,
            )

        bayes_m = bayesian_measures(
                tp_count,
                fp_count,
                tn_count,
                fn_count,
                lambda_=1,
                coverage=0.95,
            )

        # statistics based on the "assigned" threshold (a priori, less biased)
        entry.append("{:.2f} ({:.2f}, {:.2f})".format(base_m[5], bayes_m[5][2], bayes_m[5][3])) # f1
        entry.append("{:.2f} ({:.2f}, {:.2f})".format(base_m[0], bayes_m[0][2], bayes_m[0][3])) # precision
        entry.append("{:.2f} ({:.2f}, {:.2f})".format(base_m[1], bayes_m[1][2], bayes_m[1][3])) # recall/sensitivity
        entry.append("{:.2f} ({:.2f}, {:.2f})".format(base_m[2], bayes_m[2][2], bayes_m[2][3])) # specificity
        entry.append("{:.2f} ({:.2f}, {:.2f})".format(base_m[3], bayes_m[3][2], bayes_m[3][3])) # accuracy

        prec, recall, _ = pr_curve(gt, pred)
        fpr, tpr, _ = r_curve(gt, pred)

        entry.append(auc(recall, prec))
        entry.append(auc(fpr, tpr))

        table.append(entry)

    return tabulate.tabulate(table, headers, tablefmt=fmt, floatfmt=".3f")