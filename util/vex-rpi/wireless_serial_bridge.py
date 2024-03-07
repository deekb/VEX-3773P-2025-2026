import time
import socket
import threading
import serial.tools.list_ports


class DeviceNotFound(serial.SerialException):
    pass


# Parameters to determine if a device is a Vex Brain communications Port
VEX_BRAIN_PROGRAMMER_PORT_VID = 10376
VEX_BRAIN_PROGRAMMER_PORT_PID = 1281
VEX_BRAIN_PROGRAMMER_PORT_DESCRIPTION = "VEX Robotics User Port"
VEX_BRAIN_PROGRAMMER_PORT_BAUD_RATE = 115200
VEX_BRAIN_PROGRAMMER_PORT_TIMEOUT = 86400
VEX_BRAIN_PROGRAMMER_PORT = None

# Socket parameters
HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
PORT = 10001  # Port to listen on (non-privileged ports are >= 1024)

# Iterate through all devices and determine which one (if any) is the vex brain
for device in serial.tools.list_ports.comports():
    if (
            device.interface == VEX_BRAIN_PROGRAMMER_PORT_DESCRIPTION
            and device.vid == VEX_BRAIN_PROGRAMMER_PORT_VID
            and device.pid == VEX_BRAIN_PROGRAMMER_PORT_PID
    ):
        VEX_BRAIN_PROGRAMMER_PORT = device.device

# Ensure that we have a device to operate on
if VEX_BRAIN_PROGRAMMER_PORT is None:
    raise DeviceNotFound(
        "Could not find an attached device with the specified properties"
    )

serial_connection = serial.Serial(VEX_BRAIN_PROGRAMMER_PORT, VEX_BRAIN_PROGRAMMER_PORT_BAUD_RATE,
                                  timeout=VEX_BRAIN_PROGRAMMER_PORT_TIMEOUT)
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((HOST, PORT))
socket.listen()


def write(data):
    global serial_connection
    serial_connection.write(data)


def get():
    global serial_connection
    received_message = serial_connection.readline().strip()
    return received_message


def split_string(long_string, n):
    """
    Splits a long string into smaller strings every n characters.

    Args:
        long_string (str): The long string to be split.
        n (int): The number of characters in each smaller string.

    Returns:
        list: A list of smaller strings.
    """
    return [long_string[i:i + n] for i in range(0, len(long_string), n)]


def get_loop():
    while True:
        try:
            result = get()  # Get any data from the vex brain
            conn.sendall(result + b"\n")
        except OSError:
            return


def send_loop():
    while True:
        try:
            data = conn.recv(1024)  # Get data from the client to send to the vex brain
        except ConnectionResetError:
            return
        if not data:
            return

        write(data)
        time.sleep(0.02)


while True:
    get_thread = threading.Thread(target=get_loop)
    send_thread = threading.Thread(target=send_loop)
    print(f"Listening for clients on {HOST}:{PORT} ...")
    conn, addr = socket.accept()

    with conn:
        print(f"Connected to {addr}")
        get_thread.start()
        send_thread.start()
        send_thread.join()
        get_thread.join()
