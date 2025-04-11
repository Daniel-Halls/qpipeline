import re
from qpipeline.base.utils import error_and_exit


def get_job_id(input_str) -> str:
    """
    Function to get job id

    Parameters
    ----------
    input_str: str
        str with job id in it

    Returns
    -------
    job_id: str
        str of job id
    """
    job_number = re.findall(r"Submitted batch job (\d+)", input_str)
    if not job_number:
        error_and_exit(
            False,
            "Unable to find job ID. Job maybe still running but pipeline will exit",
        )
    return job_number[0]
