#!/usr/bin/env python
# coding=utf-8

import os
import click

from bob.extension.scripts.click_helper import (
    verbosity_option,
    AliasedGroup,
)

import torch
import re
import pandas
import tabulate
from matplotlib.backends.backend_pdf import PdfPages

from ..utils.plot import precision_recall_f1iso
from ..utils.plot import roc_curve
from ..utils.table import performance_table

import logging
logger = logging.getLogger(__name__)


def _validate_threshold(t, dataset):
    """Validates the user threshold selection.  Returns parsed threshold."""

    if t is None:
        return t

    # we try to convert it to float first
    t = float(t)
    if t < 0.0 or t > 1.0:
        raise ValueError("Thresholds must be within range [0.0, 1.0]")

    return t


def _load(data, threshold):
    """Plots comparison chart of all evaluated models

    Parameters
    ----------

    data : dict
        A dict in which keys are the names of the systems and the values are
        paths to ``predictions.csv`` style files.

    threshold : :py:class:`float`
        A threshold for the final classification.


    Returns
    -------

    data : dict
        A dict in which keys are the names of the systems and the values are
        dictionaries that contain two keys:

        * ``df``: A :py:class:`pandas.DataFrame` with the predictions data 
          loaded to
        * ``threshold``: The ``threshold`` parameter set on the input

    """

    use_threshold = threshold
    logger.info(f"Dataset '*': threshold = {use_threshold:.3f}'")

    # loads all data
    retval = {}
    for name, predictions_path in data.items():

        # Load predictions
        logger.info(f"Loading predictions from {predictions_path}...")
        pred_data = pandas.read_csv(predictions_path)
        pred = torch.Tensor([eval(re.sub(' +', ' ', x.replace('\n', '')).replace(' ', ',')) if isinstance(x, str) else x for x in pred_data['likelihood'].values]).double().flatten()
        gt = torch.Tensor([eval(re.sub(' +', ' ', x.replace('\n', '')).replace(' ', ',')) if isinstance(x, str) else x for x in pred_data['ground_truth'].values]).double().flatten()

        pred_data['likelihood'] = pred
        pred_data['ground_truth'] = gt

        retval[name] = dict(df=pred_data, threshold=use_threshold)

    return retval


@click.command(
    epilog="""Examples:

\b
    1. Compares system A and B, with their own predictions files:
\b
       $ bob tb compare -vv A path/to/A/predictions.csv B path/to/B/predictions.csv
""",
)
@click.argument(
        'label_path',
        nargs=-1,
        )
@click.option(
    "--output-figure",
    "-f",
    help="Path where write the output figure (any extension supported by "
    "matplotlib is possible).  If not provided, does not produce a figure.",
    required=False,
    default=None,
    type=click.Path(dir_okay=False, file_okay=True),
)
@click.option(
    "--table-format",
    "-T",
    help="The format to use for the comparison table",
    show_default=True,
    required=True,
    default="rst",
    type=click.Choice(tabulate.tabulate_formats),
)
@click.option(
    "--output-table",
    "-u",
    help="Path where write the output table. If not provided, does not write "
    "write a table to file, only to stdout.",
    required=False,
    default=None,
    type=click.Path(dir_okay=False, file_okay=True),
)
@click.option(
    "--threshold",
    "-t",
    help="This number is used to separate positive and negative cases "
    "by thresholding their score.",
    default=None,
    show_default=False,
    required=False,
)
@verbosity_option()
def compare(label_path, output_figure, table_format, output_table, 
        threshold, **kwargs):
    """Compares multiple systems together"""

    # hack to get a dictionary from arguments passed to input
    if len(label_path) % 2 != 0:
        raise click.ClickException("Input label-paths should be doubles"
                " composed of name-path entries")
    data = dict(zip(label_path[::2], label_path[1::2]))

    threshold = _validate_threshold(threshold, data)

    # load all data measures
    data = _load(data, threshold=threshold)

    if output_figure is not None:
        output_figure = os.path.realpath(output_figure)
        logger.info(f"Creating and saving plot at {output_figure}...")
        os.makedirs(os.path.dirname(output_figure), exist_ok=True)
        pdf = PdfPages(output_figure)
        pdf.savefig(precision_recall_f1iso(data))
        pdf.savefig(roc_curve(data))
        pdf.close()

    logger.info("Tabulating performance summary...")
    table = performance_table(data, table_format)
    click.echo(table)
    if output_table is not None:
        output_table = os.path.realpath(output_table)
        logger.info(f"Saving table at {output_table}...")
        os.makedirs(os.path.dirname(output_table), exist_ok=True)
        with open(output_table, "wt") as f:
            f.write(table)
