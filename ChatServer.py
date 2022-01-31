import socket
import pickle
from _thread import start_new_thread

SIGN_UP = "1"
LOGIN = "2"
EXIT = "3"
ACK = "OK"
NACK = "NOT OK"
clients_list = []
record_addr_username = {}
record_username_password = {}

HEADER_LENGTH = 1024


class Client:

    def __init__(self, client_address, client_socket):
        global clients_list
        self.socket = client_socket
        self.address = client_address
        self.messages = []
        clients_list.append(self)
        print(f"{client_address} connected to Choqondar")

    def kill_session(self):
        global clients_list
        clients_list.remove(self)

    def send(self, data):
        self.socket.send(data)

    def recv(self):
        return self.socket.recv(HEADER_LENGTH).decode()


def run(client):
    global clients_list

    while True:

        data = pickle.dumps('1. Sign Up\n2. Login\n3. Exit')
        client.send(data)

        command = client.recv()
        print(command)

        if not command: ##check she baz
            client.kill_session()
            print("Client closed connection.")
            break

        if command == SIGN_UP:
            data = pickle.dumps('Please enter your username.')
            client.send(data)
            username = client.recv()
            while username == '0' or username in record_username_password:
                data = pickle.dumps('This username is already existed or invalid. Please enter another one.')
                client.send(data)
                username = client.recv()
            data = pickle.dumps('Please enter your password.')
            client.send(data)
            password = client.recv()
            record_username_password[username] = password
            data = pickle.dumps(ACK)
            client.send(data)
            continue
            # back to main page

        elif command == LOGIN:
            data = pickle.dumps('Please enter your username.')
            client.send(data)
            username = client.recv()
            data = pickle.dumps('Please enter your password.')
            client.send(data)
            password = client.recv()
            if username in record_username_password and record_username_password[username] == password:
                # post box
                data = pickle.dumps('Welcome ' + username)
                client.send(data)
                pass
            else:
                data = pickle.dumps('Incorrect username or password.')
                client.send(data)
                continue
                # back to main page

        elif command == EXIT:
            print(client_address + " disconnected.")
            client.kill_session()
            break
        else:
            print("Not understand")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP Server
IP_address = 'localhost'
Port = '8075'
print("\33[32m \t\t\t\tChoqondar Server\33[0m")
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
