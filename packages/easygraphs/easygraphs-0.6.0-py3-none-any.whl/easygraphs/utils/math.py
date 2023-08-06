'''
Author: Zeng Siwei
Date: 2021-04-13 00:23:02
LastEditors: Zeng Siwei
LastEditTime: 2021-04-20 10:21:43
Description: 
'''
import numpy as np

def col_normalize(emb):
    '''
    Args: 
		emb: torch.Tensor
    Returns: 
		
    '''
    emb = (emb - emb.mean(0, keepdims=True)) / emb.std(0, keepdims=True)
    return emb

def scale(x):
    x = (x-np.min(x))/(np.max(x) - np.min(x))
    return x