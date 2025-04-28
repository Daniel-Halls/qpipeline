from qpipeline.base.utils import run_cmd, write_to_file, container_path
from qpipeline.qunex_setup.qunex_commands import (
    create_study,
    import_data,
    create_session_info,
    create_batch,
    set_up_hcp,
)
import re
import os
import shutil
from pathlib import Path


def map_files() -> dict:
    """
    Function to map files in qunex format.
    Pipeline dynamically maps diffusion

    Parameters
    ----------
    None

    Returns
    -------
    dict: dictionary
        dict of mapping files
    """
    return {"T1w": "T1w", "T2w": "T2w"}


def map_scans(file_mapping: dict, label: str) -> str:
    """
    Function to map scans to correct quenx file name

    Parameters
    ----------
    file_mapping: dict
        dictionary of file mapping
    label: str
        label of scan name

    Returns
    -------
    str: str object
        string object of file mapping name
    """
    dwi_match = re.match(r"(dir[\d_]*-[AP]{2})_dwi", label)
    if dwi_match:
        return f"DWI:{dwi_match.group(1)}"
    return file_mapping.get(label, label)


def parse_output(output: str, study_path: str) -> None:
    """
    Function to parse through output
    to create mapping file

    Parameters
    ----------
    output: str
        stdout of qunex command

    Returns
    -------
    None
    """
    pattern = re.compile(r"---> linked (\d+\.nii\.gz) <-- sub-[^_]+_(.*)\.nii\.gz")
    mapped_files = {}
    file_mapping = map_files()
    for match in pattern.finditer(output):
        number = match.group(1).split(".")[0]
        label = match.group(2)
        mapped_files[number] = map_scans(file_mapping, label)
    result = [f"{num} => {label}\n" for num, label in mapped_files.items()]
    write_to_file(study_path, "hcp_mapping_file.txt", result, text_is_list=True)


def set_up_qunex_study(args: dict) -> None:
    """
    Main Function for setting
    up quenx study.

    Parameters
    ----------
    args: dict
        dictionary of cmd args

    Returns
    -------
    None
    """
    print(f"Setting up directory: {args['id']}")
    qunex_con_image = container_path()
    study_create = create_study(args["study_folder"], qunex_con_image, args["id"])
    run_cmd(study_create, no_return=True)
    data_importing = import_data(
        args["study_folder"], qunex_con_image, args["id"], args["raw_data"]
    )
    import_data_output = run_cmd(data_importing)
    parse_output(import_data_output["stdout"], args["study_folder"])
    session_id = (
        re.sub("sub-", "", args["id"]) if not args["session_id"] else args["session_id"]
    )
    ses_info = create_session_info(
        args["study_folder"], qunex_con_image, args["id"], args["session_id"]
    )
    run_cmd(ses_info, no_return=True)
    if args["batch"]:
        batch_path = args["batch"]
    else:
        batch_path = os.path.join(
            os.path.dirname(Path(__file__).parent), "files", "hcp_batch.txt"
        )
    shutil.copy(
        batch_path,
        args["study_folder"],
    )
    batch = create_batch(
        args["study_folder"],
        qunex_con_image,
        args["id"],
        session_id,
        os.path.join(args["study_folder"], "hcp_batch.txt"),
    )
    run_cmd(batch, no_return=True)
    hcp_setup = set_up_hcp(
        args["study_folder"], qunex_con_image, args["id"], session_id, args["raw_data"]
    )
    run_cmd(hcp_setup, no_return=True)
    os.remove(os.path.join(args["study_folder"], "hcp_batch.txt"))
    os.remove(os.path.join(args["study_folder"], "hcp_mapping_file.txt"))
    print(f"Finished setting up directory: {args['id']}")
