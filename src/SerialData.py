from math import log, ceil, floor


class FrameType:
    CONFIGURATION = 0x1
    COMMAND = 0x2
    DATA = 0x3
    ACK = 0x8
    NACK = 0x9
    ERROR = 0xA


class ConfigurationFunction:
    SET_BAUD_RATE = 0x1
    SET_ACK_TIMEOUT = 0x2
    TRANSMIT_TOKEN = 0x3


class CommandFunction:
    QUERY_FILE = 0x1
    QUERY_FILE_CRC = 0x2
    RECEIVE_FILE = 0x3
    TRANSMIT_FILE = 0x4


def byte_count(integer):
    return ceil(log(integer + 1, 16))


def quad_count(integer):
    return ceil(byte_count(integer) / 2)


def split_int_to_bytes(bytes_, length=16):
    output_bytes = bytes()

    for _ in range(0, floor(quad_count(bytes_))):
        quad = bytes_ & 0xFF
        output_bytes = bytes([quad]) + output_bytes
        bytes_ >>= 8
    return output_bytes


def hex_format(bytes_):
    return bytes_.hex().upper()


class Frame:
    def __init__(
        self,
        frame_header=None,
        frame_type=None,
        data_length=None,
        frame_id=None,
        data=None,
        crc_function=None,
    ):
        self.frame_header = frame_header
        self._frame_type = frame_type
        self._data_length = data_length
        self.frame_id = frame_id
        self._frame_format_int = 0
        self._frame_format_bytes = bytes()
        self.data = data
        self.crc_function = crc_function
        self.crc = bytes()
        self._update_frame_format()
        self._update_crc()

    def _update_frame_format(self):
        frame_format_int = ((self._frame_type & 0xF) << 12) | (
            self._data_length & 0xFFF
        )

        self._frame_format_bytes = split_int_to_bytes(frame_format_int)

    def _update_data_length(self):
        self._data_length = self._frame_format_int & 0xFFF

    def _update_frame_type(self):
        self._frame_type = (self._frame_format_int >> 12) & 0xF

    @property
    def frame_format(self):
        return self._frame_format_int

    @frame_format.setter
    def frame_format(self, frame_format):
        self._frame_format_int = frame_format
        self._frame_format_bytes = split_int_to_bytes(frame_format)
        self._update_frame_type()
        self._update_data_length()

    def frame_format_bytes(self):
        return self._frame_format_bytes

    @property
    def data_length(self):
        return self._data_length

    @data_length.setter
    def data_length(self, data_length):
        self._data_length = data_length
        self._update_frame_format()

    @property
    def frame_type(self):
        return self._frame_type

    @frame_type.setter
    def frame_type(self, frame_type):
        self._frame_type = frame_type
        self._update_frame_format()

    def _update_crc(self):
        self.crc = split_int_to_bytes(self.crc_function(self.data))

    def get_bytearray(self):
        header = bytes(self.frame_header)
        format_ = self.frame_format_bytes()

        output = header + format_ + self.data + self.crc

        # print()
        # print(' - '.join([hex_format(header), hex_format(format_), hex_format(self.data), hex_format(self.crc)]))
        # print(' - '.join(['HEAD', 'FORM', 'DATA', ' '*(len(hex_format(self.data))-7), 'CRC']))
        # print()

        return output


#
# message = "this is my random message"
#
# frame = Frame(frame_header=split_int_to_bytes(0xEB90),
#               frame_type=FrameType.DATA,
#               data_length=len(message),
#               frame_id=1,
#               data=bytes(message, "ISO-8859-1"),
#               crc_function=crc_bytes)
#
# frame_bytes = (frame.get_bytearray())
# print(f"Message is {len(message)} bytes")
# print(f"Frame is {len(frame_bytes)} bytes")
# print(hex_format(frame_bytes))
# print(frame_bytes)
