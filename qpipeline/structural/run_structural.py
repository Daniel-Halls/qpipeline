from qpipeline.structural.qunex_structural_runner import run_structural
from qpipeline.base.cluster_support import wait_for_me
from qpipeline.base.utils import has_qunex_run_sucessfully


def hcp_structual(args: dict) -> None:
    """
    Main function for the hcp structural
    pipeline

    Parameters
    ----------
    args: dict
        dictionary of arguments

    Returns
    -------
    None
    """
    prefreesurfer_output = run_structural(args, "pre_freesurfer")
    wait_for_me(prefreesurfer_output["stdout"])
    has_qunex_run_sucessfully(args["study_folder"], "pre_freesurfer")
    print("Pre freesurfer done")

    freesurfer_output = run_structural(args, "freesurfer")
    wait_for_me(freesurfer_output["stdout"])
    has_qunex_run_sucessfully(args["study_folder"], "freesurfer")
    print("Freesurfer done")

    postfreesurfer_output = run_structural(args, "post_freesurfer")
    wait_for_me(postfreesurfer_output["stdout"])
    has_qunex_run_sucessfully(args["study_folder"], "post_freesurfer")
    print("Post freesurfer done")
