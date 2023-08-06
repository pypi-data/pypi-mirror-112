#!/usr/bin/env python
# -*- coding: utf-8 -*-

import contextlib
from itertools import cycle

import numpy
import pandas
from sklearn.metrics import auc, precision_recall_curve as pr_curve, roc_curve as r_curve

import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt

import logging

logger = logging.getLogger(__name__)

@contextlib.contextmanager
def _precision_recall_canvas(title=None):
    """Generates a canvas to draw precision-recall curves

    Works like a context manager, yielding a figure and an axes set in which
    the precision-recall curves should be added to.  The figure already
    contains F1-ISO lines and is preset to a 0-1 square region.  Once the
    context is finished, ``fig.tight_layout()`` is called.


    Parameters
    ----------

    title : :py:class:`str`, Optional
        Optional title to add to this plot


    Yields
    ------

    figure : matplotlib.figure.Figure
        The figure that should be finally returned to the user

    axes : matplotlib.figure.Axes
        An axis set where to precision-recall plots should be added to

    """

    fig, axes1 = plt.subplots(1)

    # Names and bounds
    axes1.set_xlabel("Recall")
    axes1.set_ylabel("Precision")
    axes1.set_xlim([0.0, 1.0])
    axes1.set_ylim([0.0, 1.0])

    if title is not None:
        axes1.set_title(title)

    axes1.grid(linestyle="--", linewidth=1, color="gray", alpha=0.2)
    axes2 = axes1.twinx()

    # Annotates plot with F1-score iso-lines
    f_scores = numpy.linspace(0.1, 0.9, num=9)
    tick_locs = []
    tick_labels = []
    for f_score in f_scores:
        x = numpy.linspace(0.01, 1)
        y = f_score * x / (2 * x - f_score)
        (l,) = plt.plot(x[y >= 0], y[y >= 0], color="green", alpha=0.1)
        tick_locs.append(y[-1])
        tick_labels.append("%.1f" % f_score)
    axes2.tick_params(axis="y", which="both", pad=0, right=False, left=False)
    axes2.set_ylabel("iso-F", color="green", alpha=0.3)
    axes2.set_ylim([0.0, 1.0])
    axes2.yaxis.set_label_coords(1.015, 0.97)
    axes2.set_yticks(tick_locs)  # notice these are invisible
    for k in axes2.set_yticklabels(tick_labels):
        k.set_color("green")
        k.set_alpha(0.3)
        k.set_size(8)

    # we should see some of axes 1 axes
    axes1.spines["right"].set_visible(False)
    axes1.spines["top"].set_visible(False)
    axes1.spines["left"].set_position(("data", -0.015))
    axes1.spines["bottom"].set_position(("data", -0.015))

    # we shouldn't see any of axes 2 axes
    axes2.spines["right"].set_visible(False)
    axes2.spines["top"].set_visible(False)
    axes2.spines["left"].set_visible(False)
    axes2.spines["bottom"].set_visible(False)

    # yield execution, lets user draw precision-recall plots, and the legend
    # before tighteneing the layout
    yield fig, axes1

    plt.tight_layout()


def precision_recall_f1iso(data):
    """Creates a precision-recall plot

    This function creates and returns a Matplotlib figure with a
    precision-recall plot.  The plot will be annotated with F1-score 
    iso-lines (in which the F1-score maintains the same value).


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

          A threshold for each set. Not used here.


    Returns
    -------

    figure : matplotlib.figure.Figure
        A matplotlib figure you can save or display (uses an ``agg`` backend)

    """

    lines = ["-", "--", "-.", ":"]
    colors = [
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
        "#8c564b",
        "#e377c2",
        "#7f7f7f",
        "#bcbd22",
        "#17becf",
    ]
    colorcycler = cycle(colors)
    linecycler = cycle(lines)

    with _precision_recall_canvas(title=None) as (fig, axes):

        legend = []

        for name, value in data.items():

            df = value["df"]

            # plots Recall/Precision curve
            prec, recall, _ = pr_curve(df['ground_truth'], df['likelihood'])
            _auc = auc(recall, prec)
            label = f"{name} (AUC={_auc:.2f})"
            color = next(colorcycler)
            style = next(linecycler)

            line, = axes.plot(
                recall, 
                prec, 
                color=color, 
                linestyle=style
            )
            legend.append((line, label))

        if len(label) > 1:
            axes.legend(
                [k[0] for k in legend],
                [k[1] for k in legend],
                loc="lower left",
                fancybox=True,
                framealpha=0.7,
            )

    return fig
    

