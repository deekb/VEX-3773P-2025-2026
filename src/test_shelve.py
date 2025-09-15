# demo_robot_config.py
from shelve import Shelf

# Open (or create) the configuration file
db = Shelf("robot_config.csv")
pid_coefficients = Shelf("PID_coefficients.csv")

# Save some robot configuration values
db.set("drive_motor_ports", [1, 2, 3, 4])
db.set("arm_motor_port", 5)
db.set("pid_kp", 0.75)
db.set("pid_ki", 0.02)
db.set("pid_kd", 0.15)
db.set("max_speed", 100)     # percent
db.set("autonomous_enabled", True)
db.set("team_name", "BowBots")
db.set("config", {
    "testng": 1,
    1234: "Hello"
})

print("Configuration saved!\n")

# Later in the code (or in another program run), retrieve values
drive_ports = db.get("drive_motor_ports")
kp = db.get("pid_kp")
team = db.get("team_name")
config = db.get("config")

print(config["1234"])

print("Loaded config:")
print(" Drive motor ports:", drive_ports)
print(" PID Kp:", kp)
print(" Team:", team)

# If a value doesn't exist, supply a default
gyro_port = db.get("gyro_port", None)
print(" Gyro port:", gyro_port)

# List all keys
print("\nAll configuration keys:", db.keys())

db.close()
