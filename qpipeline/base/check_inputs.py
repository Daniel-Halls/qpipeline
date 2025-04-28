import os
from qpipeline.base.utils import error_and_exit


def check_paths_absolute(paths_to_check: list) -> None:
    """
    Function to check paths
    are absolute paths

    Parameters
    ----------
    paths_to_check: list
       list of paths to
       check that they are absolute

    Returns
    -------
    None
    """
    for path in paths_to_check:
        error_and_exit(
            os.path.isabs(path),
            f"{path} is not absolute path. Qunex needs absolute paths",
        )


def check_folders_exist(paths: list) -> None:
    """
    Function to check that folders exist

    Parameters
    ----------
    paths: list
       list of paths to
       check that they exist

    Returns
    -------
    None
    """
    for path in paths:
        if not os.path.exists(path):
            error_and_exit(False, f"{path} does not exist. Please check input")


def check_complusory_arguments(args: dict) -> None:
    """
    Function to check that complusory arguments
    have been given.

    Parameters
    ----------
    args: dict
        dictionary of cmd arguments

    Returns
    -------
    None
    """
    compulsory = ["study_folder", "id"]
    if args["command"] == "setup":
        compulsory.append("raw_data")
    for key in compulsory:
        error_and_exit(
            args[key], f"Missing {key} argument. Please specify with --{key}."
        )


def check_bids_folder(bids_dir: str) -> None:
    """
    Function to do the very basic
    bids check that qunex needs.

    Parameters
    ----------
    bids_dir: str
       path to bids directory

    Returns
    -------
    None
    """
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
    folder_paths = (
        [args["study_folder"], args["raw_data"]]
        if args["raw_data"]
        else args["study_folder"]
    )
    check_paths_absolute(folder_paths)
    check_folders_exist(folder_paths)
    if args["command"] == "setup":
        check_bids_folder(args["raw_data"])
