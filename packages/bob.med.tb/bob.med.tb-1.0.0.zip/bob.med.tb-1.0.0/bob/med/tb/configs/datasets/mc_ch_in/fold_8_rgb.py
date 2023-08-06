#!/usr/bin/env python
# coding=utf-8

""" Aggregated dataset composed of Montgomery, Shenzhen and Indian datasets
(cross validation fold 8, RGB) """

from . import _maker

dataset = _maker("fold_8_rgb")