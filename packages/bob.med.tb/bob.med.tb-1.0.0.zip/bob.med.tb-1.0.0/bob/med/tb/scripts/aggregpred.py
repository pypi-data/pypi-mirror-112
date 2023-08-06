#!/usr/bin/env python
# coding=utf-8

import os
import click

from bob.extension.scripts.click_helper import (
    verbosity_option,
    AliasedGroup,
)

import shutil
import torch
import re
import pandas

import logging
logger = logging.getLogger(__name__)

@click.command(
    epilog="""Examples:

\b
    1. Aggregate multiple predictions csv files into one
\b
       $ bob tb aggregpred -vv path/to/train/predictions.csv path/to/test/predictions.csv
""",
)
@click.argument(
        'label_path',
        nargs=-1,
        )
@click.option(
    "--output-folder",
    "-f",
    help="Path where to store the aggregated csv file (created if necessary)",
    required=False,
    default=None,
    type=click.Path(dir_okay=True, file_okay=False),
)
@verbosity_option()
def aggregpred(label_path, output_folder, **kwargs):
    """Aggregate multiple predictions csv files into one"""

    # loads all data
    series = []
    for predictions_path in label_path:

        # Load predictions
        logger.info(f"Loading predictions from {predictions_path}...")
        pred_data = pandas.read_csv(predictions_path)
        pred = torch.Tensor([eval(re.sub(' +', ' ', x.replace('\n', '')).replace(' ', ',')) for x in pred_data['likelihood'].values]).double().flatten()
        gt = torch.Tensor([eval(re.sub(' +', ' ', x.replace('\n', '')).replace(' ', ',')) for x in pred_data['ground_truth'].values]).double().flatten()

        pred_data['likelihood'] = pred
        pred_data['ground_truth'] = gt

        series.append(pred_data)
    
    df = pandas.concat([s for s in series])

    logger.info(f"Output folder: {output_folder}")
    os.makedirs(output_folder, exist_ok=True)

    output_file = os.path.join(output_folder, "aggregpred.csv")
    if os.path.exists(output_file):
        backup = output_file + "~"
        if os.path.exists(backup):
            os.unlink(backup)
        shutil.move(output_file, backup)

    logger.info("Saving aggregated CSV file...")
    df.to_csv(output_file, index=False, header=True)