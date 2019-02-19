""" 
Discriminability code. Takes in output of ndmg participant-level analysis.
Currently in the root directory for safekeeping, will be moved to a better home once it's done
"""

#%%
import os, sys, re
import numpy as np, networkx as nx

#%%
def get_graph_files(ndmg_participant_dir, atlas):
    """
    ndmg_participant_dir  : ndmg participant-level analysis output directory.
    atlas  : which atlas should you get the graph for?
    Returns: list of folder locations for all graph outputs
    """
    d = os.path.abspath(ndmg_participant_dir)  # to make things easier
    out = [
        os.path.join(
            directory, filename
        )  # Returns list of absolute path files in ndmg_participant_dir that end in '_adj.csv'.
        for directory, _, filenames in os.walk(d)
        for filename in filenames
        if (
            (
                filename.endswith("_adj.csv")
                or filename.endswith("_elist.ssv")
                or filename.endswith("desikan.ssv")
            )
            and atlas in filename
        )  # Soft check on filenames. Will break if filename has 'atlas' and '_adj.csv' in it but is not the adjacency matrix for that atlas.
    ]
    return out


#%%
def numpy_from_output_graph(input_csv_file, sep=","):
    """ 
    Input: location of the .csv file for a single ndmg graph output
    Returns: Vectorized numpy matrix from that .csv file
    """
    # convert input from csv file to numpy matrix, then return
    out = nx.read_weighted_edgelist(
        input_csv_file, delimiter=sep
    )  # TODO: make sure this outputs the same thing regardless of delimiter
    out = nx.to_numpy_matrix(out)
    np.fill_diagonal(out, 0)  # for staging branch
    return np.array(out)


#%%
def matrix_and_vector_from_graphs(ndmg_participant_dir, atlas, return_files=False):
    # TODO: Figure out if there's a more computationally efficient way than building from a loop, that still absolutely guarentees that the target vector and corresponding matrix row are from the same subject
    """ 
    The main worker function. Big loop. Each loop iteration adds a row to out_matrix, and adds the subject name to out_target_vector.
    
    --------------
    Parameters: 
        ndmg_participant_dir: List of graph output locations
        atlas: Atlas to output graphs for
        csv: if True, output csv files for X and y. Else, return the tuple (matrix, target_vector).
    
    Returns: the tuple (out_matrix, out_target_vector).
    """
    out_matrix = np.empty((1, 70 * 70))  # TODO: make this dynamic to the atlas
    out_target_vector = []
    graphs = get_graph_files(ndmg_participant_dir, atlas)
    rgx = re.compile(
        r"(sub-)([a-zA-Z0-9]*)"
    )  # to be used for grabbing the subject name
    for (
        filename
    ) in (
        graphs
    ):  #  Builds the matrix and target vector element-by-element on a per-subject basis.
        if filename.endswith("ssv"):  # Account for ssv files, eric's code
            mat = numpy_from_output_graph(filename, sep=" ")
        else:
            mat = numpy_from_output_graph(filename)  # For csv files
        if mat.shape == (
            70,
            70,
        ):  # TODO: make this dynamic to the atlas, currently it's only for desikan
            sub_and_session = "".join(rgx.search(filename).groups())
            out_target_vector.append(sub_and_session)  # update out_target_vector
            out_matrix = np.append(
                out_matrix, mat.flatten()[np.newaxis, :], axis=0
            )  # TODO: implement this as a list, then convert to numpy after. I think that's more efficient.
    if return_files:
        np.savetxt(
            "{}_X.csv".format(ndmg_participant_dir),
            out_matrix[1:, :],
            fmt="%f",
            delimiter=",",
        )  # save X
        for i in out_target_vector:  # save y
            with open("{}_y.csv".format(ndmg_participant_dir), "a") as f:
                f.write(i + "\n")
    else:
        return (out_matrix[1:, :], out_target_vector)


data = "test_data"
matrix_and_vector_from_graphs(data, "desikan")
#%%
def csv_to_ssv(csv_file):
    name, ext = os.path.splitext(csv_file)
    os.rename(csv_file, name + ".ssv")

    with open(name + ".ssv", "rw") as f:
        for line in f:
            line.replace(",", " ")


# csv_to_ssv("test_data.ssv")
# with open("test_data.ssv", "r") as f4:
#     for line in f:
#         print(line)


#%%
def main(data):
    # TODO: input participant dir, output matrix_and_vector_from_graph() csv files
    # TODO: write assertion tests. Not sure if they normally go here.
    matrix_and_vector_from_graphs(data, "desikan", return_files=True)


# Call program with a file
if __name__ == "__main__":
    main(sys.argv[1])
