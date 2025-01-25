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
fig, axes = plt.subplots(len(properties), 1, figsize=(8, len(properties) * 3), tight_layout=True)
# fig.suptitle("Drivetrain Data Comparison for Left and Right Sides", fontsize=16)

# Plot properties for left and right sides
for i, prop in enumerate(properties):
    if prop in left_data:  # Check if property exists in left_data
        axes[i].plot(left_data["voltage"], left_data.get(prop, []), label=f"Left {prop.capitalize()}", color='blue')

    if prop in right_data:  # Check if property exists in right_data
        axes[i].plot(right_data["voltage"], right_data.get(prop, []), label=f"Right {prop.capitalize()}",
                     color='orange')

    axes[i].set_title(f"{prop.capitalize()} Comparison")
    axes[i].set_xlabel("Voltage")
    axes[i].set_ylabel(prop.capitalize())
    axes[i].legend()
    axes[i].grid(True)

# Adjust layout for better utilization of space
plt.tight_layout()
plt.subplots_adjust(top=0.93)  # Leave space for the main title

# Adjust the figure size to fit 8.5x11 paper (in inches)
fig.set_size_inches(8.5, 8.5)

# Save the figure as a PDF file
pdf_output_filename = 'drivetrain_comparison.pdf'
plt.savefig(pdf_output_filename, format='pdf', bbox_inches='tight')

# Save the figure as a high-resolution PNG file (1600 DPI)
png_output_filename = 'drivetrain_comparison.png'
plt.savefig(png_output_filename, format='png', dpi=190, bbox_inches='tight')

# Optionally display the plot (not necessary for just exporting to files)
plt.show()