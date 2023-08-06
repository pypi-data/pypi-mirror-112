#!/usr/bin/env python
# -*- coding: utf-8 -*-

import torch
import torch.nn as nn
import torch.nn.functional as F
from collections import OrderedDict
from .normalizer import TorchVisionNormalizer

class PASA(nn.Module):
    """
    PASA module

    Based on paper by [PASA-2019]_.

    """
    def __init__(self):
        super().__init__()
        # First convolution block
        self.fc1 = nn.Conv2d(1, 4, (3, 3), (2, 2), (1, 1))
        self.fc2 = nn.Conv2d(4, 16, (3, 3), (2, 2), (1, 1))
        self.fc3 = nn.Conv2d(1, 16, (1, 1), (4, 4))

        self.batchNorm2d_4 = nn.BatchNorm2d(4)
        self.batchNorm2d_16 = nn.BatchNorm2d(16)
        self.batchNorm2d_16_2 = nn.BatchNorm2d(16)

        # Second convolution block
        self.fc4 = nn.Conv2d(16, 24, (3, 3), (1, 1), (1, 1))
        self.fc5 = nn.Conv2d(24, 32, (3, 3), (1, 1), (1, 1))
        self.fc6 = nn.Conv2d(16, 32, (1, 1), (1, 1)) # Original stride (2, 2)

        self.batchNorm2d_24 = nn.BatchNorm2d(24)
        self.batchNorm2d_32 = nn.BatchNorm2d(32)
        self.batchNorm2d_32_2 = nn.BatchNorm2d(32)

        # Third convolution block
        self.fc7 = nn.Conv2d(32, 40, (3, 3), (1, 1), (1, 1))
        self.fc8 = nn.Conv2d(40, 48, (3, 3), (1, 1), (1, 1))
        self.fc9 = nn.Conv2d(32, 48, (1, 1), (1, 1)) # Original stride (2, 2)

        self.batchNorm2d_40 = nn.BatchNorm2d(40)
        self.batchNorm2d_48 = nn.BatchNorm2d(48)
        self.batchNorm2d_48_2 = nn.BatchNorm2d(48)

        # Fourth convolution block
        self.fc10 = nn.Conv2d(48, 56, (3, 3), (1, 1), (1, 1))
        self.fc11 = nn.Conv2d(56, 64, (3, 3), (1, 1), (1, 1))
        self.fc12 = nn.Conv2d(48, 64, (1, 1), (1, 1)) # Original stride (2, 2)

        self.batchNorm2d_56 = nn.BatchNorm2d(56)
        self.batchNorm2d_64 = nn.BatchNorm2d(64)
        self.batchNorm2d_64_2 = nn.BatchNorm2d(64)

        # Fifth convolution block
        self.fc13 = nn.Conv2d(64, 72, (3, 3), (1, 1), (1, 1))
        self.fc14 = nn.Conv2d(72, 80, (3, 3), (1, 1), (1, 1))
        self.fc15 = nn.Conv2d(64, 80, (1, 1), (1, 1)) # Original stride (2, 2)

        self.batchNorm2d_72 = nn.BatchNorm2d(72)
        self.batchNorm2d_80 = nn.BatchNorm2d(80)
        self.batchNorm2d_80_2 = nn.BatchNorm2d(80)

        self.pool2d = nn.MaxPool2d((3, 3), (2, 2)) # Pool after conv. block
        self.dense = nn.Linear(80, 1) # Fully connected layer

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

        # First convolution block
        _x = x
        x = F.relu(self.batchNorm2d_4(self.fc1(x))) # 1st convolution
        x = F.relu(self.batchNorm2d_16(self.fc2(x))) # 2nd convolution
        x = (x + F.relu(self.batchNorm2d_16_2(self.fc3(_x))))/2 # Parallel
        x = self.pool2d(x) # Pooling

        # Second convolution block
        _x = x
        x = F.relu(self.batchNorm2d_24(self.fc4(x))) # 1st convolution
        x = F.relu(self.batchNorm2d_32(self.fc5(x))) # 2nd convolution
        x = (x + F.relu(self.batchNorm2d_32_2(self.fc6(_x))))/2 # Parallel
        x = self.pool2d(x) # Pooling

        # Third convolution block
        _x = x
        x = F.relu(self.batchNorm2d_40(self.fc7(x))) # 1st convolution
        x = F.relu(self.batchNorm2d_48(self.fc8(x))) # 2nd convolution
        x = (x + F.relu(self.batchNorm2d_48_2(self.fc9(_x))))/2 # Parallel
        x = self.pool2d(x) # Pooling

        # Fourth convolution block
        _x = x
        x = F.relu(self.batchNorm2d_56(self.fc10(x))) # 1st convolution
        x = F.relu(self.batchNorm2d_64(self.fc11(x))) # 2nd convolution
        x = (x + F.relu(self.batchNorm2d_64_2(self.fc12(_x))))/2 # Parallel
        x = self.pool2d(x) # Pooling

        # Fifth convolution block
        _x = x
        x = F.relu(self.batchNorm2d_72(self.fc13(x))) # 1st convolution
        x = F.relu(self.batchNorm2d_80(self.fc14(x))) # 2nd convolution
        x = (x + F.relu(self.batchNorm2d_80_2(self.fc15(_x))))/2 # Parallel
        # no pooling

        # Global average pooling
        x = torch.mean(x.view(x.size(0), x.size(1), -1), dim=2)
        
        # Dense layer
        x = self.dense(x)
        
        # x = F.log_softmax(x, dim=1) # 0 is batch size
        
        return x

def build_pasa():
    """
    Build pasa CNN

    Returns
    -------

    module : :py:class:`torch.nn.Module`

    """

    model = PASA()
    model = [("normalizer", TorchVisionNormalizer(nb_channels=1)), 
            ("model", model)]
    model = nn.Sequential(OrderedDict(model))

    model.name = "pasa"
    return model