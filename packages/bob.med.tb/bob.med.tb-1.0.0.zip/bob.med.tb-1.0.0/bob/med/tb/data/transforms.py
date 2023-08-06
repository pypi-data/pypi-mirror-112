#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Image transformations for our pipelines

Differences between methods here and those from
:py:mod:`torchvision.transforms` is that these support multiple simultaneous
image inputs, which are required to feed segmentation networks (e.g. image and
labels or masks).  We also take care of data augmentations, in which random
flipping and rotation needs to be applied across all input images, but color
jittering, for example, only on the input image.
"""

import random

import numpy
import PIL.Image
import torchvision.transforms
import torchvision.transforms.functional
from scipy.ndimage.filters import gaussian_filter
from scipy.ndimage.interpolation import map_coordinates

class SingleAutoLevel16to8:
    """Converts a 16-bit image to 8-bit representation using "auto-level"

    This transform assumes that the input image is gray-scaled.

    To auto-level, we calculate the maximum and the minimum of the image, and
    consider such a range should be mapped to the [0,255] range of the
    destination image.

    """

    def __call__(self, img):
        imin, imax = img.getextrema()
        irange = imax - imin
        return PIL.Image.fromarray(
            numpy.round(
                255.0 * (numpy.array(img).astype(float) - imin) / irange
            ).astype("uint8"),
        ).convert("L")


class RemoveBlackBorders:
    """Remove black borders of CXR"""
    def __init__(self, threshold=0):
        self.threshold = threshold

    def __call__(self, img):
        img = numpy.asarray(img)
        mask = numpy.asarray(img) > self.threshold
        return PIL.Image.fromarray(
                img[numpy.ix_(mask.any(1), mask.any(0))]
            )

class ElasticDeformation:
    """Elastic deformation of 2D image slightly adapted from [SIMARD-2003]_.
       .. [SIMARD-2003] Simard, Steinkraus and Platt, "Best Practices for
       Convolutional Neural Networks applied to Visual Document Analysis", in
       Proc. of the International Conference on Document Analysis and
       Recognition, 2003.
       Source: https://gist.github.com/oeway/2e3b989e0343f0884388ed7ed82eb3b0
    """
    def __init__(self, alpha=1000, sigma=30, spline_order=1, mode='nearest', random_state=numpy.random, p=1):
        self.alpha = alpha
        self.sigma = sigma
        self.spline_order = spline_order
        self.mode = mode
        self.random_state = random_state
        self.p = p

    def __call__(self, img):

        if random.random() < self.p:

            img = numpy.asarray(img)
            
            assert img.ndim == 2

            shape = img.shape

            dx = gaussian_filter((self.random_state.rand(*shape) * 2 - 1),
                                self.sigma, mode="constant", cval=0) * self.alpha
            dy = gaussian_filter((self.random_state.rand(*shape) * 2 - 1),
                                self.sigma, mode="constant", cval=0) * self.alpha

            x, y = numpy.meshgrid(numpy.arange(shape[0]), numpy.arange(shape[1]), indexing='ij')
            indices = [numpy.reshape(x + dx, (-1, 1)), numpy.reshape(y + dy, (-1, 1))]
            result = numpy.empty_like(img)
            result[:, :] = map_coordinates(
                img[:, :], indices, order=self.spline_order, mode=self.mode).reshape(shape)
            return PIL.Image.fromarray(result)
        else:
            return img