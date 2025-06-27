import subprocess
import re
import os
import shutil
import glob
from qpipeline.base.signit import kill_group


def annoying_error_str() -> str:
    """
    Function to return annoying error string
    so it can be removed.

    Parameters
    ----------
    None

    Returns
    -------
    error_str: str
        str of error
    """
    return """
    /bin/sh: which: line 1: syntax error: unexpected end of file
    /bin/sh: error importing function definition for `which'
    /bin/sh: module: line 1: syntax error: unexpected end of file
    /bin/sh: error importing function definition for `module'
    /bin/sh: ml: line 1: syntax error: unexpected end of file
    /bin/sh: error importing function definition for `ml'
    
    """


def error_and_exit(
    bool_statement: bool,
    error_message: str = None,
) -> None:
    """
    Function to exit out of script
    with error message if bool statement
    is false.

    Parameters
    ----------
    bool_statement: bool
       statement to evaluate
    error_message: str
        error message to print
        out. Default is None

    Returns
    -------
    None
    """
    if not bool_statement:
        if error_message:
            anoying_str = annoying_error_str()
            error_message = re.sub(r"\[Errno 2\]", "", error_message)
            error_message = re.sub(anoying_str, "", error_message)
            print("\033[1;31m" + error_message + "\033[0;0m")
        print("Exiting...\n")
        kill_group()
        exit(1)


def run_cmd(command: list, no_return: bool = False) -> dict:
    """
    Function to run cmd command.

    Parameters
    ----------
    command: list
        command to run

    Returns
    -------
    output: dict
        dict of output from subprocess
        command
    """
    try:
        qpipe_env = os.environ.copy()
        run = subprocess.run(command, capture_output=True, shell=True, env=qpipe_env)
    except subprocess.CalledProcessError as error:
        error_and_exit(False, f"Error in calling commnd due to: {error}")
    except KeyboardInterrupt:
        run.kill()

    output = {
        key: value.decode("utf-8").strip() if isinstance(value, bytes) else value
        for key, value in vars(run).items()
    }
    if output["returncode"] != 0:
        error_and_exit(False, f"Error in calling commnd due to: {output['stderr']}")
    if no_return:
        return None
    return output


def write_to_file(
    file_path: str, name: str, text: str, text_is_list: bool = False
) -> bool:
    """
    Function to write to file.

    Parameters
    ----------
    file_path: str
        abosulte file path to
        where file is created
    name: str
        name of file
    text: str
        string to add to file
    text_is_list: bool
        if text is actually a
        list then will write to file

    Returns
    -------
    bool: boolean
        True if sucessful else
        False
    """
    try:
        with open(f"{file_path}/{name}", "w") as file:
            if text_is_list:
                file.writelines(text)
            if not text_is_list:
                file.write(text)
    except Exception as e:
        print(f"Unable to write to {file_path}/{name} due to :", e)
        return False
    return True


def container_path() -> str:
    """
    Function to get container path

    Parameters
    ----------
    None

    Returns
    -------
    str: path
       path to qunex container
    """
    return os.environ["QUNEXCONIMAGE"].rstrip()


def make_directory(
    path: str, overwrite: bool = False, ignore_errors: bool = False
) -> None:
    """
    Function to make a directory.
    If error it will exit

    Parameters
    ----------
    path: str
        string to directory path
    overwrite: bool
        overwrite any previous directories

    Returns
    -------
    None
    """

    try:
        if os.path.exists(path) and overwrite:
            shutil.rmtree(path, ignore_errors=True)
        os.mkdir(path)
    except Exception as e:
        if ignore_errors:
            return None
        error_and_exit(False, f"Unable to create directory due to {e}")


def copy_files(srcfile: str, dest: str) -> None:
    """
    Fucntion to copy a file.
    Will exit if error

    Parameters
    ----------
    srcfile: str
        file path to copy
    dest: str
        destination path

    Returns
    -------
    None
    """
    try:
        shutil.copy2(srcfile, dest)
    except Exception as e:
        error_and_exit(False, f"Unable to copy {srcfile} to {dest} due to {e}")


def delete_files_in_dir(path: str) -> None:
    """
    Function to delete all files in
    a directory

    Parameters
    ----------
    path: str
        string of path

    Returns
    ------
    None
    """
    try:
        for files in os.listdir(path):
            os.remove(files)
    except Exception as e:
        error_and_exit(f"Unable to delete files in {path} due to {e}")


def check_logs(
    logs_directory: str, command_ran: str, setup_check: bool = False
) -> list:
    """
    Function to check log files fpr
    completed files.

    Parameters
    ----------
    logs_directory: str
        directory of the log files
    command_ran: str
        str of command run
    setup_check: bool
        is the cmd that was run
        a setup cmd.

    Returns
    -------
    list: list object
        list of log files
        that have been completed
    """
    log_name = f"done_hcp_{command_ran}" if not setup_check else f"done_{command_ran}"
    return glob.glob(os.path.join(logs_directory, f"{log_name}*"))


def check_progress(sub_dir: str, command_ran: str) -> bool:
    """
    Function to check progress.
    Checks if a cmd had already been ran
    and if completed correctly.

    Parameters
    -----------
    sub_dir: str
        path to qunex sub directory
    command_ran: str
        str of command run

    Returns
    -------
    bool: boolean
        true if has been sucessfully
        completed
    """
    logs_directory = os.path.join(sub_dir, "processing", "logs", "comlogs")
    done = check_logs(logs_directory, command_ran)
    return True if done else False


def has_qunex_run_sucessfully(
    qunex_dir: str, command_ran: str, setup_check: bool = False
) -> None:
    """
    Function to check qunex log files
    to check that a given command has run sucesfully

    Parameters
    ----------
    sub_dir: str
        path to qunex sub directory
    command_ran: str
        what command to check for

    Returns
    -------
    None
    """
    logs_directory = os.path.join(qunex_dir, "processing", "logs", "comlogs")
    log_file = check_logs(logs_directory, command_ran, setup_check)
    if not log_file:
        error_and_exit(
            False,
            f"Qunex {command_ran} not run sucessfully. Please check log files at {logs_directory}",
        )


def folder_creation(folder_path: str, overwrite=False) -> None:
    """
    Function to remove folder

    Parameters
    ----------
    folder_path: str
        path to folder

    Returns
    -------
    None
    """
    if os.path.exists(folder_path) and overwrite:
        shutil.rmtree(folder_path)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
