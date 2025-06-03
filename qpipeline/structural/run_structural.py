from qpipeline.structural.qunex_structural_runner import run_structural
from qpipeline.base.cluster_support import wait_for_me
from qpipeline.base.utils import has_qunex_run_sucessfully, check_progress
import os


def run_module(module_cmd: str, sub_dir: str, args: dict) -> None:
    """
    Function to run a structural module

    Parameters
    ----------
    module_cmd: str
        str of module to be ran
    sub_dir: str
        str of subjs directory
    args: dict
        dictionary of cmd args
    
    Returns
    -------
    None
    """
    cmd = run_structural(args, module_cmd)
    wait_for_me(cmd["stdout"])
    has_qunex_run_sucessfully(sub_dir, module_cmd)
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
            print(f"{module} ran. Skipping...")
            continue
        run_module(module, sub_dir, args)
