import pandas as pd
import matplotlib.pyplot as plt

# Define the path to the CSV file
left_drivetrain_file_path = '/home/derek/PycharmProjects/VEXlib/logs/left_drivetrain.csv'
right_drivetrain_file_path = '/home/derek/PycharmProjects/VEXlib/logs/right_drivetrain.csv'

# Read the CSV file into a DataFrame
df_left = pd.read_csv(left_drivetrain_file_path)
df_right = pd.read_csv(right_drivetrain_file_path)

# Extracting time and speed values
left_time_values = df_left['time (s)']
right_time_values = df_right['time (s)']
left_speed_values = df_left['speed (% of rated)']
right_speed_values = df_right['speed (% of rated)']

# Normalize the times to start at the same timestamp and make it zero
left_time_values -= left_time_values.min()
right_time_values -= right_time_values.min()

# Sort the time values
left_sorted_indices = left_time_values.argsort()
right_sorted_indices = right_time_values.argsort()

left_time_values = left_time_values[left_sorted_indices]
left_speed_values = left_speed_values[left_sorted_indices]
right_time_values = right_time_values[right_sorted_indices]
right_speed_values = right_speed_values[right_sorted_indices]

# Plotting
plt.figure(figsize=(8, 5))
plt.plot(left_time_values, left_speed_values, label="Left Speed (cm/s)")
plt.plot(right_time_values, right_speed_values, label="Right Speed (cm/s)")

# Labels and title
plt.xlabel("Time (s)")
plt.ylabel("Speed (cm/s)")
plt.title("Time vs. Speed")
plt.legend()
plt.grid()

# Show plot
plt.show()