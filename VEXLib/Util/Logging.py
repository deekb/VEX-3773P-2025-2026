import json
import struct
import sys
from VEXLib.Util.Shelf import Shelf

from VEXLib.Util import time


class LogLevel:
    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    FATAL = "FATAL"


LOG_LEVELS = {
    LogLevel.TRACE: 1,
    LogLevel.DEBUG: 2,
    LogLevel.INFO: 3,
    LogLevel.WARN: 4,
    LogLevel.ERROR: 5,
    LogLevel.FATAL: 6,
}


def file_exists(filename):
    if sys.platform == "linux":
        import os

        return os.path.exists(filename)
    from vex import Brain

    return Brain().sdcard.filesize(filename)


class Logger:
    def __init__(self, log_name, index=None, flush_threshold=512):
        self.flush_threshold = flush_threshold
        self.log_buffer = bytearray()
        self.current_index = (
            index
            if index is not None
            else Shelf("logs/startup_count.csv").get("startup_count", 0)
        )
        self.log_file_path = "{log_name}-{index}.binlog".format(
            log_name=log_name, index=self.current_index
        )

    def log(self, *parts, log_level=LogLevel.INFO):
        try:
            if log_level not in LOG_LEVELS:
                raise ValueError("Invalid log level: " + str(log_level))

            timestamp = float(time.time())
            message_bytes = " ".join(map(str, parts)).encode("utf-8")
            log_entry = struct.pack(
                "<fBI{}s".format(len(message_bytes)),
                timestamp,
                LOG_LEVELS[log_level],
                len(message_bytes),
                message_bytes,
            )
            self.log_buffer.extend(log_entry)
            if len(self.log_buffer) >= self.flush_threshold:
                self.flush_logs()
        except MemoryError:
            self.log_buffer = []

    def log_vars(self, vars_dict, log_level=LogLevel.INFO):
        self.log(json.dumps(vars_dict), log_level=log_level)

    def flush_logs(self):
        if self.log_buffer:
            try:
                with open(self.log_file_path, "ab") as f:
                    # Ensure log_buffer is bytes before writing
                    if isinstance(self.log_buffer, bytes):
                        f.write(self.log_buffer)
                    else:
                        f.write(bytes(self.log_buffer))
                    f.flush()
                self.log_buffer = []
            except OSError:
                pass

    # Shorthand methods
    def trace(self, *parts):
        self.log(*parts, log_level=LogLevel.TRACE)

    def debug(self, *parts):
        self.log(*parts, log_level=LogLevel.DEBUG)

    def info(self, *parts):
        self.log(*parts, log_level=LogLevel.INFO)

    def warn(self, *parts):
        self.log(*parts, log_level=LogLevel.WARN)

    def error(self, *parts):
        self.log(*parts, log_level=LogLevel.ERROR)

    def fatal(self, *parts):
        self.log(*parts, log_level=LogLevel.FATAL)

    def logged(self, func, log_level=LogLevel.TRACE):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            if hasattr(func, "__name__"):
                self.log(
                    "["
                    + str(format_time(start_time))
                    + '] "'
                    + func.__name__
                    + '" called with args='
                    + str(args)
                    + ", kwargs="
                    + str(kwargs),
                    log_level=log_level,
                )
            else:
                self.log(
                    "["
                    + str(format_time(start_time))
                    + '] "'
                    + str(func)
                    + '" called with args='
                    + str(args)
                    + ", kwargs="
                    + str(kwargs),
                    log_level=log_level,
                )

            output = func(*args, **kwargs)
            end_time = time.time()
            elapsed = end_time - start_time

            if hasattr(func, "__name__"):
                self.log(
                    "["
                    + str(format_time(end_time))
                    + '] "'
                    + func.__name__
                    + '" finished in '
                    + str(format_time(elapsed))
                    + " with output: "
                    + str(output),
                    log_level=log_level,
                )
            else:
                self.log(
                    "["
                    + str(format_time(end_time))
                    + '] "'
                    + str(func)
                    + '" finished in '
                    + str(format_time(elapsed))
                    + " with output: "
                    + str(output),
                    log_level=log_level,
                )

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
