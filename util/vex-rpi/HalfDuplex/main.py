import threading

from serial_connection import SerialConnection
from config import VEX_BRAIN_PROGRAMMER_PORT
from network_socket import NetworkSocket
from connection_synchronizer import ConnectionSynchronizer
from data_relay import socket_to_serial, serial_to_socket
from logger import log

def main():
    # Initialize objects
    connection_synchronizer = ConnectionSynchronizer()
    serial_connection = SerialConnection(device_path=VEX_BRAIN_PROGRAMMER_PORT)
    network_socket = NetworkSocket()

    # Find VEX Brain device
    if not serial_connection.find_vex_brain():
        log(f"[main]: Could not find device at {VEX_BRAIN_PROGRAMMER_PORT}, aborting.")
        return

    # Start Network Socket Listener
    network_socket.start_listener()

    # Wait for client connection
    network_socket.establish_connection()

    # Establish Serial Connection
    if not serial_connection.establish_connection():
        log("[main]: Serial connection could not be established.")
        return

    # Set connection state to connected
    connection_synchronizer.set_both_connected()

    # Start data relay threads
    socket_to_serial_thread = threading.Thread(target=socket_to_serial,
                                               args=(network_socket, serial_connection, connection_synchronizer))
    serial_to_socket_thread = threading.Thread(target=serial_to_socket,
                                               args=(network_socket, serial_connection, connection_synchronizer))
    socket_to_serial_thread.start()
    serial_to_socket_thread.start()
    socket_to_serial_thread.join()
    serial_to_socket_thread.join()


if __name__ == "__main__":
    main()
