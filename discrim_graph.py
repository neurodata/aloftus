#!/usr/bin/env python
# coding: utf-8

from pathlib import Path
import os, re, sys
import numpy as np
import networkx as nx
from collections import Counter

# TODO: Figure out a better way to organize subject IDs
# TODO: make code work for all atlases, not just desikan
# TODO: make it work when one of the graphs is not n_roi x n_roi (e.g., 70x70 for desikan). Currently breaks if that happens

# list of numpy matrices
def get_x(input_path: str, output_name: str) -> None:
    """ input: directory with .csv file outputs from ndmg """
    input_path = Path(input_path)
    num_subj = len([i for i in input_path.iterdir()])
    graphs = [
        nx.read_weighted_edgelist(str(i), delimiter=",") for i in input_path.iterdir()
    ]
    graphs = [
        nx.to_numpy_array(g, nodelist=sorted(list(graphs[i].nodes())))
        for i, g in enumerate(graphs)
    ]
    for i, _ in enumerate(graphs):
        np.fill_diagonal(graphs[i], 0)

    graphs = np.array(graphs)
    graphs_final = np.reshape(graphs, (num_subj, 70 * 70))
    np.savetxt("{}.csv".format(output_name), graphs_final, fmt="%f", delimiter=",")


def get_y(input_path: str, output_name: str) -> None:
    """ Outputs a csv file where each row i is (theoretically) the subject id for graphs_final[i, :]. """
    input_path = Path(input_path)
    rgx = r"(sub-)([a-zA-Z0-9]*)"

    Y = [str(i) for i in input_path.iterdir()]
    Y = [re.findall(rgx, Y[i])[0][1] for i, _ in enumerate(Y)]

    print(
        "Counter for subject IDs: ", Counter(Y)
    )  # Check to make sure each subj has duplicates

    for i in Y:  # make Y vector file
        with open("{}.csv".format(output_name), "a") as f:
            f.write(i + "\n")


def main():
    p = "desikan_res-1x1x1"
    get_x(p, "HNU1_X")
    get_y(p, "HNU1_Y")


if __name__ == "__main__":
    main()

# Potential thing I'm worried about: making sure order of subjects was preserved across this whole thing, otherwise the Y vector won't be the correct order
