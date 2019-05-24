#%%
import matplotlib.pyplot as plt
import os
import sys

sys.path.insert(0, os.getcwd())
import visualize
import discriminability
from pathlib import Path
import networkx as nx
import numpy as np
import re
import pandas as pd

#%%
names = ["master (HNU1)", "staging (HNU1)", "from 02/17, dev (HNU1)"]
disc = [np.nan, 0.96, 0.83]
n = [np.nan, 100, 80]

df = pd.DataFrame({"branch": names, "discriminability": disc, "number of graphs": n})
df
