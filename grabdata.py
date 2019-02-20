""" Grab all .ssv files in a directory. """
import shutil
import os


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
                or filename.endswith("_adj.ssv")
            )
            and atlas in filename
        )  # Soft check on filenames. Will break if filename has 'atlas' and '_adj.csv' in it but is not the adjacency matrix for that atlas.
    ]
    return out


def files_to_out(inp, out):
    """
    inp: List, each element == absolute path to filename
    Send all files in list to output directory. 
    """
    out = os.path.abspath(out)
    for filename in inp:
        filename = os.path.abspath
        name = os.path.basename(filename)
        shutil.copy(filename, out + "/{}".format(name))

