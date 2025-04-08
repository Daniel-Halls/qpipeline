from qpipeline.base.utils import container_path, run_cmd
from qpipeline.structural.structural_commands import pre_freesurfer


def prefreesurfer(args: dict) -> None:
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
    print(f"Ruuning PreFreesurfer on: {args['id']}")
    qunex_con_image = container_path()
    prefreesurfer_command = pre_freesurfer(
        args["study_folder"], args["id"], qunex_con_image, args["queue"]
    )
    command = run_cmd(prefreesurfer_command)
    print(command)
