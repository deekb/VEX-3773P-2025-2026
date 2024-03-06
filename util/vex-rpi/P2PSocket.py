import socket
import select
import threading
import time
import os
import random
import argparse
from rich import print

from rich.console import Console

OUTGOING = 1
INCOMING = 2

console = Console()

class P2PClient:
    def __init__(self, incoming_address, outgoing_address):
        self.incoming_address = (socket.gethostbyname(incoming_address[0]), incoming_address[1])
        self.outgoing_address = (socket.gethostbyname(outgoing_address[0]), outgoing_address[1])
        self.incomming_messages_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.outgoing_messages_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.incomming_messages_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.outgoing_messages_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.incoming_messages = []
        self.outgoing_messages = []
        self.connected = 0
    
    def start_listening(self):
        self.incomming_messages_socket.bind(self.incoming_address)
        self.incomming_messages_socket.listen(1)
        with console.status(f"Listening for peers on {self.incoming_address[0]}:{self.incoming_address[1]}") as status:
            read_list = [self.incomming_messages_socket]
            while True:            
                readable, _, _ = select.select(read_list, (), ())
                if self.incomming_messages_socket in readable:
                    other_peer_socket, other_peer_address = self.incomming_messages_socket.accept()
                    if other_peer_address[0] == self.outgoing_address[0]:
                        self.incomming_messages_socket, _ = other_peer_socket, other_peer_address
                        status.stop()
                        self.connected |= INCOMING
                        print(f"[bold green]Connected to other peer {other_peer_address[0]}:{other_peer_address[1]}")
                        break
                    else:
                        status.stop()
                        print(f"[bold red]Connection is coming from the wrong ip address, expected: {self.outgoing_address[0]}, got {other_peer_address[0]}")
                        other_peer_socket.close()
                time.sleep(0.1)
                
            
    def establish_connection(self):
        while True:
            try:
                self.outgoing_messages_socket.connect(self.outgoing_address)
                self.connected |= OUTGOING
                break
            except ConnectionRefusedError:
                time.sleep(1)
    
    def is_connected(self):
        return self.connected == INCOMING | OUTGOING
        
    
    def get_message(self):
        if self.incoming_messages:
            return self.incoming_messages.pop(0)
        else:
            return None
    
    def send_message(self, message):
        self.outgoing_messages.append(message)
    
    def send_thread(self):
        while True:
            if self.outgoing_messages and self.is_connected():
                for _ in range(len(self.outgoing_messages)):
                    self.outgoing_messages_socket.sendall(self.outgoing_messages.pop(0).encode())
    
    def recieve_thread(self):
        while True:
            if self.is_connected():
                self.incoming_messages.append(self.incomming_messages_socket.recv(1024).decode())


def main():
    
    parser = argparse.ArgumentParser("Dual-Sockets")
    parser.add_argument("--listening-address", dest="listening_address", help="The IP address and port to listen for peers on, seperated by a colon", type=str, required=True)
    parser.add_argument("--other-peer-address", dest="other_peer_address", help="The IP address and port of the peer to connect to, seperated by a colon", type=str, required=True)

    args = parser.parse_args()
    
        
    listening_address = args.listening_address.split(":")
    listening_address[1] = int(listening_address[1])
    
    other_peer_address = args.other_peer_address.split(":")
    other_peer_address[1] = int(other_peer_address[1])
    
    peer = P2PClient(tuple(listening_address), tuple(other_peer_address))

    listening_thread = threading.Thread(target=peer.start_listening)
    send_thread = threading.Thread(target=peer.send_thread)
    recieve_thread = threading.Thread(target=peer.recieve_thread)

    listening_thread.start()
    send_thread.start()
    recieve_thread.start()
    
    peer.establish_connection()
    while not peer.is_connected():
        time.sleep(0.1)
    
    print("Connected to peer")
    to_send = input(">>>")
    peer.send_message(to_send)
    while True:
        recieved = peer.get_message()
        if recieved:
            
            print(recieved)
            peer.send_message("Got: " + recieved)
        
    

if __name__ == "__main__":
    main()

