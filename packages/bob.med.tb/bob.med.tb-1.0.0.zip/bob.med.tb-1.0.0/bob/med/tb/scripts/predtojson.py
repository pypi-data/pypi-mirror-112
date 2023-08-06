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


def _load(data):
    """Load prediction.csv files

    Parameters
    ----------

    data : dict
        A dict in which keys are the names of the systems and the values are
        paths to ``predictions.csv`` style files.


    Returns
    -------

    data : dict
        A dict in which keys are the names of the systems and the values are
        dictionaries that contain two keys:

        * ``df``: A :py:class:`pandas.DataFrame` with the predictions data 
          loaded to

    """

    # loads all data
    retval = {}
    for name, predictions_path in data.items():

        # Load predictions
        logger.info(f"Loading predictions from {predictions_path}...")
        pred_data = pandas.read_csv(predictions_path)
        pred = torch.Tensor([eval(re.sub(' +', ' ', x.replace('\n', '')).replace(' ', ',')) for x in pred_data['likelihood'].values]).double()
        gt = torch.Tensor([eval(re.sub(' +', ' ', x.replace('\n', '')).replace(' ', ',')) for x in pred_data['ground_truth'].values]).double()

        if pred.shape[1] == 1 and gt.shape[1] == 1:
            pred = torch.flatten(pred)
            gt = torch.flatten(gt)

        pred_data['likelihood'] = pred
        pred_data['ground_truth'] = gt

        retval[name] = dict(df=pred_data)

    return retval


@click.command(
    epilog="""Examples:

\b
    1. Convert predictions of radiological signs to a JSON dataset file_
\b
       $ bob tb predtojson -vv train path/to/train/predictions.csv test path/to/test/predictions.csv
""",
)
@click.argument(
        'label_path',
        nargs=-1,
        )
@click.option(
    "--output-folder",
    "-f",
    help="Path where to store the json file (created if does not exist)",
    required=False,
    default=None,
    type=click.Path(dir_okay=True, file_okay=False),
)
@verbosity_option()
def predtojson(label_path, output_folder, **kwargs):
    """Convert predictions to dataset"""

    # hack to get a dictionary from arguments passed to input
    if len(label_path) % 2 != 0:
        raise click.ClickException("Input label-paths should be doubles"
                " composed of name-path entries")
    data = dict(zip(label_path[::2], label_path[1::2]))

    # load all data measures
    data = _load(data)

    logger.info(f"Output folder: {output_folder}")
    os.makedirs(output_folder, exist_ok=True)

    output_file = os.path.join(output_folder, "dataset.json")
    if os.path.exists(output_file):
        backup = output_file + "~"
        if os.path.exists(backup):
            os.unlink(backup)
        shutil.move(output_file, backup)

    logger.info("Saving JSON file...")
    with open(output_file, "a+", newline="") as f:
        
        f.write('{')
        for i, (name, value) in enumerate(data.items()):
            if i > 0:
                f.write(',')
                
            df = value["df"]
            f.write('"'+name+'": [')
            for index, row in df.iterrows():
                if index > 0:
                    f.write(',')
                f.write('["' + row['filename'] + '", ')
                f.write(str(row['ground_truth'][0].item()))
                f.write(',')
                f.write(str([format(x, '.20f') for x in torch.tensor(row['likelihood']).tolist()]).replace("'", ""))
                f.write(']')
            f.write(']')
        f.write('}')
            
