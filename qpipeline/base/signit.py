import signal
import os
import sys


class Signit_handler:
    """
    A SIGINT handler class. Handles Ctrl+C cleanly by killing all
    processes in the same process group (including children).
    """

    def __init__(self) -> None:
        self.register_handler()
        self.suppress_messages = False

        # Make sure this process is its own process group leader
        os.setpgrp()

    def register_handler(self) -> None:
        """
        Register the SIGINT handler.
        """
        signal.signal(signal.SIGINT, self.handle_sigint)

    def handle_sigint(self, sig, frame) -> None:
        """
        Handle the SIGINT signal (Ctrl+C).
        Kill all processes in the current process group.
        """
        if not self.suppress_messages:
            print("\nReceived kill signal (Ctrl+C)")

        try:
            os.killpg(os.getpgrp(), signal.SIGTERM)
        except Exception as e:
            print(f"Error while killing process group: {e}", file=sys.stderr)

        if not self.suppress_messages:
            print("Exiting...")

        sys.exit(0)

    @property
    def get_suppress_messages(self):
        return self.suppress_messages

    @get_suppress_messages.setter
    def set_suppress_messages(self, value: bool) -> None:
        self.suppress_messages = value
