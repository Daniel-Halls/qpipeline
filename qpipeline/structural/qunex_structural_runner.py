from qpipeline.base.utils import container_path, run_cmd


def run_structural(args: dict, stage: str) -> dict:
    """
    Run QuNex HCP structural pipeline.

    Parameters
    ----------
    args: dict
        Dictionary of command arguments
        (study_folder, id, queue, is_flair).
    stage: str
        Either 'pre_freesurfer', 'freesurfer'
        or 'post_freesurfer.

    Returns
    -------
    dict: run_cmd output
        Output from run_cmd.
    """
    print(f"Running: {stage.replace('_', '-').title()}", flush=True)
    qunex_con_image = container_path()
    cmd = build_structural_cmd(
        study_folder=args["study_folder"],
        qunex_con_image=qunex_con_image,
        queue=args.get("queue", ""),
        stage=stage,
        is_flair=args.get("is_flair", False),
    )
    return run_cmd([cmd])


def build_structural_cmd(
    study_folder: str,
    qunex_con_image: str,
    queue: str,
    stage: str,
    is_flair: bool = False,
) -> str:
    """
    Builds the QuNex structural command.

    Parameters
    ----------
    study_folder: str
        Path to study folder.
    qunex_con_image: str
        Container path.
    queue: str
        Cluster queue.
    stage: str
        Either 'pre_freesurfer' or 'freesurfer'.
    is_flair: bool
        If True and stage is 'freesurfer',
        add the --hcp_fs_flair flag.

    Returns
    -------
    str
        Full QuNex command.
    """
    cmd = f"""qunex_container hcp_{stage} \\
      --bind={study_folder}:{study_folder} \\
      --sessionsfolder={study_folder}/sessions \\
      --batchfile={study_folder}/processing/batch.txt \\
      --container={qunex_con_image} \\
      --overwrite=yes"""

    if stage == "freesurfer" and is_flair:
        cmd += " \\\n      --hcp_fs_flair=TRUE"

    if queue:
        cmd += f""" \\
      --bash_pre="module load qunex-img/0.100.0;module load cuda-img/9.1" \\
      --scheduler="SLURM,time=24:00:00,ntasks=1,cpus-per-task=1,mem-per-cpu=50000,partition={queue},qos=img,gres=gpu:1,jobname={stage}" """

    return cmd
