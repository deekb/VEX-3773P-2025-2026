from src.SerialFrame import SerialFrame, FrameType


def test_serial_frame():
    # Create a SerialFrame instance with sample data
    original_data = b"Hello, World!"
    frame_id = 1
    data_type = "str"

    frame = SerialFrame(frame_id=frame_id, data_type=data_type, frame_type=FrameType.ACKNOWLEDGE, data=original_data)
    print("Original Frame:")
    print(frame)

    # Convert the frame to bytes for transmission
    frame_bytes = frame.to_bytes()
    print("\nByte Representation:")
    print(frame_bytes)

    # Simulate receiving the byte data (in real case, it would be read from the serial)
    random_data = b'\x00\x01' + frame_bytes + b'\x02\x03'  # Normal data
    print("\nSimulated Received Data (No Errors):")
    print(random_data)

    # Use the from_bytes method to create a new SerialFrame from the received bytes
    try:
        received_frame = SerialFrame.from_bytes(random_data)
        print("\nReceived Frame (No Errors):")
        print(received_frame)
    except ValueError as e:
        print(f"Error: {e}")

    # --- Simulate Errors ---
    print("\nSimulating Errors in Data Transmission:")

    # 1. Corrupted Start Byte (e.g., change start byte to 0xABCD)
    corrupted_start_byte_data = b'\xAB\xCD' + frame_bytes[2:]
    try:
        received_frame = SerialFrame.from_bytes(corrupted_start_byte_data)
        print("\nReceived Frame (Corrupted Start Byte):")
        print(received_frame)
    except ValueError as e:
        print(f"Error (Corrupted Start Byte): {e}")

    # 2. Incorrect Frame ID (e.g., change frame ID)
    incorrect_frame_id_data = frame_bytes[:2] + b'\x00\x00\x00\x02' + frame_bytes[6:]
    try:
        received_frame = SerialFrame.from_bytes(incorrect_frame_id_data)
        print("\nReceived Frame (Incorrect Frame ID):")
        print(received_frame)
    except ValueError as e:
        print(f"Error (Incorrect Frame ID): {e}")

    # 3. Truncated Data (e.g., remove part of the data)
    truncated_data = frame_bytes[:-5]  # Remove 5 bytes from the end
    try:
        received_frame = SerialFrame.from_bytes(truncated_data)
        print("\nReceived Frame (Truncated Data):")
        print(received_frame)
    except ValueError as e:
        print(f"Error (Truncated Data): {e}")

    # 4. Corrupted Data (e.g., change some data bytes)
    corrupted_data = frame_bytes[:14] + b'\xFF\xFF' + frame_bytes[16:]
    try:
        received_frame = SerialFrame.from_bytes(corrupted_data)
        print("\nReceived Frame (Corrupted Data):")
        print(received_frame)
    except ValueError as e:
        print(f"Error (Corrupted Data): {e}")


# Run the test program
if __name__ == "__main__":
    test_serial_frame()
