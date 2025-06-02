from qpipeline.structural.qunex_structural_runner import run_structural
from qpipeline.base.cluster_support import wait_for_me
from qpipeline.base.utils import has_qunex_run_sucessfully, check_progress
import os


def run_module(module_cmd, sub_dir, args):
    cmd = run_structural(args, "pre_freesurfer")
    wait_for_me(cmd["stdout"])
    has_qunex_run_sucessfully(sub_dir, "pre_freesurfer")
    print(f"{module_cmd} done")


def hcp_structual(args: dict) -> None:
    """
    Main function for the hcp structural
    pipeline

    Parameters
    ----------
    args: dict
        dictionary of arguments

    Returns
    -------
    None
    """
    sub_dir = os.path.join(args["study_folder"], args["id"])
    modules = ["pre_freesurfer", "freesurfer", "post_freesurfer"]
    for module in modules:
        if check_progress(sub_dir, module):
            print(f"{module} ran. Skipping")
        run_module(module, sub_dir, args)
