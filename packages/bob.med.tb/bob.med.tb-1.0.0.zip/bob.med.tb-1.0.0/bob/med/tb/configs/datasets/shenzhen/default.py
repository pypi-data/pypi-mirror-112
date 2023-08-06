#!/usr/bin/env python
# coding=utf-8

"""Shenzhen dataset for TB detection (default protocol)

* Split reference: first 64% of TB and healthy CXR for "train" 16% for 
* "validation", 20% for "test"
* This configuration resolution: 512 x 512 (default)
* See :py:mod:`bob.med.tb.data.shenzhen` for dataset details
"""

from . import _maker

dataset = _maker("default")