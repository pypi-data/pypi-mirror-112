#!/usr/bin/env python
# -*- coding: utf-8 -*-

import torch
import torch.nn as nn
import torch.nn.functional as F

class LogisticRegression(nn.Module):
    """
    Radiological signs to Tuberculosis module

    """
    def __init__(self, input_size):
        super().__init__()
        self.linear = torch.nn.Linear(input_size, 1)

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
        output = self.linear(x)

        return output

def build_logistic_regression(input_size):
    """
    Build logistic regression module

    Returns
    -------

    module : :py:class:`torch.nn.Module`

    """

    model = LogisticRegression(input_size)
    model.name = "logistic_regression"
    return model