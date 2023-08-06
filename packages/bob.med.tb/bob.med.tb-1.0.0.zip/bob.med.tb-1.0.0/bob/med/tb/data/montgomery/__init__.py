#!/usr/bin/env python
# coding=utf-8

"""Montgomery dataset for computer-aided diagnosis

The Montgomery database has been established to foster research
in computer-aided diagnosis of pulmonary diseases with a special
focus on pulmonary tuberculosis (TB).

* Reference: [MONTGOMERY-SHENZHEN-2014]_
* Original resolution (height x width or width x height): 4020 x 4892
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
from ..loader import load_pil_baw, make_delayed

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
        data=load_pil_baw(os.path.join(
            bob.extension.rc.get(
                "bob.med.tb.montgomery.datadir", os.path.realpath(os.curdir)
            ), sample["data"])),
        label=sample["label"],
    )


def _loader(context, sample):
    # "context" is ignored in this case - database is homogeneous
    # we returned delayed samples to avoid loading all images at once
    return make_delayed(sample, _raw_data_loader)


dataset = JSONDataset(
    protocols=_protocols,
    fieldnames=("data", "label"),
    loader=_loader,
)
"""Montgomery dataset object"""
