from qpipeline.base.utils import container_path, run_cmd


def diffusion_cmd(
    study_folder: str, sub_id: str, qunex_con_image: str, queue: str, no_gpu: bool
) -> str:
    """
    Diffusion qunex cmd

    Parameters
    ----------
    study_folder: str
        Path to study folder.
    sub_id: str
        Subject ID.
    qunex_con_image: str
        Container path.
    queue: str
        Cluster queue
    no_gpu: bool
        Don't use gpu

    Returns
    -------
    cmd: str
        str of cmd
    """

    cmd = f"""qunex_container hcp_diffusion \\
      --bind={study_folder}:{study_folder} \\
      --sessionsfolder={study_folder}/{sub_id}/sessions \\
      --batchfile={study_folder}/{sub_id}/processing/batch.txt \\
      --container={qunex_con_image} \\
      --overwrite=yes"""
    if no_gpu:
        cmd += " \\\n      --hcp_dwi_nogpu"
    if queue:
        cmd += f""" \\
      --bash_pre="module load qunex-img/0.100.0;module load cuda-img/9.1" \\
      --scheduler="SLURM,time=24:00:00,ntasks=1,cpus-per-task=1,mem-per-cpu=50000,partition={queue},qos=img,gres=gpu:1,jobname=diffusion_{sub_id}" """

    return cmd


def hcp_diffusion(args: dict) -> None:
    """
    Main function to run diffusion pipeline

    Parameters
    ----------
    args: dict
        cmd line args

    Returns
    -------
    None
    """
    print(f"Running Diffusion pipeline on: {args['id']}")
    qunex_con_image = container_path()
    diff_cmd = diffusion_cmd(
        study_folder=args["study_folder"],
        sub_id=args["id"],
        qunex_con_image=qunex_con_image,
        queue=args.get("queue", ""),
        no_gpu=args["no_gpu"],
    )
    run_cmd(diff_cmd, no_return=True)
    if args["queue"]:
        print(f"Submitted to {args['queue']}")
