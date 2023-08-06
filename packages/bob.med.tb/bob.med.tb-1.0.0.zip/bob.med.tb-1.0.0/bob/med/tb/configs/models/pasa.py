#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""CNN for Tuberculosis Detection

Implementation of the model architecture proposed by F. Pasa in the article
"Efficient Deep Network Architectures for Fast Chest X-Ray Tuberculosis 
Screening and Visualization".

Reference: [PASA-2019]_
"""

from torch.optim import Adam
from torch.nn import BCEWithLogitsLoss
from ...models.pasa import build_pasa


##### Config #####
lr = 8e-5

# model
model = build_pasa()

# optimizer
optimizer = Adam(model.parameters(), lr=lr)

# criterion
criterion = BCEWithLogitsLoss()
