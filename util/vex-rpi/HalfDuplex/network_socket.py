from logger import log
import atexit
import socket


class NetworkSocket:
    def __init__(self, host="0.0.0.0", port=10002, buffer_size=1024, timeout=1):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.timeout = timeout
        self.socket = None
        self.connection = None
        self.client_address = None

    def start_listener(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        log(f"[NetworkSocket.start_listener] Listening for client at {self.host}:{self.port}")

    def establish_connection(self):
        log(f"[NetworkSocket.start_listener] Waiting for client to connect")
        self.connection, self.client_address = self.socket.accept()
        self.connection.settimeout(self.timeout)
        log(f"[NetworkSocket.start_listener] Connected to client at {self.client_address[0]}:{self.client_address[1]}")
        atexit.register(self.close)

    def send_message(self, message, end="\n"):
        self.connection.sendall((message + end).encode())

    def receive_message(self):
        received = self.connection.recv(self.buffer_size).decode()
        if received == "":
            return None
        return received.strip("\n")

    def close(self):
        if self.socket:
            self.socket.close()
