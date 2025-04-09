from qpipeline.base.utils import make_directory, run_cmd, error_and_exit
from qpipeline.base.setup import load_module
import os


def file_paths(study_folder: str, sub_id: str) -> dict:
    subject_folder = os.path.join(
        study_folder, sub_id, "sessions", sub_id, "hcp", sub_id
    )

    return {
        "subject_folder": subject_folder,
        "MNINonLinear": os.path.join(subject_folder, "MNINonLinear"),
        "T1w": os.path.join(subject_folder, "T1w"),
        "T2w": os.path.join(subject_folder, "T2w"),
        "qpipeline": os.path.join(subject_folder, ".qpipeline"),
    }


def abletorun(T2path):
    if "T2wToT1wDistortionCorrectAndReg" not in os.listdir(T2path):
        error_and_exit(False, "Unable to continue with FLAIR pipeline as")


def flair_pipeline(args):
    load_module("freesurfer-img/7.4.1")
    paths = file_paths(args["study_folder"], args["id"])
    abletorun(paths["T2w"])
    make_directory(paths["qpipeline"])
    run_cmd(
        [
            "mri_synthstrip",
            "-i",
            os.path.join(paths["T2w"], "T2w_acpc_brain.nii.gz"),
            "-o",
            os.path.join(paths["qpipeline"], "T2w_acpc_brain.nii.gz"),
        ],
        no_return=True,
    )
    run_cmd(
        [
            "mri_synthstrip",
            "-i",
            os.path.join(paths["T1w"], "T1w_acpc_brain.nii.gz"),
            "-o",
            os.path.join(paths["qpipeline"], "T1w_acpc_brain.nii.gz"),
        ],
        no_return=True,
    )
