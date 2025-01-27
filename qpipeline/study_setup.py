import os
import shutil
from pathlib import Path
from .utils import run_cmd, write_to_file
from .qunex_commands import create_study, import_data, create_session_info, create_batch
import re


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
    write_to_file(study_path, ".hcp_mapping_file.txt", result, text_is_list=True)


def set_up_qunex_study(args: dict) -> None:
    """
    Function for main set up quenx study

    Parameters
    ----------
    args: dict
        dictionary of cmd args

    Returns
    -------
    None
    """
    qunex_con_image = os.environ["QUNEXCONIMAGE"].rstrip()
    study_create = create_study(args["study_folder"], qunex_con_image, args["id"])
    create_study_output = run_cmd(study_create)
    data_importing = import_data(
        args["study_folder"], qunex_con_image, args["id"], args["raw_data"]
    )
    import_data_output = run_cmd(data_importing)
    parse_output(import_data_output["stdout"], args["study_folder"])
    session_id = re.sub("sub-", "", args["id"])
    ses_info = create_session_info(
        args["study_folder"], qunex_con_image, args["id"], session_id
    )
    ses_info_output = run_cmd(ses_info)
    shutil.copy(
        os.path.join(Path(__file__).parent, "files", "hcp_batch.txt"),
        args["study_folder"],
    )
    batch = create_batch(
        args["study_folder"],
        qunex_con_image,
        args["id"],
        session_id,
        os.path.join(args["study_folder"], "hcp_batch.txt"),
    )
    batch_ouput = run_cmd(batch)
