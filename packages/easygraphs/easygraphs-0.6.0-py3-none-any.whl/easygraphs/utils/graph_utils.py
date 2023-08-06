import numpy as np


def generate_random_mask(n, prob_a = 0.8, prob_b = 0.1):
    train_mask = (np.random.rand(n) < prob_a).astype(int)
    val_random = (np.random.rand(n) < (prob_b / (1-prob_a))).astype(int)
   
    val_select = (np.ones(n) - train_mask)
    val_mask = np.zeros(n, dtype=int)
    for i in range(n):
        if val_select[i] == 1 and val_random[i] == True:
            val_mask[i] = 1
    test_mask = np.ones(n) - train_mask - val_mask
    return train_mask, val_mask, test_mask