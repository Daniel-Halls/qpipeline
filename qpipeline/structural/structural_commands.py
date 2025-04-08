def pre_freesurfer(study_folder: str, sub_id: str, qunex_con_image: str, queue: str):
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
    """
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
