#%%
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import os, sys, re
from math import sqrt, ceil
import discriminability

#%%
def nearest_square(num):
    """ 
    Return the smallest square number greater than `num`.
    For use in visualize_biggraph(), to make the correct number of axes.
    
    Parameters:
    -----------
        num: int

    Returns: 
    --------
        int. Square number.
    """
    return (
        ceil(sqrt(num)) ** 2
    )  # derek -- this is what I was talking about over the phone. See its implementation in visualize_biggraph().


def visualize_graph(graph_inp, log10=True, save=False, filetype="ssv", name=""):
    """
    Given an input .ssv file, output a graph.

    Parameters:
    -----------
        graph_inp  : str. .ssv or .csv edgelist.
        log10  : bool. whether to output a log-scale graph
        save  : bool. If True, save plot as file.

    Returns:
    --------
        plot if not save.
    """
    graph_inp = os.path.abspath(graph_inp)
    if filetype == "csv":
        nx_graph = nx.read_weighted_edgelist(graph_inp, delimiter=",")
    else:
        nx_graph = nx.read_weighted_edgelist(graph_inp)
    mat = nx.to_numpy_matrix(nx_graph)
    if log10:
        plot = plt.imshow(np.log10(mat + 1), cmap="plasma")
        plt.show()
    else:
        plot = plt.imshow(mat, cmap="plasma")

    if save:
        plt.savefig(name + ".png")
    else:
        return plot


def visualize_biggraph(ndmg_participant_dir, save=False, outname=""):
    # TODO: figure out a way to have the empty boxes at the end be blank, rather than empty title-less boxes
    # TODO: figure out a way to use visualize_graph to get the elements of each `axi`, this reuses code too much
    """ 
    Given an input directory, output a summary png file.

    Parameters:
    -----------
        ndmg_participant_dir  : str. Directory containing output files.
        save  : bool. If True, save the figure as a file.
        outname  : str. Name of output .png file
    """
    subls = discriminability.get_graph_files(ndmg_participant_dir)
    rgx = re.compile(r"(sub-)([a-zA-Z0-9]*(_ses-)([a-zA-Z0-9]*))")
    sq = nearest_square(len(subls))
    rows = int(sqrt(sq))
    cols = int(sqrt(sq))

    fig, ax = plt.subplots(rows, cols, figsize=(rows * 2.5, cols * 2.5))
    for i, axi in enumerate(ax.flat):
        if i < len(subls):
            sub = "-".join(rgx.search(subls[i]).groups()[1:-2:2])
            graph_inp = os.path.abspath(subls[i])
            nx_graph = nx.read_weighted_edgelist(graph_inp)
            mat = nx.to_numpy_matrix(nx_graph)
            axi.imshow(np.log10(mat + 1), cmap="plasma")
            axi.set_title(sub)
        else:
            break

    fig.subplots_adjust(hspace=rows * 0.05)
    if save:
        plt.savefig(outname + ".png")
    else:
        plt.show()


#%%
if __name__ == "__main__":
    p, out = sys.argv[1], sys.argv[2]
    visualize_biggraph(p, save=True, outname=out)
