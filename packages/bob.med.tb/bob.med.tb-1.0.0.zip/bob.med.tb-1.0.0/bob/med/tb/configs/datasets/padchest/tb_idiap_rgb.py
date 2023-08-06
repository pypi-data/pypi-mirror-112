#!/usr/bin/env python
# coding=utf-8

"""Padchest tuberculosis (idiap protocol, rgb) dataset for 
computer-aided diagnosis

The 125 healthy images are the first 125 padchest images with the following
parameters: Label = "Normal", MethodLabel = "Physician", Projection = "PA"

* Split reference: first 80% of TB and healthy CXR for "train", rest for "test"
* See :py:mod:`bob.med.tb.data.padchest` for dataset details
* This configuration resolution: 224 x 224 (default)
"""

from . import _maker

dataset = _maker("tb_idiap", resize_size=256, cc_size=224)