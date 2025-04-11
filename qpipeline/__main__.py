from qpipeline.base.args import qpipeline_args
from qpipeline.base.setup import set_environment
from qpipeline.base.Qpipeline import Qpipeline
from qpipeline.base.signit import Signit_handler


def main():
    Signit_handler()
    args = qpipeline_args()
    set_environment()
    pipeline = Qpipeline()
    pipeline.qpipeline_handler(args["command"], args)
    exit()


if __name__ == "__main__":
    main()
