import subprocess
import re
import os
import shutil


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
            error_message = re.sub(r"\[Errno 2\]", "", error_message)
            print("\033[1;31m" + error_message + "\033[0;0m")
        print("Exiting...\n")
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
