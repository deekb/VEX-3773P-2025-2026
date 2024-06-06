import socket
import time
import threading
import queue
from .config import *

class NetworkHandler:
    def __init__(self, host, port, log_window):
        self.host = host
        self.port = port
        self.log_window = log_window
        self.socket = None
        self.attempting_socket_connection = False

        self.shutdown_triggered = False

        self.last_ping_send_time_in_seconds = 0
        self.last_ping_response_time_in_milliseconds = 0
        self.last_heartbeat_time_in_seconds = 0

        self.send_queue = queue.Queue()
        self.receive_queue = queue.Queue()

        self.send_thread = threading.Thread(target=self.send_loop)
        self.receive_thread = threading.Thread(target=self.receive_loop)

    def attempt_connection(self, retry_on_failure=True):
        if self.attempting_socket_connection:
            print("[attempt_connection]: Warning: Another thread is already attempting to reconnect the socket")
            return
        self.attempting_socket_connection = True
        first_try = True
        while (first_try or retry_on_failure) and not self.shutdown_triggered:
            try:
                print("attempt connect")
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.settimeout(1)
                self.socket.connect((self.host, self.port))
                break
            except (ConnectionRefusedError, ConnectionAbortedError, socket.gaierror, OSError):
                print(f"Reconnect attempt failed, retrying in {SOCKET_RECONNECT_INTERVAL_IN_SECONDS} seconds")
                time.sleep(SOCKET_RECONNECT_INTERVAL_IN_SECONDS)
            first_try = False
        if self.shutdown_triggered:
            print("Shutdown triggered while attempting reconnection to the socket")
        else:
            self.socket.settimeout(1)
            print("Successfully reconnected to the socket")
            self.attempting_socket_connection = False

    def start_network_loop(self):
        self.attempt_connection()
        self.send_thread.start()
        self.receive_thread.start()
        while not self.shutdown_triggered:
            try:
                line = self.receive_queue.get(timeout=1)
                self.log_window.log(line, "\n")
            except queue.Empty:
                continue

    def send_message(self, message, end="\n"):
        self.send_queue.put(str(message) + str(end))

    def send_loop(self):
        while not self.shutdown_triggered:
            try:
                message = self.send_queue.get(timeout=1)
                if self.socket and not self.attempting_socket_connection:
                    self.socket.sendall(message.encode())
            except queue.Empty:
                continue
            except (ConnectionResetError, BrokenPipeError):
                if not self.attempting_socket_connection:
                    print("[send_loop]: Robot socket disconnected, attempting reconnect...")
                    self.attempt_connection()

    def receive_loop(self):
        while not self.shutdown_triggered:
            try:
                received = self.socket.recv(1024)
                if not received:
                    if not self.attempting_socket_connection:
                        print("[receive_loop]: Got no data, assuming robot socket disconnected, attempting reconnect...")
                        self.attempt_connection()
                else:
                    messages = received.decode().split("\n")
                    for message in messages:
                        self.receive_queue.put(message)
            except socket.timeout:
                continue
            except (ConnectionResetError, BrokenPipeError, OSError) as e:
                print(f"receive_loop failed: {e}")
                if not self.attempting_socket_connection:
                    print("[receive_loop]: Robot socket disconnected, attempting reconnect...")
                    self.attempt_connection()

    def ping_robot(self):
        self.send_message(PING_ROBOT_MESSAGE)
        self.last_ping_send_time_in_seconds = time.monotonic()

    def ping_rpi(self):
        self.send_message(PING_RPI_MESSAGE)
        self.last_ping_send_time_in_seconds = time.monotonic()

    def ping_robot_loop(self):
        while not self.shutdown_triggered:
            self.ping_robot()
            time.sleep(ROBOT_PING_FREQUENCY_IN_SECONDS)

    def ping_rpi_loop(self):
        while not self.shutdown_triggered:
            self.ping_rpi()
            time.sleep(RPI_PING_FREQUENCY_IN_SECONDS)

    def communications_online(self):
        return not self.attempting_socket_connection

    def robot_is_online(self, online_threshold_in_seconds=ONLINE_THRESHOLD_IN_SECONDS):
        time_since_heartbeat = (time.monotonic() - self.last_heartbeat_time_in_seconds)
        return time_since_heartbeat < online_threshold_in_seconds

    def robot_ping_time(self):
        return self.last_ping_response_time_in_milliseconds

    def restart_rpi(self):
        self.send_message("RPI:RESTART")

    def restart_robot(self):
        self.send_message("ROBOT:RESTART")

    def restart_rpi_bridge(self):
        self.send_message("RPI:RESTART_BRIDGE")

    def shutdown(self):
        self.shutdown_triggered = True
        self.send_thread.join()
        self.receive_thread.join()
        if self.socket:
            self.socket.close()
