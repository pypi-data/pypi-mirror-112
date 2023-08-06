#!/usr/bin/env python
# coding=utf-8

"""NIH CXR14 (relabeled, idiap protocol) dataset for computer-aided diagnosis

* See :py:mod:`bob.med.tb.data.nih_cxr14_re` for split details
* This configuration resolution: 512 x 512 (default)
* See :py:mod:`bob.med.tb.data.nih_cxr14_re` for dataset details
"""

from . import _maker

dataset = _maker("idiap")
