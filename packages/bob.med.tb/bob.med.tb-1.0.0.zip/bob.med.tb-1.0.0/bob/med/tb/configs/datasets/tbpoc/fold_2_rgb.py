#!/usr/bin/env python
# coding=utf-8

"""TB-POC dataset for TB detection (cross validation fold 2)

* Split reference: none (stratified kfolding)
* This configuration resolution: 512 x 512 (default)
* See :py:mod:`bob.med.tb.data.tbpoc` for dataset details
"""

from . import _maker

dataset = _maker("fold_2", RGB=True)