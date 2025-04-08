from qpipeline.base.args import qpipeline_args
from qpipeline.base.setup import set_environment
from qpipeline.base.Qpipeline import Qpipeline


def main():
    args = qpipeline_args()
    set_environment()
    pipeline = Qpipeline()
    pipeline.qpipeline_handler(args["command"], args)
    exit()


if __name__ == "__main__":
    main()
