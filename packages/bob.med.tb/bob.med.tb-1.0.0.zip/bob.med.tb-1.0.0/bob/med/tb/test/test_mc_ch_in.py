#!/usr/bin/env python
# coding=utf-8


"""Tests for the aggregated Montgomery-Shenzhen-Indian dataset"""

import os

import numpy
import nose.tools

from ..configs.datasets.mc_ch_in import default as mc_ch_in
from ..configs.datasets.montgomery import default as mc
from ..configs.datasets.shenzhen import default as ch
from ..configs.datasets.indian import default as indian
from ..configs.datasets.mc_ch_in import fold_0 as mc_ch_in_f0
from ..configs.datasets.montgomery import fold_0 as mc_f0
from ..configs.datasets.shenzhen import fold_0 as ch_f0
from ..configs.datasets.indian import fold_0 as indian_f0
from ..configs.datasets.mc_ch_in import fold_1 as mc_ch_in_f1
from ..configs.datasets.montgomery import fold_1 as mc_f1
from ..configs.datasets.shenzhen import fold_1 as ch_f1
from ..configs.datasets.indian import fold_1 as indian_f1
from ..configs.datasets.mc_ch_in import fold_2 as mc_ch_in_f2
from ..configs.datasets.montgomery import fold_2 as mc_f2
from ..configs.datasets.shenzhen import fold_2 as ch_f2
from ..configs.datasets.indian import fold_2 as indian_f2
from ..configs.datasets.mc_ch_in import fold_3 as mc_ch_in_f3
from ..configs.datasets.montgomery import fold_3 as mc_f3
from ..configs.datasets.shenzhen import fold_3 as ch_f3
from ..configs.datasets.indian import fold_3 as indian_f3
from ..configs.datasets.mc_ch_in import fold_4 as mc_ch_in_f4
from ..configs.datasets.montgomery import fold_4 as mc_f4
from ..configs.datasets.shenzhen import fold_4 as ch_f4
from ..configs.datasets.indian import fold_4 as indian_f4
from ..configs.datasets.mc_ch_in import fold_5 as mc_ch_in_f5
from ..configs.datasets.montgomery import fold_5 as mc_f5
from ..configs.datasets.shenzhen import fold_5 as ch_f5
from ..configs.datasets.indian import fold_5 as indian_f5
from ..configs.datasets.mc_ch_in import fold_6 as mc_ch_in_f6
from ..configs.datasets.montgomery import fold_6 as mc_f6
from ..configs.datasets.shenzhen import fold_6 as ch_f6
from ..configs.datasets.indian import fold_6 as indian_f6
from ..configs.datasets.mc_ch_in import fold_7 as mc_ch_in_f7
from ..configs.datasets.montgomery import fold_7 as mc_f7
from ..configs.datasets.shenzhen import fold_7 as ch_f7
from ..configs.datasets.indian import fold_7 as indian_f7
from ..configs.datasets.mc_ch_in import fold_8 as mc_ch_in_f8
from ..configs.datasets.montgomery import fold_8 as mc_f8
from ..configs.datasets.shenzhen import fold_8 as ch_f8
from ..configs.datasets.indian import fold_8 as indian_f8
from ..configs.datasets.mc_ch_in import fold_9 as mc_ch_in_f9
from ..configs.datasets.montgomery import fold_9 as mc_f9
from ..configs.datasets.shenzhen import fold_9 as ch_f9
from ..configs.datasets.indian import fold_9 as indian_f9
from ..configs.datasets.mc_ch_in import fold_0_rgb as mc_ch_in_f0_rgb
from ..configs.datasets.montgomery import fold_0_rgb as mc_f0_rgb
from ..configs.datasets.shenzhen import fold_0_rgb as ch_f0_rgb
from ..configs.datasets.indian import fold_0_rgb as indian_f0_rgb
from ..configs.datasets.mc_ch_in import fold_1_rgb as mc_ch_in_f1_rgb
from ..configs.datasets.montgomery import fold_1_rgb as mc_f1_rgb
from ..configs.datasets.shenzhen import fold_1_rgb as ch_f1_rgb
from ..configs.datasets.indian import fold_1_rgb as indian_f1_rgb
from ..configs.datasets.mc_ch_in import fold_2_rgb as mc_ch_in_f2_rgb
from ..configs.datasets.montgomery import fold_2_rgb as mc_f2_rgb
from ..configs.datasets.shenzhen import fold_2_rgb as ch_f2_rgb
from ..configs.datasets.indian import fold_2_rgb as indian_f2_rgb
from ..configs.datasets.mc_ch_in import fold_3_rgb as mc_ch_in_f3_rgb
from ..configs.datasets.montgomery import fold_3_rgb as mc_f3_rgb
from ..configs.datasets.shenzhen import fold_3_rgb as ch_f3_rgb
from ..configs.datasets.indian import fold_3_rgb as indian_f3_rgb
from ..configs.datasets.mc_ch_in import fold_4_rgb as mc_ch_in_f4_rgb
from ..configs.datasets.montgomery import fold_4_rgb as mc_f4_rgb
from ..configs.datasets.shenzhen import fold_4_rgb as ch_f4_rgb
from ..configs.datasets.indian import fold_4_rgb as indian_f4_rgb
from ..configs.datasets.mc_ch_in import fold_5_rgb as mc_ch_in_f5_rgb
from ..configs.datasets.montgomery import fold_5_rgb as mc_f5_rgb
from ..configs.datasets.shenzhen import fold_5_rgb as ch_f5_rgb
from ..configs.datasets.indian import fold_5_rgb as indian_f5_rgb
from ..configs.datasets.mc_ch_in import fold_6_rgb as mc_ch_in_f6_rgb
from ..configs.datasets.montgomery import fold_6_rgb as mc_f6_rgb
from ..configs.datasets.shenzhen import fold_6_rgb as ch_f6_rgb
from ..configs.datasets.indian import fold_6_rgb as indian_f6_rgb
from ..configs.datasets.mc_ch_in import fold_7_rgb as mc_ch_in_f7_rgb
from ..configs.datasets.montgomery import fold_7_rgb as mc_f7_rgb
from ..configs.datasets.shenzhen import fold_7_rgb as ch_f7_rgb
from ..configs.datasets.indian import fold_7_rgb as indian_f7_rgb
from ..configs.datasets.mc_ch_in import fold_8_rgb as mc_ch_in_f8_rgb
from ..configs.datasets.montgomery import fold_8_rgb as mc_f8_rgb
from ..configs.datasets.shenzhen import fold_8_rgb as ch_f8_rgb
from ..configs.datasets.indian import fold_8_rgb as indian_f8_rgb
from ..configs.datasets.mc_ch_in import fold_9_rgb as mc_ch_in_f9_rgb
from ..configs.datasets.montgomery import fold_9_rgb as mc_f9_rgb
from ..configs.datasets.shenzhen import fold_9_rgb as ch_f9_rgb
from ..configs.datasets.indian import fold_9_rgb as indian_f9_rgb
from .utils import rc_variable_set

