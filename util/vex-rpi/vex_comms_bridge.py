import time

import socket

import serial

import serial.tools.list_ports
import binascii


class DeviceNotFound(serial.SerialException):
    pass


# Parameters to determine if a device is a Vex Brain communications Port
VEX_BRAIN_PROGRAMMER_PORT_VID = 10376 
VEX_BRAIN_PROGRAMMER_PORT_PID = 1281
VEX_BRAIN_PROGRAMMER_PORT_DESCRIPTION = "VEX Robotics User Port"
VEX_BRAIN_PROGRAMMER_PORT_BAUD_RATE = 115200
VEX_BRAIN_PROGRAMMER_PORT_TIMEOUT = 5
VEX_BRAIN_PROGRAMMER_PORT = None

# Socket parameters
HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
PORT = 7777  # Port to listen on (non-privileged ports are > 1023)


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


serial_connection = serial.Serial(VEX_BRAIN_PROGRAMMER_PORT, VEX_BRAIN_PROGRAMMER_PORT_BAUD_RATE, timeout=VEX_BRAIN_PROGRAMMER_PORT_TIMEOUT)
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

while True:
    conn, addr = socket.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            result = get()  # Get any data from the vex brain
            data = conn.recv(1024)  # Get data from the client to send to the vex brain
            if not data:
                break
            conn.sendall(result)
            write(data + b"\n")