from VEXLib.Robot.NewTickBasedRobot import TickBasedRobot
from VEXLib.Util.ContinuousTimer import time
from SerialFrame import SerialFrame, FrameType
from vex import Thread


class SerialCommunication:
    def __init__(self, tx_port, rx_port):
        self.tx_port = open(tx_port, "wb")
        self.rx_port = open(rx_port, "rb")
        self.transmits = []
        self.receives = []
        self.thread = Thread(self._mainloop)

    def _mainloop(self):
        while True:
            self._tick()

    def process_transmits(self):
        if self.transmits:
            self.tx_port.write(self.transmits.pop(0))

    def process_receives(self):
        got = self.rx_port.read(1024)
        if got:
            self.receives.append(got)

    def send(self, message):
        self.transmits.append(message)

    def receive(self, block=False):
        if block:
            while not self.receives:
                pass
        if self.receives:
            return self.receives.pop(0)
        return None

    def _tick(self):
        self.process_transmits()
        self.process_receives()


class Robot(TickBasedRobot):
    def __init__(self, brain, autonomous):
        super().__init__(brain)
        self.serial_communication = SerialCommunication("/dev/port2", '/dev/port1"')
        self.time = time()
        self.serial_communication.send("Hello World")
        self.input_buffer = b""
        self._target_tick_duration_ms = 5
        self._warning_tick_duration_ms = 10

    def periodic(self):
        # print(self.serial_communication.receives)
        self.input_buffer += self.serial_communication.receive(True)
        try:
            received = SerialFrame.from_bytes(self.input_buffer)
            ack_frame = SerialFrame(
                frame_id=received.frame_id,
                frame_type=FrameType.ACKNOWLEDGE,
                data_type='ACK',
                data=b"ACK"
            )
            self.serial_communication.send(ack_frame.to_bytes())
            self.input_buffer = b""
        except ValueError:
            pass