@rc_variable_set('bob.med.tb.montgomery.datadir')
@rc_variable_set('bob.med.tb.shenzhen.datadir')
@rc_variable_set('bob.med.tb.indian.datadir')
def test_dataset_consistency():

    # Default protocol
    mc_ch_in_dataset = mc_ch_in.dataset
    assert isinstance(mc_ch_in_dataset, dict)

    mc_dataset = mc.dataset
    ch_dataset = ch.dataset
    in_dataset = indian.dataset

    assert "train" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"]) \
            + len(in_dataset["train"])
        )

    assert "validation" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"]) \
            + len(in_dataset["validation"])
        )

    assert "test" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"]) \
            + len(in_dataset["test"])
        )

    # Fold 0
    mc_ch_in_dataset = mc_ch_in_f0.dataset
    assert isinstance(mc_ch_in_dataset, dict)

    mc_dataset = mc_f0.dataset
    ch_dataset = ch_f0.dataset
    in_dataset = indian_f0.dataset

    assert "train" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"]) \
            + len(in_dataset["train"])
        )

    assert "validation" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"]) \
            + len(in_dataset["validation"])
        )

    assert "test" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"]) \
            + len(in_dataset["test"])
        )

    # Fold 1
    mc_ch_in_dataset = mc_ch_in_f1.dataset
    assert isinstance(mc_ch_in_dataset, dict)

    mc_dataset = mc_f1.dataset
    ch_dataset = ch_f1.dataset
    in_dataset = indian_f1.dataset

    assert "train" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"]) \
            + len(in_dataset["train"])
        )

    assert "validation" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"]) \
            + len(in_dataset["validation"])
        )

    assert "test" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"]) \
            + len(in_dataset["test"])
        )

    # Fold 2
    mc_ch_in_dataset = mc_ch_in_f2.dataset
    assert isinstance(mc_ch_in_dataset, dict)

    mc_dataset = mc_f2.dataset
    ch_dataset = ch_f2.dataset
    in_dataset = indian_f2.dataset

    assert "train" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"]) \
            + len(in_dataset["train"])
        )

    assert "validation" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"]) \
            + len(in_dataset["validation"])
        )

    assert "test" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"]) \
            + len(in_dataset["test"])
        )

    # Fold 3
    mc_ch_in_dataset = mc_ch_in_f3.dataset
    assert isinstance(mc_ch_in_dataset, dict)

    mc_dataset = mc_f3.dataset
    ch_dataset = ch_f3.dataset
    in_dataset = indian_f3.dataset

    assert "train" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"]) \
            + len(in_dataset["train"])
        )

    assert "validation" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"]) \
            + len(in_dataset["validation"])
        )

    assert "test" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"]) \
            + len(in_dataset["test"])
        )

    # Fold 4
    mc_ch_in_dataset = mc_ch_in_f4.dataset
    assert isinstance(mc_ch_in_dataset, dict)

    mc_dataset = mc_f4.dataset
    ch_dataset = ch_f4.dataset
    in_dataset = indian_f4.dataset

    assert "train" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"]) \
            + len(in_dataset["train"])
        )

    assert "validation" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"]) \
            + len(in_dataset["validation"])
        )

    assert "test" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"]) \
            + len(in_dataset["test"])
        )

    # Fold 5
    mc_ch_in_dataset = mc_ch_in_f5.dataset
    assert isinstance(mc_ch_in_dataset, dict)

    mc_dataset = mc_f5.dataset
    ch_dataset = ch_f5.dataset
    in_dataset = indian_f5.dataset

    assert "train" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"]) \
            + len(in_dataset["train"])
        )

    assert "validation" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"]) \
            + len(in_dataset["validation"])
        )

    assert "test" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"]) \
            + len(in_dataset["test"])
        )

    # Fold 6
    mc_ch_in_dataset = mc_ch_in_f6.dataset
    assert isinstance(mc_ch_in_dataset, dict)

    mc_dataset = mc_f6.dataset
    ch_dataset = ch_f6.dataset
    in_dataset = indian_f6.dataset

    assert "train" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"]) \
            + len(in_dataset["train"])
        )

    assert "validation" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"]) \
            + len(in_dataset["validation"])
        )

    assert "test" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"]) \
            + len(in_dataset["test"])
        )

    # Fold 7
    mc_ch_in_dataset = mc_ch_in_f7.dataset
    assert isinstance(mc_ch_in_dataset, dict)

    mc_dataset = mc_f7.dataset
    ch_dataset = ch_f7.dataset
    in_dataset = indian_f7.dataset

    assert "train" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"]) \
            + len(in_dataset["train"])
        )

    assert "validation" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"]) \
            + len(in_dataset["validation"])
        )

    assert "test" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"]) \
            + len(in_dataset["test"])
        )

    # Fold 8
    mc_ch_in_dataset = mc_ch_in_f8.dataset
    assert isinstance(mc_ch_in_dataset, dict)

    mc_dataset = mc_f8.dataset
    ch_dataset = ch_f8.dataset
    in_dataset = indian_f8.dataset

    assert "train" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"]) \
            + len(in_dataset["train"])
        )

    assert "validation" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"]) \
            + len(in_dataset["validation"])
        )

    assert "test" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"]) \
            + len(in_dataset["test"])
        )

    # Fold 9
    mc_ch_in_dataset = mc_ch_in_f9.dataset
    assert isinstance(mc_ch_in_dataset, dict)

    mc_dataset = mc_f9.dataset
    ch_dataset = ch_f9.dataset
    in_dataset = indian_f9.dataset

    assert "train" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"]) \
            + len(in_dataset["train"])
        )

    assert "validation" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"]) \
            + len(in_dataset["validation"])
        )

    assert "test" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"]) \
            + len(in_dataset["test"])
        )

    # Fold 0, RGB
    mc_ch_in_dataset = mc_ch_in_f0_rgb.dataset
    assert isinstance(mc_ch_in_dataset, dict)

    mc_dataset = mc_f0_rgb.dataset
    ch_dataset = ch_f0_rgb.dataset
    in_dataset = indian_f0_rgb.dataset

    assert "train" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"]) \
            + len(in_dataset["train"])
        )

    assert "validation" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"]) \
            + len(in_dataset["validation"])
        )

    assert "test" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"]) \
            + len(in_dataset["test"])
        )

    # Fold 1, RGB
    mc_ch_in_dataset = mc_ch_in_f1_rgb.dataset
    assert isinstance(mc_ch_in_dataset, dict)

    mc_dataset = mc_f1_rgb.dataset
    ch_dataset = ch_f1_rgb.dataset
    in_dataset = indian_f1_rgb.dataset

    assert "train" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"]) \
            + len(in_dataset["train"])
        )

    assert "validation" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"]) \
            + len(in_dataset["validation"])
        )

    assert "test" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"]) \
            + len(in_dataset["test"])
        )

    # Fold 2, RGB
    mc_ch_in_dataset = mc_ch_in_f2_rgb.dataset
    assert isinstance(mc_ch_in_dataset, dict)

    mc_dataset = mc_f2_rgb.dataset
    ch_dataset = ch_f2_rgb.dataset
    in_dataset = indian_f2_rgb.dataset

    assert "train" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"]) \
            + len(in_dataset["train"])
        )

    assert "validation" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"]) \
            + len(in_dataset["validation"])
        )

    assert "test" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"]) \
            + len(in_dataset["test"])
        )

    # Fold 3, RGB
    mc_ch_in_dataset = mc_ch_in_f3_rgb.dataset
    assert isinstance(mc_ch_in_dataset, dict)

    mc_dataset = mc_f3_rgb.dataset
    ch_dataset = ch_f3_rgb.dataset
    in_dataset = indian_f3_rgb.dataset

    assert "train" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"]) \
            + len(in_dataset["train"])
        )

    assert "validation" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"]) \
            + len(in_dataset["validation"])
        )

    assert "test" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"]) \
            + len(in_dataset["test"])
        )

    # Fold 4, RGB
    mc_ch_in_dataset = mc_ch_in_f4_rgb.dataset
    assert isinstance(mc_ch_in_dataset, dict)

    mc_dataset = mc_f4_rgb.dataset
    ch_dataset = ch_f4_rgb.dataset
    in_dataset = indian_f4_rgb.dataset

    assert "train" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"]) \
            + len(in_dataset["train"])
        )

    assert "validation" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"]) \
            + len(in_dataset["validation"])
        )

    assert "test" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"]) \
            + len(in_dataset["test"])
        )

    # Fold 5, RGB
    mc_ch_in_dataset = mc_ch_in_f5_rgb.dataset
    assert isinstance(mc_ch_in_dataset, dict)

    mc_dataset = mc_f5_rgb.dataset
    ch_dataset = ch_f5_rgb.dataset
    in_dataset = indian_f5_rgb.dataset

    assert "train" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"]) \
            + len(in_dataset["train"])
        )

    assert "validation" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"]) \
            + len(in_dataset["validation"])
        )

    assert "test" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"]) \
            + len(in_dataset["test"])
        )

    # Fold 6, RGB
    mc_ch_in_dataset = mc_ch_in_f6_rgb.dataset
    assert isinstance(mc_ch_in_dataset, dict)

    mc_dataset = mc_f6_rgb.dataset
    ch_dataset = ch_f6_rgb.dataset
    in_dataset = indian_f6_rgb.dataset

    assert "train" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"]) \
            + len(in_dataset["train"])
        )

    assert "validation" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"]) \
            + len(in_dataset["validation"])
        )

    assert "test" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"]) \
            + len(in_dataset["test"])
        )

    # Fold 7, RGB
    mc_ch_in_dataset = mc_ch_in_f7_rgb.dataset
    assert isinstance(mc_ch_in_dataset, dict)

    mc_dataset = mc_f7_rgb.dataset
    ch_dataset = ch_f7_rgb.dataset
    in_dataset = indian_f7_rgb.dataset

    assert "train" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"]) \
            + len(in_dataset["train"])
        )

    assert "validation" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"]) \
            + len(in_dataset["validation"])
        )

    assert "test" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"]) \
            + len(in_dataset["test"])
        )

    # Fold 8, RGB
    mc_ch_in_dataset = mc_ch_in_f8_rgb.dataset
    assert isinstance(mc_ch_in_dataset, dict)

    mc_dataset = mc_f8_rgb.dataset
    ch_dataset = ch_f8_rgb.dataset
    in_dataset = indian_f8_rgb.dataset

    assert "train" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"]) \
            + len(in_dataset["train"])
        )

    assert "validation" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"]) \
            + len(in_dataset["validation"])
        )

    assert "test" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"]) \
            + len(in_dataset["test"])
        )

    # Fold 9, RGB
    mc_ch_in_dataset = mc_ch_in_f9_rgb.dataset
    assert isinstance(mc_ch_in_dataset, dict)

    mc_dataset = mc_f9_rgb.dataset
    ch_dataset = ch_f9_rgb.dataset
    in_dataset = indian_f9_rgb.dataset

    assert "train" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"]) \
            + len(in_dataset["train"])
        )

    assert "validation" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"]) \
            + len(in_dataset["validation"])
        )

    assert "test" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"]) \
            + len(in_dataset["test"])
        )