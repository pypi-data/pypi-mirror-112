#!/usr/bin/env python
# coding=utf-8

"""Shenzhen dataset for computer-aided diagnosis
(extended with DensenetRS predictions)

The standard digital image database for Tuberculosis is created by the 
National Library of Medicine, Maryland, USA in collaboration with Shenzhen 
No.3 People’s Hospital, Guangdong Medical College, Shenzhen, China. 
The Chest X-rays are from out-patient clinics, and were captured as part of 
the daily routine using Philips DR Digital Diagnose systems. 

* Reference: [MONTGOMERY-SHENZHEN-2014]_
* Original resolution (height x width or width x height): 3000 x 3000 or less
* Split reference: none
* Protocol ``default``:

  * Training samples: 64% of TB and healthy CXR (including labels)
  * Validation samples: 16% of TB and healthy CXR (including labels)
  * Test samples: 20% of TB and healthy CXR (including labels)

"""

import os
import pkg_resources

import bob.extension

from ..dataset import JSONDataset
from ..loader import make_delayed

_protocols = [
    pkg_resources.resource_filename(__name__, "default.json"),
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
"""Extended Shenzhen dataset object"""