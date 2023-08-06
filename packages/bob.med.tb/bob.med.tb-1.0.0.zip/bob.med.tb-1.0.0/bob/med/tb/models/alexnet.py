#!/usr/bin/env python
# -*- coding: utf-8 -*-

import torch
import torch.nn as nn
import torchvision.models as models
from collections import OrderedDict
from .normalizer import TorchVisionNormalizer

class Alexnet(nn.Module):
    """
    Alexnet module

    Note: only usable with a normalized dataset

    """
    def __init__(self, pretrained=False):
        super(Alexnet, self).__init__()

        # Load pretrained model
        self.model_ft = models.alexnet(pretrained=pretrained)

        # Adapt output features
        self.model_ft.classifier[4] = nn.Linear(4096,512)
        self.model_ft.classifier[6] = nn.Linear(512,1)

    def forward(self, x):
        """

        Parameters
        ----------

        x : list
            list of tensors.

        Returns
        -------

        tensor : :py:class:`torch.Tensor`

        """

        return self.model_ft(x)


def build_alexnet(pretrained=False):
    """
    Build Alexnet CNN

    Returns
    -------

    module : :py:class:`torch.nn.Module`

    """

    model = Alexnet(pretrained=pretrained)
    model = [("normalizer", TorchVisionNormalizer()), 
            ("model", model)]
    model = nn.Sequential(OrderedDict(model))

    model.name = "AlexNet"
    return model