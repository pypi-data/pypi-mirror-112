#!/usr/bin/env python
# coding=utf-8

"""HIV-TB dataset for TB detection (cross validation fold 1)

* Split reference: none (stratified kfolding)
* This configuration resolution: 512 x 512 (default)
* See :py:mod:`bob.med.tb.data.hivtb` for dataset details
"""

from . import _maker

dataset = _maker("fold_1")