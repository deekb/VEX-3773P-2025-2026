import csv
import json

# Input and output file paths
csv_file_path = 'input/left_drivetrain.csv'
json_file_path = 'input/left_drivetrain_3.json'

# Initialize the JSON structure
data = {
    "voltage": [],
    "power": [],
    "efficiency": [],
    "speed": [],
    "torque": []
}

# Read the CSV file and populate the JSON structure
with open(csv_file_path, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        data["voltage"].append(float(row["input_power (% of rated)"]))
        data["power"].append(float(row["output_power (W)"]))
        data["efficiency"].append(float(row["efficiency (%)"]))
        data["speed"].append(float(row["speed (% of rated)"]))
        data["torque"].append(float(row["torque (Nm)"]))

# Write the JSON structure to a file
with open(json_file_path, mode='w') as json_file:
    json.dump(data, json_file, indent=4)

print(f"CSV data has been converted to JSON and saved to {json_file_path}")