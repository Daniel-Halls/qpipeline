def create_study(study_folder: str, qunex_con_image: str) -> list:
    """
    Function for the qunex create study command

    Parameteres
    -----------
    study_folder: str
        study folder path
    qunex_con_image: str
        qunex container path


    Returns
    -------
    list: list object
        list of command
    """

    return [
        f"""qunex_container create_study \\
        --studyfolder={study_folder}\\
        --bind={study_folder}:{study_folder}\\
        --container={qunex_con_image}
        """
    ]


def import_data(
    study_folder: str,
    qunex_con_image: str,
    raw_data: str,
) -> list:
    """
    Function for the qunex import bids command

    Parameteres
    -----------
    study_folder: str
        study folder path
    qunex_con_image: str
        qunex container path
    sub_id: str
        subject id
    raw_data: str
        path to raw data

    Returns
    -------
    list: list object
        list of command
    """

    return [
        f"""qunex_container import_bids \\
    --sessionsfolder={study_folder}/sessions \\
    --inbox={raw_data} \\
    --action=copy \\
    --archive=leave \\
    --overwrite=no \\
    --bind={study_folder}:{study_folder},{raw_data}:{raw_data} \\
    --container={qunex_con_image}
    """
    ]


def create_session_info(
    study_folder: str,
    qunex_con_image: str,
) -> list:
    """
    Function for the qunex import bids command

    Parameteres
    -----------
    study_folder: str
        study folder path
    qunex_con_image: str
        qunex container path
    sub_id: str
        subject id
    session_id: str
        session id

    Returns
    -------
    list: list object
        list of command
    """

    return [
        f"""qunex_container create_session_info \\
    --sessionsfolder={study_folder}/sessions \\
    --bind={study_folder}:{study_folder} \\
    --mapping={study_folder}/hcp_mapping_file.txt \\
    --container={qunex_con_image}
    """
    ]


def create_batch(
    study_folder: str,
    qunex_con_image: str,
    path_to_batch: str,
) -> list:
    """
    Function for the qunex import bids command

    Parameteres
    -----------
    study_folder: str
        study folder path
    qunex_con_image: str
        qunex container path
    path_to_batch: str
        path to batch file

    Returns
    -------
    list: list object
        list of command
    """

    return [
        f"""qunex_container create_batch \\
    --bind={study_folder}:{study_folder} \\
    --sessionsfolder={study_folder}/sessions \\
    --targetfile={study_folder}/processing/batch.txt \\
    --paramfile={path_to_batch} \\
    --overwrite=yes \\
    --container={qunex_con_image}
    """
    ]


def set_up_hcp(
    study_folder: str,
    qunex_con_image: str,
    raw_data: str,
) -> list:
    """
    Function for the qunex import bids command

    Parameteres
    -----------
    study_folder: str
        study folder path
    qunex_con_image: str
        qunex container path
    sub_id: str
        subject id
    session_id: str
        session id
    raw_data: str
        path to raw data

    Returns
    -------
    list: list object
        list of command
    """

    return [
        f"""qunex_container setup_hcp \\
    --bind={study_folder}:{study_folder},{raw_data}:{raw_data} \\
    --sessionsfolder={study_folder}/sessions \\
    --batchfile={study_folder}/processing/batch.txt \\
    --container={qunex_con_image}
    """
    ]
