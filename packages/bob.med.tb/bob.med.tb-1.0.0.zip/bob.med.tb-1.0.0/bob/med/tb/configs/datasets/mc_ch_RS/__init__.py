#!/usr/bin/env python
# coding=utf-8
        
from torch.utils.data.dataset import ConcatDataset

def _maker(protocol):

    if protocol == "default":
        from ..montgomery_RS import default as mc
        from ..shenzhen_RS import default as ch
    elif protocol == "fold_0":
        from ..montgomery_RS import fold_0 as mc
        from ..shenzhen_RS import fold_0 as ch
    elif protocol == "fold_1":
        from ..montgomery_RS import fold_1 as mc
        from ..shenzhen_RS import fold_1 as ch
    elif protocol == "fold_2":
        from ..montgomery_RS import fold_2 as mc
        from ..shenzhen_RS import fold_2 as ch
    elif protocol == "fold_3":
        from ..montgomery_RS import fold_3 as mc
        from ..shenzhen_RS import fold_3 as ch
    elif protocol == "fold_4":
        from ..montgomery_RS import fold_4 as mc
        from ..shenzhen_RS import fold_4 as ch
    elif protocol == "fold_5":
        from ..montgomery_RS import fold_5 as mc
        from ..shenzhen_RS import fold_5 as ch
    elif protocol == "fold_6":
        from ..montgomery_RS import fold_6 as mc
        from ..shenzhen_RS import fold_6 as ch
    elif protocol == "fold_7":
        from ..montgomery_RS import fold_7 as mc
        from ..shenzhen_RS import fold_7 as ch
    elif protocol == "fold_8":
        from ..montgomery_RS import fold_8 as mc
        from ..shenzhen_RS import fold_8 as ch
    elif protocol == "fold_9":
        from ..montgomery_RS import fold_9 as mc
        from ..shenzhen_RS import fold_9 as ch

    mc = mc.dataset
    ch = ch.dataset

    dataset = {}
    dataset['__train__'] = ConcatDataset([mc["__train__"], ch["__train__"]])
    dataset['train'] = ConcatDataset([mc["train"], ch["train"]])
    dataset['__valid__'] = ConcatDataset([mc["__valid__"], ch["__valid__"]])
    dataset['validation'] = ConcatDataset([mc["validation"], ch["validation"]])
    dataset['test'] = ConcatDataset([mc["test"], ch["test"]])

    return dataset