import os
import subprocess


def load_module(module_name: str) -> None:
    """
    Function to load module
    and update the python path

    Parameters
    ----------
    module_name: str
        module name

    Returns
    -------
    None
    """
    module = get_module_paths(module_name)
    update_env(module.stdout.splitlines())


def get_module_paths(module_name) -> str:
    """
    Function to run the module
    and get the enviormental variables

    Parameters
    ----------
    module_name: str
        module name

    Returns
    -------
    None

    """
    return subprocess.run(
        ["bash", "-c", f"module load {module_name} && env"],
        capture_output=True,
        text=True,
    )


def update_env(output: str) -> None:
    """
    Function to update
    python enviormental variables
    for a given module.

    Parameters
    ----------
    output: str
        stdout of subprocess call
        with module

    Returns
    -------
    None
    """
    for line in output:
        key, _, value = line.partition("=")
        os.environ[key] = value


def set_environment():
    """
    Wrapper function to load
    qunex environment

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    load_module("extension/imaging")
    load_module("qunex-img/0.100.0")
