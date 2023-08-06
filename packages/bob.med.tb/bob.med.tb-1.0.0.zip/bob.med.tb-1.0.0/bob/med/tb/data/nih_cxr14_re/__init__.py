#!/usr/bin/env python
# coding=utf-8

"""NIH CXR14 (relabeled) dataset for computer-aided diagnosis

This dataset was extracted from the clinical PACS database at the National 
Institutes of Health Clinical Center (USA) and represents 60% of all 
their radiographs. It contains labels for fourteen common radiological 
signs in this order: cardiomegaly, emphysema, effusion, hernia, infiltration,
mass, nodule, atelectasis, pneumothorax, pleural thickening, pneumonia, 
fibrosis, edema and consolidation. 
This is the relabeled version created in the CheXNeXt study.

* Reference: [NIH-CXR14-2017]_
* Original resolution (height x width or width x height): 1024 x 1024
* Labels: [CHEXNEXT-2018]_
* Split reference: [CHEXNEXT-2018]_
* Protocol ``default``:

  * Training samples: 98'637 (including labels)
  * Validation samples: 6'350 (including labels)
  * Test samples: 0

* Protocol `ìdiap``:
  * Images path adapted to Idiap infrastructure

"""

import os
import pkg_resources

import bob.extension

from ..dataset import JSONDataset
from ..loader import load_pil_rgb, make_delayed

_protocols = [
    pkg_resources.resource_filename(__name__, "default.json"),
    pkg_resources.resource_filename(__name__, "idiap.json"),
    pkg_resources.resource_filename(__name__, "cardiomegaly_idiap.json"),
]


def _raw_data_loader(sample):
    return dict(
        data=load_pil_rgb(
            os.path.join(
                bob.extension.rc.get(
                    "bob.med.tb.nih_cxr14_re.datadir", os.path.realpath(os.curdir)
                ),
                sample["data"],
            )
        ),
        label=sample["label"],
    )


def _loader(context, sample):
    # "context" is ignored in this case - database is homogeneous
    # we returned delayed samples to avoid loading all images at once
    return make_delayed(sample, _raw_data_loader)


dataset = JSONDataset(
    protocols=_protocols, fieldnames=("data", "label"), loader=_loader,
)
"""NIH CXR14 (relabeled) dataset object"""
