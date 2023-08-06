#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""AlexNet

Pretrained AlexNet
"""

from torch.optim import SGD
from torch.nn import BCEWithLogitsLoss
from ...models.alexnet import build_alexnet


##### Config #####
lr = 0.001

# model
model = build_alexnet(pretrained=True)

# optimizer
optimizer = SGD(model.parameters(), lr=lr, momentum=0.1)

# criterion
criterion = BCEWithLogitsLoss()
