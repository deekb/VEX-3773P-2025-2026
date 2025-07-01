# Define a constant for the start byte (16 bits)
START_BYTE = 0xEB90

# Define the length of each element of the frame in a dictionary
FRAME_ELEMENT_LENGTHS = {
    "start_byte": 2,  # 16 bits = 2 bytes
    "frame_id": 4,  # 32 bits = 4 bytes
    "length": 4,  # 32 bits = 4 bytes
    "frame_type": 1,  # 8 bits = 1 byte
    "data_type_length": 1,  # 8 bits = 1 byte (length of data_type)
    "data_type": None,  # Variable length, determined by data_type
    "data": None,  # Variable length, determined by the data length
    "crc": 2,  # 16 bits = 2 bytes
}


class FrameType(object):
    """Class representing frame types."""

    INVALID = 0x0
    CONFIGURATION = 0x1
    COMMAND = 0x2
    DATA = 0x3
    RESERVED_1 = 0x4
    RESERVED_2 = 0x5
    RESERVED_3 = 0x6
    RESERVED_4 = 0x7
    ACKNOWLEDGE = 0x8
    NEGATIVE_ACKNOWLEDGE = 0x9
    FRAME_ERROR = 0xA
    RESERVED_5 = 0xB
    RESERVED_6 = 0xC
    RESERVED_7 = 0xD
    RESERVED_8 = 0xE
    INVALID_2 = 0xF


def crc_xmodem(data: bytes) -> int:
    """Calculate the CRC XMODEM checksum (16-bit)."""
    crc = 0x0000
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021  # XMODEM polynomial
            else:
                crc <<= 1
            crc &= 0xFFFF  # Keep CRC as a 16-bit value
    return crc


class SerialFrame:
    def __init__(self, frame_id: int, frame_type: int, data_type: str, data: bytes):
        self.frame_id = frame_id
        self.frame_type = frame_type
        self.data_type = data_type
        self.data = data

    @property
    def length(self) -> int:
        """Get the length of the data."""
        return len(self.data)

    def to_bytes(self) -> bytes:
        """Convert the frame to a byte representation for transmission."""
        start_byte_bytes = START_BYTE.to_bytes(
            FRAME_ELEMENT_LENGTHS["start_byte"], "big"
        )
        frame_id_bytes = self.frame_id.to_bytes(
            FRAME_ELEMENT_LENGTHS["frame_id"], "big"
        )
        length_bytes = self.length.to_bytes(FRAME_ELEMENT_LENGTHS["length"], "big")

        data_type_bytes = self.data_type.encode("utf-8")
        data_type_length = len(data_type_bytes).to_bytes(
            FRAME_ELEMENT_LENGTHS["data_type_length"], "big"
        )
        data_type_full = data_type_length + data_type_bytes

        frame_type_bytes = self.frame_type.to_bytes(
            FRAME_ELEMENT_LENGTHS["frame_type"], "big"
        )  # Add frame type byte

        # Concatenate the components before calculating the CRC
        frame_bytes = (
            start_byte_bytes
            + frame_id_bytes
            + length_bytes
            + frame_type_bytes
            + data_type_full
            + self.data
        )

        # Calculate the CRC XMODEM checksum
        crc = crc_xmodem(frame_bytes)
        crc_bytes = crc.to_bytes(FRAME_ELEMENT_LENGTHS["crc"], "big")

        return frame_bytes + crc_bytes

    @classmethod
    def from_bytes(cls, byte_data: bytes) -> "SerialFrame":
        """Create a SerialFrame instance from byte data and verify the checksum."""
        start_byte_length = FRAME_ELEMENT_LENGTHS["start_byte"]
        frame_id_length = FRAME_ELEMENT_LENGTHS["frame_id"]
        length_length = FRAME_ELEMENT_LENGTHS["length"]
        frame_type_length = FRAME_ELEMENT_LENGTHS["frame_type"]
        crc_length = FRAME_ELEMENT_LENGTHS["crc"]

        # Minimum frame size check before proceeding with parsing
        min_frame_size = (
            start_byte_length + frame_id_length + length_length + frame_type_length + 1
        )  # Add 1 byte for data_type_length field
        if len(byte_data) < min_frame_size:
            raise ValueError(
                "Incomplete frame: Expected at least %d bytes, got %d"
                % (min_frame_size, len(byte_data))
            )

        start_index = byte_data.find(START_BYTE.to_bytes(start_byte_length, "big"))
        if start_index == -1:
            raise ValueError(
                "Start byte not found in the data. Data: %s..." % str(byte_data[:30])
            )

        # Extract frame_id (4 bytes)
        frame_id = int.from_bytes(
            byte_data[
                start_index
                + start_byte_length : start_index
                + start_byte_length
                + frame_id_length
            ],
            "big",
        )

        # Extract length (4 bytes)
        length = int.from_bytes(
            byte_data[
                start_index
                + start_byte_length
                + frame_id_length : start_index
                + start_byte_length
                + frame_id_length
                + length_length
            ],
            "big",
        )

        # Check if there's enough data for the full frame including the payload and CRC
        full_frame_size = min_frame_size + length + crc_length  # Total size of frame
        if len(byte_data) < full_frame_size:
            raise ValueError(
                "Incomplete frame: Expected %d bytes, got %d"
                % (full_frame_size, len(byte_data))
            )

        # Extract frame_type (1 byte)
        frame_type = byte_data[
            start_index + start_byte_length + frame_id_length + length_length
        ]

        # Extract data_type_length (1 byte) and the data_type itself
        data_type_length = byte_data[
            start_index
            + start_byte_length
            + frame_id_length
            + length_length
            + frame_type_length
        ]
        data_type_start = (
            start_index
            + start_byte_length
            + frame_id_length
            + length_length
            + frame_type_length
            + 1
        )
        data_type_end = data_type_start + data_type_length
        data_type = byte_data[data_type_start:data_type_end].decode("utf-8")

        # Extract the data (variable length based on 'length')
        data_start = data_type_end
        data = byte_data[data_start : data_start + length]

        # Extract the checksum (last 2 bytes)
        received_crc = int.from_bytes(
            byte_data[data_start + length : data_start + length + crc_length], "big"
        )

        # Recalculate the CRC for the frame data (excluding the received CRC)
        frame_bytes = byte_data[start_index : data_start + length]
        calculated_crc = crc_xmodem(frame_bytes)

        # Verify if the received CRC matches the calculated CRC
        if received_crc != calculated_crc:
            raise ValueError(
                "Checksum mismatch! Received: %d, Calculated: %d"
                % (received_crc, calculated_crc)
            )

        # If checksums match, create and return the SerialFrame object
        return cls(
            frame_id=frame_id, frame_type=frame_type, data_type=data_type, data=data
        )

    def __str__(self) -> str:
        """Return a string representation of the frame."""
        return (
            "Frame ID: %d, Frame Type: %d, Length: %d bytes, Data Type: %s, Data: %s"
            % (self.frame_id, self.frame_type, self.length, self.data_type, self.data)
        )
