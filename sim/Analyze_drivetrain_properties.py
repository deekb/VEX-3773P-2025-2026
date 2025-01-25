import json
import numpy as np
import matplotlib.pyplot as plt

# Load JSON data for the left and right drivetrain
with open('drivetrain_data_left.json', 'r') as file:
    left_data = json.load(file)

with open('drivetrain_data_right.json', 'r') as file:
    right_data = json.load(file)

# Define the properties to plot
properties = ["torque", "power", "speed"]


# Normalize the data for each property to scale them similarly
def normalize(values):
    return values
    # values = np.array(values)
    # return (values - np.min(values)) / (np.ptp(values))  # Normalize to range [0, 1]


# Apply normalization to all properties
for side_data in [left_data, right_data]:
    for prop in properties:
        if prop in side_data:  # Make sure the property exists in the dataset before normalizing
            side_data[prop] = normalize(side_data[prop])

# Create subplots
fig, axes = plt.subplots(len(properties), 2, figsize=(12, len(properties) * 3), tight_layout=True)
fig.suptitle("Drivetrain Data Comparison for Left and Right Sides", fontsize=16)

# Plot properties for left and right sides
for i, prop in enumerate(properties):
    if prop in left_data:  # Check if property exists in left_data
        axes[i, 0].plot(left_data["voltage"], left_data.get(prop, []), label=f"Left {prop.capitalize()}", color='blue')
        axes[i, 0].set_title(f"Left {prop.capitalize()}")
        axes[i, 0].set_xlabel("Voltage")
        axes[i, 0].set_ylabel(prop.capitalize())
        axes[i, 0].grid(True)

    if prop in right_data:  # Check if property exists in right_data
        axes[i, 1].plot(right_data["voltage"], right_data.get(prop, []), label=f"Right {prop.capitalize()}",
                        color='orange')
        axes[i, 1].set_title(f"Right {prop.capitalize()}")
        axes[i, 1].set_xlabel("Voltage")
        axes[i, 1].set_ylabel(prop.capitalize())
        axes[i, 1].grid(True)

# Adjust layout for better utilization of space
plt.tight_layout()
plt.subplots_adjust(top=0.93)  # Leave space for the main title

# Show the plot
plt.show()