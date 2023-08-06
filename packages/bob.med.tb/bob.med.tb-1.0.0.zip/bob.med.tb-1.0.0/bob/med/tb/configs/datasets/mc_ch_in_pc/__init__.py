#!/usr/bin/env python
# coding=utf-8
        
from torch.utils.data.dataset import ConcatDataset

def _maker(protocol):

    if protocol == "default":
        from ..montgomery import default as mc
        from ..shenzhen import default as ch
        from ..indian import default as indian
        from ..padchest import tb_idiap as pc
    elif protocol == "rgb":
        from ..montgomery import rgb as mc
        from ..shenzhen import rgb as ch
        from ..indian import rgb as indian
        from ..padchest import tb_idiap_rgb as pc

    mc = mc.dataset
    ch = ch.dataset
    indian = indian.dataset
    pc = pc.dataset

    dataset = {}
    dataset['__train__'] = ConcatDataset([mc["__train__"], ch["__train__"], indian["__train__"], pc["__train__"]])
    dataset['train'] = ConcatDataset([mc["train"], ch["train"], indian["train"], pc["train"]])
    dataset['__valid__'] = ConcatDataset([mc["__valid__"], ch["__valid__"], indian["__valid__"], pc["__valid__"]])
    dataset['test'] = ConcatDataset([mc["test"], ch["test"], indian["test"], pc["test"]])

    return dataset