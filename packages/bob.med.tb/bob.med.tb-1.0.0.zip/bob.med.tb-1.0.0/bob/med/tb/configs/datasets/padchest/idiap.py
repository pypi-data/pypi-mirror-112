#!/usr/bin/env python
# coding=utf-8

"""Padchest (idiap protocol) dataset for computer-aided diagnosis

* See :py:mod:`bob.med.tb.data.padchest` for dataset details
* This configuration resolution: 512 x 512 (default)
"""

from . import _maker

dataset = _maker("idiap")
