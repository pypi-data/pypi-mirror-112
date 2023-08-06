#!/usr/bin/env python
# coding=utf-8
        
from torch.utils.data.dataset import ConcatDataset

def _maker(protocol):

    if protocol == "default":
        from ..montgomery import default as mc
        from ..shenzhen import default as ch
    elif protocol == "rgb":
        from ..montgomery import rgb as mc
        from ..shenzhen import rgb as ch
    elif protocol == "fold_0":
        from ..montgomery import fold_0 as mc
        from ..shenzhen import fold_0 as ch
    elif protocol == "fold_1":
        from ..montgomery import fold_1 as mc
        from ..shenzhen import fold_1 as ch
    elif protocol == "fold_2":
        from ..montgomery import fold_2 as mc
        from ..shenzhen import fold_2 as ch
    elif protocol == "fold_3":
        from ..montgomery import fold_3 as mc
        from ..shenzhen import fold_3 as ch
    elif protocol == "fold_4":
        from ..montgomery import fold_4 as mc
        from ..shenzhen import fold_4 as ch
    elif protocol == "fold_5":
        from ..montgomery import fold_5 as mc
        from ..shenzhen import fold_5 as ch
    elif protocol == "fold_6":
        from ..montgomery import fold_6 as mc
        from ..shenzhen import fold_6 as ch
    elif protocol == "fold_7":
        from ..montgomery import fold_7 as mc
        from ..shenzhen import fold_7 as ch
    elif protocol == "fold_8":
        from ..montgomery import fold_8 as mc
        from ..shenzhen import fold_8 as ch
    elif protocol == "fold_9":
        from ..montgomery import fold_9 as mc
        from ..shenzhen import fold_9 as ch
    elif protocol == "fold_0_rgb":
        from ..montgomery import fold_0_rgb as mc
        from ..shenzhen import fold_0_rgb as ch
    elif protocol == "fold_1_rgb":
        from ..montgomery import fold_1_rgb as mc
        from ..shenzhen import fold_1_rgb as ch
    elif protocol == "fold_2_rgb":
        from ..montgomery import fold_2_rgb as mc
        from ..shenzhen import fold_2_rgb as ch
    elif protocol == "fold_3_rgb":
        from ..montgomery import fold_3_rgb as mc
        from ..shenzhen import fold_3_rgb as ch
    elif protocol == "fold_4_rgb":
        from ..montgomery import fold_4_rgb as mc
        from ..shenzhen import fold_4_rgb as ch
    elif protocol == "fold_5_rgb":
        from ..montgomery import fold_5_rgb as mc
        from ..shenzhen import fold_5_rgb as ch
    elif protocol == "fold_6_rgb":
        from ..montgomery import fold_6_rgb as mc
        from ..shenzhen import fold_6_rgb as ch
    elif protocol == "fold_7_rgb":
        from ..montgomery import fold_7_rgb as mc
        from ..shenzhen import fold_7_rgb as ch
    elif protocol == "fold_8_rgb":
        from ..montgomery import fold_8_rgb as mc
        from ..shenzhen import fold_8_rgb as ch
    elif protocol == "fold_9_rgb":
        from ..montgomery import fold_9_rgb as mc
        from ..shenzhen import fold_9_rgb as ch

    mc = mc.dataset
    ch = ch.dataset

    dataset = {}
    dataset['__train__'] = ConcatDataset([mc["__train__"], ch["__train__"]])
    dataset['train'] = ConcatDataset([mc["train"], ch["train"]])
    dataset['__valid__'] = ConcatDataset([mc["__valid__"], ch["__valid__"]])
    dataset['validation'] = ConcatDataset([mc["validation"], ch["validation"]])
    dataset['test'] = ConcatDataset([mc["test"], ch["test"]])

    return dataset