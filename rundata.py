import os

""" iterate over each sample_dir. Call run_ndmg on each dir. """


def run_ndmg(in_dir, out_dir):
    """
    in_dir : The full path to whatever BIDs-formatted input directory for the current loop
    out_dir : Full path for output of the current loop
    """

    NDMG_CMD = "docker run -ti -v {}:/inputs -v {}:/outputs neurodata/m3r-release:0.1.1 --modality dwi /inputs /outputs participant --nproc 40".format(
        in_dir, out_dir
    )
    print(NDMG_CMD)
    os.system(NDMG_CMD)


def main():
    if not os.path.exists("parent_out"):
        os.mkdir("parent_out")

    for in_dir in os.listdir(os.getcwd()):
        if os.path.isdir(in_dir):

            out_dir = "{}_out".format(in_dir)
            os.mkdir(os.path.join("parent_out", out_dir))
            indir = os.path.abspath(in_dir)
            outdir = os.path.abspath(out_dir)

            run_ndmg(indir, outdir)
            print(indir)
            print(outdir)


main()
