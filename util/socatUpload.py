import socket
import time
from src.SerialFrame import SerialFrame, FrameType

# Constants
HOST = 'raspberrypi.local'  # Replace with the IP address of the robot
PORT = 3773  # The port number used for communication
CHUNK_SIZE = 1024  # Size of each data chunk sent
TIMEOUT = 2  # Timeout in seconds for waiting for an ACK


def send_data_frame(s, frame_id, data):
    """Send a data frame and wait for ACK."""
    # Create a SerialFrame for the data
    data_frame = SerialFrame(
        frame_id=frame_id,
        frame_type=FrameType.DATA,
        data_type='text',
        data=data
    )

    # Send the data frame
    s.sendall(data_frame.to_bytes())

    # Wait for ACK with accumulated data
    start_time = time.time()
    accumulated_data = b""  # Store accumulated bytes

    while True:
        # Set the timeout for receiving data
        s.settimeout(TIMEOUT)

        try:
            # Receive data from the socket
            response = s.recv(1024)
            accumulated_data += response  # Accumulate received data
            # print("Accumulated data:", accumulated_data)  # Debugging output

            # Try to decode the SerialFrame from accumulated data
            try:
                ack_frame = SerialFrame.from_bytes(accumulated_data)
                # Check if the received frame is an ACK for the correct frame_id
                if ack_frame.frame_type == FrameType.ACKNOWLEDGE and ack_frame.frame_id == frame_id:
                    print("ACK received for frame ID:", frame_id)
                    break  # ACK received, exit the loop
            except ValueError:
                pass
                # If not a valid frame, continue accumulating data
                # print("Incomplete or invalid frame, waiting for more data...")

            # If we exceed the timeout, stop waiting
            if time.time() - start_time > TIMEOUT:
                print("Timeout reached, no ACK received.")
                break
        except (socket.timeout, ValueError) as e:
            print("Error receiving data:", e)
            # Optionally, handle timeout or errors here
            continue  # Retry if there's an issue receiving the data


def main():
    # Create a socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        # Step 2: Wait for the robot to respond with READY for the file transfer
        # response = s.recv(1024)
        # print("Received response:", response)

        frame_id = 0

        while True:
            data = b" "
            data += b"\0" * (2000)

            send_data_frame(s, frame_id, data)

            # Increment the frame ID for the next frame
            frame_id += 1


if __name__ == "__main__":
    main()
