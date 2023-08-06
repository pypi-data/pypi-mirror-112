#!/usr/bin/env python
# coding=utf-8

"""TB-POC dataset for computer-aided diagnosis

* Reference: [TB-POC-2018]_
* Original resolution (height x width or width x height): 2048 x 2500
* Split reference: none
* Stratified kfold protocol:

  * Training samples: 72% of TB and healthy CXR (including labels)
  * Validation samples: 18% of TB and healthy CXR (including labels)
  * Test samples: 10% of TB and healthy CXR (including labels)

"""

import os
import pkg_resources

import bob.extension

from ..dataset import JSONDataset
from ..loader import load_pil_baw, make_delayed

_protocols = [
    pkg_resources.resource_filename(__name__, "fold_0.json"),
    pkg_resources.resource_filename(__name__, "fold_1.json"),
    pkg_resources.resource_filename(__name__, "fold_2.json"),
    pkg_resources.resource_filename(__name__, "fold_3.json"),
    pkg_resources.resource_filename(__name__, "fold_4.json"),
    pkg_resources.resource_filename(__name__, "fold_5.json"),
    pkg_resources.resource_filename(__name__, "fold_6.json"),
    pkg_resources.resource_filename(__name__, "fold_7.json"),
    pkg_resources.resource_filename(__name__, "fold_8.json"),
    pkg_resources.resource_filename(__name__, "fold_9.json"),
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
"""Extended TB-POC dataset object"""