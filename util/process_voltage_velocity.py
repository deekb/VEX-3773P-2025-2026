# lines = open("../logs/voltage_velocity.csv").readlines()
# outfile = open("../logs/voltage_velocity_small.csv", "w")
#
# for i, line in enumerate(lines, start=0):
#     if (i % 4) == 0:
#         outfile.write(line)

import pandas as pd

MAX_SPEED_METERS_PER_SECOND = 1.77

# Set the option to display all columns
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)

# Load CSV
df = pd.read_csv("../logs/voltage_velocity_small.csv")

print("Original dataframe:")
print(df.head(n=20))


# ----------------------------------------
# 1. CREATE LEFT + RIGHT DATAFRAMES
# ----------------------------------------

left_df = df[["time", "left_voltage", "left_speed"]].copy()
right_df = df[["time", "right_voltage", "right_speed"]].copy()

# ----------------------------------------
# 2. SCALE SPEED TO -10 to 10
# ----------------------------------------

left_df["left_speed"] *= (10 / MAX_SPEED_METERS_PER_SECOND)
right_df["right_speed"] *= (10 / MAX_SPEED_METERS_PER_SECOND)


# ----------------------------------------
# 3. COMPUTE ACCELERATION AND VOLTAGE Δ
# ----------------------------------------
# acceleration = Δspeed / Δtime
# voltage_delta = Δvoltage / Δtime

def compute_derivatives(data, voltage_col, speed_col):
    d = data.copy()

    d["delta_time"] = d["time"].diff()
    d["delta_speed"] = d[speed_col].diff()

    # acceleration (speed change per second)
    # d["acceleration"] = d["delta_speed"] / d["delta_time"]
    return d


left_df = compute_derivatives(left_df, "left_voltage", "left_speed")
right_df = compute_derivatives(right_df, "right_voltage", "right_speed")

# ----------------------------------------
# 4. SHOW RESULTS
# ----------------------------------------

print("\nLeft drivetrain dataframe:")
print(left_df.head(n=20))

print("\nRight drivetrain dataframe:")
print(right_df.head(n=20))

left_df["speed_bin"] = pd.cut(left_df['left_speed'], bins=range(-10, 11, 1))

left_df = left_df.drop("time", axis=1)

left_df = left_df.sort_values("speed_bin")

grouped = left_df.groupby('speed_bin')

print("\nLeft speed bins:")
bins = [bin for bin in grouped]

print(bins[0])