#!/usr/bin/env python
# coding=utf-8

"""Padchest cardiomegaly (idiap protocol) dataset for computer-aided diagnosis

The first 40 images with cardiomegaly.
parameters: Label = "Normal", MethodLabel = "Physician", Projection = "PA"

* Split reference: first 100% of cardiomegaly for "train"
* See :py:mod:`bob.med.tb.data.padchest` for dataset details
* This configuration resolution: 512 x 512 (default)
"""

from . import _maker

dataset = _maker("cardiomegaly_idiap", RGB=False)
