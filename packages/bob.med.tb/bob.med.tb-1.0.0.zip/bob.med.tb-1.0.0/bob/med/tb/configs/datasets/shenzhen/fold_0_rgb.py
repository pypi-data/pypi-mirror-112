#!/usr/bin/env python
# coding=utf-8

"""Shenzhen dataset for TB detection (cross validation fold 0, RGB)

* Split reference: first 80% of TB and healthy CXR for "train", rest for "test"
* This configuration resolution: 512 x 512 (default)
* See :py:mod:`bob.med.tb.data.shenzhen` for dataset details
"""

from . import _maker

dataset = _maker("fold_0", RGB=True)