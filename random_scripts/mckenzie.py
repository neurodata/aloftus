#%%
import matplotlib.pyplot as plt
import numpy as np

# %matplotlib inline


def foo():
    for i in range(10):
        print(i)
        # bar()


def bar():
    for j in "abcdefghijklmnop":
        print(j)


foo()
#%%
x = np.arange(1, 10)
y = np.arange(1, 10)


plt.plot(x, y)
