from qpipeline.base.utils import container_path, run_cmd


def diffusion_cmd(
    study_folder: str, sub_id: str, qunex_con_image: str, queue: str
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
        Cluster queue.

    """

    cmd = f"""qunex_container hcp_diffusion \\
      --bind={study_folder}:{study_folder} \\
      --sessionsfolder={study_folder}/{sub_id}/sessions \\
      --batchfile={study_folder}/{sub_id}/processing/batch.txt \\
      --container={qunex_con_image} \\
      --overwrite=yes"""
    if queue:
        cmd += f""" \\
      --bash_pre="module load qunex-img/0.100.0;module load cuda-img/9.1" \\
      --scheduler="SLURM,time=24:00:00,ntasks=1,cpus-per-task=1,mem-per-cpu=50000,partition={queue},qos=img,gres=gpu:1,jobname=diffusion_{sub_id}" """

    return cmd


def run_diffusion(args: dict) -> None:
    print(f"Running Diffusion pipeline on: {args['id']}")
    qunex_con_image = container_path()
    diff_cmd = diffusion_cmd(
        study_folder=args["study_folder"],
        sub_id=args["id"],
        qunex_con_image=qunex_con_image,
        queue=args.get("queue", ""),
    )
    run_cmd(diff_cmd, no_return=True)
    if args["queue"]:
        print(f"Submitted to {args['queue']}")
