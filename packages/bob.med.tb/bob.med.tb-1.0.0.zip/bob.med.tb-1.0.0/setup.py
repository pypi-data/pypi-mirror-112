#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, dist
dist.Distribution(dict(setup_requires=['bob.extension']))

from bob.extension.utils import load_requirements, find_packages
install_requires = load_requirements()


setup(
    name='bob.med.tb',
    version=open("version.txt").read().rstrip(),
    description='Active Tuberculosis Detection On CXR Package for Bob',

    url='https://gitlab.idiap.ch/graposo/bob.med.tb',
    license='GPLv3',

    # there may be multiple authors (separate entries by comma)
    author='Geoffrey Raposo',
    author_email='geoffrey.raposo@idiap.ch',

    # there may be a maintainer apart from the author - you decide
    #maintainer='?',
    #maintainer_email='email@example.com',

    # you may add more keywords separating those by commas (a, b, c, ...)
    keywords = "bob",

    long_description=open('README.rst').read(),

    # leave this here, it is pretty standard
    packages=find_packages(),
    include_package_data=True,
    zip_safe = False,

    install_requires=install_requires,

    entry_points={
        # main entry for the bob tb cli
        "bob.cli": ["tb = bob.med.tb.scripts.tb:tb"],
        # bob tb sub-commands
        "bob.med.tb.cli": [
            "config = bob.med.tb.scripts.config:config",
            "dataset = bob.med.tb.scripts.dataset:dataset",
            "train = bob.med.tb.scripts.train:train",
            "predict = bob.med.tb.scripts.predict:predict",
            "evaluate = bob.med.tb.scripts.evaluate:evaluate",
            "predtojson = bob.med.tb.scripts.predtojson:predtojson",
            "aggregpred = bob.med.tb.scripts.aggregpred:aggregpred",
            "compare =  bob.med.tb.scripts.compare:compare",
        ],
        # bob train configurations
        "bob.med.tb.config": [
            # models
            "pasa = bob.med.tb.configs.models.pasa",
            "signs_to_tb = bob.med.tb.configs.models.signs_to_tb",
            "logistic_regression = bob.med.tb.configs.models.logistic_regression",
            "densenet_rs = bob.med.tb.configs.models_datasets.densenet_rs",
            "alexnet = bob.med.tb.configs.models.alexnet",
            "alexnet_pre = bob.med.tb.configs.models.alexnet_pretrained",
            "densenet = bob.med.tb.configs.models.densenet",
            "densenet_pre = bob.med.tb.configs.models.densenet_pretrained",

            # montgomery dataset (and cross-validation folds)
            "montgomery = bob.med.tb.configs.datasets.montgomery.default",
            "montgomery_rgb = bob.med.tb.configs.datasets.montgomery.rgb",
            "montgomery_f0 = bob.med.tb.configs.datasets.montgomery.fold_0",
            "montgomery_f1 = bob.med.tb.configs.datasets.montgomery.fold_1",
            "montgomery_f2 = bob.med.tb.configs.datasets.montgomery.fold_2",
            "montgomery_f3 = bob.med.tb.configs.datasets.montgomery.fold_3",
            "montgomery_f4 = bob.med.tb.configs.datasets.montgomery.fold_4",
            "montgomery_f5 = bob.med.tb.configs.datasets.montgomery.fold_5",
            "montgomery_f6 = bob.med.tb.configs.datasets.montgomery.fold_6",
            "montgomery_f7 = bob.med.tb.configs.datasets.montgomery.fold_7",
            "montgomery_f8 = bob.med.tb.configs.datasets.montgomery.fold_8",
            "montgomery_f9 = bob.med.tb.configs.datasets.montgomery.fold_9",
            "montgomery_f0_rgb = bob.med.tb.configs.datasets.montgomery.fold_0_rgb",
            "montgomery_f1_rgb = bob.med.tb.configs.datasets.montgomery.fold_1_rgb",
            "montgomery_f2_rgb = bob.med.tb.configs.datasets.montgomery.fold_2_rgb",
            "montgomery_f3_rgb = bob.med.tb.configs.datasets.montgomery.fold_3_rgb",
            "montgomery_f4_rgb = bob.med.tb.configs.datasets.montgomery.fold_4_rgb",
            "montgomery_f5_rgb = bob.med.tb.configs.datasets.montgomery.fold_5_rgb",
            "montgomery_f6_rgb = bob.med.tb.configs.datasets.montgomery.fold_6_rgb",
            "montgomery_f7_rgb = bob.med.tb.configs.datasets.montgomery.fold_7_rgb",
            "montgomery_f8_rgb = bob.med.tb.configs.datasets.montgomery.fold_8_rgb",
            "montgomery_f9_rgb = bob.med.tb.configs.datasets.montgomery.fold_9_rgb",

            # extended montgomery dataset (with radiological signs)
            "montgomery_rs = bob.med.tb.configs.datasets.montgomery_RS.default",
            "montgomery_rs_f0 = bob.med.tb.configs.datasets.montgomery_RS.fold_0",
            "montgomery_rs_f1 = bob.med.tb.configs.datasets.montgomery_RS.fold_1",
            "montgomery_rs_f2 = bob.med.tb.configs.datasets.montgomery_RS.fold_2",
            "montgomery_rs_f3 = bob.med.tb.configs.datasets.montgomery_RS.fold_3",
            "montgomery_rs_f4 = bob.med.tb.configs.datasets.montgomery_RS.fold_4",
            "montgomery_rs_f5 = bob.med.tb.configs.datasets.montgomery_RS.fold_5",
            "montgomery_rs_f6 = bob.med.tb.configs.datasets.montgomery_RS.fold_6",
            "montgomery_rs_f7 = bob.med.tb.configs.datasets.montgomery_RS.fold_7",
            "montgomery_rs_f8 = bob.med.tb.configs.datasets.montgomery_RS.fold_8",
            "montgomery_rs_f9 = bob.med.tb.configs.datasets.montgomery_RS.fold_9",

            # shenzhen dataset (and cross-validation folds)
            "shenzhen = bob.med.tb.configs.datasets.shenzhen.default",
            "shenzhen_rgb = bob.med.tb.configs.datasets.shenzhen.rgb",
            "shenzhen_f0 = bob.med.tb.configs.datasets.shenzhen.fold_0",
            "shenzhen_f1 = bob.med.tb.configs.datasets.shenzhen.fold_1",
            "shenzhen_f2 = bob.med.tb.configs.datasets.shenzhen.fold_2",
            "shenzhen_f3 = bob.med.tb.configs.datasets.shenzhen.fold_3",
            "shenzhen_f4 = bob.med.tb.configs.datasets.shenzhen.fold_4",
            "shenzhen_f5 = bob.med.tb.configs.datasets.shenzhen.fold_5",
            "shenzhen_f6 = bob.med.tb.configs.datasets.shenzhen.fold_6",
            "shenzhen_f7 = bob.med.tb.configs.datasets.shenzhen.fold_7",
            "shenzhen_f8 = bob.med.tb.configs.datasets.shenzhen.fold_8",
            "shenzhen_f9 = bob.med.tb.configs.datasets.shenzhen.fold_9",
            "shenzhen_f0_rgb = bob.med.tb.configs.datasets.shenzhen.fold_0_rgb",
            "shenzhen_f1_rgb = bob.med.tb.configs.datasets.shenzhen.fold_1_rgb",
            "shenzhen_f2_rgb = bob.med.tb.configs.datasets.shenzhen.fold_2_rgb",
            "shenzhen_f3_rgb = bob.med.tb.configs.datasets.shenzhen.fold_3_rgb",
            "shenzhen_f4_rgb = bob.med.tb.configs.datasets.shenzhen.fold_4_rgb",
            "shenzhen_f5_rgb = bob.med.tb.configs.datasets.shenzhen.fold_5_rgb",
            "shenzhen_f6_rgb = bob.med.tb.configs.datasets.shenzhen.fold_6_rgb",
            "shenzhen_f7_rgb = bob.med.tb.configs.datasets.shenzhen.fold_7_rgb",
            "shenzhen_f8_rgb = bob.med.tb.configs.datasets.shenzhen.fold_8_rgb",
            "shenzhen_f9_rgb = bob.med.tb.configs.datasets.shenzhen.fold_9_rgb",

            # extended shenzhen dataset (with radiological signs)
            "shenzhen_rs = bob.med.tb.configs.datasets.shenzhen_RS.default",
            "shenzhen_rs_f0 = bob.med.tb.configs.datasets.shenzhen_RS.fold_0",
            "shenzhen_rs_f1 = bob.med.tb.configs.datasets.shenzhen_RS.fold_1",
            "shenzhen_rs_f2 = bob.med.tb.configs.datasets.shenzhen_RS.fold_2",
            "shenzhen_rs_f3 = bob.med.tb.configs.datasets.shenzhen_RS.fold_3",
            "shenzhen_rs_f4 = bob.med.tb.configs.datasets.shenzhen_RS.fold_4",
            "shenzhen_rs_f5 = bob.med.tb.configs.datasets.shenzhen_RS.fold_5",
            "shenzhen_rs_f6 = bob.med.tb.configs.datasets.shenzhen_RS.fold_6",
            "shenzhen_rs_f7 = bob.med.tb.configs.datasets.shenzhen_RS.fold_7",
            "shenzhen_rs_f8 = bob.med.tb.configs.datasets.shenzhen_RS.fold_8",
            "shenzhen_rs_f9 = bob.med.tb.configs.datasets.shenzhen_RS.fold_9",

            # indian dataset (and cross-validation folds)
            "indian = bob.med.tb.configs.datasets.indian.default",
            "indian_rgb = bob.med.tb.configs.datasets.indian.rgb",
            "indian_f0 = bob.med.tb.configs.datasets.indian.fold_0",
            "indian_f1 = bob.med.tb.configs.datasets.indian.fold_1",
            "indian_f2 = bob.med.tb.configs.datasets.indian.fold_2",
            "indian_f3 = bob.med.tb.configs.datasets.indian.fold_3",
            "indian_f4 = bob.med.tb.configs.datasets.indian.fold_4",
            "indian_f5 = bob.med.tb.configs.datasets.indian.fold_5",
            "indian_f6 = bob.med.tb.configs.datasets.indian.fold_6",
            "indian_f7 = bob.med.tb.configs.datasets.indian.fold_7",
            "indian_f8 = bob.med.tb.configs.datasets.indian.fold_8",
            "indian_f9 = bob.med.tb.configs.datasets.indian.fold_9",
            "indian_f0_rgb = bob.med.tb.configs.datasets.indian.fold_0_rgb",
            "indian_f1_rgb = bob.med.tb.configs.datasets.indian.fold_1_rgb",
            "indian_f2_rgb = bob.med.tb.configs.datasets.indian.fold_2_rgb",
            "indian_f3_rgb = bob.med.tb.configs.datasets.indian.fold_3_rgb",
            "indian_f4_rgb = bob.med.tb.configs.datasets.indian.fold_4_rgb",
            "indian_f5_rgb = bob.med.tb.configs.datasets.indian.fold_5_rgb",
            "indian_f6_rgb = bob.med.tb.configs.datasets.indian.fold_6_rgb",
            "indian_f7_rgb = bob.med.tb.configs.datasets.indian.fold_7_rgb",
            "indian_f8_rgb = bob.med.tb.configs.datasets.indian.fold_8_rgb",
            "indian_f9_rgb = bob.med.tb.configs.datasets.indian.fold_9_rgb",

            # extended indian dataset (with radiological signs)
            "indian_rs = bob.med.tb.configs.datasets.indian_RS.default",
            "indian_rs_f0 = bob.med.tb.configs.datasets.indian_RS.fold_0",
            "indian_rs_f1 = bob.med.tb.configs.datasets.indian_RS.fold_1",
            "indian_rs_f2 = bob.med.tb.configs.datasets.indian_RS.fold_2",
            "indian_rs_f3 = bob.med.tb.configs.datasets.indian_RS.fold_3",
            "indian_rs_f4 = bob.med.tb.configs.datasets.indian_RS.fold_4",
            "indian_rs_f5 = bob.med.tb.configs.datasets.indian_RS.fold_5",
            "indian_rs_f6 = bob.med.tb.configs.datasets.indian_RS.fold_6",
            "indian_rs_f7 = bob.med.tb.configs.datasets.indian_RS.fold_7",
            "indian_rs_f8 = bob.med.tb.configs.datasets.indian_RS.fold_8",
            "indian_rs_f9 = bob.med.tb.configs.datasets.indian_RS.fold_9",

            # montgomery-shenzhen aggregated dataset
            "mc_ch = bob.med.tb.configs.datasets.mc_ch.default",
            "mc_ch_rgb = bob.med.tb.configs.datasets.mc_ch.rgb",
            "mc_ch_f0 = bob.med.tb.configs.datasets.mc_ch.fold_0",
            "mc_ch_f1 = bob.med.tb.configs.datasets.mc_ch.fold_1",
            "mc_ch_f2 = bob.med.tb.configs.datasets.mc_ch.fold_2",
            "mc_ch_f3 = bob.med.tb.configs.datasets.mc_ch.fold_3",
            "mc_ch_f4 = bob.med.tb.configs.datasets.mc_ch.fold_4",
            "mc_ch_f5 = bob.med.tb.configs.datasets.mc_ch.fold_5",
            "mc_ch_f6 = bob.med.tb.configs.datasets.mc_ch.fold_6",
            "mc_ch_f7 = bob.med.tb.configs.datasets.mc_ch.fold_7",
            "mc_ch_f8 = bob.med.tb.configs.datasets.mc_ch.fold_8",
            "mc_ch_f9 = bob.med.tb.configs.datasets.mc_ch.fold_9",
            "mc_ch_f0_rgb = bob.med.tb.configs.datasets.mc_ch.fold_0_rgb",
            "mc_ch_f1_rgb = bob.med.tb.configs.datasets.mc_ch.fold_1_rgb",
            "mc_ch_f2_rgb = bob.med.tb.configs.datasets.mc_ch.fold_2_rgb",
            "mc_ch_f3_rgb = bob.med.tb.configs.datasets.mc_ch.fold_3_rgb",
            "mc_ch_f4_rgb = bob.med.tb.configs.datasets.mc_ch.fold_4_rgb",
            "mc_ch_f5_rgb = bob.med.tb.configs.datasets.mc_ch.fold_5_rgb",
            "mc_ch_f6_rgb = bob.med.tb.configs.datasets.mc_ch.fold_6_rgb",
            "mc_ch_f7_rgb = bob.med.tb.configs.datasets.mc_ch.fold_7_rgb",
            "mc_ch_f8_rgb = bob.med.tb.configs.datasets.mc_ch.fold_8_rgb",
            "mc_ch_f9_rgb = bob.med.tb.configs.datasets.mc_ch.fold_9_rgb",

            # extended montgomery-shenzhen aggregated dataset
            # (with radiological signs)
            "mc_ch_rs = bob.med.tb.configs.datasets.mc_ch_RS.default",
            "mc_ch_rs_f0 = bob.med.tb.configs.datasets.mc_ch_RS.fold_0",
            "mc_ch_rs_f1 = bob.med.tb.configs.datasets.mc_ch_RS.fold_1",
            "mc_ch_rs_f2 = bob.med.tb.configs.datasets.mc_ch_RS.fold_2",
            "mc_ch_rs_f3 = bob.med.tb.configs.datasets.mc_ch_RS.fold_3",
            "mc_ch_rs_f4 = bob.med.tb.configs.datasets.mc_ch_RS.fold_4",
            "mc_ch_rs_f5 = bob.med.tb.configs.datasets.mc_ch_RS.fold_5",
            "mc_ch_rs_f6 = bob.med.tb.configs.datasets.mc_ch_RS.fold_6",
            "mc_ch_rs_f7 = bob.med.tb.configs.datasets.mc_ch_RS.fold_7",
            "mc_ch_rs_f8 = bob.med.tb.configs.datasets.mc_ch_RS.fold_8",
            "mc_ch_rs_f9 = bob.med.tb.configs.datasets.mc_ch_RS.fold_9",

            # montgomery-shenzhen-indian aggregated dataset
            "mc_ch_in = bob.med.tb.configs.datasets.mc_ch_in.default",
            "mc_ch_in_rgb = bob.med.tb.configs.datasets.mc_ch_in.rgb",
            "mc_ch_in_f0 = bob.med.tb.configs.datasets.mc_ch_in.fold_0",
            "mc_ch_in_f1 = bob.med.tb.configs.datasets.mc_ch_in.fold_1",
            "mc_ch_in_f2 = bob.med.tb.configs.datasets.mc_ch_in.fold_2",
            "mc_ch_in_f3 = bob.med.tb.configs.datasets.mc_ch_in.fold_3",
            "mc_ch_in_f4 = bob.med.tb.configs.datasets.mc_ch_in.fold_4",
            "mc_ch_in_f5 = bob.med.tb.configs.datasets.mc_ch_in.fold_5",
            "mc_ch_in_f6 = bob.med.tb.configs.datasets.mc_ch_in.fold_6",
            "mc_ch_in_f7 = bob.med.tb.configs.datasets.mc_ch_in.fold_7",
            "mc_ch_in_f8 = bob.med.tb.configs.datasets.mc_ch_in.fold_8",
            "mc_ch_in_f9 = bob.med.tb.configs.datasets.mc_ch_in.fold_9",
            "mc_ch_in_f0_rgb = bob.med.tb.configs.datasets.mc_ch_in.fold_0_rgb",
            "mc_ch_in_f1_rgb = bob.med.tb.configs.datasets.mc_ch_in.fold_1_rgb",
            "mc_ch_in_f2_rgb = bob.med.tb.configs.datasets.mc_ch_in.fold_2_rgb",
            "mc_ch_in_f3_rgb = bob.med.tb.configs.datasets.mc_ch_in.fold_3_rgb",
            "mc_ch_in_f4_rgb = bob.med.tb.configs.datasets.mc_ch_in.fold_4_rgb",
            "mc_ch_in_f5_rgb = bob.med.tb.configs.datasets.mc_ch_in.fold_5_rgb",
            "mc_ch_in_f6_rgb = bob.med.tb.configs.datasets.mc_ch_in.fold_6_rgb",
            "mc_ch_in_f7_rgb = bob.med.tb.configs.datasets.mc_ch_in.fold_7_rgb",
            "mc_ch_in_f8_rgb = bob.med.tb.configs.datasets.mc_ch_in.fold_8_rgb",
            "mc_ch_in_f9_rgb = bob.med.tb.configs.datasets.mc_ch_in.fold_9_rgb",

            # extended montgomery-shenzhen-indian aggregated dataset
            # (with radiological signs)
            "mc_ch_in_rs = bob.med.tb.configs.datasets.mc_ch_in_RS.default",
            "mc_ch_in_rs_f0 = bob.med.tb.configs.datasets.mc_ch_in_RS.fold_0",
            "mc_ch_in_rs_f1 = bob.med.tb.configs.datasets.mc_ch_in_RS.fold_1",
            "mc_ch_in_rs_f2 = bob.med.tb.configs.datasets.mc_ch_in_RS.fold_2",
            "mc_ch_in_rs_f3 = bob.med.tb.configs.datasets.mc_ch_in_RS.fold_3",
            "mc_ch_in_rs_f4 = bob.med.tb.configs.datasets.mc_ch_in_RS.fold_4",
            "mc_ch_in_rs_f5 = bob.med.tb.configs.datasets.mc_ch_in_RS.fold_5",
            "mc_ch_in_rs_f6 = bob.med.tb.configs.datasets.mc_ch_in_RS.fold_6",
            "mc_ch_in_rs_f7 = bob.med.tb.configs.datasets.mc_ch_in_RS.fold_7",
            "mc_ch_in_rs_f8 = bob.med.tb.configs.datasets.mc_ch_in_RS.fold_8",
            "mc_ch_in_rs_f9 = bob.med.tb.configs.datasets.mc_ch_in_RS.fold_9",

            # tbpoc dataset (and cross-validation folds)
            "tbpoc_f0 = bob.med.tb.configs.datasets.tbpoc.fold_0",
            "tbpoc_f1 = bob.med.tb.configs.datasets.tbpoc.fold_1",
            "tbpoc_f2 = bob.med.tb.configs.datasets.tbpoc.fold_2",
            "tbpoc_f3 = bob.med.tb.configs.datasets.tbpoc.fold_3",
            "tbpoc_f4 = bob.med.tb.configs.datasets.tbpoc.fold_4",
            "tbpoc_f5 = bob.med.tb.configs.datasets.tbpoc.fold_5",
            "tbpoc_f6 = bob.med.tb.configs.datasets.tbpoc.fold_6",
            "tbpoc_f7 = bob.med.tb.configs.datasets.tbpoc.fold_7",
            "tbpoc_f8 = bob.med.tb.configs.datasets.tbpoc.fold_8",
            "tbpoc_f9 = bob.med.tb.configs.datasets.tbpoc.fold_9",
            "tbpoc_f0_rgb = bob.med.tb.configs.datasets.tbpoc.fold_0_rgb",
            "tbpoc_f1_rgb = bob.med.tb.configs.datasets.tbpoc.fold_1_rgb",
            "tbpoc_f2_rgb = bob.med.tb.configs.datasets.tbpoc.fold_2_rgb",
            "tbpoc_f3_rgb = bob.med.tb.configs.datasets.tbpoc.fold_3_rgb",
            "tbpoc_f4_rgb = bob.med.tb.configs.datasets.tbpoc.fold_4_rgb",
            "tbpoc_f5_rgb = bob.med.tb.configs.datasets.tbpoc.fold_5_rgb",
            "tbpoc_f6_rgb = bob.med.tb.configs.datasets.tbpoc.fold_6_rgb",
            "tbpoc_f7_rgb = bob.med.tb.configs.datasets.tbpoc.fold_7_rgb",
            "tbpoc_f8_rgb = bob.med.tb.configs.datasets.tbpoc.fold_8_rgb",
            "tbpoc_f9_rgb = bob.med.tb.configs.datasets.tbpoc.fold_9_rgb",

            # extended tbpoc dataset (with radiological signs)
            "tbpoc_rs_f0 = bob.med.tb.configs.datasets.tbpoc_RS.fold_0",
            "tbpoc_rs_f1 = bob.med.tb.configs.datasets.tbpoc_RS.fold_1",
            "tbpoc_rs_f2 = bob.med.tb.configs.datasets.tbpoc_RS.fold_2",
            "tbpoc_rs_f3 = bob.med.tb.configs.datasets.tbpoc_RS.fold_3",
            "tbpoc_rs_f4 = bob.med.tb.configs.datasets.tbpoc_RS.fold_4",
            "tbpoc_rs_f5 = bob.med.tb.configs.datasets.tbpoc_RS.fold_5",
            "tbpoc_rs_f6 = bob.med.tb.configs.datasets.tbpoc_RS.fold_6",
            "tbpoc_rs_f7 = bob.med.tb.configs.datasets.tbpoc_RS.fold_7",
            "tbpoc_rs_f8 = bob.med.tb.configs.datasets.tbpoc_RS.fold_8",
            "tbpoc_rs_f9 = bob.med.tb.configs.datasets.tbpoc_RS.fold_9",

            # hivtb dataset (and cross-validation folds)
            "hivtb_f0 = bob.med.tb.configs.datasets.hivtb.fold_0",
            "hivtb_f1 = bob.med.tb.configs.datasets.hivtb.fold_1",
            "hivtb_f2 = bob.med.tb.configs.datasets.hivtb.fold_2",
            "hivtb_f3 = bob.med.tb.configs.datasets.hivtb.fold_3",
            "hivtb_f4 = bob.med.tb.configs.datasets.hivtb.fold_4",
            "hivtb_f5 = bob.med.tb.configs.datasets.hivtb.fold_5",
            "hivtb_f6 = bob.med.tb.configs.datasets.hivtb.fold_6",
            "hivtb_f7 = bob.med.tb.configs.datasets.hivtb.fold_7",
            "hivtb_f8 = bob.med.tb.configs.datasets.hivtb.fold_8",
            "hivtb_f9 = bob.med.tb.configs.datasets.hivtb.fold_9",
            "hivtb_f0_rgb = bob.med.tb.configs.datasets.hivtb.fold_0_rgb",
            "hivtb_f1_rgb = bob.med.tb.configs.datasets.hivtb.fold_1_rgb",
            "hivtb_f2_rgb = bob.med.tb.configs.datasets.hivtb.fold_2_rgb",
            "hivtb_f3_rgb = bob.med.tb.configs.datasets.hivtb.fold_3_rgb",
            "hivtb_f4_rgb = bob.med.tb.configs.datasets.hivtb.fold_4_rgb",
            "hivtb_f5_rgb = bob.med.tb.configs.datasets.hivtb.fold_5_rgb",
            "hivtb_f6_rgb = bob.med.tb.configs.datasets.hivtb.fold_6_rgb",
            "hivtb_f7_rgb = bob.med.tb.configs.datasets.hivtb.fold_7_rgb",
            "hivtb_f8_rgb = bob.med.tb.configs.datasets.hivtb.fold_8_rgb",
            "hivtb_f9_rgb = bob.med.tb.configs.datasets.hivtb.fold_9_rgb",

            # extended hivtb dataset (with radiological signs)
            "hivtb_rs_f0 = bob.med.tb.configs.datasets.hivtb_RS.fold_0",
            "hivtb_rs_f1 = bob.med.tb.configs.datasets.hivtb_RS.fold_1",
            "hivtb_rs_f2 = bob.med.tb.configs.datasets.hivtb_RS.fold_2",
            "hivtb_rs_f3 = bob.med.tb.configs.datasets.hivtb_RS.fold_3",
            "hivtb_rs_f4 = bob.med.tb.configs.datasets.hivtb_RS.fold_4",
            "hivtb_rs_f5 = bob.med.tb.configs.datasets.hivtb_RS.fold_5",
            "hivtb_rs_f6 = bob.med.tb.configs.datasets.hivtb_RS.fold_6",
            "hivtb_rs_f7 = bob.med.tb.configs.datasets.hivtb_RS.fold_7",
            "hivtb_rs_f8 = bob.med.tb.configs.datasets.hivtb_RS.fold_8",
            "hivtb_rs_f9 = bob.med.tb.configs.datasets.hivtb_RS.fold_9",

            # montgomery-shenzhen-indian-padchest aggregated dataset
            "mc_ch_in_pc = bob.med.tb.configs.datasets.mc_ch_in_pc.default",
            "mc_ch_in_pc_rgb = bob.med.tb.configs.datasets.mc_ch_in_pc.rgb",

            # extended montgomery-shenzhen-indian-padchest aggregated dataset
            # (with radiological signs)
            "mc_ch_in_pc_rs = bob.med.tb.configs.datasets.mc_ch_in_pc_RS.default",

            # NIH CXR14 (relabeled)
            "nih_cxr14 = bob.med.tb.configs.datasets.nih_cxr14_re.default",
            "nih_cxr14_idiap = bob.med.tb.configs.datasets.nih_cxr14_re.idiap",
            "nih_cxr14_cm_idiap = bob.med.tb.configs.datasets.nih_cxr14_re.cardiomegaly_idiap",

            # NIH CXR14 / PadChest aggregated dataset
            "nih_cxr14_pc_idiap = bob.med.tb.configs.datasets.nih_cxr14_re_pc.idiap",

            # PadChest
            "padchest_idiap = bob.med.tb.configs.datasets.padchest.idiap",
            "padchest_tb_idiap = bob.med.tb.configs.datasets.padchest.tb_idiap",
            "padchest_no_tb_idiap = bob.med.tb.configs.datasets.padchest.no_tb_idiap",
            "padchest_tb_idiap_rgb = bob.med.tb.configs.datasets.padchest.tb_idiap_rgb",
            "padchest_cm_idiap = bob.med.tb.configs.datasets.padchest.cardiomegaly_idiap",

            # extended PadChestTB dataset (with radiological signs)
            "padchest_tb_idiap_rs = bob.med.tb.configs.datasets.padchest_RS.tb_idiap",
        ]
    },

    # check classifiers, add and remove as you see fit
    # full list here: https://pypi.org/classifiers/
    # don't remove the Bob framework unless it's not a bob package
    classifiers = [
        'Framework :: Bob',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)