#!/usr/bin/env python
# coding=utf-8

"""Montgomery dataset for TB detection (cross validation fold 4)

* Split reference: first 64% of TB and healthy CXR for "train" 16% for 
* "validation", 20% for "test"
* This configuration resolution: 512 x 512 (default)
* See :py:mod:`bob.med.tb.data.montgomery` for dataset details
"""

from . import _maker

dataset = _maker("fold_4")