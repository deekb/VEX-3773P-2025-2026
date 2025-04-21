# CRC-CCITT (XModem) algorithm parameters
POLYNOMIAL = 0x1021  # Polynomial used for CRC calculations
PRESET = 0  # Initial preset value for the CRC register


def _initial(byte):
    """
    Compute the initial CRC for a given byte. This creates a lookup table entry
    for faster CRC calculation in the main loop.

    Args:
        byte (int): The byte for which to compute the initial CRC.

    Returns:
        int: The computed CRC value.
    """
    crc = 0
    byte = byte << 8  # Shift byte to align it with CRC register
    for _ in range(8):  # Process each bit in the byte
        if (crc ^ byte) & 0x8000:  # Check if the MSB differs
            crc = (crc << 1) ^ POLYNOMIAL  # Shift left and XOR with the polynomial
        else:
            crc = crc << 1  # Just shift left if no difference
        byte = byte << 1  # Shift the input byte to the next bit
    return crc


# Precompute a lookup table for fast CRC calculation
crc_lookup_table = [_initial(i) for i in range(256)]


def _update_crc(crc, byte):
    """
    Update the current CRC value with a new byte.

    Args:
        crc (int): The current CRC value.
        byte (int): The next byte to process.

    Returns:
        int: The updated CRC value.
    """
    byte = 0xFF & byte  # Mask the byte to ensure it is 8 bits

    # XOR the higher byte of the CRC with the new byte
    tmp = (crc >> 8) ^ byte
    crc = (crc << 8) ^ crc_lookup_table[tmp & 0xFF]  # Lookup table for speed

    # Ensure CRC stays within 16 bits
    crc = crc & 0xFFFF
    return crc


def crc_string(data):
    """
    Calculate the CRC for a string.

    Args:
        data (str): The input string for which to calculate the CRC.

    Returns:
        int: The computed CRC value.
    """
    crc = PRESET  # Start with the preset value
    for char in data:  # Process each character in the string
        crc = _update_crc(crc, ord(char))  # Convert character to byte and update CRC
    return crc


def crc_bytes(bytes_data):
    """
    Calculate the CRC for a sequence of bytes.

    Args:
        bytes_data (list of int): A variable number of bytes to calculate the CRC for.

    Returns:
        int: The computed CRC value.
    """
    crc = PRESET  # Start with the preset value
    for byte in bytes_data:  # Process each byte in the input
        crc = _update_crc(crc, byte)
    return crc
