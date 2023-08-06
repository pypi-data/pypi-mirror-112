#!/usr/bin/env python
# -*- coding: utf-8 -*-

import torch
import torch.nn as nn
import torch.nn.functional as F

class SignsToTB(nn.Module):
    """
    Radiological signs to Tuberculosis module

    """
    def __init__(self, input_size, hidden_size):
        super().__init__()
        self.input_size = input_size
        self.hidden_size  = hidden_size
        self.fc1 = torch.nn.Linear(self.input_size, self.hidden_size)
        self.relu = torch.nn.ReLU()
        self.fc2 = torch.nn.Linear(self.hidden_size, 1)

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
        hidden = self.fc1(x)
        relu = self.relu(hidden)

        output = self.fc2(relu)

        return output

def build_signs_to_tb(input_size, hidden_size):
    """
    Build SignsToTB shallow model

    Returns
    -------

    module : :py:class:`torch.nn.Module`

    """

    model = SignsToTB(input_size, hidden_size)
    model.name = "signs_to_tb"
    return model