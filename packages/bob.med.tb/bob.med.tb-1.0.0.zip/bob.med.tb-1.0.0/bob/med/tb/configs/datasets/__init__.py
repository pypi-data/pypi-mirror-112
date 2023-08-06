#!/usr/bin/env python
# coding=utf-8

from torchvision.transforms import RandomRotation
import random
import torch
import numpy as np

"""Standard configurations for dataset setup"""

RANDOM_ROTATION = [RandomRotation(15)]
"""Shared data augmentation based on random rotation only"""

def make_subset(l, transforms=[], prefixes=[], suffixes=[]):
    """Creates a new data set, applying transforms

    .. note::

       This is a convenience function for our own dataset definitions inside
       this module, guaranteeting homogenity between dataset definitions
       provided in this package.  It assumes certain strategies for data
       augmentation that may not be translatable to other applications.


    Parameters
    ----------

    l : list
        List of delayed samples

    transforms : list
        A list of transforms that needs to be applied to all samples in the set

    prefixes : list
        A list of data augmentation operations that needs to be applied
        **before** the transforms above

    suffixes : list
        A list of data augmentation operations that needs to be applied
        **after** the transforms above


    Returns
    -------

    subset : :py:class:`bob.med.tb.data.utils.SampleListDataset`
        A pre-formatted dataset that can be fed to one of our engines

    """
    
    from ...data.utils import SampleListDataset as wrapper

    return wrapper(l, prefixes + transforms + suffixes)


def make_dataset(subsets_groups, transforms=[], t_transforms=[], 
                post_transforms=[]):
    """Creates a new configuration dataset from a list of dictionaries 
    and transforms

    This function takes as input a list of dictionaries as those that can be 
    returned by :py:meth:`bob.med.tb.data.dataset.JSONDataset.subsets` 
    mapping protocol names (such as ``train``, ``dev`` and ``test``) to
    :py:class:`bob.med.tb.data.sample.DelayedSample` lists, and a set of
    transforms, and returns a dictionary applying
    :py:class:`bob.med.tb.data.utils.SampleListDataset` to these
    lists, and our standard data augmentation if a ``train`` set exists.

    For example, if ``subsets`` is composed of two sets named ``train`` and
    ``test``, this function will yield a dictionary with the following entries:

    * ``__train__``: Wraps the ``train`` subset, includes data augmentation
      (note: datasets with names starting with ``_`` (underscore) are excluded
      from prediction and evaluation by default, as they contain data
      augmentation transformations.)
    * ``train``: Wraps the ``train`` subset, **without** data augmentation
    * ``test``: Wraps the ``test`` subset, **without** data augmentation

    .. note::

       This is a convenience function for our own dataset definitions inside
       this module, guaranteeting homogenity between dataset definitions
       provided in this package.  It assumes certain strategies for data
       augmentation that may not be translatable to other applications.


    Parameters
    ----------

    subsets : list
        A list of dictionaries that contains the delayed sample lists 
        for a number of named lists. The subsets will be aggregated in one
        final subset. If one of the keys is ``train``, our standard dataset
        augmentation transforms are appended to the definition of that subset.
        All other subsets remain un-augmented.

    transforms : list
        A list of transforms that needs to be applied to all samples in the set

    t_transforms : list
        A list of transforms that needs to be applied to the train samples

    post_transforms : list
        A list of transforms that needs to be applied to all samples in the set
        after all the other transforms


    Returns
    -------

    dataset : dict
        A pre-formatted dataset that can be fed to one of our engines. It maps
        string names to
        :py:class:`bob.med.tb.data.utils.SampleListDataset`'s.

    """

    retval = {}

    if len(subsets_groups) == 1:
        subsets = subsets_groups[0]
    else:
        # If multiple subsets groups: aggregation
        aggregated_subsets = {}
        for subsets in subsets_groups:
            for key in subsets.keys():
                if key in aggregated_subsets:
                    aggregated_subsets[key] += subsets[key]
                    # Shuffle if data comes from multiple datasets
                    random.shuffle(aggregated_subsets[key])
                else:
                    aggregated_subsets[key] = subsets[key]
        subsets = aggregated_subsets
        
    # Add post_transforms after t_transforms for the train set
    t_transforms += post_transforms

    for key in subsets.keys():

        retval[key] = make_subset(subsets[key], transforms=transforms, 
                                suffixes=post_transforms)
        if key == "train":
            retval["__train__"] = make_subset(subsets[key],
                    transforms=transforms,
                    suffixes=(t_transforms)
                    )
        if key == "validation":
            # also use it for validation during training
            retval["__valid__"] = retval[key]

    if ("__train__" in retval) and ("train" in retval) \
            and ("__valid__" not in retval):
        # if the dataset does not have a validation set, we use the unaugmented
        # training set as validation set
        retval["__valid__"] = retval["train"]

    return retval


