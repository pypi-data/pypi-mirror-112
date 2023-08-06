#!/usr/bin/env python
# coding=utf-8

"""Extended Padchest TB dataset for TB detection (default protocol)
(extended with DensenetRS predictions)

* Split reference: 64%/16%/20%
* See :py:mod:`bob.med.tb.data.padchest_RS` for dataset details
* This configuration resolution: 512 x 512 (default)
"""

from . import _maker

dataset = _maker("tb_idiap")