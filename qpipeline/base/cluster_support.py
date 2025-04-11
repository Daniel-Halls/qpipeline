import re
import time
import threading
import os
from qpipeline.base.utils import error_and_exit, run_cmd


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


class Queue_Monitoring:
    """
    Class to Monitor cluster queue
    for jobs completion.

    Usage
    ----
    queue = Queue_Monitoring()
    queue.monitor(list_of_job_ids)
    """

    def __init__(self) -> None:
        self.__spinner_running = True
        print("Waiting for job to finish")

    def monitor(self, job_id: list) -> None:
        """
        Main method to monitor queue.

        Parameters
        ----------
        job_id: list
            list of job_ids

        Returns
        -------
        None
        """

        self.__spinner_running = True
        spinner_thread = threading.Thread(target=self.__spinner, daemon=True)
        spinner_thread.start()

        try:
            completed_jobs = []
            time.sleep(100)
            while True:
                for job in job_id:
                    if job not in completed_jobs:
                        running = self.__check_job(job)
                        if not running:
                            completed_jobs.append(job)

                    if len(completed_jobs) == len(job_id):
                        print("All jobs have finihsed")
                        break
                    time.sleep(300)

        except KeyboardInterrupt:
            exit(0)
        finally:
            self.__spinner_running = False
            spinner_thread.join()

    def __spinner(self) -> None:
        """
        Method to run spinner bar
        while monitoring the queue.
        """
        hash_line = ""
        max_hashes = 50
        adding_hash = True

        while self.__spinner_running:
            if adding_hash:
                hash_line += "#"
                if len(hash_line) >= max_hashes:
                    adding_hash = False
            else:
                hash_line = hash_line[:-1]
                if len(hash_line) == 0:
                    adding_hash = True

            print(
                f"\033[1B\r{hash_line.ljust(max_hashes)}\033[1A",
                end="",
            )
            time.sleep(0.1)

    def __check_job(self, job_id: str) -> bool:
        """
        Method to check job progress.

        Parameters
        ----------
        job_id: str
            job ID of fsl sub job

        Returns
        -------
        bool: boolean
            True if job is still running
            or False if completed.
        """
        output = run_cmd(
            [os.path.join(os.environ["FSLDIR"], "bin", "fsl_sub_report"), job_id]
        )
        if "Finished" in output["stdout"]:
            return False
        if "Failed" in output["stdout"]:
            print(f"JOB {job_id} FAILED. CHECK LOGS")
            return False
        return True


def wait_for_me(command_output: str) -> None:
    """
    Monitor the cluster for job status.

    Parameters
    ----------
    command_output: str
        output of qunex cmd

    Returns
    -------
    None

    """
    job_id = get_job_id(command_output)
    queue = Queue_Monitoring()
    queue.monitor([job_id])
