#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""DenseNet"""

from torch.optim import Adam
from torch.nn import BCEWithLogitsLoss
from ...models.densenet import build_densenet


##### Config #####
lr = 0.0001

# model
model = build_densenet(pretrained=False)

# optimizer
optimizer = Adam(model.parameters(), lr=lr)

# criterion
criterion = BCEWithLogitsLoss()
