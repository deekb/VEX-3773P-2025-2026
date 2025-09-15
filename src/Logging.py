import struct
import json
import sys
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
    _shared_index = None
    _index_file = "index.json"

    def __init__(self, log_name='main', flush_threshold=1024):
        self.flush_threshold = flush_threshold
        self.log_buffer = bytearray()
        self.current_index = self._get_or_create_shared_index(log_name)
        self.log_file_path = "{log_name}-{index}.binlog".format(log_name=log_name, index=self.current_index)

    @classmethod
    def _get_or_create_shared_index(cls, log_name):
        index_data = {}
        if file_exists(cls._index_file):
            try:
                with open(cls._index_file, "r") as f:
                    index_data = json.load(f)
            except json.JSONDecodeError:
                index_data = {}

        if "index" in index_data:
            index_data["index"] += 1
        else:
            index_data["index"] = 1

        # if log_name in index_data:
        #     index_data[log_name] += 1
        # else:
        #     index_data[log_name] = 1

        with open(cls._index_file, "w") as f:
            json.dump(index_data, f)

        return index_data["index"]
        # return index_data[log_name]

    def log(self, *parts, log_level=LogLevel.INFO):
        try:
            if log_level not in LOG_LEVELS:
                raise ValueError("Invalid log level: " + str(log_level))

            timestamp = float(time.time())
            message_bytes = " ".join(map(str, parts)).encode('utf-8')
            log_entry = struct.pack(
                '<fBI{}s'.format(len(message_bytes)),
                timestamp,
                LOG_LEVELS[log_level],
                len(message_bytes),
                message_bytes
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
                with open(self.log_file_path, 'ab') as f:
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
    def trace(self, *parts): self.log(*parts, log_level=LogLevel.TRACE)
    def debug(self, *parts): self.log(*parts, log_level=LogLevel.DEBUG)
    def info(self, *parts): self.log(*parts, log_level=LogLevel.INFO)
    def warn(self, *parts): self.log(*parts, log_level=LogLevel.WARN)
    def error(self, *parts): self.log(*parts, log_level=LogLevel.ERROR)
    def fatal(self, *parts): self.log(*parts, log_level=LogLevel.FATAL)

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

def format_time(seconds):
    millis = int((seconds % 1) * 1000)
    seconds = int(seconds)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "{:02}:{:02}:{:02}.{:03}".format(hours, minutes, seconds, millis)