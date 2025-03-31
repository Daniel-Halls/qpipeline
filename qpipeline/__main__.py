from .args import qpipeline_args
from .setup import set_environment
from .study_setup import set_up_qunex_study
from .structural_preprocessing import strucutral_hcp


def main():
    arg = qpipeline_args()
    set_environment()
    if not arg["skip_study_setup"]:
        print("\nSetting up qunex study")
        print("-" * 100)
        set_up_qunex_study(arg)
    strucutral_hcp(arg)


if __name__ == "__main__":
    main()
