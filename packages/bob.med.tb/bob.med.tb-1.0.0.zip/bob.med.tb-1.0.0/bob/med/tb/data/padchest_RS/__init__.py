#!/usr/bin/env python
# coding=utf-8

"""Padchest TB dataset for computer-aided diagnosis

A large chest x-ray image dataset with multi-label annotated reports.
This dataset includes more than 160,000 images from 67,000 patients that were 
interpreted and reported by radiologists at Hospital San Juan (Spain) from 2009
to 2017, covering six different position views and additional information on
image acquisition and patient demography.

We keep only "PA" images here and only the "Tuberculosis" subset with an
equivalent number of "normal" images.

* Reference: [PADCHEST-2019]_
* Original resolution: variable, original size
* Labels: [PADCHEST-2019]_
* Split reference: 64%/16%/20%
* Protocol ``default``:

  * Training samples: 160
  * Validation samples: 40
  * Test samples: 50

* Protocol `ìdiap``:
  * Images path adapted to Idiap infrastructure

* Labels: DensenetRS predictions
"""

import os
import pkg_resources

import bob.extension

from ..dataset import JSONDataset
from ..loader import make_delayed

_protocols = [
    pkg_resources.resource_filename(__name__, "tb_idiap.json"),
]


def _raw_data_loader(sample):
    return dict(
        data=sample["data"],
        label=sample["label"]
    )


def _loader(context, sample):
    # "context" is ignored in this case - database is homogeneous
    # we returned delayed samples to avoid loading all images at once
    return make_delayed(sample, _raw_data_loader, key=sample["filename"])


dataset = JSONDataset(
    protocols=_protocols,
    fieldnames=("filename", "label", "data"),
    loader=_loader,
)
"""Padchest dataset object"""