def get_samples_weights(dataset):
    """Compute the weights of all the samples of the dataset to balance it
    using the sampler of the dataloader
    
    This function takes as input a :py:class:`torch.utils.data.dataset.Dataset` 
    and computes the weights to balance each class in the dataset and the
    datasets themselves if we have a ConcatDataset.


    Parameters
    ----------

    dataset : torch.utils.data.dataset.Dataset
        An instance of torch.utils.data.dataset.Dataset
        ConcatDataset are supported


    Returns
    -------

    samples_weights : :py:class:`torch.Tensor`
        the weights for all the samples in the dataset given as input

    """

    samples_weights = []

    if isinstance(dataset, torch.utils.data.ConcatDataset):
        for ds in dataset.datasets:

            # Weighting only for binary labels
            if isinstance(ds._samples[0].label, int):
            
                # Groundtruth
                targets = []
                for s in ds._samples:
                    targets.append(s.label)
                targets = torch.tensor(targets)

                # Count number of samples per class
                class_sample_count = torch.tensor(
                    [(targets == t).sum() for t in torch.unique(targets, sorted=True)])

                weight = 1. / class_sample_count.float()

                samples_weights.append(torch.tensor([weight[t] for t in targets]))
            
            else:
                # We only weight to sample equally from each dataset
                samples_weights.append(torch.full((len(ds),), 1. / len(ds)))
        
        # Concatenate sample weights from all the datasets
        samples_weights = torch.cat(samples_weights)
        
    else:
        # Weighting only for binary labels
        if isinstance(dataset._samples[0].label, int):
            # Groundtruth
            targets = []
            for s in dataset._samples:
                targets.append(s.label)
            targets = torch.tensor(targets)

            # Count number of samples per class
            class_sample_count = torch.tensor(
                [(targets == t).sum() for t in torch.unique(targets, sorted=True)])

            weight = 1. / class_sample_count.float()

            samples_weights = torch.tensor([weight[t] for t in targets])

        else:
            # Equal weights for non-binary labels
            samples_weights = torch.ones(len(dataset._samples))
    
    return samples_weights


def get_positive_weights(dataset):
    """Compute the positive weights of each class of the dataset to balance 
    the BCEWithLogitsLoss criterion
    
    This function takes as input a :py:class:`torch.utils.data.dataset.Dataset` 
    and computes the positive weights of each class to use them to have 
    a balanced loss.


    Parameters
    ----------

    dataset : torch.utils.data.dataset.Dataset
        An instance of torch.utils.data.dataset.Dataset
        ConcatDataset are supported


    Returns
    -------

    positive_weights : :py:class:`torch.Tensor`
        the positive weight of each class in the dataset given as input

    """
    targets = []

    if isinstance(dataset, torch.utils.data.ConcatDataset):

        for ds in dataset.datasets:            
            for s in ds._samples:
                targets.append(s.label)

    else:
        for s in dataset._samples:
            targets.append(s.label)

    targets = torch.tensor(targets)
    
    # Binary labels
    if len(list(targets.shape)) == 1:
        class_sample_count = [float((targets == t).sum().item()) for t in torch.unique(targets, sorted=True)]

        # Divide negatives by positives
        positive_weights = torch.tensor([class_sample_count[0]/class_sample_count[1]]).reshape(-1)

    # Multiclass labels
    else:
        class_sample_count = torch.sum(targets, dim=0)
        negative_class_sample_count = torch.full((targets.size()[1],), float(targets.size()[0])) - class_sample_count
        
        positive_weights = negative_class_sample_count / (class_sample_count + negative_class_sample_count)
    
    return positive_weights