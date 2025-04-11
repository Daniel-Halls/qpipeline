from qpipeline.structural.prefreesurfer.run_prefreesurfer import prefreesurfer
from qpipeline.base.cluster_support import wait_for_me
from qpipeline.base.utils import has_qunex_run_sucessfully


def hcp_structual(args):
    prefreesurfer_output = prefreesurfer(args)
    print(prefreesurfer_output)
    wait_for_me(prefreesurfer_output["stdout"])
    has_qunex_run_sucessfully(args["study_folder"], "pre_freesurfer")
    print("Prefreesurfer done")
