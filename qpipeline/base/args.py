import argparse


def qpipeline_modules():
    base = argparse.ArgumentParser(
        prog="qpipeline",
        description=print(splash()),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    base.add_subparsers(dest="command", required=True)
    return base


def qpipeline_args():
    base = qpipeline_modules()
    study_setup_args = base.add_subparsers("setup")
    hcp_setup_args(study_setup_args)


def hcp_setup_args(study_setup_args) -> dict:
    """
    Function to take

    Parameters
    ----------
    None

    Returns
    -------
    dict: dictionary
        dict of cmd args
    """
    study_setup_args.add_argument(
        "-s",
        "--study_folder",
        help="Path to study folder",
        dest="study_folder",
        required=True,
    )
    study_setup_args.add_argument(
        "-r",
        "--raw_data",
        help="Path to raw data",
        dest="raw_data",
        required=True,
    )
    study_setup_args.add_argument(
        "-i",
        "--id",
        help="Subject ID",
        dest="id",
        required=True,
    )
    study_setup_args.add_argument(
        "-q",
        "--queue",
        help="Queue name to submit to",
        dest="queue",
        required=True,
    )
    study_setup_args.add_argument(
        "-S",
        "--skip_study_setup",
        dest="skip_study_setup",
        help="Skip study set up",
        default=False,
        action="store_true",
    )

    return vars(study_setup_args.parse_args())


def splash() -> str:
    """
    Function to return Splash

    Parameters
    ---------
    None

    Returns
    -------
    str: string object
        splash string
    """
    return """
               .__                 .__   .__                 
  ____________  |__|______    ____  |  |  |__|  ____    ____  
 / ____/\____ \ |  |\____ \ _/ __ \ |  |  |  | /    \ _/ __ \ 
< <_|  ||  |_> >|  ||  |_> >\  ___/ |  |__|  ||   |  \\  ___/ 
 \__   ||   __/ |__||   __/  \___  >|____/|__||___|  / \___  >
    |__||__|        |__|         \/                \/      \/ 
    """
