from qpipeline.base.utils import (
    run_cmd,
    write_to_file,
    container_path,
    has_qunex_run_sucessfully,
    error_and_exit,
    folder_creation,
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


def data_check(data_type: str, batch: str) -> str:
    """
    Function to check data to decide on
    which batch to use

    Parameters
    ----------
    data_type: str
        string of data type.
        Can be none, however
        then needs batch
    batch: str
        batch file path.
        Can be none, however
        then needs data_type

    Returns
    -------
    data_type: str
        str of data type
    """
    datatype = datatype_checker(data_type, batch)
    error_and_exit(datatype, "Unable to work out how to process batch file")
    return data_type


def study_create(
    study_folder: str,
    qunex_con_image: str,
) -> None:
    """
    Warpper function around create_study
    function

    Parameters
    -----------
    study_folder: str
        string to study folder
    qunex_con_image: str
        qunex conatiner image path

    Returns
    -------
    None
    """
    study_create = create_study(study_folder, qunex_con_image)
    run_cmd(study_create, no_return=True)
    has_qunex_run_sucessfully(study_folder, "create_study", setup_check=True)


def data_importing(
    study_folder: str,
    qunex_con_image: str,
    raw_data: str,
) -> None:
    """
    Warpper function around

    Parameters
    -----------
    study_folder: str
        string to study folder
    qunex_con_image: str
        qunex conatiner image path
    raw_data: str
        path to raw data

    Returns
    -------
    None
    """

    data_importing = import_data(
        study_folder,
        qunex_con_image,
        raw_data,
    )

    import_data_output = run_cmd(data_importing)
    has_qunex_run_sucessfully(study_folder, "import_bids", setup_check=True)
    parse_output(import_data_output["stdout"], study_folder)


def create_session(study_folder: str, qunex_con_image: str) -> str:
    """
    Warpper function around create_session
    function

    Parameters
    -----------
    study_folder: str
        string to study folder
    qunex_con_image: str
        qunex conatiner image path
    id: str
        sub id

    Returns
    -------
    session_id: str
        session id for
        created session
    """
    ses_info = create_session_info(study_folder, qunex_con_image)
    run_cmd(ses_info, no_return=True)
    has_qunex_run_sucessfully(study_folder, "create_session_info", setup_check=True)


def process_batch(
    datatype: str,
    study_folder: str,
    batch_input: str,
    qunex_con_image: str,
) -> None:
    """
    Warpper function around create_batch
    function

    Parameters
    -----------
    datatype: str
        str of data type
    study_folder: str
        string to study folder
    batch_input: str
        str of custom batch, can be None.
    qunex_con_image: str
        qunex conatiner image path

    Returns
    -------
    None
    """

    batch_file(datatype, study_folder, batch_input)

    batch = create_batch(
        study_folder,
        qunex_con_image,
        os.path.join(study_folder, "hcp_batch.txt"),
    )
    run_cmd(batch, no_return=True)
    has_qunex_run_sucessfully(study_folder, "create_batch", setup_check=True)


def hcp_data_setup(study_folder: str, qunex_con_image: str, raw_data: str) -> None:
    """
    Warpper function around create_batch
    function

    Parameters
    -----------
    study_folder: str
        string to study folder
    qunex_con_image: str
        qunex conatiner image path
    raw_data: str
        path to raw data

    Returns
    -------
    None
    """
    hcp_setup = set_up_hcp(study_folder, qunex_con_image, raw_data)
    run_cmd(hcp_setup, no_return=True)
    has_qunex_run_sucessfully(study_folder, "setup_hcp", setup_check=True)


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
    datatype = data_check(args["data_type"], args["batch"])
    print("Setting up Subjects")
    print(f"Data type: {datatype}")
    print(f"Overwriting {args['study_folder']}") if args["overwrite"] else None
    qunex_con_image = container_path()
    folder_creation(args["study_folder"], args["overwrite"])
    study_create(args["study_folder"], qunex_con_image)
    data_importing(args["study_folder"], qunex_con_image, args["raw_data"])

    create_session(args["study_folder"], qunex_con_image)

    process_batch(
        datatype,
        args["study_folder"],
        args["batch"],
        qunex_con_image,
    )

    hcp_data_setup(args["study_folder"], qunex_con_image, args["raw_data"])
    os.remove(os.path.join(args["study_folder"], "hcp_batch.txt"))
    os.remove(os.path.join(args["study_folder"], "hcp_mapping_file.txt"))
    print("Finished setting up")