def roc_curve(data, title=None):
    """Creates a ROC plot

    This function creates and returns a Matplotlib figure with a
    ROC plot.


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

          A threshold for each set. Not used here.


    Returns
    -------

    figure : matplotlib.figure.Figure
        A matplotlib figure you can save or display (uses an ``agg`` backend)

    """

    fig, axes = plt.subplots(1)

    # Names and bounds
    axes.set_xlabel("1 - specificity")
    axes.set_ylabel("Sensitivity")
    axes.set_xlim([0.0, 1.0])
    axes.set_ylim([0.0, 1.0])

    # we should see some of axes 1 axes
    axes.spines["right"].set_visible(False)
    axes.spines["top"].set_visible(False)
    axes.spines["left"].set_position(("data", -0.015))
    axes.spines["bottom"].set_position(("data", -0.015))

    if title is not None:
        axes.set_title(title)

    axes.grid(linestyle="--", linewidth=1, color="gray", alpha=0.2)

    plt.tight_layout()

    lines = ["-", "--", "-.", ":"]
    colors = [
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
        "#8c564b",
        "#e377c2",
        "#7f7f7f",
        "#bcbd22",
        "#17becf",
    ]
    colorcycler = cycle(colors)
    linecycler = cycle(lines)
        
    legend = []

    for name, value in data.items():

        df = value["df"]

        # plots roc curve
        fpr, tpr, _ = r_curve(df['ground_truth'], df['likelihood'])
        _auc = auc(fpr, tpr)
        label = f"{name} (AUC={_auc:.2f})"
        color = next(colorcycler)
        style = next(linecycler)

        line, = axes.plot(
            fpr, 
            tpr, 
            color=color,
            linestyle=style
        )
        legend.append((line, label))

    if len(label) > 1:
        axes.legend(
            [k[0] for k in legend],
            [k[1] for k in legend],
            loc="lower right",
            fancybox=True,
            framealpha=0.7,
        )

    return fig


def relevance_analysis_plot(data, title=None):
    """Create an histogram plot to show the relative importance of features


    Parameters
    ----------

    data : :py:class:`list`
        The list of values (one for each feature)


    Returns
    -------

    figure : matplotlib.figure.Figure
        A matplotlib figure you can save or display (uses an ``agg`` backend)

    """

    fig, axes = plt.subplots(1, 1, figsize=(6,6))

    # Names and bounds
    axes.set_xlabel("Features")
    axes.set_ylabel("Importance")

    # we should see some of axes 1 axes
    axes.spines["right"].set_visible(False)
    axes.spines["top"].set_visible(False)

    if title is not None:
        axes.set_title(title)

    #818C2E = likely
    #F2921D = could be
    #8C3503 = unlikely
    
    labels = ['Cardiomegaly', 'Emphysema', 'Pleural effusion', 
                'Hernia', 'Infiltration', 'Mass', 'Nodule', 
                'Atelectasis', 'Pneumothorax', 'Pleural thickening', 
                'Pneumonia', 'Fibrosis', 'Edema', 'Consolidation']
    bars = axes.bar(labels, data, color='#8C3503')
    
    bars[2].set_color('#818C2E')
    bars[4].set_color('#818C2E')
    bars[10].set_color('#818C2E')
    bars[5].set_color('#F2921D')
    bars[6].set_color('#F2921D')
    bars[7].set_color('#F2921D')
    bars[11].set_color('#F2921D')
    bars[13].set_color('#F2921D')

    for tick in axes.get_xticklabels():
        tick.set_rotation(90)

    fig.tight_layout()

    return fig