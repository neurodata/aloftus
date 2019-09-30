#%%
import shutil
from dipy.workflows.workflow import Workflow

class DmriReg(Workflow):

    def run(self, input_files, text_to_append="dipy", out_dir="", out_file="append.txt"):
        """
        Parameters
        ----------
        input_files : string
            path to input files.
        text_to_append : str, optional
            Text appended to file, by default "dipy"
        out_dir : str, optional
            Resulting file location, by default ""
        out_file : str, optional
            Name of result file to be saved, by default "append.txt"
        """