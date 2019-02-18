#%%
import os
import numpy as np
import pandas as pd

#%%
""" 
Sample output (ssv files):

Column 0: range(1, 71)
Column 0: range(2, 71)
Column 3: random numbers in range(10000)
--------------
2 66 863
2 67 4019
2 68 4816
2 69 29
2 70 56
2 71 5358
3 5 87
3 8 390
3 9 2626
3 10 9056
3 11 2514
3 12 1626
3 13 251
"""
#%%

# Make three columns
# I'm an idiot ... I could have just copied two of the pre-existing files and used those as a sample dataset
def make_sample_dataset():
    state = np.random.RandomState(0)
    a = np.arange(1, 71)
    b = state.permutation(70)
    c = np.random.randint(0, 10000, 70)
    out = np.vstack((a, b, c)).T

    return out
