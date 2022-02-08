import socket
import pickle
from _thread import start_new_thread
from vidgear.gears import VideoGear
from vidgear.gears import NetGear

import new_client

EXIT = "3"
ACK = "ACK"
NACK = "NACK"
HEADER_LENGTH = 1024


class Client:

    def __init__(self, client_address, client_socket):
        self.socket = client_socket
        self.address = client_address
        self.messages = []
        print(f"{client_address} connected to Shalqam")

    def send(self, data):
        self.socket.send(data)

    def recv(self):
        return self.socket.recv(HEADER_LENGTH).decode()


def run(client):
    while True:

        data = pickle.dumps('Welcome to Choghondar.\n1. Minion \n2. Flower \n3. Exit')
        client.send(data)  # menu

        command = client.recv()

        if not command:
            print("Client closed connection.")
            break

        if command == '1' or command == '2':
            # client has requested a video
            print("Client requested video with id {}".format(command))
            ################----------#################
        elif command == EXIT:
            print(str(client_address) + " disconnected.")
            new_client.Main()
            break
        else:
            print("Not understand")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP Server
IP_address = 'localhost'
Port = '9090'
print("\33[32m \t\t\t\tShalqam Server\33[0m")
server.bind((IP_address, int(Port)))
server.listen(20)
print(f"Listening for connections on {IP_address}:{Port} ...")

while True:
    try:
        client_socket, client_address = server.accept()
        start_new_thread(run, (Client(client_address, client_socket),))

    except Exception as e:
        print("Exiting")
        break

print("Closing server socket")
server.close()
