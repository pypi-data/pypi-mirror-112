#!/usr/bin/env python
# coding=utf-8

""" Aggregated dataset composed of Montgomery and Shenzhen datasets
(cross validation fold 1, RGB) """

from . import _maker

dataset = _maker("fold_1_rgb")