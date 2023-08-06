.. -*- coding: utf-8 -*-

=====================================
 Application Program Interface (API)
=====================================

.. To update these lists, run the following command on the root of the package:
.. find bob -name '*.py' | sed -e 's#/#.#g;s#.py$##g;s#.__init__##g' | sort
.. You may apply further filtering to update only one of the subsections below


Data Manipulation
-----------------

.. autosummary::
   :toctree: api/data

   bob.med.tb.data.dataset
   bob.med.tb.data.loader
   bob.med.tb.data.sample
   bob.med.tb.data.utils
   bob.med.tb.data.transforms


Datasets
--------

.. autosummary::
   :toctree: api/dataset

   bob.med.tb.data.montgomery
   bob.med.tb.data.montgomery_RS
   bob.med.tb.data.shenzhen
   bob.med.tb.data.shenzhen_RS
   bob.med.tb.data.indian
   bob.med.tb.data.indian_RS
   bob.med.tb.data.nih_cxr14_re
   bob.med.tb.data.padchest
   bob.med.tb.data.padchest_RS
   bob.med.tb.data.hivtb
   bob.med.tb.data.hivtb_RS
   bob.med.tb.data.tbpoc
   bob.med.tb.data.tbpoc_RS


Engines
-------

.. autosummary::
   :toctree: api/engine

   bob.med.tb.engine
   bob.med.tb.engine.trainer
   bob.med.tb.engine.predictor
   bob.med.tb.engine.evaluator


Neural Network Models
---------------------

.. autosummary::
   :toctree: api/models

   bob.med.tb.models
   bob.med.tb.models.normalizer
   bob.med.tb.models.alexnet
   bob.med.tb.models.densenet
   bob.med.tb.models.densenet_rs
   bob.med.tb.models.pasa
   bob.med.tb.models.signs_to_tb
   bob.med.tb.models.logistic_regression
   


Toolbox
-------

.. autosummary::
   :toctree: api/utils

   bob.med.tb.utils
   bob.med.tb.utils.checkpointer
   bob.med.tb.utils.grad_cams
   bob.med.tb.utils.measure
   bob.med.tb.utils.resources
   bob.med.tb.utils.summary


.. _bob.med.tb.configs:

Preset Configurations
---------------------

Preset configurations for baseline systems

This module contains preset configurations for baseline FCN architectures and
datasets.


Models
======

.. autosummary::
   :toctree: api/configs/models
   :template: config.rst

   bob.med.tb.configs.models.pasa
   bob.med.tb.configs.models.alexnet
   bob.med.tb.configs.models.alexnet_pretrained
   bob.med.tb.configs.models.densenet
   bob.med.tb.configs.models.densenet_pretrained
   bob.med.tb.configs.models.signs_to_tb
   bob.med.tb.configs.models.logistic_regression
   bob.med.tb.configs.models_datasets.densenet_rs


.. _bob.med.tb.configs.datasets:

Datasets
========

.. automodule:: bob.med.tb.configs.datasets

