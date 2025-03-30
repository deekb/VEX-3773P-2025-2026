import json
import sys

from VEXLib.Util import time
from vex import Brain


"""
Here's how I determine log level:

For whom am I writing the log line?
    If Developers:
        Do I need to log states of variables?
            Yes → DEBUG
            No → TRACE
    If System operators:
        Do I log because of an unwanted state?
            No → INFO
            Yes:
                Can the process continue with the unwanted state?
                    Yes → WARN
                    No:
                        Can the application continue with the unwanted state?
                            Yes → ERROR
                            No → FATAL
"""


class LogLevel:
    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    FATAL = "FATAL"


def file_exists(filename):
    if sys.platform == "linux":
        import os
        return os.path.exists(filename)
    return Brain().sdcard.filesize(filename)


class Logger:
    _shared_index = None  # Shared index used by all instances
    _index_file = "logs/index.json"  # Shared index file

    def __init__(self, sd_card, brain_screen: Brain.Lcd, log_name_prefix):
        self.sd_card = sd_card
        self.brain_screen = brain_screen
        self.log_name_prefix = log_name_prefix

        self.current_index = self._get_or_create_shared_index()
        self.log_file_path = "logs/" + str(self.log_name_prefix) + "-" + str(self.current_index) + ".log"

    @classmethod
    def _get_or_create_shared_index(cls):
        if cls._shared_index is not None:
            return cls._shared_index

        if file_exists(cls._index_file):
            try:
                with open(cls._index_file, "r") as file:
                    data = json.load(file)
                    cls._shared_index = data.get("log_index", 1)
            except json.JSONDecodeError:
                cls._shared_index = 1
        else:
            cls._shared_index = 1

        cls._increment_shared_index()
        return cls._shared_index

    @classmethod
    def _increment_shared_index(cls):
        with open(cls._index_file, "w") as file:
            json.dump({"log_index": cls._shared_index + 1}, file)

    def log(self, *parts, end="\n", log_level=LogLevel.INFO):
        message = " ".join(map(str, parts)) + end

        start_time = time.time()
        self.sd_card.appendfile(self.log_file_path, bytearray("<" + log_level + "> " + message))
        end_time = time.time()

        elapsed_time = end_time - start_time

    def trace(self, *parts, end="\n"):
        self.log(*parts, end=end, log_level=LogLevel.TRACE)

    def debug(self, *parts, end="\n"):
        self.log(*parts, end=end, log_level=LogLevel.DEBUG)

    def info(self, *parts, end="\n"):
        self.log(*parts, end=end, log_level=LogLevel.INFO)

    def warn(self, *parts, end="\n"):
        self.log(*parts, end=end, log_level=LogLevel.WARN)

    def error(self, *parts, end="\n"):
        self.log(*parts, end=end, log_level=LogLevel.ERROR)

    def fatal(self, *parts, end="\n"):
        self.log(*parts, end=end, log_level=LogLevel.FATAL)

    def logged(self, func, log_level=LogLevel.TRACE):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            if hasattr(func, "__name__"):
                self.log("[" + str(format_time(start_time)) + "] \"" + func.__name__ + "\" called with args=" + str(
                    args) + ", kwargs=" + str(kwargs), log_level=log_level)
            else:
                self.log("[" + str(format_time(start_time)) + "] \"" + str(func) + "\" called with args=" + str(
                    args) + ", kwargs=" + str(kwargs), log_level=log_level)

            output = func(*args, **kwargs)
            end_time = time.time()
            elapsed = end_time - start_time

            if hasattr(func, "__name__"):
                self.log("[" + str(format_time(end_time)) + "] \"" + func.__name__ + "\" finished in " + str(
                    format_time(elapsed)) + " with output: " + str(output), log_level=log_level)
            else:
                self.log("[" + str(format_time(end_time)) + "] \"" + str(func) + "\" finished in " + str(
                    format_time(elapsed)) + " with output: " + str(output), log_level=log_level)

            return output

        return wrapper


class TimeSeriesLogger:
    def __init__(self, filename, fieldnames=None):
        """
        Initialize the logger with a file name and an optional list of fieldnames.
        If no fieldnames are provided, the class will try to infer them from the data.

        :param filename: The name of the CSV file where data will be written.
        :param fieldnames: List of column names (fields) in the CSV file. Defaults to None.
        """
        self.filename = filename
        self.fieldnames = fieldnames
        self._initialize_csv(False)

    def _initialize_csv(self, force_overwrite):
        """Initialize the CSV file by writing the header if the file doesn't already exist."""
        if not file_exists(self.filename) or force_overwrite:
            # If the file doesn't exist, create it and write the header row
            if self.fieldnames:
                with open(self.filename, 'w') as file:
                    header = ','.join(self.fieldnames) + '\n'
                    file.write(header)
            else:
                raise ValueError("Fieldnames must be provided when creating a new CSV file.")
        else:
            # If the file already exists, make sure the fieldnames match
            with open(self.filename, 'r') as file:
                existing_header = file.readline().strip()
                existing_fieldnames = existing_header.split(',')
                if self.fieldnames and self.fieldnames != existing_fieldnames:
                    self._initialize_csv(True)

    def write_data(self, data):
        """
        Write a row of data to the CSV file. The data should be a dictionary where keys
        correspond to the fieldnames.

        :param data: A dictionary with keys corresponding to the fieldnames.
        """
        if not self.fieldnames:
            # Infer fieldnames from the first row of data if not provided at initialization
            self.fieldnames = list(data.keys())
            self._initialize_csv()  # Re-initialize CSV file with inferred fieldnames

        Brain().sdcard.appendfile(self.filename, bytearray(','.join(str(data[field]) for field in self.fieldnames) + '\n'))

    def read_data(self):
        """
        Read all the data from the CSV file and return it as a list of dictionaries.

        :return: A list of dictionaries where each dictionary represents a row of data.
        """
        data = []
        with open(self.filename, 'r') as file:
            # Read the header (first line) to get the fieldnames
            header = file.readline().strip()
            fieldnames = header.split(',')
            # Read the rest of the rows
            for line in file:
                values = line.strip().split(',')
                row = {fieldnames[i]: values[i] for i in range(len(fieldnames))}
                data.append(row)
        return data


def format_time(seconds):
    millis = int((seconds % 1) * 1000)
    seconds = int(seconds)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "{:02}:{:02}:{:02}.{:03}".format(hours, minutes, seconds, millis)


# t = TimeSeriesLogger("/home/derek/PycharmProjects/VEXlib/logs/CONSTANTS.csv")

# print(t.read_data())
