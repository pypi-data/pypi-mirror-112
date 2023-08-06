#!/usr/bin/env python
# coding=utf-8

def _maker(protocol, resize_size=512, cc_size=512, RGB=True):

    from ....data.transforms import RemoveBlackBorders, SingleAutoLevel16to8
    import torchvision.transforms as transforms
    from ....data.padchest import dataset as raw
    from .. import make_dataset as mk

    post_transforms = []
    if not RGB:
        post_transforms = [transforms.Lambda(lambda x: x.convert("L"))]

    return mk(
            [raw.subsets(protocol)], 
            [
                SingleAutoLevel16to8(),
                transforms.Resize(resize_size),
                transforms.CenterCrop(cc_size)
            ],
            [transforms.RandomHorizontalFlip()],
            post_transforms
        )