.. autosummary::
   :toctree: api/configs/datasets
   :template: config.rst

   bob.med.tb.configs.datasets.hivtb.fold_0
   bob.med.tb.configs.datasets.hivtb.fold_0_rgb
   bob.med.tb.configs.datasets.hivtb.fold_1
   bob.med.tb.configs.datasets.hivtb.fold_1_rgb
   bob.med.tb.configs.datasets.hivtb.fold_2
   bob.med.tb.configs.datasets.hivtb.fold_2_rgb
   bob.med.tb.configs.datasets.hivtb.fold_3
   bob.med.tb.configs.datasets.hivtb.fold_3_rgb
   bob.med.tb.configs.datasets.hivtb.fold_4
   bob.med.tb.configs.datasets.hivtb.fold_4_rgb
   bob.med.tb.configs.datasets.hivtb.fold_5
   bob.med.tb.configs.datasets.hivtb.fold_5_rgb
   bob.med.tb.configs.datasets.hivtb.fold_6
   bob.med.tb.configs.datasets.hivtb.fold_6_rgb
   bob.med.tb.configs.datasets.hivtb.fold_7
   bob.med.tb.configs.datasets.hivtb.fold_7_rgb
   bob.med.tb.configs.datasets.hivtb.fold_8
   bob.med.tb.configs.datasets.hivtb.fold_8_rgb
   bob.med.tb.configs.datasets.hivtb.fold_9
   bob.med.tb.configs.datasets.hivtb.fold_9_rgb
   bob.med.tb.configs.datasets.hivtb_RS.fold_0
   bob.med.tb.configs.datasets.hivtb_RS.fold_1
   bob.med.tb.configs.datasets.hivtb_RS.fold_2
   bob.med.tb.configs.datasets.hivtb_RS.fold_3
   bob.med.tb.configs.datasets.hivtb_RS.fold_4
   bob.med.tb.configs.datasets.hivtb_RS.fold_5
   bob.med.tb.configs.datasets.hivtb_RS.fold_6
   bob.med.tb.configs.datasets.hivtb_RS.fold_7
   bob.med.tb.configs.datasets.hivtb_RS.fold_8
   bob.med.tb.configs.datasets.hivtb_RS.fold_9
   bob.med.tb.configs.datasets.indian.default
   bob.med.tb.configs.datasets.indian.fold_0
   bob.med.tb.configs.datasets.indian.fold_0_rgb
   bob.med.tb.configs.datasets.indian.fold_1
   bob.med.tb.configs.datasets.indian.fold_1_rgb
   bob.med.tb.configs.datasets.indian.fold_2
   bob.med.tb.configs.datasets.indian.fold_2_rgb
   bob.med.tb.configs.datasets.indian.fold_3
   bob.med.tb.configs.datasets.indian.fold_3_rgb
   bob.med.tb.configs.datasets.indian.fold_4
   bob.med.tb.configs.datasets.indian.fold_4_rgb
   bob.med.tb.configs.datasets.indian.fold_5
   bob.med.tb.configs.datasets.indian.fold_5_rgb
   bob.med.tb.configs.datasets.indian.fold_6
   bob.med.tb.configs.datasets.indian.fold_6_rgb
   bob.med.tb.configs.datasets.indian.fold_7
   bob.med.tb.configs.datasets.indian.fold_7_rgb
   bob.med.tb.configs.datasets.indian.fold_8
   bob.med.tb.configs.datasets.indian.fold_8_rgb
   bob.med.tb.configs.datasets.indian.fold_9
   bob.med.tb.configs.datasets.indian.fold_9_rgb
   bob.med.tb.configs.datasets.indian.rgb
   bob.med.tb.configs.datasets.indian_RS.default
   bob.med.tb.configs.datasets.indian_RS.fold_0
   bob.med.tb.configs.datasets.indian_RS.fold_1
   bob.med.tb.configs.datasets.indian_RS.fold_2
   bob.med.tb.configs.datasets.indian_RS.fold_3
   bob.med.tb.configs.datasets.indian_RS.fold_4
   bob.med.tb.configs.datasets.indian_RS.fold_5
   bob.med.tb.configs.datasets.indian_RS.fold_6
   bob.med.tb.configs.datasets.indian_RS.fold_7
   bob.med.tb.configs.datasets.indian_RS.fold_8
   bob.med.tb.configs.datasets.indian_RS.fold_9
   bob.med.tb.configs.datasets.mc_ch.default
   bob.med.tb.configs.datasets.mc_ch.fold_0
   bob.med.tb.configs.datasets.mc_ch.fold_0_rgb
   bob.med.tb.configs.datasets.mc_ch.fold_1
   bob.med.tb.configs.datasets.mc_ch.fold_1_rgb
   bob.med.tb.configs.datasets.mc_ch.fold_2
   bob.med.tb.configs.datasets.mc_ch.fold_2_rgb
   bob.med.tb.configs.datasets.mc_ch.fold_3
   bob.med.tb.configs.datasets.mc_ch.fold_3_rgb
   bob.med.tb.configs.datasets.mc_ch.fold_4
   bob.med.tb.configs.datasets.mc_ch.fold_4_rgb
   bob.med.tb.configs.datasets.mc_ch.fold_5
   bob.med.tb.configs.datasets.mc_ch.fold_5_rgb
   bob.med.tb.configs.datasets.mc_ch.fold_6
   bob.med.tb.configs.datasets.mc_ch.fold_6_rgb
   bob.med.tb.configs.datasets.mc_ch.fold_7
   bob.med.tb.configs.datasets.mc_ch.fold_7_rgb
   bob.med.tb.configs.datasets.mc_ch.fold_8
   bob.med.tb.configs.datasets.mc_ch.fold_8_rgb
   bob.med.tb.configs.datasets.mc_ch.fold_9
   bob.med.tb.configs.datasets.mc_ch.fold_9_rgb
   bob.med.tb.configs.datasets.mc_ch.rgb
   bob.med.tb.configs.datasets.mc_ch_RS.default
   bob.med.tb.configs.datasets.mc_ch_RS.fold_0
   bob.med.tb.configs.datasets.mc_ch_RS.fold_1
   bob.med.tb.configs.datasets.mc_ch_RS.fold_2
   bob.med.tb.configs.datasets.mc_ch_RS.fold_3
   bob.med.tb.configs.datasets.mc_ch_RS.fold_4
   bob.med.tb.configs.datasets.mc_ch_RS.fold_5
   bob.med.tb.configs.datasets.mc_ch_RS.fold_6
   bob.med.tb.configs.datasets.mc_ch_RS.fold_7
   bob.med.tb.configs.datasets.mc_ch_RS.fold_8
   bob.med.tb.configs.datasets.mc_ch_RS.fold_9
   bob.med.tb.configs.datasets.mc_ch_in.default
   bob.med.tb.configs.datasets.mc_ch_in.fold_0
   bob.med.tb.configs.datasets.mc_ch_in.fold_0_rgb
   bob.med.tb.configs.datasets.mc_ch_in.fold_1
   bob.med.tb.configs.datasets.mc_ch_in.fold_1_rgb
   bob.med.tb.configs.datasets.mc_ch_in.fold_2
   bob.med.tb.configs.datasets.mc_ch_in.fold_2_rgb
   bob.med.tb.configs.datasets.mc_ch_in.fold_3
   bob.med.tb.configs.datasets.mc_ch_in.fold_3_rgb
   bob.med.tb.configs.datasets.mc_ch_in.fold_4
   bob.med.tb.configs.datasets.mc_ch_in.fold_4_rgb
   bob.med.tb.configs.datasets.mc_ch_in.fold_5
   bob.med.tb.configs.datasets.mc_ch_in.fold_5_rgb
   bob.med.tb.configs.datasets.mc_ch_in.fold_6
   bob.med.tb.configs.datasets.mc_ch_in.fold_6_rgb
   bob.med.tb.configs.datasets.mc_ch_in.fold_7
   bob.med.tb.configs.datasets.mc_ch_in.fold_7_rgb
   bob.med.tb.configs.datasets.mc_ch_in.fold_8
   bob.med.tb.configs.datasets.mc_ch_in.fold_8_rgb
   bob.med.tb.configs.datasets.mc_ch_in.fold_9
   bob.med.tb.configs.datasets.mc_ch_in.fold_9_rgb
   bob.med.tb.configs.datasets.mc_ch_in.rgb
   bob.med.tb.configs.datasets.mc_ch_in_RS.default
   bob.med.tb.configs.datasets.mc_ch_in_RS.fold_0
   bob.med.tb.configs.datasets.mc_ch_in_RS.fold_1
   bob.med.tb.configs.datasets.mc_ch_in_RS.fold_2
   bob.med.tb.configs.datasets.mc_ch_in_RS.fold_3
   bob.med.tb.configs.datasets.mc_ch_in_RS.fold_4
   bob.med.tb.configs.datasets.mc_ch_in_RS.fold_5
   bob.med.tb.configs.datasets.mc_ch_in_RS.fold_6
   bob.med.tb.configs.datasets.mc_ch_in_RS.fold_7
   bob.med.tb.configs.datasets.mc_ch_in_RS.fold_8
   bob.med.tb.configs.datasets.mc_ch_in_RS.fold_9
   bob.med.tb.configs.datasets.mc_ch_in_pc.default
   bob.med.tb.configs.datasets.mc_ch_in_pc.rgb
   bob.med.tb.configs.datasets.mc_ch_in_pc_RS.default
   bob.med.tb.configs.datasets.montgomery.default
   bob.med.tb.configs.datasets.montgomery.fold_0
   bob.med.tb.configs.datasets.montgomery.fold_0_rgb
   bob.med.tb.configs.datasets.montgomery.fold_1
   bob.med.tb.configs.datasets.montgomery.fold_1_rgb
   bob.med.tb.configs.datasets.montgomery.fold_2
   bob.med.tb.configs.datasets.montgomery.fold_2_rgb
   bob.med.tb.configs.datasets.montgomery.fold_3
   bob.med.tb.configs.datasets.montgomery.fold_3_rgb
   bob.med.tb.configs.datasets.montgomery.fold_4
   bob.med.tb.configs.datasets.montgomery.fold_4_rgb
   bob.med.tb.configs.datasets.montgomery.fold_5
   bob.med.tb.configs.datasets.montgomery.fold_5_rgb
   bob.med.tb.configs.datasets.montgomery.fold_6
   bob.med.tb.configs.datasets.montgomery.fold_6_rgb
   bob.med.tb.configs.datasets.montgomery.fold_7
   bob.med.tb.configs.datasets.montgomery.fold_7_rgb
   bob.med.tb.configs.datasets.montgomery.fold_8
   bob.med.tb.configs.datasets.montgomery.fold_8_rgb
   bob.med.tb.configs.datasets.montgomery.fold_9
   bob.med.tb.configs.datasets.montgomery.fold_9_rgb
   bob.med.tb.configs.datasets.montgomery.rgb
   bob.med.tb.configs.datasets.montgomery_RS.default
   bob.med.tb.configs.datasets.montgomery_RS.fold_0
   bob.med.tb.configs.datasets.montgomery_RS.fold_1
   bob.med.tb.configs.datasets.montgomery_RS.fold_2
   bob.med.tb.configs.datasets.montgomery_RS.fold_3
   bob.med.tb.configs.datasets.montgomery_RS.fold_4
   bob.med.tb.configs.datasets.montgomery_RS.fold_5
   bob.med.tb.configs.datasets.montgomery_RS.fold_6
   bob.med.tb.configs.datasets.montgomery_RS.fold_7
   bob.med.tb.configs.datasets.montgomery_RS.fold_8
   bob.med.tb.configs.datasets.montgomery_RS.fold_9
   bob.med.tb.configs.datasets.nih_cxr14_re.cardiomegaly_idiap
   bob.med.tb.configs.datasets.nih_cxr14_re.default
   bob.med.tb.configs.datasets.nih_cxr14_re.idiap
   bob.med.tb.configs.datasets.nih_cxr14_re_pc.idiap
   bob.med.tb.configs.datasets.padchest.cardiomegaly_idiap
   bob.med.tb.configs.datasets.padchest.idiap
   bob.med.tb.configs.datasets.padchest.no_tb_idiap
   bob.med.tb.configs.datasets.padchest.tb_idiap
   bob.med.tb.configs.datasets.padchest.tb_idiap_rgb
   bob.med.tb.configs.datasets.padchest_RS.tb_idiap
   bob.med.tb.configs.datasets.shenzhen.default
   bob.med.tb.configs.datasets.shenzhen.fold_0
   bob.med.tb.configs.datasets.shenzhen.fold_0_rgb
   bob.med.tb.configs.datasets.shenzhen.fold_1
   bob.med.tb.configs.datasets.shenzhen.fold_1_rgb
   bob.med.tb.configs.datasets.shenzhen.fold_2
   bob.med.tb.configs.datasets.shenzhen.fold_2_rgb
   bob.med.tb.configs.datasets.shenzhen.fold_3
   bob.med.tb.configs.datasets.shenzhen.fold_3_rgb
   bob.med.tb.configs.datasets.shenzhen.fold_4
   bob.med.tb.configs.datasets.shenzhen.fold_4_rgb
   bob.med.tb.configs.datasets.shenzhen.fold_5
   bob.med.tb.configs.datasets.shenzhen.fold_5_rgb
   bob.med.tb.configs.datasets.shenzhen.fold_6
   bob.med.tb.configs.datasets.shenzhen.fold_6_rgb
   bob.med.tb.configs.datasets.shenzhen.fold_7
   bob.med.tb.configs.datasets.shenzhen.fold_7_rgb
   bob.med.tb.configs.datasets.shenzhen.fold_8
   bob.med.tb.configs.datasets.shenzhen.fold_8_rgb
   bob.med.tb.configs.datasets.shenzhen.fold_9
   bob.med.tb.configs.datasets.shenzhen.fold_9_rgb
   bob.med.tb.configs.datasets.shenzhen.rgb
   bob.med.tb.configs.datasets.shenzhen_RS.default
   bob.med.tb.configs.datasets.shenzhen_RS.fold_0
   bob.med.tb.configs.datasets.shenzhen_RS.fold_1
   bob.med.tb.configs.datasets.shenzhen_RS.fold_2
   bob.med.tb.configs.datasets.shenzhen_RS.fold_3
   bob.med.tb.configs.datasets.shenzhen_RS.fold_4
   bob.med.tb.configs.datasets.shenzhen_RS.fold_5
   bob.med.tb.configs.datasets.shenzhen_RS.fold_6
   bob.med.tb.configs.datasets.shenzhen_RS.fold_7
   bob.med.tb.configs.datasets.shenzhen_RS.fold_8
   bob.med.tb.configs.datasets.shenzhen_RS.fold_9
   bob.med.tb.configs.datasets.tbpoc.fold_0
   bob.med.tb.configs.datasets.tbpoc.fold_0_rgb
   bob.med.tb.configs.datasets.tbpoc.fold_1
   bob.med.tb.configs.datasets.tbpoc.fold_1_rgb
   bob.med.tb.configs.datasets.tbpoc.fold_2
   bob.med.tb.configs.datasets.tbpoc.fold_2_rgb
   bob.med.tb.configs.datasets.tbpoc.fold_3
   bob.med.tb.configs.datasets.tbpoc.fold_3_rgb
   bob.med.tb.configs.datasets.tbpoc.fold_4
   bob.med.tb.configs.datasets.tbpoc.fold_4_rgb
   bob.med.tb.configs.datasets.tbpoc.fold_5
   bob.med.tb.configs.datasets.tbpoc.fold_5_rgb
   bob.med.tb.configs.datasets.tbpoc.fold_6
   bob.med.tb.configs.datasets.tbpoc.fold_6_rgb
   bob.med.tb.configs.datasets.tbpoc.fold_7
   bob.med.tb.configs.datasets.tbpoc.fold_7_rgb
   bob.med.tb.configs.datasets.tbpoc.fold_8
   bob.med.tb.configs.datasets.tbpoc.fold_8_rgb
   bob.med.tb.configs.datasets.tbpoc.fold_9
   bob.med.tb.configs.datasets.tbpoc.fold_9_rgb
   bob.med.tb.configs.datasets.tbpoc_RS.fold_0
   bob.med.tb.configs.datasets.tbpoc_RS.fold_1
   bob.med.tb.configs.datasets.tbpoc_RS.fold_2
   bob.med.tb.configs.datasets.tbpoc_RS.fold_3
   bob.med.tb.configs.datasets.tbpoc_RS.fold_4
   bob.med.tb.configs.datasets.tbpoc_RS.fold_5
   bob.med.tb.configs.datasets.tbpoc_RS.fold_6
   bob.med.tb.configs.datasets.tbpoc_RS.fold_7
   bob.med.tb.configs.datasets.tbpoc_RS.fold_8
   bob.med.tb.configs.datasets.tbpoc_RS.fold_9

.. include:: links.rst
