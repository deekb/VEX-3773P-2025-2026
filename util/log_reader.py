import struct
import json
from rich.pretty import Pretty
from rich.console import Console

console = Console()

LOG_LEVELS_REV = {1: "TRACE", 2: "DEBUG", 3: "INFO", 4: "WARN", 5: "ERROR", 6: "FATAL"}
LOG_LEVEL_COLORS = {
    "TRACE": "dim white",
    "DEBUG": "cyan",
    "INFO": "green",
    "WARN": "yellow",
    "ERROR": "red",
    "FATAL": "bold red"
}

def read_logs(log_file):
    with open(log_file, 'rb') as f:
        while True:
            # Read header: float (4 bytes), unsigned char (1 byte), unsigned int (4 bytes)
            header = f.read(9)
            if not header or len(header) < 9:
                break

            timestamp, log_level, msg_len = struct.unpack('<fBI', header)
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

                # Convert float timestamp to minutes:seconds.ms
                total_seconds = int(timestamp)
                minutes = total_seconds // 60
                seconds = total_seconds % 60
                milliseconds = int((timestamp % 1) * 1000)
                ts_str = f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

                if isinstance(msg_obj, dict):
                    console.print(f"[bold white]{ts_str}[/bold white] [{color}][{level_name}][/{color}]")
                    console.print(Pretty(msg_obj, indent_size=4))
                else:
                    console.print(f"[bold white]{ts_str}[/bold white] [{color}][{level_name}][/{color}] {msg_obj}")

            except Exception as e:
                console.print(f"[red]Error decoding log entry: {e}[/red]")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Read and pretty-print binary log files.")
    parser.add_argument("logfile", help="Path to the binary log file")
    args = parser.parse_args()
    read_logs(args.logfile)