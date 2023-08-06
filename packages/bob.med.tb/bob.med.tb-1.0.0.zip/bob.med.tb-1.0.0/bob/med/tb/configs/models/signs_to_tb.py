#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Feedforward network for Tuberculosis Detection

Simple feedforward network taking radiological signs in output
and predicting tuberculosis presence in output.
"""

from torch.optim import Adam
from torch.nn import BCEWithLogitsLoss
from ...models.signs_to_tb import build_signs_to_tb


##### Config #####
lr = 1e-2

# model
model = build_signs_to_tb(14, 10)

# optimizer
optimizer = Adam(model.parameters(), lr=lr)

# criterion
criterion = BCEWithLogitsLoss()
