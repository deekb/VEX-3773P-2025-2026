from VEXLib.Util import time
import json

from vex import Brain


class Logger:
    _shared_index = None  # Shared index used by all instances
    _index_file = "logs/index.json"  # Shared index file

    def __init__(self, sd_card, log_name_prefix):
        """
        Initializes the logger by ensuring a shared index is used consistently across instances,
        and opens a single log file for writing during the program lifecycle.

        :param sd_card: External storage object
        :param log_name_prefix: Prefix for the log file names
        """
        self.sd_card = sd_card
        self.log_name_prefix = log_name_prefix

        # Get the shared index and ensure it's only incremented once
        self.current_index = self._get_or_create_shared_index()
        self.log_file_path = "logs/" + str(self.log_name_prefix) + "-" + str(self.current_index) + ".log"

    @classmethod
    def _get_or_create_shared_index(cls):
        """
        Retrieves or creates the shared logging index from 'index.json'.
        Ensures the index is incremented only once even if multiple Logger instances are created.

        :return: Current index for the log file
        """
        if cls._shared_index is not None:
            # Reuse the shared index if already loaded
            return cls._shared_index

        # Load the index from file or initialize it
        if Brain().sdcard.filesize(cls._index_file):
            try:
                with open(cls._index_file, "r") as file:
                    data = json.load(file)
                    cls._shared_index = data.get("log_index", 1)
            except json.JSONDecodeError:
                # Handle a corrupted JSON file
                cls._shared_index = 1
        else:
            cls._shared_index = 1

        # Increment the index for the next session and save it
        cls._increment_shared_index()

        return cls._shared_index

    @classmethod
    def _increment_shared_index(cls):
        """
        Increments the shared index and saves it back to 'index.json'.
        Ensures the shared index is updated for the next session.
        """
        with open(cls._index_file, "w") as file:
            json.dump({"log_index": cls._shared_index + 1}, file)

    def log(self, *parts, end="\n"):
        """
        Logs a message to the log file. Writes the message into the open file.

        :param message: Message to be logged.
        """
        message = " ".join(map(str, parts)) + end
        self.sd_card.appendfile(self.log_file_path, bytearray(message))


def format_time(seconds):
    """
    Formats a time value in seconds to HH:MM:SS.MS format.

    :param seconds: Time in seconds
    :return: A string representing the formatted time.
    """
    millis = int((seconds % 1) * 1000)
    seconds = int(seconds)
    mins, secs = divmod(seconds, 60)
    hours, mins = divmod(mins, 60)
    return "{:02}:{:02}:{:02}.{:03}".format(hours, mins, secs, millis)


def logged(func, logger: Logger = print):
    def wrapper(*args, **kwargs):
        if logger is print:
            log_func = print
        else:
            log_func = logger.log

        start_time = time.time()
        if hasattr(func, "__name__"):
            log_func("[" + str(format_time(start_time)) + "] \"" + func.__name__ + "\" called with args=" + str(
                args) + ", kwargs=" + str(kwargs))
        else:
            log_func("[" + str(format_time(start_time)) + "] \"" + str(func) + "\" called with args=" + str(
                args) + ", kwargs=" + str(kwargs))

        output = func(*args, **kwargs)
        end_time = time.time()
        elapsed = end_time - start_time

        if hasattr(func, "__name__"):
            log_func("[" + str(format_time(end_time)) + "] \"" + func.__name__ + "\" finished in " + str(
                format_time(elapsed)) + " with output: " + str(output))
        else:
            log_func("[" + str(format_time(end_time)) + "] \"" + str(func) + "\" finished in " + str(
                format_time(elapsed)) + " with output: " + str(output))

        return output

    return wrapper


# @logged
# def hello(name):
#     print(f"Hello {name}")
#
#
# hello("Derek")
