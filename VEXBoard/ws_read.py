import json
import os
import time

import websocket
from VEXLib.Util.MD5sum import md5sum_file

DIRECTORY = "/home/derek/PycharmProjects/VEXlib/src"
ROBOT_WS = "ws://192.168.4.1/ws"

def get_file_hashes():
    """Get hashes of all files in the directory."""
    hashes = {}
    for file in os.listdir(DIRECTORY):
        full_path = os.path.join(DIRECTORY, file)
        if os.path.isfile(full_path):
            hashes[file] = md5sum_file(full_path)
    return hashes


def send_file_hashes():
    ws = websocket.create_connection(ROBOT_WS)
    file_hashes = get_file_hashes()
    print(json.dumps(list(file_hashes.keys())))
    ws.send("FILES " + json.dumps(list(file_hashes.keys())))
    while True:
        line = ws.recv()
        print(line)
        if line.startswith("HASHES"):
            hashes = eval(line.split(" ", 1)[1])
            need_to_upload = [file for file, hash_ in file_hashes.items() if hash_ != hashes[file]]
            for file in need_to_upload:
                print(f"Uploading {file}")
                ws.send(f"UPLOAD {file} {os.path.getsize(os.path.join(DIRECTORY, file))}")
                with open(os.path.join(DIRECTORY, file)) as f:
                    chunk = f.read(100)
                    while chunk:
                        chunk = f.read(100)
                        ws.send(chunk + "\n")
                        time.sleep(0.1)

print(get_file_hashes())
send_file_hashes()
