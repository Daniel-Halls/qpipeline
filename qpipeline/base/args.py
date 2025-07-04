import argparse
import sys
from qpipeline.base.check_inputs import valid_data_types


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
    return f"""
               .__                 .__   .__                 
  ____________  |__|______    ____  |  |  |__|  ____    ____  
 / ____/\____ \ |  |\____ \ _/ __ \ |  |  |  | /    \ _/ __ \ 
< <_|  ||  |_> >|  ||  |_> >\  ___/ |  |__|  ||   |  \\\\  ___/ 
 \__   ||   __/ |__||   __/  \___  >|____/|__||___|  / \___  >
    |__||__|        |__|         \/                \/      \/ 
{"-" * 75}    
    """


def valid_options() -> list:
    """
    Function to return all the valid
    options avaible

    Parameters
    ----------
    None

    Returns
    -------
    list: list object
        list of valid option
    """
    return ["setup", "structural", "diffusion"]


def usage_message() -> None:
    """
    Function to print a basic
    usage message and exit

    Parameters
    ----------
    None

    Returns
    -------
    str: string
        string of usage message
    """
    print(f"""
    {splash()}
qpipeline is a set of warpper scripts around
qunex/hcp pipelines to make it easier to use.

It consists of the following subcommands:
    - setup (qunex folder HCP set up)
    - strucutral (pre-freesurfer, freesurfer, post-freesurfer)
    - diffusion (HCP diffusion pipeline)

run qpipeline sub_command --help for further info
    """)
    exit(0)


def invalid_options(option: str, avaiable_options: list) -> None:
    """
    Function to print and exit
    after an invalid option
    was given

    Parameters
    ----------
    option: str
        str of option given
    avaiable_options: list
        list of avaiable options

    Returns
    -------
    None
    """
    print(splash())
    print(f"{option} is an invalid option")
    print("Please specify from", *avaiable_options)
    print("or run --help")
    exit(1)


def check_subcommand() -> None:
    """
    Function to check the subcommand
    given to pipeline.

    Parameters
    -----------
    None

    Returns
    -------
    None
    """

    avaiable_options = valid_options()
    if len(sys.argv) <= 1 or sys.argv[1] in ["-h", "--help"]:
        usage_message()
    if sys.argv[1] not in avaiable_options:
        invalid_options(sys.argv[1], avaiable_options)


def qpipeline_modules() -> object:
    """
    Function to set up
    base parser and add subparsers

    Parameters
    ----------
    None

    Returns
    -------
    object: ArgumentParser
        argparser object
    """

    base_parser = argparse.ArgumentParser(
        prog="qpipeline",
        description=print(splash()),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = base_parser.add_subparsers(dest="command")
    hcp_setup_args(subparsers)
    strucutral_commands(subparsers)
    diffusion_commands(subparsers)
    return base_parser


def default_args(args: object) -> None:
    """
    Function to add in default arguments

    Parameters
    ----------
    args: object
        ArgParser object

    Returns
    -------
    None
    """
    args.add_argument(
        "-s",
        "--study_folder",
        help="Path to study folder",
        dest="study_folder",
    )
    args.add_argument(
        "-L",
        "--Load_env",
        help="""Use this option to load qunex enviorment (currently only works on nottingham cluster)""",
        dest="load",
        action="store_true",
    )


def hcp_setup_args(args) -> dict:
    """
    Function to take hcp set up
    arguments

    Parameters
    ----------
    args: object
        ArgParser object

    Returns
    -------
    dict: dictionary
        dict of cmd args
    """
    study_setup_args = args.add_parser("setup", help="Set up study")
    default_args(study_setup_args)
    study_setup_args.add_argument(
        "-O",
        "--overwrite",
        help="Overwrite exsiting study folder",
        dest="overwrite",
        action="store_true",
    )
    study_setup_args.add_argument(
        "-r",
        "--raw_data",
        help="Path to raw data",
        dest="raw_data",
        required=True,
    )
    study_setup_args.add_argument(
        "-d",
        "--data_type",
        help="""
        Which type of data (HCP style or biobank) is being processed.
        Either HCP or biobank (case insensitive)
        """,
        choices=valid_data_types(),
        dest="data_type",
    )
    study_setup_args.add_argument(
        "-b",
        "--batch",
        help="""
        Full path to a custom batch file with parameters for the hcp pipeline. 
        Must be called hcp_batch.txt""",
        dest="batch",
    )


def strucutral_commands(args) -> dict:
    """
    Function to take hcp structural
    arguments

    Parameters
    ----------
    args: object
        ArgParser object

    Returns
    -------
    dict: dictionary
        dict of cmd args
    """
    strucutral_args = args.add_parser(
        "structural", help="To run pre-freesurfer/freesurfer/post freesurfer of HCP"
    )
    default_args(strucutral_args)
    strucutral_args.add_argument(
        "-q",
        "--queue",
        help="""Which queue to submit to. 
        Leave this as none if not running on cluster""",
        dest="queue",
    )
    strucutral_args.add_argument(
        "-F", "--FLAIR", help="Is T2 a FLAIR image", dest="flair", action="store_true"
    )


def diffusion_commands(args) -> dict:
    """
    Function to take hcp diffusion
    arguments

    Parameters
    ----------
    args: object
        ArgParser object

    Returns
    -------
    dict: dictionary
        dict of cmd args
    """
    diffusion_args = args.add_parser("diffusion", help="To run HCP diffusion pipeline")
    default_args(diffusion_args)
    diffusion_args.add_argument(
        "-q",
        "--queue",
        help="""Which queue to submit to. 
        Leave this as none if not running on cluster""",
        dest="queue",
    )
    diffusion_args.add_argument(
        "-N",
        "--no_gpu",
        help="Don't use eddy GPU",
        dest="no_gpu",
        action="store_true",
    )


def qpipeline_args() -> dict:
    """
    main function to return
    all the args for sub modules

    Parameters
    ----------
    None

    Returns
    -------
    dict: dictionary
        dict of all args
    """
    check_subcommand()
    parser = qpipeline_modules()
    args = parser.parse_args()

    # If no arguments after subcommand, show help for that subparser
    if args.command == "setup" and len(sys.argv) <= 3:
        parser.parse_args(["setup", "--help"])
    if args.command == "structural" and len(sys.argv) <= 3:
        parser.parse_args(["structural", "--help"])
    if args.command == "diffusion" and len(sys.argv) <= 3:
        parser.parse_args(["diffusion", "--help"])

    return vars(args)
