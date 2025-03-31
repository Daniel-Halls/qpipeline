from qpipeline.base.args import qpipeline_args
from qpipeline.base.setup import set_environment
from qpipeline.qunex_setup.study_setup import set_up_qunex_study


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
