#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""CNN for radiological findings detection

A Densenet121 model for radiological extraction

"""

import torch
import torchvision.models as models
from torch.optim import Adam
from torch.nn import BCEWithLogitsLoss
import torch.nn as nn
from ...models.densenet_rs import build_densenetrs

# Import the default protocol if none is available
if 'dataset' not in locals():
    from ..datasets.nih_cxr14_re.default import dataset

##### Config #####
lr = 1e-4

# model
model = build_densenetrs()

# optimizer
optimizer = Adam(
                filter(lambda p: p.requires_grad, model.model.model_ft.parameters()), 
                lr=lr)

# criterion
criterion = BCEWithLogitsLoss()
criterion_valid = BCEWithLogitsLoss()