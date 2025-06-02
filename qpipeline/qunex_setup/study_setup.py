from qpipeline.base.utils import (
    run_cmd,
    write_to_file,
    container_path,
    has_qunex_run_sucessfully,
    error_and_exit,
    remove_folder,
)
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


def get_session_id(session_folder):
    """
    Function to get session
    id as qunex doesn't seem
    to allow custom ids when
    using bids......

    Parameters
    ----------
    session_folder: str
        string to session folder

    Returns
    -------
    session_id: str
        string of session id
    """
    qunex_stuff = ["archive", "specs", "QC", "inbox"]
    session_folder_content = os.listdir(session_folder)
    try:
        session_id = [
            sess_name
            for sess_name in session_folder_content
            if sess_name not in qunex_stuff
        ][0]
    except Exception:
        error_and_exit(
            False,
            f"Cannot find session name. Please check name in {session_folder} and update mapping files",
        )
    return session_id


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
    pattern = re.compile(
        r"---> linked (\d+\.nii\.gz) <-- sub-[^_]+_(?:ses-[^_]+_)?(.*)\.nii\.gz"
    )
    mapped_files = {}
    file_mapping = map_files()
    for match in pattern.finditer(output):
        number = match.group(1).split(".")[0]
        label = match.group(2)
        mapped_files[number] = map_scans(file_mapping, label)
    result = [f"{num} => {label}\n" for num, label in mapped_files.items()]
    write_to_file(study_path, "hcp_mapping_file.txt", result, text_is_list=True)


def batch_file(data_type: str, study_path: str, customse_batch: str = None) -> None:
    """
    Function to process batch file

    Parameters
    ----------
    data_type: str
        str of datatype the input
    study_path: str
        str of path to study path
    customse_batch: str
        str of custom batch.
        Default is None

    Returns
    -------
    None
    """
    if customse_batch:
        batch_path = customse_batch
    else:
        batch_path = os.path.join(
            os.path.dirname(Path(__file__).parent),
            "files",
            f"{data_type.lower()}_data_batch.txt",
        )
    shutil.copy(batch_path, os.path.join(study_path, "hcp_batch.txt"))


def datatype_checker(data_type: str, customse_batch: str = None) -> str:
    """
    Function to check what type of
    batch file to use.

    Parameters
    ----------
    data_type: str
        str of datatype the input
        data is
    customse_batch: str
        str of custom batch.
        Default is None

    Returns
    -------
    str: string object
        str of data type to process

    """
    if customse_batch:
        return "Custom"
    if data_type:
        return data_type.lower()
    return None


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
    datatype = datatype_checker(args["data_type"], args["batch"])
    error_and_exit(datatype, "Unable to work out how to process batch file")
    print(f"Setting up Subject: {args['id']}")
    print(f"Data type: {datatype}")
    qunex_con_image = container_path()
    subjects_folder = os.path.join(args["study_folder"], args["id"])
    remove_folder(subjects_folder)
    study_create = create_study(args["study_folder"], qunex_con_image, args["id"])
    run_cmd(study_create, no_return=True)
    has_qunex_run_sucessfully(subjects_folder, "create_study", setup_check=True)
    data_importing = import_data(
        args["study_folder"],
        qunex_con_image,
        args["id"],
        args["raw_data"],
    )

    import_data_output = run_cmd(data_importing)
    has_qunex_run_sucessfully(subjects_folder, "import_bids", setup_check=True)
    parse_output(import_data_output["stdout"], args["study_folder"])
    session_id = get_session_id(os.path.join(subjects_folder, "sessions"))
    ses_info = create_session_info(
        args["study_folder"], qunex_con_image, args["id"], session_id
    )
    run_cmd(ses_info, no_return=True)
    has_qunex_run_sucessfully(subjects_folder, "create_session_info", setup_check=True)
    batch_file(datatype, args["study_folder"], args["batch"])
    batch = create_batch(
        args["study_folder"],
        qunex_con_image,
        args["id"],
        session_id,
        os.path.join(args["study_folder"], "hcp_batch.txt"),
    )
    run_cmd(batch, no_return=True)
    has_qunex_run_sucessfully(subjects_folder, "create_batch", setup_check=True)
    hcp_setup = set_up_hcp(
        args["study_folder"], qunex_con_image, args["id"], session_id, args["raw_data"]
    )
    run_cmd(hcp_setup, no_return=True)
    has_qunex_run_sucessfully(subjects_folder, "setup_hcp", setup_check=True)
    os.remove(os.path.join(args["study_folder"], "hcp_batch.txt"))
    os.remove(os.path.join(args["study_folder"], "hcp_mapping_file.txt"))
    print(f"Finished setting up directory: {args['id']}")
