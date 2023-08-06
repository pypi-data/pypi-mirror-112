#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for transforms"""

import os
import random

import nose.tools
import pkg_resources

import numpy
import PIL.Image

from ..data.transforms import RemoveBlackBorders, ElasticDeformation, SingleAutoLevel16to8
from ..data.loader import load_pil
from ..data.montgomery import dataset as raw

def _data_file(f):
    return pkg_resources.resource_filename(__name__, os.path.join("data", f))

def test_remove_black_borders():
    # Get a raw sample with black border
    data_file = _data_file("raw_with_black_border.png")
    raw_with_black_border = PIL.Image.open(data_file)

    # Remove the black border
    rbb = RemoveBlackBorders()
    raw_rbb_removed = rbb(raw_with_black_border)

    # Get the same sample without black border
    data_file_2 = _data_file("raw_without_black_border.png")
    raw_without_black_border = PIL.Image.open(data_file_2)

    # Compare both
    raw_rbb_removed = numpy.asarray(raw_rbb_removed)
    raw_without_black_border = numpy.asarray(raw_without_black_border)
    
    numpy.testing.assert_array_equal(raw_without_black_border, raw_rbb_removed)

def test_elastic_deformation():
    # Get a raw sample without deformation
    data_file = _data_file("raw_without_elastic_deformation.png")
    raw_without_deformation = PIL.Image.open(data_file)

    # Elastic deforms the raw
    ed = ElasticDeformation(random_state=numpy.random.RandomState(seed=100))
    raw_deformed = ed(raw_without_deformation)

    # Get the same sample already deformed (with seed=100)
    data_file_2 = _data_file("raw_with_elastic_deformation.png")
    raw_2 = PIL.Image.open(data_file_2)

    # Compare both
    raw_deformed = numpy.asarray(raw_deformed)
    raw_2 = numpy.asarray(raw_2)

    numpy.testing.assert_array_equal(raw_deformed, raw_2)

def test_load_pil_16bit():

    # If the ratio is higher 0.5, image is probably clipped
    Level16to8 = SingleAutoLevel16to8()
    
    data_file = _data_file("16bits.png")
    image = numpy.array(Level16to8(load_pil(data_file)))
    
    count_pixels = numpy.count_nonzero(image)
    count_max_value = numpy.count_nonzero(image == image.max())
    
    assert count_max_value/count_pixels < 0.5

    # It should not do anything to an image already in 8 bits
    data_file = _data_file("raw_without_black_border.png")
    img_loaded = load_pil(data_file)
    
    original_8bits = numpy.array(img_loaded)
    leveled_8bits = numpy.array(Level16to8(img_loaded))
    
    numpy.testing.assert_array_equal(original_8bits, leveled_8bits)