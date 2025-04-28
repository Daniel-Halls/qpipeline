import os
from qpipeline.base.utils import error_and_exit


def make_paths_absolute(args: dict, paths_to_make_abs: list) -> str:
    """
    Function to turn paths
    into absolute paths

    Parameters
    ----------
    args: dict
       cmd line arguments
    paths_to_make_abs: list
       list of keys to make
    """
    for path in paths_to_make_abs:
        args[path] = os.path.abspath(path)
    return args


def check_folders_exist(paths: list) -> None:
    for path in paths:
        if not os.path.exists(path):
            error_and_exit(False, f"{path} does not exist. Please check input")


def check_complusory_arguments(args: dict) -> None:
    compulsory = ["study_folder", "id"]
    if args["command"] == "setup":
        compulsory.append("raw_data")
    for key in compulsory:
        error_and_exit(
            args[key], f"Missing {key} argument. Please specify with --{key}."
        )


def check_bids_folder(bids_dir: str) -> None:
    anat_dir = os.path.join(bids_dir, "anat")
    dwi_dir = os.path.join(bids_dir, "dwi")
    anat_data = True if (os.path.exists(anat_dir) and os.listdir(anat_dir)) else False
    dwi_data = True if (os.path.exists(dwi_dir) and os.listdir(dwi_dir)) else False
    error_and_exit(anat_data, "No structural data found. Please check bids directory")
    error_and_exit(dwi_data, "No diffusion data found. Please check bids directory")


def check_input(args: dict) -> None:
    """
    Function to check inputs.
    Checks for complusory arguments,
    that paths are absolute, folder exists
    and if setup bids data exists.

    Parameters
    ----------
    args: dict
        cmd line arguments

    Returns
    -------
    None
    """
    check_complusory_arguments(args)
    subselect_keys = (
        ["study_folder", "raw_data"] if args["raw_data"] else ["study_folder"]
    )
    paths_to_check = {key: args[key] for key in subselect_keys if key in subselect_keys}
    args = make_paths_absolute(args, list(paths_to_check.keys()))
    check_folders_exist(list(paths_to_check.valeus()))
    if args["command"] == "setup":
        check_bids_folder(args["raw_data"])
