#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Feedforward network for Tuberculosis Detection

Simple feedforward network taking radiological signs in output
and predicting tuberculosis presence in output.
"""

from torch.optim import Adam
from torch.nn import BCEWithLogitsLoss
from ...models.logistic_regression import build_logistic_regression


##### Config #####
lr = 1e-2

# model
model = build_logistic_regression(14)

# optimizer
optimizer = Adam(model.parameters(), lr=lr)

# criterion
criterion = BCEWithLogitsLoss()
