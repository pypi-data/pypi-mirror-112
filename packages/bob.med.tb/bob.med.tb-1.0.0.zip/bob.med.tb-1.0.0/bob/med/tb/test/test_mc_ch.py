#!/usr/bin/env python
# coding=utf-8


"""Tests for the aggregated Montgomery-Shenzhen dataset"""

import os

import numpy
import nose.tools

from ..configs.datasets.mc_ch import default as mc_ch
from ..configs.datasets.montgomery import default as mc
from ..configs.datasets.shenzhen import default as ch
from ..configs.datasets.mc_ch import fold_0 as mc_ch_f0
from ..configs.datasets.montgomery import fold_0 as mc_f0
from ..configs.datasets.shenzhen import fold_0 as ch_f0
from ..configs.datasets.mc_ch import fold_1 as mc_ch_f1
from ..configs.datasets.montgomery import fold_1 as mc_f1
from ..configs.datasets.shenzhen import fold_1 as ch_f1
from ..configs.datasets.mc_ch import fold_2 as mc_ch_f2
from ..configs.datasets.montgomery import fold_2 as mc_f2
from ..configs.datasets.shenzhen import fold_2 as ch_f2
from ..configs.datasets.mc_ch import fold_3 as mc_ch_f3
from ..configs.datasets.montgomery import fold_3 as mc_f3
from ..configs.datasets.shenzhen import fold_3 as ch_f3
from ..configs.datasets.mc_ch import fold_4 as mc_ch_f4
from ..configs.datasets.montgomery import fold_4 as mc_f4
from ..configs.datasets.shenzhen import fold_4 as ch_f4
from ..configs.datasets.mc_ch import fold_5 as mc_ch_f5
from ..configs.datasets.montgomery import fold_5 as mc_f5
from ..configs.datasets.shenzhen import fold_5 as ch_f5
from ..configs.datasets.mc_ch import fold_6 as mc_ch_f6
from ..configs.datasets.montgomery import fold_6 as mc_f6
from ..configs.datasets.shenzhen import fold_6 as ch_f6
from ..configs.datasets.mc_ch import fold_7 as mc_ch_f7
from ..configs.datasets.montgomery import fold_7 as mc_f7
from ..configs.datasets.shenzhen import fold_7 as ch_f7
from ..configs.datasets.mc_ch import fold_8 as mc_ch_f8
from ..configs.datasets.montgomery import fold_8 as mc_f8
from ..configs.datasets.shenzhen import fold_8 as ch_f8
from ..configs.datasets.mc_ch import fold_9 as mc_ch_f9
from ..configs.datasets.montgomery import fold_9 as mc_f9
from ..configs.datasets.shenzhen import fold_9 as ch_f9
from ..configs.datasets.mc_ch import fold_0_rgb as mc_ch_f0_rgb
from ..configs.datasets.montgomery import fold_0_rgb as mc_f0_rgb
from ..configs.datasets.shenzhen import fold_0_rgb as ch_f0_rgb
from ..configs.datasets.mc_ch import fold_1_rgb as mc_ch_f1_rgb
from ..configs.datasets.montgomery import fold_1_rgb as mc_f1_rgb
from ..configs.datasets.shenzhen import fold_1_rgb as ch_f1_rgb
from ..configs.datasets.mc_ch import fold_2_rgb as mc_ch_f2_rgb
from ..configs.datasets.montgomery import fold_2_rgb as mc_f2_rgb
from ..configs.datasets.shenzhen import fold_2_rgb as ch_f2_rgb
from ..configs.datasets.mc_ch import fold_3_rgb as mc_ch_f3_rgb
from ..configs.datasets.montgomery import fold_3_rgb as mc_f3_rgb
from ..configs.datasets.shenzhen import fold_3_rgb as ch_f3_rgb
from ..configs.datasets.mc_ch import fold_4_rgb as mc_ch_f4_rgb
from ..configs.datasets.montgomery import fold_4_rgb as mc_f4_rgb
from ..configs.datasets.shenzhen import fold_4_rgb as ch_f4_rgb
from ..configs.datasets.mc_ch import fold_5_rgb as mc_ch_f5_rgb
from ..configs.datasets.montgomery import fold_5_rgb as mc_f5_rgb
from ..configs.datasets.shenzhen import fold_5_rgb as ch_f5_rgb
from ..configs.datasets.mc_ch import fold_6_rgb as mc_ch_f6_rgb
from ..configs.datasets.montgomery import fold_6_rgb as mc_f6_rgb
from ..configs.datasets.shenzhen import fold_6_rgb as ch_f6_rgb
from ..configs.datasets.mc_ch import fold_7_rgb as mc_ch_f7_rgb
from ..configs.datasets.montgomery import fold_7_rgb as mc_f7_rgb
from ..configs.datasets.shenzhen import fold_7_rgb as ch_f7_rgb
from ..configs.datasets.mc_ch import fold_8_rgb as mc_ch_f8_rgb
from ..configs.datasets.montgomery import fold_8_rgb as mc_f8_rgb
from ..configs.datasets.shenzhen import fold_8_rgb as ch_f8_rgb
from ..configs.datasets.mc_ch import fold_9_rgb as mc_ch_f9_rgb
from ..configs.datasets.montgomery import fold_9_rgb as mc_f9_rgb
from ..configs.datasets.shenzhen import fold_9_rgb as ch_f9_rgb
from .utils import rc_variable_set

