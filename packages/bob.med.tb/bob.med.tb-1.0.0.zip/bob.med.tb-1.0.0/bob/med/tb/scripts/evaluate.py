#!/usr/bin/env python
# coding=utf-8

import os
import click

from bob.extension.scripts.click_helper import (
    verbosity_option,
    ConfigCommand,
    ResourceOption,
)

from ..engine.evaluator import run

import logging

logger = logging.getLogger(__name__)


def _validate_threshold(t, dataset):
    """Validates the user threshold selection.  Returns parsed threshold."""

    if t is None:
        return 0.5

    try:
        # we try to convert it to float first
        t = float(t)
        if t < 0.0 or t > 1.0:
            raise ValueError("Float thresholds must be within range [0.0, 1.0]")
    except ValueError:
        # it is a bit of text - assert dataset with name is available
        if not isinstance(dataset, dict):
            raise ValueError(
                "Threshold should be a floating-point number "
                "if your provide only a single dataset for evaluation"
            )
        if t not in dataset:
            raise ValueError(
                f"Text thresholds should match dataset names, "
                f"but {t} is not available among the datasets provided ("
                f"({', '.join(dataset.keys())})"
            )

    return t


@click.command(
    entry_point_group="bob.med.tb.config",
    cls=ConfigCommand,
    epilog="""Examples:

\b
    1. Runs evaluation on an existing dataset configuration:
\b
       $ bob tb evaluate -vv montgomery --predictions-folder=path/to/predictions --output-folder=path/to/results
""",
)
@click.option(
    "--output-folder",
    "-o",
    help="Path where to store the analysis result (created if does not exist)",
    required=True,
    default="results",
    type=click.Path(),
    cls=ResourceOption,
)
@click.option(
    "--predictions-folder",
    "-p",
    help="Path where predictions are currently stored",
    required=True,
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    cls=ResourceOption,
)
@click.option(
    "--dataset",
    "-d",
    help="A torch.utils.data.dataset.Dataset instance implementing a dataset "
    "to be used for evaluation purposes, possibly including all pre-processing "
    "pipelines required or, optionally, a dictionary mapping string keys to "
    "torch.utils.data.dataset.Dataset instances.  All keys that do not start "
    "with an underscore (_) will be processed.",
    required=True,
    cls=ResourceOption,
)
@click.option(
    "--threshold",
    "-t",
    help="This number is used to define positives and negatives from "
    "probability maps, and report F1-scores (a priori). It "
    "should either come from the training set or a separate validation set "
    "to avoid biasing the analysis.  Optionally, if you provide a multi-set "
    "dataset as input, this may also be the name of an existing set from "
    "which the threshold will be estimated (highest F1-score) and then "
    "applied to the subsequent sets.  This number is also used to print "
    "the test set F1-score a priori performance",
    default=None,
    show_default=False,
    required=False,
    cls=ResourceOption,
)
@click.option(
    "--steps",
    "-S",
    help="This number is used to define the number of threshold steps to "
    "consider when evaluating the highest possible F1-score on test data.",
    default=1000,
    show_default=True,
    required=True,
    cls=ResourceOption,
)
@verbosity_option(cls=ResourceOption)
def evaluate(
    output_folder,
    predictions_folder,
    dataset,
    threshold,
    steps,
    **kwargs,
):
    """Evaluates a CNN on a tuberculosis prediction task.

    Note: batch size of 1 is required on the predictions.
    """

    threshold = _validate_threshold(threshold, dataset)

    if not isinstance(dataset, dict):
        dataset = {"test": dataset}

    if isinstance(threshold, str):
        # first run evaluation for reference dataset
        logger.info(f"Evaluating threshold on '{threshold}' set")
        f1_threshold, eer_threshold = run(
            dataset[threshold], threshold, predictions_folder, steps=steps
        )
        if f1_threshold != None and eer_threshold != None:
            logger.info(f"Set --f1_threshold={f1_threshold:.5f}")
            logger.info(f"Set --eer_threshold={eer_threshold:.5f}")

    # now run with the
    for k, v in dataset.items():
        if k.startswith("_"):
            logger.info(f"Skipping dataset '{k}' (not to be evaluated)")
            continue
        logger.info(f"Analyzing '{k}' set...")
        run(
            v,
            k,
            predictions_folder,
            output_folder,
            f1_thresh=f1_threshold,
            eer_thresh=eer_threshold,
            steps=steps,
        )