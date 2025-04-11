from qpipeline.base.utils import container_path, run_cmd

from qpipeline.base.utils import container_path, run_cmd


def prefreesurfer(args: dict, stage: str = "pre_freesurfer") -> dict:
    """
    Generalized function to run QuNex HCP pre_freesurfer or freesurfer.

    Parameters
    ----------
    args: dict
        Dictionary of command arguments (study_folder, id, queue, is_flair).
    stage: str
        Either 'pre_freesurfer' or 'freesurfer'.

    Returns
    -------
    dict
        Output from run_cmd.
    """
    print(f"Running {stage.replace('_', ' ').title()} on: {args['id']}")
    qunex_con_image = container_path()

    cmd = build_freesurfer_cmd(
        study_folder=args["study_folder"],
        sub_id=args["id"],
        qunex_con_image=qunex_con_image,
        queue=args.get("queue", ""),
        stage=stage,
        is_flair=args.get("is_flair", False),
    )

    return run_cmd([cmd])


def build_freesurfer_cmd(
    study_folder: str,
    sub_id: str,
    qunex_con_image: str,
    queue: str,
    stage: str,
    is_flair: bool = False,
) -> str:
    """
    Builds the QuNex container command for pre_freesurfer or freesurfer.

    Parameters
    ----------
    study_folder: str
        Path to study folder.
    sub_id: str
        Subject ID.
    qunex_con_image: str
        Container path.
    queue: str
        Cluster queue.
    stage: str
        Either 'pre_freesurfer' or 'freesurfer'.
    is_flair: bool
        If True and stage is 'freesurfer', add the --hcp_fs_flair flag.

    Returns
    -------
    str
        Full QuNex command.
    """
    cmd = f"""qunex_container hcp_{stage} \\
      --bind={study_folder}:{study_folder} \\
      --sessionsfolder={study_folder}/{sub_id}/sessions \\
      --batchfile={study_folder}/{sub_id}/processing/batch.txt \\
      --container={qunex_con_image} \\
      --overwrite=yes"""

    if stage == "freesurfer" and is_flair:
        cmd += " \\\n      --hcp_fs_flair=TRUE"

    if queue:
        cmd += f""" \\
      --bash_pre="module load qunex-img/0.100.0;module load cuda-img/9.1" \\
      --scheduler="SLURM,time=24:00:00,ntasks=1,cpus-per-task=1,mem-per-cpu=50000,partition={queue},qos=img,gres=gpu:1,jobname=qc-{stage}_{sub_id}" """

    return [cmd]

def prefreesurfer(args: dict) -> dict:
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
    print(f"Runing PreFreesurfer on: {args['id']}")
    qunex_con_image = container_path()
    prefreesurfer_command = pre_freesurfer(
        args["study_folder"], args["id"], qunex_con_image, args["queue"]
    )
    return run_cmd(prefreesurfer_command)


def pre_freesurfer(
    study_folder: str, sub_id: str, qunex_con_image: str, queue: str
) -> None:
    """
    qunex prefreesurfer command

    Parameters
    ----------
    study_folder: str
        path to study folder
    sub_id: str
        path to
    qunex_con_image: str
        path to qunex container
        image
    queue: str
        which cluster queue to submit to

    Returns
    -------
    None
    """

    prefreesurfer_cmd = f"""qunex_container hcp_pre_freesurfer \\
      --bind={study_folder}:{study_folder} \\
      --sessionsfolder={study_folder}/{sub_id}/sessions \\
      --batchfile={study_folder}/{sub_id}/processing/batch.txt \\
      --container={qunex_con_image} \\
      --overwrite=yes"""
    
    if queue:
        prefreesurfer_cmd = (
            prefreesurfer_cmd
            + f""" \\
            --bash_pre="module load qunex-img/0.100.0;module load cuda-img/9.1" \\
            --scheduler="SLURM,time=24:00:00,ntasks=1,cpus-per-task=1,mem-per-cpu=50000,partition={queue},qos=img,gres=gpu:1,jobname=qc-pre_freesurfer_{sub_id}" """
        )
    return [prefreesurfer_cmd]

def freesurfer(
    study_folder: str, sub_id: str, qunex_con_image: str, queue: str, is_flair: bool
) -> None:
    """
    qunex freesurfer command

    Parameters
    ----------
    study_folder: str
        path to study folder
    sub_id: str
        path to
    qunex_con_image: str
        path to qunex container
        image
    queue: str
        which cluster queue to submit to
    is_flair: bool
        is T2 a flair image
    Returns
    -------
    None
    """

    freesurfer_cmd = f"""qunex_container hcp_freesurfer \\
      --bind={study_folder}:{study_folder} \\
      --sessionsfolder={study_folder}/{sub_id}/sessions \\
      --batchfile={study_folder}/{sub_id}/processing/batch.txt \\
      --container={qunex_con_image} \\
      --overwrite=no"""
    ]
    if is_flair:
        """ \\
        --hcp_fs_flair=TRUE"""
    
    if queue:
        freesurfer_cmd = (
            freesurfer_cmd
            + f""" \\
            --bash_pre="module load qunex-img/0.100.0;module load cuda-img/9.1" \\
            --scheduler="SLURM,time=24:00:00,ntasks=1,cpus-per-task=1,mem-per-cpu=50000,partition={queue},qos=img,gres=gpu:1,jobname=qc-pre_freesurfer_{sub_id}" """
        )
    return [freesurfer_cmd]