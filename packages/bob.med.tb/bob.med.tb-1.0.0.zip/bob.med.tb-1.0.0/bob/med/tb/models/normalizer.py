#!/usr/bin/env python
# coding=utf-8

"""A network model that prefixes a z-normalization step to any other module"""


import torch
import torch.nn


class TorchVisionNormalizer(torch.nn.Module):
    """A simple normalizer that applies the standard torchvision normalization

    This module does not learn.

    Parameters
    ----------

    nb_channels : :py:class:`int`, Optional
        Number of images channels fed to the model
    """

    def __init__(self, nb_channels=3):
        super(TorchVisionNormalizer, self).__init__()
        mean = torch.zeros(nb_channels)[None, :, None, None]
        std = torch.ones(nb_channels)[None, :, None, None]
        self.register_buffer('mean', mean)
        self.register_buffer('std', std)
        self.name = "torchvision-normalizer"

    def set_mean_std(self, mean, std):
        mean = torch.as_tensor(mean)[None, :, None, None]
        std = torch.as_tensor(std)[None, :, None, None]
        self.register_buffer('mean', mean)
        self.register_buffer('std', std)

    def forward(self, inputs):
        return inputs.sub(self.mean).div(self.std)