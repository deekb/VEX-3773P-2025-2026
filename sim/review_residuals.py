import re
import matplotlib.pyplot as plt
from datetime import datetime
import ast  # safer than eval()

# Load log file
with open('../DrivetrainDebug.log', 'r') as f:
    log_lines = f.readlines()

# Regex pattern to match timestamps
timestamp_pattern = r"(\d{2}:\d{2}\.\d{3}) \[INFO\]"

# Storage lists
times = []
target_positions = []
current_positions = []
target_headings = []
current_headings = []

start_time = None
i = 0

while i < len(log_lines) - 1:
    timestamp_match = re.match(timestamp_pattern, log_lines[i].strip())

    if timestamp_match:
        timestamp_str = timestamp_match.group(1)
        try:
            timestamp = datetime.strptime(timestamp_str, "%M:%S.%f")
        except ValueError:
            timestamp = datetime.strptime(timestamp_str, "%H:%M.%f")

        # The next line should contain the dictionary
        next_line = log_lines[i + 1].strip()

        # Check if the next line looks like a dict
        if next_line.startswith("{") and next_line.endswith("}"):
            try:
                data = ast.literal_eval(next_line)  # safer than eval()

                if start_time is None:
                    start_time = timestamp

                # Compute elapsed time in seconds
                elapsed = (timestamp - start_time).total_seconds()

                times.append(elapsed)
                target_positions.append(data.get("target_position"))
                current_positions.append(data.get("current_position"))
                target_headings.append(data.get("target_heading (rev)"))
                current_headings.append(data.get("current_heading (rev)"))

            except Exception as e:
                print(f"Error parsing dict on line {i+2}: {e}")
        i += 2  # move to next timestamp+dict pair
    else:
        i += 1  # skip non-matching lines

# --- Plot Results ---
if not times:
    print("No data parsed. Please verify log format.")
else:
    plt.figure(figsize=(10, 6))

    # --- Position Plot ---
    plt.subplot(2, 1, 1)
    plt.plot(times, target_positions, label="Target Position", color='b')
    plt.plot(times, current_positions, label="Current Position", color='g')
    plt.xlabel("Time (s)")
    plt.ylabel("Position (m)")
    plt.title("Target and Current Position Over Time")
    plt.legend()

    # --- Heading Plot ---
    plt.subplot(2, 1, 2)
    plt.plot(times, target_headings, label="Target Heading (rev)", color='r')
    plt.plot(times, current_headings, label="Current Heading (rev)", color='orange')
    plt.xlabel("Time (s)")
    plt.ylabel("Heading (rev)")
    plt.title("Target and Current Heading Over Time")
    plt.legend()

    plt.tight_layout()
    plt.show()
