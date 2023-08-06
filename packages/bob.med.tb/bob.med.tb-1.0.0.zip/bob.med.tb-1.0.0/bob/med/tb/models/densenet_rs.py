#!/usr/bin/env python
# -*- coding: utf-8 -*-

import torch
import torch.nn as nn
import torchvision.models as models
from collections import OrderedDict
from .normalizer import TorchVisionNormalizer

class DensenetRS(nn.Module):
    """
    Densenet121 module for radiological extraction

    """
    def __init__(self):
        super(DensenetRS, self).__init__()

        # Load pretrained model
        self.model_ft = models.densenet121(pretrained=True)

        # Adapt output features
        num_ftrs = self.model_ft.classifier.in_features
        self.model_ft.classifier = nn.Linear(num_ftrs, 14)

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


def build_densenetrs():
    """
    Build DensenetRS CNN

    Returns
    -------

    module : :py:class:`torch.nn.Module`

    """

    model = DensenetRS()
    model = [("normalizer", TorchVisionNormalizer()), 
            ("model", model)]
    model = nn.Sequential(OrderedDict(model))

    model.name = "DensenetRS"
    return model