@rc_variable_set('bob.med.tb.montgomery.datadir')
@rc_variable_set('bob.med.tb.shenzhen.datadir')
def test_dataset_consistency():

    # Default protocol
    mc_ch_dataset = mc_ch.dataset
    assert isinstance(mc_ch_dataset, dict)

    mc_dataset = mc.dataset
    ch_dataset = ch.dataset

    assert "train" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"])
        )

    assert "validation" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"])
        )

    assert "test" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"])
        )

    # f0 protocol
    mc_ch_dataset = mc_ch_f0.dataset
    assert isinstance(mc_ch_dataset, dict)

    mc_dataset = mc_f0.dataset
    ch_dataset = ch_f0.dataset

    assert "train" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"])
        )

    assert "validation" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"])
        )

    assert "test" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"])
        )

    # f1 protocol
    mc_ch_dataset = mc_ch_f1.dataset
    assert isinstance(mc_ch_dataset, dict)

    mc_dataset = mc_f1.dataset
    ch_dataset = ch_f1.dataset

    assert "train" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"])
        )

    assert "validation" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"])
        )

    assert "test" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"])
        )

    # f2 protocol
    mc_ch_dataset = mc_ch_f2.dataset
    assert isinstance(mc_ch_dataset, dict)

    mc_dataset = mc_f2.dataset
    ch_dataset = ch_f2.dataset

    assert "train" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"])
        )

    assert "validation" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"])
        )

    assert "test" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"])
        )

    # f3 protocol
    mc_ch_dataset = mc_ch_f3.dataset
    assert isinstance(mc_ch_dataset, dict)

    mc_dataset = mc_f3.dataset
    ch_dataset = ch_f3.dataset

    assert "train" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"])
        )

    assert "validation" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"])
        )

    assert "test" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"])
        )

    # f4 protocol
    mc_ch_dataset = mc_ch_f4.dataset
    assert isinstance(mc_ch_dataset, dict)

    mc_dataset = mc_f4.dataset
    ch_dataset = ch_f4.dataset

    assert "train" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"])
        )

    assert "validation" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"])
        )

    assert "test" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"])
        )

    # f5 protocol
    mc_ch_dataset = mc_ch_f5.dataset
    assert isinstance(mc_ch_dataset, dict)

    mc_dataset = mc_f5.dataset
    ch_dataset = ch_f5.dataset

    assert "train" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"])
        )

    assert "validation" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"])
        )

    assert "test" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"])
        )

    # f6 protocol
    mc_ch_dataset = mc_ch_f6.dataset
    assert isinstance(mc_ch_dataset, dict)

    mc_dataset = mc_f6.dataset
    ch_dataset = ch_f6.dataset

    assert "train" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"])
        )

    assert "validation" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"])
        )

    assert "test" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"])
        )

    # f7 protocol
    mc_ch_dataset = mc_ch_f7.dataset
    assert isinstance(mc_ch_dataset, dict)

    mc_dataset = mc_f7.dataset
    ch_dataset = ch_f7.dataset

    assert "train" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"])
        )

    assert "validation" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"])
        )

    assert "test" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"])
        )

    # f8 protocol
    mc_ch_dataset = mc_ch_f8.dataset
    assert isinstance(mc_ch_dataset, dict)

    mc_dataset = mc_f8.dataset
    ch_dataset = ch_f8.dataset

    assert "train" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"])
        )

    assert "validation" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"])
        )

    assert "test" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"])
        )

    # f9 protocol
    mc_ch_dataset = mc_ch_f9.dataset
    assert isinstance(mc_ch_dataset, dict)

    mc_dataset = mc_f9.dataset
    ch_dataset = ch_f9.dataset

    assert "train" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"])
        )

    assert "validation" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"])
        )

    assert "test" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"])
        )

    # f0 protocol RGB
    mc_ch_dataset = mc_ch_f0_rgb.dataset
    assert isinstance(mc_ch_dataset, dict)

    mc_dataset = mc_f0_rgb.dataset
    ch_dataset = ch_f0_rgb.dataset

    assert "train" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"])
        )

    assert "validation" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"])
        )

    assert "test" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"])
        )

    # f1 protocol RGB
    mc_ch_dataset = mc_ch_f1_rgb.dataset
    assert isinstance(mc_ch_dataset, dict)

    mc_dataset = mc_f1_rgb.dataset
    ch_dataset = ch_f1_rgb.dataset

    assert "train" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"])
        )

    assert "validation" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"])
        )

    assert "test" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"])
        )

    # f2 protocol RGB
    mc_ch_dataset = mc_ch_f2_rgb.dataset
    assert isinstance(mc_ch_dataset, dict)

    mc_dataset = mc_f2_rgb.dataset
    ch_dataset = ch_f2_rgb.dataset

    assert "train" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"])
        )

    assert "validation" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"])
        )

    assert "test" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"])
        )

    # f3 protocol RGB
    mc_ch_dataset = mc_ch_f3_rgb.dataset
    assert isinstance(mc_ch_dataset, dict)

    mc_dataset = mc_f3_rgb.dataset
    ch_dataset = ch_f3_rgb.dataset

    assert "train" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"])
        )

    assert "validation" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"])
        )

    assert "test" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"])
        )

    # f4 protocol RGB
    mc_ch_dataset = mc_ch_f4_rgb.dataset
    assert isinstance(mc_ch_dataset, dict)

    mc_dataset = mc_f4_rgb.dataset
    ch_dataset = ch_f4_rgb.dataset

    assert "train" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"])
        )

    assert "validation" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"])
        )

    assert "test" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"])
        )

    # f5 protocol RGB
    mc_ch_dataset = mc_ch_f5_rgb.dataset
    assert isinstance(mc_ch_dataset, dict)

    mc_dataset = mc_f5_rgb.dataset
    ch_dataset = ch_f5_rgb.dataset

    assert "train" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"])
        )

    assert "validation" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"])
        )

    assert "test" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"])
        )

    # f6 protocol RGB
    mc_ch_dataset = mc_ch_f6_rgb.dataset
    assert isinstance(mc_ch_dataset, dict)

    mc_dataset = mc_f6_rgb.dataset
    ch_dataset = ch_f6_rgb.dataset

    assert "train" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"])
        )

    assert "validation" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"])
        )

    assert "test" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"])
        )

    # f7 protocol RGB
    mc_ch_dataset = mc_ch_f7_rgb.dataset
    assert isinstance(mc_ch_dataset, dict)

    mc_dataset = mc_f7_rgb.dataset
    ch_dataset = ch_f7_rgb.dataset

    assert "train" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"])
        )

    assert "validation" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"])
        )

    assert "test" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"])
        )

    # f8 protocol RGB
    mc_ch_dataset = mc_ch_f8_rgb.dataset
    assert isinstance(mc_ch_dataset, dict)

    mc_dataset = mc_f8_rgb.dataset
    ch_dataset = ch_f8_rgb.dataset

    assert "train" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"])
        )

    assert "validation" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"])
        )

    assert "test" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"])
        )

    # f9 protocol RGB
    mc_ch_dataset = mc_ch_f9_rgb.dataset
    assert isinstance(mc_ch_dataset, dict)

    mc_dataset = mc_f9_rgb.dataset
    ch_dataset = ch_f9_rgb.dataset

    assert "train" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"])
        )

    assert "validation" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"])
        )

    assert "test" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"])
        )