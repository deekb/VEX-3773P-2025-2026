import socket
import threading
import time

# Socket parameters
HOST = "192.168.1.1"
PORT = 10002  # Port to connect to (non-privileged ports are >= 1024)
SOCKET_RECONNECT_INTERVAL_IN_SECONDS = 1


class NetworkHandler:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None
        self.attempting_socket_connection = False
        self.shutdown_triggered = False

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
        while not self.shutdown_triggered:
            received = self.get_message()
            if not received:
                continue

            for line in received:
                if not line:
                    continue
                print(line)

    def send_message(self, message, end="\n"):
        if self.attempting_socket_connection or self.socket is None:
            return  # No socket connected
        try:
            self.socket.sendall((str(message) + str(end)).encode())
        except (ConnectionResetError, BrokenPipeError):
            if not self.attempting_socket_connection:
                print("[send_message]: Robot socket disconnected, attempting reconnect...")
                self.attempt_connection()

    def get_message(self):
        try:
            received = self.socket.recv(1024)
            if not received:
                if not self.attempting_socket_connection:
                    print("[get_messages]: Got no data, assuming robot socket disconnected, attempting reconnect...")
                    self.attempt_connection()
            return received.decode().split("\n")
        except socket.timeout:
            pass
        except (ConnectionResetError, BrokenPipeError, OSError,) as e:
            print(f"get_messages failed: {e}")
            if not self.attempting_socket_connection:
                print("[get_messages]: Robot socket disconnected, attempting reconnect...")
                self.attempt_connection()

    def shutdown(self):
        self.shutdown_triggered = True


if __name__ == "__main__":
    network_handler = NetworkHandler(HOST, PORT)
    network_thread = threading.Thread(target=network_handler.start_network_loop)

    try:
        network_thread.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    print("Exiting")
    network_handler.shutdown()
