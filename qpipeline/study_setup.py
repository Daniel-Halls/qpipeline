import os


def study_create(study_folder: str, qunex_con_image: str, sub_id: str) -> str:
    return f"""
qunex_container create_study \
--studyfolder="{study_folder}/{sub_id}" \
--bind="{study_folder}:{study_folder}" \
--container="{qunex_con_image}" 
"""


def set_up_qunex_study(args):
    qunex_con_image = os.environ["QUNEXCONIMAGE"]
    create_study = study_create(args["study_folder"], qunex_con_image, args["id"])
    print(create_study)
    # run_cmd()
