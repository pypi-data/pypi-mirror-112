#!/usr/bin/env python
# coding=utf-8

"""Indian collection dataset for computer-aided diagnosis
(extended with DensenetRS predictions)

The Indian collection database has been established to foster research
in computer-aided diagnosis of pulmonary diseases with a special
focus on pulmonary tuberculosis (TB).

* Reference: [INDIAN-2013]_
* Original resolution (height x width or width x height): more than 1024 x 1024
* Split reference: [INDIAN-2013]_ with 20% of train set for the validation set

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
"""Extended Indian dataset object"""
