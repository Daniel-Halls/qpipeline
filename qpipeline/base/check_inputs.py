import os
from pathlib import Path
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


def check_datatype(args: dict) -> None:
    """
    Function to check given datatype

    Parameters
    ----------
    args: dict
        cmd arguments

    Returns
    --------
    None
    """
    error_and_exit(
        any(arg in ["batch", "data_type"] for arg in args.keys()),
        "Please provide either datatype --data_type {hcp,biobank} or custom batch with --batch",
    )


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
    compulsory = ["study_folder"]
    if args["command"] == "setup":
        compulsory.append("raw_data")
        check_datatype(args)
    else:
        compulsory.append("id")

    for key in compulsory:
        error_and_exit(
            args[key], f"Missing {key} argument. Please specify with --{key}."
        )


def check_folder_recursively(base_path: str, folder: str) -> list:
    """
    Function to recusively search
    for a given directory

    Parameters
    ----------
    base_path: str
        base path to search
    folder: str
        str of folder to search
        for
    Returns
    -------
    list: list object
        list of path of given folder
    """
    return [path for path in Path(base_path).rglob(folder)]


def check_folder_is_setup(path) -> bool:
    try:
        bidds_folder_path = path[0]
    except IndexError:
        return False
    return True if os.listdir(bidds_folder_path) else False


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
    error_and_exit(os.path.isdir(bids_dir), "Bids Folder does not exists")
    folders_to_look_for = ["anat", "dwi"]
    for folder in folders_to_look_for:
        folder_path = check_folder_recursively(bids_dir, folder)
        everything_ok = check_folder_is_setup(folder_path)
        error_and_exit(
            everything_ok, f"{folder} not found. Please check bids directory"
        )


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
        if "raw_data" in args.keys()
        else [args["study_folder"]]
    )
    check_paths_absolute(folder_paths)

    if args["command"] == "setup":
        check_bids_folder(args["raw_data"])


def valid_data_types() -> list:
    """
    Function to check that datatype is
    valid.

    Parameters
    ----------
    None

    Returns
    -------
    list: list object
        list of accpetable datatypes
    """
    return ["hcp", "biobank"]
