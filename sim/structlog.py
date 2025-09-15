import struct
import json
import sys
import time
# from vex import Brain
from rich import print
from rich.pretty import Pretty
from rich.console import Console

console = Console()

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

LOG_LEVEL_COLORS = {
    LogLevel.TRACE: "dim white",
    LogLevel.DEBUG: "cyan",
    LogLevel.INFO: "green",
    LogLevel.WARN: "yellow",
    LogLevel.ERROR: "red",
    LogLevel.FATAL: "bold red"
}

def file_exists(filename):
    if sys.platform == "linux":
        import os
        return os.path.exists(filename)
    return Brain().sdcard.filesize(filename)


class Logger:
    _shared_index = None  # Shared index used by all instances
    _index_file = "index.json"  # Shared index file

    def __init__(self, log_name='main', flush_threshold=1024):
        self.flush_threshold = flush_threshold
        self.log_buffer = bytearray()
        self.current_index = self._get_or_create_shared_index()
        self.log_file_path = str(log_name) + "-" + str(self.current_index) + ".binlog"

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

    def log(self, *parts, log_level=LogLevel.INFO):
        if log_level not in LOG_LEVELS:
            raise ValueError(f"Invalid log level: {log_level}")

        timestamp = int(time.time())
        message_bytes = " ".join(map(str, parts)).encode('utf-8')
        message_length = len(message_bytes)

        log_entry = struct.pack(
            f'IBI{message_length}s',
            timestamp,
            LOG_LEVELS[log_level],
            message_length,
            message_bytes
        )

        self.log_buffer.extend(log_entry)
        if len(self.log_buffer) >= self.flush_threshold:
            self.flush_logs()

    def log_vars(self, vars_dict, log_level=LogLevel.INFO):
        if log_level not in LOG_LEVELS:
            raise ValueError(f"Invalid log level: {log_level}")

        timestamp = int(time.time())
        vars_json = json.dumps(vars_dict, separators=(',', ':'))
        vars_bytes = vars_json.encode('utf-8')
        vars_length = len(vars_bytes)

        log_entry = struct.pack(
            f'IBI{vars_length}s',
            timestamp,
            LOG_LEVELS[log_level],
            vars_length,
            vars_bytes
        )

        self.log_buffer.extend(log_entry)
        if len(self.log_buffer) >= self.flush_threshold:
            self.flush_logs()

    def flush_logs(self):
        if self.log_buffer:
            with open(self.log_file_path, 'ab') as file:
                file.write(self.log_buffer)
                file.flush()
            self.log_buffer.clear()

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


def safe_dict(d):
    def safe_value(v):
        try:
            json.dumps(v)
            return v
        except TypeError:
            return str(v)
    return {k: safe_value(v) for k, v in d.items() if not k.startswith('_')}


logger = Logger()
logger.debug("Locals:")
logger.log_vars(safe_dict(locals()), log_level=LogLevel.DEBUG)
logger.debug("Globals:")
logger.log_vars(safe_dict(globals()), log_level=LogLevel.DEBUG)
logger.log_vars({"time": time.time_ns()}, log_level=LogLevel.DEBUG)
logger.fatal("This is a fatal log message for testing purposes.")
logger.flush_logs()

LOG_LEVELS_REV = {1: "TRACE", 2: "DEBUG", 3: "INFO", 4: "WARN", 5: "ERROR", 6: "FATAL"}

def read_logs(log_file='log.bin'):
    with open(log_file, 'rb') as f:
        while True:
            header = f.read(12)
            if not header or len(header) < 12:
                break
            timestamp, log_level, msg_len = struct.unpack('IBI', header)
            msg_bytes = f.read(msg_len)
            if len(msg_bytes) < msg_len:
                break
            try:
                msg = msg_bytes.decode('utf-8')
                try:
                    msg_obj = json.loads(msg)
                except json.JSONDecodeError:
                    msg_obj = msg

                level_name = LOG_LEVELS_REV.get(log_level, log_level)
                color = LOG_LEVEL_COLORS.get(level_name, "white")

                # If it's structured data, pretty-print on next line
                if isinstance(msg_obj, dict):
                    console.print(
                        f"[bold white]{timestamp}[/bold white] "
                        f"[{color}][{level_name}][/{color}]"
                    )
                    console.print(Pretty(msg_obj, indent_size=4))

                # Otherwise print all in one line
                else:
                    console.print(
                        f"[bold white]{timestamp}[/bold white] "
                        f"[{color}][{level_name}][/{color}] {msg_obj}"
                    )

            except Exception as e:
                console.print(f"[red]Error decoding log entry: {e}[/red]")

# Usage
read_logs('main-1.binlog')
