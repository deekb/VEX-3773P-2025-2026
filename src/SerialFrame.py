from math import log, ceil, floor
from CRC import crc_bytes

# TODO: Ensure 0xA (\n) won't screw up transmission

def byte_count(integer):
    return ceil(log(integer + 1, 16))


def quad_count(integer):
    return ceil(byte_count(integer) / 2)


def split_int_to_bytes(bytes_, length=16):
    output_bytes = bytes()

    for _ in range(0, floor(quad_count(bytes_))):
        quad = bytes_ & 0xff
        output_bytes = bytes([quad]) + output_bytes
        bytes_ >>= 8
    return output_bytes


def hex_format(bytes_):
    return bytes_.hex().upper()


from math import log, ceil, floor
from CRC import crc_bytes

# Constants
FRAME_HEADER = split_int_to_bytes(0xEB90)
FRAME_HEADER_SIZE = 2  # 16 bits or 2 bytes
FRAME_TYPE_SIZE = 1  # 4 bits or part of a byte
DATA_LENGTH_SIZE = 2  # 12 bits or 2 bytes
FRAME_ID_SIZE = 2  # 16 bits or 2 bytes
CRC_SIZE = 4  # 32 bits or 4 bytes

MAX_DATA_SIZE = 512  # 4096 bits or 512 bytes


class FrameType:
    CONFIGURATION = 0x1
    COMMAND = 0x2
    DATA = 0x3
    ACK = 0x8
    NACK = 0x9
    ERROR = 0xA


class Frame:
    def __init__(self):
        # Start with enough space for header, type, data length, frame ID, but no data initially
        self.data = bytearray(FRAME_HEADER_SIZE + FRAME_TYPE_SIZE + DATA_LENGTH_SIZE + FRAME_ID_SIZE + CRC_SIZE)
        self.payload = bytearray()  # This will store the actual data payload
        self._frame_id = 0  # Initial frame ID

    @property
    def bytes(self):
        # Return the full frame (header + type + data + CRC)
        return self.data[:-CRC_SIZE] + self.payload + self.data[-CRC_SIZE:]

    @bytes.setter
    def bytes(self, bytes_):
        # Allows setting the entire byte sequence if necessary
        self.data = bytearray(bytes_[:len(self.data) - CRC_SIZE])
        self.payload = bytearray(bytes_[len(self.data) - CRC_SIZE:-CRC_SIZE])
        self.data[-CRC_SIZE:] = bytes_[-CRC_SIZE:]

    @property
    def frame_header(self):
        return self.data[0:FRAME_HEADER_SIZE]

    @frame_header.setter
    def frame_header(self, value):
        self.data[0:FRAME_HEADER_SIZE] = value

    @property
    def frame_type(self):
        return (self.data[FRAME_HEADER_SIZE] >> 4) & 0xF

    @frame_type.setter
    def frame_type(self, value):
        value = (value & 0xF) << 4
        self.data[FRAME_HEADER_SIZE] = value | (self.data[FRAME_HEADER_SIZE] & 0x0F)

    @property
    def data_length(self):
        length_bytes = self.data[
                       FRAME_HEADER_SIZE + FRAME_TYPE_SIZE: FRAME_HEADER_SIZE + FRAME_TYPE_SIZE + DATA_LENGTH_SIZE]
        return int.from_bytes(length_bytes, byteorder='big') & 0xFFF  # 12-bit data length

    @data_length.setter
    def data_length(self, value):
        # Data length is 12 bits, store it in 2 bytes
        value = value & 0xFFF
        length_bytes = value.to_bytes(DATA_LENGTH_SIZE, byteorder='big')
        self.data[
        FRAME_HEADER_SIZE + FRAME_TYPE_SIZE: FRAME_HEADER_SIZE + FRAME_TYPE_SIZE + DATA_LENGTH_SIZE] = length_bytes

    @property
    def frame_id(self):
        frame_id_bytes = self.data[FRAME_HEADER_SIZE + FRAME_TYPE_SIZE + DATA_LENGTH_SIZE:
                                   FRAME_HEADER_SIZE + FRAME_TYPE_SIZE + DATA_LENGTH_SIZE + FRAME_ID_SIZE]
        return int.from_bytes(frame_id_bytes, byteorder='big')

    @frame_id.setter
    def frame_id(self, value):
        # Frame ID is 16 bits
        value = value & 0xFFFF
        frame_id_bytes = value.to_bytes(FRAME_ID_SIZE, byteorder='big')
        self.data[FRAME_HEADER_SIZE + FRAME_TYPE_SIZE + DATA_LENGTH_SIZE:
                  FRAME_HEADER_SIZE + FRAME_TYPE_SIZE + DATA_LENGTH_SIZE + FRAME_ID_SIZE] = frame_id_bytes

    @property
    def crc(self):
        # Return the CRC part of the frame
        return self.data[-CRC_SIZE:]

    @crc.setter
    def crc(self, value):
        self.data[-CRC_SIZE:] = value

    def calculate_crc(self):
        # Calculate CRC over the entire frame excluding the CRC bytes
        crc_value = crc_bytes(self.data[:-CRC_SIZE] + self.payload)
        self.crc = crc_value.to_bytes(CRC_SIZE, byteorder='big')

    def set_data(self, payload):
        """Sets the data payload and adjusts the frame."""
        if len(payload) > MAX_DATA_SIZE:
            raise ValueError(f"Data payload cannot exceed {MAX_DATA_SIZE} bytes.")

        # Set the data payload and update the data length
        self.payload = bytearray(payload)
        self.data_length = len(self.payload)

        # After setting data, we need to recalculate the CRC
        self.calculate_crc()

    def prepare_frame(self, frame_type, frame_id=None):
        # Set basic frame components
        self.frame_header = FRAME_HEADER
        self.frame_type = frame_type

        # Handle frame ID
        if frame_id is None:
            frame_id = self._frame_id
            self._frame_id = (self._frame_id + 1) & 0xFFFF  # Auto-increment with wrap-around
        self.frame_id = frame_id

        # Calculate and set CRC (after setting data)
        self.calculate_crc()


# Example usage
frame = Frame()
frame.prepare_frame(FrameType.COMMAND)
frame.set_data(b'This is a test message')
bytes_ = frame.bytes
print(bytes_)
print(bytes_.hex().upper())
