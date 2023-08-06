#!/usr/bin/env python
# coding=utf-8

"""Padchest dataset for computer-aided diagnosis

A large chest x-ray image dataset with multi-label annotated reports.
This dataset includes more than 160,000 images from 67,000 patients that were 
interpreted and reported by radiologists at Hospital San Juan (Spain) from 2009
to 2017, covering six different position views and additional information on
image acquisition and patient demography.

We keep only "PA" images here.

* Reference: [PADCHEST-2019]_
* Original resolution: variable, original size
* Labels: [PADCHEST-2019]_
* Split reference: no split
* Protocol ``default``:

  * Training samples: 96'269
  * Validation samples: 0
  * Test samples: 0

* Protocol `ìdiap``:
  * Images path adapted to Idiap infrastructure

* Labels:

['COPD signs',
'Chilaiditi sign',
'NSG tube',
'abnormal foreign body',
'abscess',
'adenopathy',
'air bronchogram',
'air fluid level',
'air trapping',
'alveolar pattern',
'aortic aneurysm',
'aortic atheromatosis',
'aortic button enlargement',
'aortic elongation',
'aortic endoprosthesis',
'apical pleural thickening',
'artificial aortic heart valve',
'artificial heart valve',
'artificial mitral heart valve',
'asbestosis signs',
'ascendent aortic elongation',
'atelectasis',
'atelectasis basal',
'atypical pneumonia',
'axial hyperostosis',
'azygoesophageal recess shift',
'azygos lobe',
'blastic bone lesion',
'bone cement',
'bone metastasis',
'breast mass',
'bronchiectasis',
'bronchovascular markings',
'bullas',
'calcified adenopathy',
'calcified densities',
'calcified fibroadenoma',
'calcified granuloma',
'calcified mediastinal adenopathy',
'calcified pleural plaques',
'calcified pleural thickening',
'callus rib fracture',
'cardiomegaly',
'catheter',
'cavitation',
'central vascular redistribution',
'central venous catheter',
'central venous catheter via jugular vein',
'central venous catheter via subclavian vein',
'central venous catheter via umbilical vein',
'cervical rib',
'chest drain tube',
'chronic changes',
'clavicle fracture',
'consolidation',
'costochondral junction hypertrophy',
'costophrenic angle blunting',
'cyst',
'dai',
'descendent aortic elongation',
'dextrocardia',
'diaphragmatic eventration',
'double J stent',
'dual chamber device',
'electrical device',
'emphysema',
'empyema',
'end on vessel',
'endoprosthesis',
'endotracheal tube',
'esophagic dilatation',
'exclude',
'external foreign body',
'fibrotic band',
'fissure thickening',
'flattened diaphragm',
'fracture',
'gastrostomy tube',
'goiter',
'granuloma',
'ground glass pattern',
'gynecomastia',
'heart insufficiency',
'heart valve calcified',
'hemidiaphragm elevation',
'hiatal hernia',
'hilar congestion',
'hilar enlargement',
'humeral fracture',
'humeral prosthesis',
'hydropneumothorax',
'hyperinflated lung',
'hypoexpansion',
'hypoexpansion basal',
'increased density',
'infiltrates',
'interstitial pattern',
'kerley lines',
'kyphosis',
'laminar atelectasis',
'lepidic adenocarcinoma',
'lipomatosis',
'lobar atelectasis',
'loculated fissural effusion',
'loculated pleural effusion',
'lung metastasis',
'lung vascular paucity',
'lymphangitis carcinomatosa',
'lytic bone lesion',
'major fissure thickening',
'mammary prosthesis',
'mass',
'mastectomy',
'mediastinal enlargement',
'mediastinal mass',
'mediastinal shift',
'mediastinic lipomatosis',
'metal',
'miliary opacities',
'minor fissure thickening',
'multiple nodules',
'nephrostomy tube',
'nipple shadow',
'nodule',
'non axial articular degenerative changes',
'normal',
'obesity',
'osteopenia',
'osteoporosis',
'osteosynthesis material',
'pacemaker',
'pectum carinatum',
'pectum excavatum',
'pericardial effusion',
'pleural effusion',
'pleural mass',
'pleural plaques',
'pleural thickening',
'pneumomediastinum',
'pneumonia',
'pneumoperitoneo',
'pneumothorax',
'post radiotherapy changes',
'prosthesis',
'pseudonodule',
'pulmonary artery enlargement',
'pulmonary artery hypertension',
'pulmonary edema',
'pulmonary fibrosis',
'pulmonary hypertension',
'pulmonary mass',
'pulmonary venous hypertension',
'reservoir central venous catheter',
'respiratory distress',
'reticular interstitial pattern',
'reticulonodular interstitial pattern',
'rib fracture',
'right sided aortic arch',
'round atelectasis',
'sclerotic bone lesion',
'scoliosis',
'segmental atelectasis',
'single chamber device',
'soft tissue mass',
'sternoclavicular junction hypertrophy',
'sternotomy',
'subacromial space narrowing',
'subcutaneous emphysema',
'suboptimal study',
'superior mediastinal enlargement',
'supra aortic elongation',
'surgery',
'surgery breast',
'surgery heart',
'surgery humeral',
'surgery lung',
'surgery neck',
'suture material',
'thoracic cage deformation',
'total atelectasis',
'tracheal shift',
'tracheostomy tube',
'tuberculosis',
'tuberculosis sequelae',
'unchanged',
'vascular hilar enlargement',
'vascular redistribution',
'ventriculoperitoneal drain tube',
'vertebral anterior compression',
'vertebral compression',
'vertebral degenerative changes',
'vertebral fracture',
'volume loss']
"""

import os
import pkg_resources

import bob.extension

from ..dataset import JSONDataset
from ..loader import load_pil, make_delayed

_protocols = [
    pkg_resources.resource_filename(__name__, "idiap.json"),
    pkg_resources.resource_filename(__name__, "tb_idiap.json"),
    pkg_resources.resource_filename(__name__, "no_tb_idiap.json"),
    pkg_resources.resource_filename(__name__, "cardiomegaly_idiap.json"),
]


def _raw_data_loader(sample):
    return dict(
        data=load_pil(
            os.path.join(
                bob.extension.rc.get(
                    "bob.med.tb.padchest.datadir", os.path.realpath(os.curdir)
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
"""Padchest dataset object"""
