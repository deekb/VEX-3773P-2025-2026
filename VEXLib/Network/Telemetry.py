from VEXLib.Threading.SafeList import SafeList
from .Constants import FILE_TERMINATION_CHARACTER
from vex import *
import sys

brain = Brain()


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
