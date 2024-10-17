import matplotlib.pyplot as plt

# Read data from file
data = []
with open("PID_test.txt", "r") as file:
    for line in file:
        if line.startswith("PIDF:"):
            measurement = {}
            entries = line.split(":")
            entries = entries[1:]  # Discard PIDF header
            
            for entry in entries:
                name, value = entry.split("=")
                measurement[name] = float(value)

            data.append(measurement)

timestamps = range(len(data))

names = data[0].keys()

# Plotting
plt.figure(figsize=(10, 6))

for name in names:
    plt.plot(timestamps, [entry[name] for entry in data], label=name)
plt.xlabel("Time")
plt.ylabel("Value")
plt.title("Controller Parameters Over Time")
plt.legend()
plt.grid(True)
plt.show()

