#!/usr/bin/env python
# coding=utf-8

"""Padchest tuberculosis (no TB idiap protocol) dataset for computer-aided diagnosis

* Protocol ``no TB idiap``:

  * Training samples: 20'126
  * Validation samples: 1'500
  * Test samples: 0

* Images path adapted to Idiap infrastructure

* Labels:
  cardiomegaly, emphysema, effusion, hernia, infiltration,
  mass, nodule, atelectasis, pneumothorax, pleural thickening, pneumonia, 
  fibrosis, edema and consolidation
"""

from . import _maker

dataset = _maker("no_tb_idiap")
