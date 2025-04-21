import json

import matplotlib.pyplot as plt


# Function to rescale voltage data to 0-100 range
def rescale_voltage(voltage_data):
    min_voltage = min(voltage_data)
    max_voltage = max(voltage_data)
    return [(v - min_voltage) / (max_voltage - min_voltage) * 100 for v in voltage_data]


# Load JSON data for the left and right drivetrain
with open("input/drivetrain_data_left.json", "r") as file:
    left_data_old = json.load(file)

with open("input/drivetrain_data_right.json", "r") as file:
    right_data_old = json.load(file)

with open("input/drivetrain_data_left_2.json", "r") as file:
    left_data = json.load(file)

with open("input/drivetrain_data_right_2.json", "r") as file:
    right_data = json.load(file)

# Rescale voltage data
left_data["voltage"] = rescale_voltage(left_data["voltage"])
right_data["voltage"] = rescale_voltage(right_data["voltage"])
left_data_old["voltage"] = rescale_voltage(left_data_old["voltage"])
right_data_old["voltage"] = rescale_voltage(right_data_old["voltage"])

# Define the properties to plot and their units
properties = ["torque", "power", "speed"]

units = {"torque": "Nm", "power": "W", "speed": "% of rated speed"}

# Create subplots
fig, axes = plt.subplots(
    len(properties), 1, figsize=(8, len(properties) * 3), tight_layout=True
)

# Plot properties for left and right sides
for i, prop in enumerate(properties):
    if prop in left_data:  # Check if property exists in left_data
        axes[i].plot(
            left_data["voltage"],
            left_data.get(prop, []),
            label=f"Left {prop.capitalize()}",
            color="blue",
        )
    if prop in right_data:  # Check if property exists in right_data
        axes[i].plot(
            right_data["voltage"],
            right_data.get(prop, []),
            label=f"Right {prop.capitalize()}",
            color="orange",
        )
    if prop in left_data_old:  # Check if property exists in left_data_old
        axes[i].plot(
            left_data_old["voltage"],
            left_data_old.get(prop, []),
            label=f"Left {prop.capitalize()} Old",
            color="blue",
            linestyle=":",
        )
    if prop in right_data_old:  # Check if property exists in right_data_old
        axes[i].plot(
            right_data_old["voltage"],
            right_data_old.get(prop, []),
            label=f"Right {prop.capitalize()} Old",
            color="orange",
            linestyle=":",
        )

    axes[i].set_title(f"{prop.capitalize()} Comparison")
    axes[i].set_xlabel("PWM Duty Cycle (%)")
    axes[i].set_ylabel(f"{prop.capitalize()} ({units[prop]})")
    axes[i].set_xlim(0, 100)  # Set x-axis limits from 0 to 100
    axes[i].legend(
        loc="upper left", framealpha=0.8
    )  # Set legend to top left with 80% transparency
    axes[i].grid(True)

# Adjust layout for better utilization of space
plt.tight_layout()

# Adjust the figure size to use the right amount of space on a piece of paper
fig.set_size_inches(8.5, 8.5)

# Save the figure as a high-resolution PNG file (600 DPI)
png_output_filename = "output/drivetrain_comparison.png"
plt.savefig(png_output_filename, format="png", dpi=600, bbox_inches="tight")

plt.show()
