#!/usr/bin/env python
# coding=utf-8

def _maker(protocol, size=512):

    from ....data.transforms import RemoveBlackBorders
    import torchvision.transforms as transforms
    from ....data.nih_cxr14_re import dataset as raw
    from .. import make_dataset as mk

    # ImageNet normalization
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                         std=[0.229, 0.224, 0.225])

    return mk(
            [raw.subsets(protocol)], 
            [transforms.Resize((size, size))],
            [transforms.RandomHorizontalFlip()],
            [transforms.ToTensor(), normalize]
        )