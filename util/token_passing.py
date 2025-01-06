class Device:
    def __init__(self, name):
        self.name = name
        self.has_token = False

    def send_data(self, data):
        if self.has_token:
            print(f"{self.name} is sending data: {data}")
            self.has_token = False
        else:
            print(f"{self.name} cannot send data without the token.")

    def receive_token(self):
        self.has_token = True
        print(f"{self.name} received the token.")

    def pass_token(self, other_device):
        print(f"{self.name} is passing the token to {other_device.name}.")
        other_device.receive_token()


# Initialize two devices
device_A = Device("Device A")
device_B = Device("Device B")

# Start the token with Device A
device_A.receive_token()

# Device A sends data
device_A.send_data("Hello from A")
# Device B sends data without token
device_B.send_data("Hello from B")

# Device A passes the token to Device B
device_A.pass_token(device_B)

# Device B sends data
device_B.send_data("Hello from B")

# Device B passes the token back to Device A
device_B.pass_token(device_A)

# Device A sends data again
device_A.send_data("Goodbye from A")
