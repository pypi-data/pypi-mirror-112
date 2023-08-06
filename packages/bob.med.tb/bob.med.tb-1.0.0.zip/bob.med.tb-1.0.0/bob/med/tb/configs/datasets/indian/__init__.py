#!/usr/bin/env python
# coding=utf-8

def _maker(protocol, resize_size=512, cc_size=512, RGB=False):

    from ....data.transforms import RemoveBlackBorders, ElasticDeformation
    from torchvision import transforms
    from ....data.indian import dataset as raw
    from .. import make_dataset as mk

    post_transforms = []
    if RGB:
        post_transforms = [transforms.Lambda(lambda x: x.convert("RGB")),
                transforms.ToTensor()]

    return mk(
        [raw.subsets(protocol)], 
        [
            RemoveBlackBorders(), 
            transforms.Resize(resize_size), 
            transforms.CenterCrop(cc_size)
        ],
        [ElasticDeformation(p=0.8)],
        post_transforms
        )