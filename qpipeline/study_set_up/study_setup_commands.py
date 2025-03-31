def create_study(study_folder: str, qunex_con_image: str, sub_id: str) -> list:
    """
    Function for the qunex create study command

    Parameteres
    -----------
    study_folder: str
        study folder path
    qunex_con_image: str
        qunex container path
    sub_id: str
        subject id

    Returns
    -------
    list: list object
        list of command
    """

    return [
        f"""qunex_container create_study \\
        --studyfolder={study_folder}/{sub_id}\\
        --bind={study_folder}:{study_folder}\\
        --container={qunex_con_image}
        """
    ]


def import_data(
    study_folder: str, qunex_con_image: str, sub_id: str, raw_data: str
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
    --sessionsfolder={study_folder}/{sub_id}/sessions \\
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
    sub_id: str,
    session_id: str,
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
    --sessionsfolder={study_folder}/{sub_id}/sessions \\
    --sessions={session_id} \\
    --bind={study_folder}:{study_folder} \\
    --mapping={study_folder}/hcp_mapping_file.txt \\
    --container={qunex_con_image}
    """
    ]


def create_batch(
    study_folder: str,
    qunex_con_image: str,
    sub_id: str,
    session_id: str,
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
    sub_id: str
        subject id
    session_id: str
        session id
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
    --sessionsfolder={study_folder}/{sub_id}/sessions \\
    --targetfile={study_folder}/{sub_id}/processing/batch.txt \\
    --paramfile={path_to_batch} \\
    --sessions={session_id} \\
    --overwrite=yes \\
    --sourcefiles={study_folder}/{sub_id}/sessions/{session_id}/session_hcp.txt \\
    --container={qunex_con_image}
    """
    ]


def set_up_hcp(
    study_folder: str,
    qunex_con_image: str,
    sub_id: str,
    session_id: str,
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
    --sessionsfolder={study_folder}/{sub_id}/sessions \\
    --sessions={session_id} \\
    --sourcefolder={study_folder}/{sub_id}/sessions/{session_id} \\
    --sourcefile={study_folder}/{sub_id}/sessions/{session_id}/session_hcp.txt \\
    --existing=add \\
    --hcp_folderstructure=hcpls \\
    --container={qunex_con_image}
    """
    ]


def pre_freesurfer(study_folder, sub_id, qunex_con_image, queue):
    return [
        f"""qunex_container hcp_pre_freesurfer \\
      --bind={study_folder}:{study_folder} \\
      --sessionsfolder={study_folder}/{sub_id}/sessions \\
      --batchfile={study_folder}/{sub_id}/processing/batch.txt \\
      --container={qunex_con_image} \\
      --overwrite=yes \\
      --bash_pre="module load qunex-img/0.100.0;module load cuda-img/9.1 \\
      --scheduler="SLURM,time=24:00:00,ntasks=1,cpus-per-task=1,mem-per-cpu=50000,partition={queue},qos=img,gres=gpu:1,jobname=qc-pre_freesurfer_{sub_id}"
      """
    ]
