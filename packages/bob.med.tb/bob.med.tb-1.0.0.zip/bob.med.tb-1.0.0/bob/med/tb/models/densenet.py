#!/usr/bin/env python
# -*- coding: utf-8 -*-

import torch
import torch.nn as nn
import torchvision.models as models
from collections import OrderedDict
from .normalizer import TorchVisionNormalizer

class Densenet(nn.Module):
    """
    Densenet module

    Note: only usable with a normalized dataset

    """
    def __init__(self, pretrained=False):
        super(Densenet, self).__init__()

        # Load pretrained model
        self.model_ft = models.densenet121(pretrained=pretrained)

        # Adapt output features
        self.model_ft.classifier = nn.Sequential(
                                        nn.Linear(1024,256), 
                                        nn.Linear(256,1)
                                        )

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


def build_densenet(pretrained=False, nb_channels=3):
    """
    Build Densenet CNN

    Returns
    -------

    module : :py:class:`torch.nn.Module`

    """

    model = Densenet(pretrained=pretrained)
    model = [("normalizer", TorchVisionNormalizer(nb_channels=nb_channels)), 
            ("model", model)]
    model = nn.Sequential(OrderedDict(model))

    model.name = "Densenet"
    return model