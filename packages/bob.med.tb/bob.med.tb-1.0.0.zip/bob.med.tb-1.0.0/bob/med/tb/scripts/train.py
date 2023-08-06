#!/usr/bin/env python
# coding=utf-8

import os

import click
import torch
from torch.nn import BCEWithLogitsLoss
from torch.utils.data import DataLoader, WeightedRandomSampler
from ..configs.datasets import get_samples_weights, get_positive_weights

from bob.extension.scripts.click_helper import (
    verbosity_option,
    ConfigCommand,
    ResourceOption,
)

from ..utils.checkpointer import Checkpointer
from ..engine.trainer import run
from .tb import download_to_tempfile
from ..models.normalizer import TorchVisionNormalizer

import logging
logger = logging.getLogger(__name__)


@click.command(
    entry_point_group="bob.med.tb.config",
    cls=ConfigCommand,
    epilog="""Examples:

\b
    1. Trains PASA model with Montgomery dataset,
       on a GPU (``cuda:0``):

       $ bob tb train -vv pasa montgomery --batch-size=4 --device="cuda:0"

""",
)
@click.option(
    "--output-folder",
    "-o",
    help="Path where to store the generated model (created if does not exist)",
    required=True,
    type=click.Path(),
    default="results",
    cls=ResourceOption,
)
@click.option(
    "--model",
    "-m",
    help="A torch.nn.Module instance implementing the network to be trained",
    required=True,
    cls=ResourceOption,
)
@click.option(
    "--dataset",
    "-d",
    help="A torch.utils.data.dataset.Dataset instance implementing a dataset "
    "to be used for training the model, possibly including all pre-processing "
    "pipelines required or, optionally, a dictionary mapping string keys to "
    "torch.utils.data.dataset.Dataset instances.  At least one key "
    "named ``train`` must be available.  This dataset will be used for "
    "training the network model.  The dataset description must include all "
    "required pre-processing, including eventual data augmentation.  If a "
    "dataset named ``__train__`` is available, it is used prioritarily for "
    "training instead of ``train``.  If a dataset named ``__valid__`` is "
    "available, it is used for model validation (and automatic check-pointing) "
    "at each epoch.",
    required=True,
    cls=ResourceOption,
)
@click.option(
    "--optimizer",
    help="A torch.optim.Optimizer that will be used to train the network",
    required=True,
    cls=ResourceOption,
)
@click.option(
    "--criterion",
    help="A loss function to compute the CNN error for every sample "
    "respecting the PyTorch API for loss functions (see torch.nn.modules.loss)",
    required=True,
    cls=ResourceOption,
)
@click.option(
    "--criterion_valid",
    help="A specific loss function for the validation set to compute the CNN"
    "error for every sample respecting the PyTorch API for loss functions"
    "(see torch.nn.modules.loss)",
    required=False,
    cls=ResourceOption,
)
@click.option(
    "--batch-size",
    "-b",
    help="Number of samples in every batch (this parameter affects "
    "memory requirements for the network).  If the number of samples in "
    "the batch is larger than the total number of samples available for "
    "training, this value is truncated.  If this number is smaller, then "
    "batches of the specified size are created and fed to the network "
    "until there are no more new samples to feed (epoch is finished).  "
    "If the total number of training samples is not a multiple of the "
    "batch-size, the last batch will be smaller than the first, unless "
    "--drop-incomplete--batch is set, in which case this batch is not used.",
    required=True,
    show_default=True,
    default=1,
    type=click.IntRange(min=1),
    cls=ResourceOption,
)
@click.option(
    "--drop-incomplete-batch/--no-drop-incomplete-batch",
    "-D",
    help="If set, then may drop the last batch in an epoch, in case it is "
    "incomplete.  If you set this option, you should also consider "
    "increasing the total number of epochs of training, as the total number "
    "of training steps may be reduced",
    required=True,
    show_default=True,
    default=False,
    cls=ResourceOption,
)
@click.option(
    "--epochs",
    "-e",
    help="Number of epochs (complete training set passes) to train for",
    show_default=True,
    required=True,
    default=1000,
    type=click.IntRange(min=1),
    cls=ResourceOption,
)
@click.option(
    "--checkpoint-period",
    "-p",
    help="Number of epochs after which a checkpoint is saved. "
    "A value of zero will disable check-pointing. If checkpointing is "
    "enabled and training stops, it is automatically resumed from the "
    "last saved checkpoint if training is restarted with the same "
    "configuration.",
    show_default=True,
    required=True,
    default=0,
    type=click.IntRange(min=0),
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
    "--seed",
    "-s",
    help="Seed to use for the random number generator",
    show_default=True,
    required=False,
    default=42,
    type=click.IntRange(min=0),
    cls=ResourceOption,
)
@click.option(
    "--num_workers",
    "-ns",
    help="Number of parallel threads to use",
    show_default=True,
    required=False,
    default=0,
    type=click.IntRange(min=0),
    cls=ResourceOption,
)
@click.option(
    "--weight",
    "-w",
    help="Path or URL to pretrained model file (.pth extension)",
    required=False,
    cls=ResourceOption,
)
@click.option(
    "--normalization",
    "-n",
    help="Z-Normalization of input images: 'imagenet' for ImageNet parameters,"
    " 'current' for parameters of the current trainset, "
    "'none' for no normalization.",
    required=False,
    default="none",
    cls=ResourceOption,
)
@verbosity_option(cls=ResourceOption)
def train(
    model,
    optimizer,
    output_folder,
    epochs,
    batch_size,
    drop_incomplete_batch,
    criterion,
    criterion_valid,
    dataset,
    checkpoint_period,
    device,
    seed,
    num_workers,
    weight,
    normalization,
    verbose,
    **kwargs,
):
    """Trains an CNN to perform tuberculosis detection

    Training is performed for a configurable number of epochs, and generates at
    least a final_model.pth.  It may also generate a number of intermediate
    checkpoints.  Checkpoints are model files (.pth files) that are stored
    during the training and useful to resume the procedure in case it stops
    abruptly.
    """

    torch.manual_seed(seed)

    use_dataset = dataset
    validation_dataset = None
    if isinstance(dataset, dict):
        if "__train__" in dataset:
            logger.info("Found (dedicated) '__train__' set for training")
            use_dataset = dataset["__train__"]
        else:
            use_dataset = dataset["train"]

        if "__valid__" in dataset:
            logger.info("Found (dedicated) '__valid__' set for validation")
            logger.info("Will checkpoint lowest loss model on validation set")
            validation_dataset = dataset["__valid__"]

    # Create weighted random sampler
    train_samples_weights = get_samples_weights(use_dataset)
    train_samples_weights = train_samples_weights.to(
                    device=device, non_blocking=torch.cuda.is_available()
                )
    train_sampler = WeightedRandomSampler(train_samples_weights, len(train_samples_weights), replacement=True)

    # Redefine a weighted criterion if possible
    if isinstance(criterion, torch.nn.BCEWithLogitsLoss):
        positive_weights = get_positive_weights(use_dataset)
        positive_weights = positive_weights.to(
                        device=device, non_blocking=torch.cuda.is_available()
                    )
        criterion = BCEWithLogitsLoss(pos_weight=positive_weights)
    else:
        logger.warning("Weighted criterion not supported")

    # PyTorch dataloader
    data_loader = DataLoader(
        dataset=use_dataset,
        batch_size=batch_size,
        num_workers=num_workers,
        drop_last=drop_incomplete_batch,
        pin_memory=torch.cuda.is_available(),
        sampler=train_sampler
    )

    valid_loader = None
    if validation_dataset is not None:

        # Redefine a weighted valid criterion if possible
        if isinstance(criterion_valid, torch.nn.BCEWithLogitsLoss) or criterion_valid is None:
            positive_weights = get_positive_weights(validation_dataset)
            positive_weights = positive_weights.to(
                            device=device, non_blocking=torch.cuda.is_available()
                        )
            criterion_valid = BCEWithLogitsLoss(pos_weight=positive_weights)
        else:
            logger.warning("Weighted valid criterion not supported")

        valid_loader = DataLoader(
                dataset=validation_dataset,
                batch_size=batch_size,
                num_workers=num_workers,
                shuffle=False,
                drop_last=False,
                pin_memory=torch.cuda.is_available(),
                )

    # Create z-normalization model layer if needed
    if normalization == "imagenet":
        model.normalizer.set_mean_std([0.485, 0.456, 0.406],
                                    [0.229, 0.224, 0.225])
        logger.info("Z-normalization with ImageNet mean and std")
    elif normalization == "current":
        # Compute mean/std of current train subset
        temp_dl = DataLoader(
            dataset=use_dataset,
            batch_size=len(use_dataset)
        )

        data = next(iter(temp_dl))
        mean = data[1].mean(dim=[0,2,3])
        std = data[1].std(dim=[0,2,3])

        model.normalizer.set_mean_std(mean, std)

        # Format mean and std for logging
        mean = str([round(x, 3) for x in ((mean * 10**3).round() / (10**3)).tolist()])
        std = str([round(x, 3) for x in ((std * 10**3).round() / (10**3)).tolist()])
        logger.info("Z-normalization with mean {} and std {}".format(mean, std))

    # Checkpointer
    checkpointer = Checkpointer(model, optimizer, path=output_folder)

    # Load pretrained weights if needed
    if weight is not None:
        if weight.startswith("http"):
            logger.info(f"Temporarily downloading '{weight}'...")
            f = download_to_tempfile(weight, progress=True)
            weight_fullpath = os.path.abspath(f.name)
        else:
            weight_fullpath = os.path.abspath(weight)
        checkpointer.load(weight_fullpath, strict=False)

    arguments = {}
    arguments["epoch"] = 0
    arguments["max_epoch"] = epochs

    logger.info("Training for {} epochs".format(arguments["max_epoch"]))
    logger.info("Continuing from epoch {}".format(arguments["epoch"]))

    run(
        model,
        data_loader,
        valid_loader,
        optimizer,
        criterion,
        checkpointer,
        checkpoint_period,
        device,
        arguments,
        output_folder,
        criterion_valid,
    )