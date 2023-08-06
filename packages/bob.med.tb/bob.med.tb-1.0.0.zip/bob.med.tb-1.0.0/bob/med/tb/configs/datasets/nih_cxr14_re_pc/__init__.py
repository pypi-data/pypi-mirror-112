#!/usr/bin/env python
# coding=utf-8
    
from torch.utils.data.dataset import ConcatDataset

def _maker(protocol):

    if protocol == "idiap":
        from ..nih_cxr14_re import idiap as nih_cxr14_re
        from ..padchest import no_tb_idiap as padchest_no_tb

    nih_cxr14_re = nih_cxr14_re.dataset
    padchest_no_tb = padchest_no_tb.dataset

    dataset = {}
    dataset['__train__'] = ConcatDataset([nih_cxr14_re["__train__"], padchest_no_tb["__train__"]])
    dataset['train'] = ConcatDataset([nih_cxr14_re["train"], padchest_no_tb["train"]])
    dataset['__valid__'] = ConcatDataset([nih_cxr14_re["__valid__"], padchest_no_tb["__valid__"]])
    dataset['validation'] = ConcatDataset([nih_cxr14_re["validation"], padchest_no_tb["validation"]])
    dataset['test'] = nih_cxr14_re["test"]

    return dataset