#!/usr/bin/env python
# coding=utf-8

"""Indian dataset for TB detection (cross validation fold 7)

* Split reference: [INDIAN-2013]_ with 20% of train set for the validation set
* This configuration resolution: 512 x 512 (default)
* See :py:mod:`bob.med.tb.data.indian` for dataset details
"""

from . import _maker

dataset = _maker("fold_7")