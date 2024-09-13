from logger import log
import serial
import termios


class SerialConnection:
    def __init__(self, device_path, baud_rate=115200, timeout=1):
        self.device_path = device_path
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.serial_connection = None

    def find_vex_brain(self):
        try:
            serial_port = serial.Serial(port=self.device_path, baudrate=self.baud_rate, timeout=self.timeout)
            read_data = serial_port.read()
        except serial.serialutil.SerialException as err:
            log("[SerialConnection.find_vex_brain]: No device found")
            return False
        log(f"[SerialConnection.find_vex_brain]: Found device: {self.device_path}")
        return True

    def establish_connection(self):
        if not self.device_path:
            raise RuntimeError("Can't establish a connection without initializing a device first")
        try:
            self.serial_connection = serial.Serial(self.device_path, self.baud_rate, timeout=self.timeout)
            return True
        except serial.SerialException:
            return False

    def send_message(self, data, end="\n"):
        self.serial_connection.write((data + end).encode())

    def get_message(self):
        try:
            return self.serial_connection.readline().strip().decode()
        except UnicodeDecodeError:
            return

    def discard_serial_buffers(self):
        if self.serial_connection:
            try:
                self.serial_connection.reset_input_buffer()
                self.serial_connection.reset_output_buffer()
                log("[SerialConnection.discard_serial_buffers]: Discarded serial buffers")
            except termios.error:
                log("[SerialConnection.discard_serial_buffers]: termios.error while discarding serial buffers")
        else:
            log("[SerialConnection.discard_serial_buffers]: No serial connection, nothing to discard")

    def close(self):
        if self.serial_connection:
            self.serial_connection.close()
