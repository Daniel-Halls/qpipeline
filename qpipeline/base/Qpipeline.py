class Qpipeline:
    """
    Main class of qpipeline

    Determines what part of the pipeline
    should be ran.

    Usage
    -----
    pipeline = Qpipeline()
    pipeline.qpipeline_handler(args['command'], args)
    """

    def __init__(self):
        pass

    def setup(self, **kwargs):
        """
        Set up function entry method
        """
        from qpipeline.qunex_setup.study_setup import set_up_qunex_study

        set_up_qunex_study(kwargs)

    def qpipeline_handler(self, command: str, args: str):
        """
        Method to determine what part of the pipeline
        should be ran based on user input
        """
        func = getattr(self, command)
        func(**{key: value for key, value in args.items() if key != "command"})
