#!/usr/bin/env python
# coding=utf-8


"""Common utilities"""

import contextlib

import torch
import torch.utils.data
import PIL
import numpy as np
from torchvision.transforms import Compose, ToTensor


class SampleListDataset(torch.utils.data.Dataset):
    """PyTorch dataset wrapper around Sample lists

    A transform object can be passed that will be applied to the image, ground
    truth and mask (if present).

    It supports indexing such that dataset[i] can be used to get ith sample.

    Parameters
    ----------

    samples : list
        A list of :py:class:`bob.med.tb.data.sample.Sample` objects

    transforms : :py:class:`list`, Optional
        a list of transformations to be applied to **both** image and
        ground-truth data.  Notice a last transform
        (:py:class:`torchvision.transforms.transforms.ToTensor`) is always 
        applied - you do not need to add that.

    """

    def __init__(self, samples, transforms=[]):

        self._samples = samples
        self.transforms = transforms

    @property
    def transforms(self):
        return self._transforms.transforms[:-1]

    @transforms.setter
    def transforms(self, l):
        if any([isinstance(t, ToTensor) for t in l]):
            self._transforms = Compose(l)
        else:
            self._transforms = Compose(l + [ToTensor()])

    def copy(self, transforms=None):
        """Returns a deep copy of itself, optionally resetting transforms

        Parameters
        ----------

        transforms : :py:class:`list`, Optional
            An optional list of transforms to set in the copy.  If not
            specified, use ``self.transforms``.
        """

        return SampleListDataset(self._samples, transforms or self.transforms)

    def random_permute(self, feature):
        """Randomly permute feature values from all samples

        Useful for permutation feature importance computation

        Parameters
        ----------

        feature : int
            The position of the feature
        """
        feature_values = np.zeros(len(self))

        for k, s in enumerate(self._samples):
            features = s.data['data']
            if isinstance(features, list):
                feature_values[k] = features[feature]
        
        np.random.shuffle(feature_values)

        for k, s in enumerate(self._samples):
            features = s.data["data"]
            features[feature] = feature_values[k]

    def __len__(self):
        """

        Returns
        -------

        size : int
            size of the dataset

        """
        return len(self._samples)

    def __getitem__(self, key):
        """

        Parameters
        ----------

        key : int, slice

        Returns
        -------

        sample : list
            The sample data: ``[key, image, label]``

        """

        if isinstance(key, slice):
            return [self[k] for k in range(*key.indices(len(self)))]
        else:  # we try it as an int
            item = data = self._samples[key]
            if not isinstance(data, dict):
                key = item.key
                data = item.data  # triggers data loading

            retval = data["data"]

            if self._transforms and isinstance(retval, PIL.Image.Image):
                retval = self._transforms(retval)
            elif isinstance(retval, list):
                retval = torch.FloatTensor(retval)

            if "label" in data:
                if isinstance(data["label"], list):
                    return [key, retval, torch.FloatTensor(data["label"])]
                else:
                    return [key, retval, data["label"]]
            
            return [item.key, retval]