import io
import json
import random
import sys

from VEXLib.Robot.TickBasedRobot import TickBasedRobot
from VEXLib.Util.MD5sum import md5sum_file
from vex import Thread, wait, MSEC


class SerialCommunication:
    def __init__(self, tx_port, rx_port):
        self.tx_port = open(tx_port, "wb")
        self.rx_port = open(rx_port, "rb")
        self.transmits = []
        self.receives = []
        self.receive_thread = Thread(self.receive_loop)
        self.transmit_thread = Thread(self.transmit_loop)

    def process_transmits(self):
        if self.transmits:
            self.tx_port.write(self.transmits.pop(0) + "\n")

    def process_receives(self):
        got = self.rx_port.read(1024)
        if got:
            self.receives.append(got.decode())

    def send(self, message):
        self.transmits.append(message)

    def receive(self, block=False):
        if block:
            while not self.receives:
                pass
        if self.receives:
            received = self.receives.pop(0)
            if received.endswith("\n"):
                received = received[:-1]
            return received
        return None

    def peek(self, block=False):
        if self.receives:
            return self.receives[-1]
        else:
            return None

    def peek_buffer(self, block=False):
        if self.receives:
            return "".join(self.receives)
        else:
            return None

    def transmit_loop(self):
        while True:
            self.process_transmits()

    def receive_loop(self):
        while True:
            self.process_receives()


class ErrorHandledRobot(TickBasedRobot):
    def __init__(self, brain):
        super().__init__(brain)
        self.serial_communication = SerialCommunication("/dev/port1", "/dev/port2")

    def start(self):
        try:
            super().start()
        except Exception as e:
            exception_buffer = io.StringIO()
            sys.print_exception(e, exception_buffer)
            while True:
                self.serial_communication.send(
                    str(exception_buffer.getvalue())[:-1]
                    + "".join([str(hex(random.randint(0, 16))) for _ in range(16)])
                    + "\n"
                )
                wait(1000, MSEC)


def file_hash(filepath):
    try:
        return md5sum_file(filepath)
    except OSError:
        return None


def get_file_hashes(filenames):
    """Generate dictionary of file hashes on the robot."""
    hashes = {}
    for file in filenames:
        hashes[file] = file_hash(file) or "MISSING"
    return hashes


class Robot(ErrorHandledRobot):
    def __init__(self, brain):
        super().__init__(brain)

    def start(self):
        self.brain.screen.print("Startup")
        while True:
            wait(20, MSEC)
            data = self.serial_communication.peek_buffer(True)
            if not data:
                continue
            print(data)

            if data.startswith("FILES"):
                print("STARTS WITH FILES")
                # Compute and send local file hashes
                try:
                    files = eval(data.split(" ", 1)[1])
                except SyntaxError:
                    print("SyntaxError while processing FILES, continuing")
                    continue
                print(files)
                print("Getting my hashes...")
                files_hashes = get_file_hashes(files)
                print(files_hashes)
                print("Sending hashes")
                self.serial_communication.tx_port.write(
                    ("HASHES " + json.dumps(files_hashes)[:100]).encode()
                )
                self.serial_communication.tx_port.write(
                    (json.dumps(files_hashes)[100:] + "\n").encode()
                )
                self.serial_communication.receives = []

            elif data.startswith("UPLOAD"):
                try:
                    parts = data.split(" ", 2)
                    filename, size = parts[1], int(parts[2])
                except ValueError:
                    pass

                # Receive and save the file
                with open(filename, "wb") as f:
                    while size > 0:
                        chunk = self.serial_communication.receive()
                        f.write(chunk)
                        size -= len(chunk)
                self.serial_communication.send("RECEIVED " + str(filename))
