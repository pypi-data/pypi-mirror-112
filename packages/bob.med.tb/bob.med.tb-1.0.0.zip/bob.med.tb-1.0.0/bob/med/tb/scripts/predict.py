#!/usr/bin/env python
# coding=utf-8

import os
import shutil
import tempfile
import copy

import click
import torch
import numpy as np
from sklearn import metrics
from torch.utils.data import DataLoader, ConcatDataset
from matplotlib.backends.backend_pdf import PdfPages

from bob.extension.scripts.click_helper import (
    verbosity_option,
    ConfigCommand,
    ResourceOption,
)

from ..engine.predictor import run
from ..utils.checkpointer import Checkpointer

from .tb import download_to_tempfile
from ..utils.plot import relevance_analysis_plot

import logging
logger = logging.getLogger(__name__)


@click.command(
    entry_point_group="bob.med.tb.config",
    cls=ConfigCommand,
    epilog="""Examples:

\b
    1. Runs prediction on an existing dataset configuration:
\b
       $ bob tb predict -vv pasa montgomery --weight=path/to/model_final.pth --output-folder=path/to/predictions

""",
)
@click.option(
    "--output-folder",
    "-o",
    help="Path where to store the predictions (created if does not exist)",
    required=True,
    default="results",
    cls=ResourceOption,
    type=click.Path(),
)
@click.option(
    "--model",
    "-m",
    help="A torch.nn.Module instance implementing the network to be evaluated",
    required=True,
    cls=ResourceOption,
)
@click.option(
    "--dataset",
    "-d",
    help="A torch.utils.data.dataset.Dataset instance implementing a dataset "
    "to be used for running prediction, possibly including all pre-processing "
    "pipelines required or, optionally, a dictionary mapping string keys to "
    "torch.utils.data.dataset.Dataset instances.  All keys that do not start "
    "with an underscore (_) will be processed.",
    required=True,
    cls=ResourceOption,
)
@click.option(
    "--batch-size",
    "-b",
    help="Number of samples in every batch (this parameter affects memory requirements for the network)",
    required=True,
    show_default=True,
    default=1,
    type=click.IntRange(min=1),
    cls=ResourceOption,
)
@click.option(
    "--device",
    "-d",
    help='A string indicating the device to use (e.g. "cpu" or "cuda:0")',
    show_default=True,
    required=True,
    default="cpu",
    cls=ResourceOption,
)
@click.option(
    "--weight",
    "-w",
    help="Path or URL to pretrained model file (.pth extension)",
    required=True,
    cls=ResourceOption,
)
@click.option(
    "--relevance-analysis",
    "-r",
    help="If set, generate relevance analysis pdfs to indicate the relative"
    "importance of each feature",
    is_flag=True,
    cls=ResourceOption,
)
@click.option(
    "--grad-cams",
    "-g",
    help="If set, generate grad cams for each prediction (must use batch of 1)",
    is_flag=True,
    cls=ResourceOption,
)
@verbosity_option(cls=ResourceOption)
def predict(output_folder, model, dataset, batch_size, device, weight, 
            relevance_analysis, grad_cams, **kwargs):
    """Predicts Tuberculosis presence (probabilities) on input images"""

    dataset = dataset if isinstance(dataset, dict) else dict(test=dataset)
    
    if weight.startswith("http"):
        logger.info(f"Temporarily downloading '{weight}'...")
        f = download_to_tempfile(weight, progress=True)
        weight_fullpath = os.path.abspath(f.name)
    else:
        weight_fullpath = os.path.abspath(weight)

    checkpointer = Checkpointer(model)
    checkpointer.load(weight_fullpath, strict=False)

    # Logistic regressor weights
    if model.name == "logistic_regression":
        logger.info(f"Logistic regression identified: saving model weights")
        for param in model.parameters():
            model_weights = np.array(param.data.reshape(-1))
            break
        filepath = os.path.join(output_folder, "LogReg_Weights.pdf")
        logger.info(f"Creating and saving weights plot at {filepath}...")
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        pdf = PdfPages(filepath)
        pdf.savefig(relevance_analysis_plot(
            model_weights, 
            title="LogReg model weights"))
        pdf.close()

    for k,v in dataset.items():

        if k.startswith("_"):
            logger.info(f"Skipping dataset '{k}' (not to be evaluated)")
            continue

        logger.info(f"Running inference on '{k}' set...")

        data_loader = DataLoader(
            dataset=v,
            batch_size=batch_size,
            shuffle=False,
            pin_memory=torch.cuda.is_available(),
        )
        predictions = run(model, data_loader, k, device, output_folder, grad_cams)

        # Relevance analysis using permutation feature importance
        if(relevance_analysis):
            if isinstance(v, ConcatDataset) or not isinstance(v._samples[0].data["data"], list):
                logger.info(f"Relevance analysis only possible with radiological signs as input. Cancelling...")
                continue

            nb_features = len(v._samples[0].data["data"])

            if nb_features == 1:
                logger.info(f"Relevance analysis not possible with one feature")
            else:
                logger.info(f"Starting relevance analysis for subset '{k}'...")

                all_mse = []
                for f in range(nb_features):

                    v_original = copy.deepcopy(v)

                    # Randomly permute feature values from all samples
                    v.random_permute(f)

                    data_loader = DataLoader(
                        dataset=v,
                        batch_size=batch_size,
                        shuffle=False,
                        pin_memory=torch.cuda.is_available(),
                    )

                    predictions_with_mean = run(model,
                                                data_loader,
                                                k,
                                                device,
                                                output_folder + "_temp")

                    # Compute MSE between original and new predictions
                    all_mse.append(metrics.mean_squared_error(
                        np.array(predictions)[:,1],
                        np.array(predictions_with_mean)[:,1]
                        ))

                    # Back to original values
                    v = v_original
                
                # Remove temporary folder
                shutil.rmtree(output_folder + "_temp", ignore_errors=True)
                
                filepath = os.path.join(output_folder, k + "_RA.pdf")
                logger.info(f"Creating and saving plot at {filepath}...")
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                pdf = PdfPages(filepath)
                pdf.savefig(relevance_analysis_plot(
                    all_mse, 
                    title=k.capitalize() + " set relevance analysis"))
                pdf.close()
