from logger import log
import socket
import traceback


def socket_to_serial(network_socket, serial_connection, connection_synchronizer):
    while True:
        if connection_synchronizer.get_both_connected() and not connection_synchronizer.get_any_restart_requested():
            try:
                received = network_socket.receive_message()
                if received is None:
                    log("[socket_to_serial]: Got empty packet, socket is disconnected")
                    connection_synchronizer.network_socket_is_connected = False
                    log(f"[socket_to_serial]: Informed connection_synchronizer that the network socket was disconnected")
                    break
                elif received == "RPI:RESTART_BRIDGE":
                    log("[socket_to_serial]: Got RPI:RESTART_BRIDGE")
                    connection_synchronizer.bridge_restart_requested = True
                elif received == "RPI:RESTART":
                    log("[socket_to_serial]: Got RPI:RESTART")
                    connection_synchronizer.rpi_restart_requested = True
            except (TimeoutError, socket.timeout):
                log("[socket_to_serial]: timeout while getting data from network socket")
                continue
            except ConnectionResetError:
                log(f"[socket_to_serial]: Connection reset in network_socket.receive_message: {traceback.format_exc()}")
                connection_synchronizer.network_socket_is_connected = False
                log(f"[socket_to_serial]: Informed connection_synchronizer that the network socket was disconnected")
                break
            except Exception:
                log(f"[socket_to_serial]: Critical error in network_socket.receive_message: {traceback.format_exc()}")
                connection_synchronizer.network_socket_is_connected = False
                log(f"[socket_to_serial]: Informed connection_synchronizer that the network socket was disconnected")
                break
            try:
                if self.
                serial_connection.send_message(received)
            except Exception:
                log(f"[socket_to_serial]: Critical error in serial_connection.send_message: {traceback.format_exc()}")
                connection_synchronizer.serial_is_connected = False
                log(f"[socket_to_serial]: Informed connection_synchronizer that the serial connection was disconnected")
                break
        else:
            log("[socket_to_serial]: connection_synchronizer says to terminate")
            break
    log("[socket_to_serial]: Terminating")


def serial_to_socket(network_socket, serial_connection, connection_synchronizer):
    while True:
        if connection_synchronizer.get_both_connected() and not connection_synchronizer.get_any_restart_requested():
            try:
                received = serial_connection.get_message()
                if not received:
                    log("[serial_to_socket]: timeout while getting data from serial connection")
                    continue
            except Exception:
                log(f"[serial_to_socket]: Critical error in serial_connection.get_message: {traceback.format_exc()}")
                connection_synchronizer.serial_is_connected = False
                log(f"[serial_to_socket]: Informed connection_synchronizer that the serial connection was disconnected")
                break
            try:
                network_socket.send_message(received)
            except BrokenPipeError:
                log(f"[serial_to_socket]: Broken pipe in network_socket.send_message")
                connection_synchronizer.network_socket_is_connected = False
                log(f"[serial_to_socket]: Informed connection_synchronizer that the network socket was disconnected")
                break
            except Exception:
                log(f"[serial_to_socket]: Critical error in network_socket.send_message: {traceback.format_exc()}")
                connection_synchronizer.network_socket_is_connected = False
                log(f"[serial_to_socket]: Informed connection_synchronizer that the network socket was disconnected")
                break
        else:
            log("[serial_to_socket]: connection_synchronizer says to terminate")
            break
    log("[serial_to_socket]: Terminating")
