import socket
import pickle
ACK = "ACK"
NACK = "NACK"
HEADER_LENGTH = 1024
password = '0'

CONNECT_TO_EXTERNAL_SERVER = "server"
lOGIN_AS_ADMIN = "admin"

class Client:

    def __init__(self, client_address, client_socket):
        global clients_list
        self.socket = client_socket
        self.address = client_address
        self.messages = []
        clients_list.append(self)
        print(f"{client_address} connected to Admin server")

    def send(self, data):
        self.socket.send(data)

    def recv(self):
        return self.socket.recv(HEADER_LENGTH).decode()

class Firewall():
    state = True
    port_list = []
    def __init__(self, arg):
        self.arg = arg

    def update(self, mode) :
        self.state = mode
        self.port_list = []
    def add_port(self, port) :

        self.port_list.append(port)

    def drop_port(self, port):
        self.port_list = self.port_list.remove(port)


def run(client):
    global clients_list

    firewall = Firewall()

    while True:

        data = pickle.dumps('menu:\n *Connect to external server \n *login as admin')
        client.send(data)

        command = client.recv()

        if command == CONNECT_TO_EXTERNAL_SERVER :
            data = pickle.dumps('which server?')
            client.send(data)
            command = client.recv()
            if firewall.state : # means the firewall is white
                if int(command) in firewall.port_list :
                    data = pickle.dumps('ACK')
                    client.send(data)
                else :
                    data = pickle.dumps('NACK')
                    client.send(data)
            else :
                if int(command) in firewall.port_list :
                    data = pickle.dumps('NACK')
                    client.send(data)
                else :
                    data = pickle.dumps('ACK')
                    client.send(data)
        elif command == lOGIN_AS_ADMIN :
            data = pickle.dumps('password')
            client.send(data)
            command = client.recv()
            if password == '0' or password == command:
                password == command

                data = pickle.dumps('Admin logged in')
                client.send(data)

                while True :
                    command = client.recv()
                    if command == 'white' :
                        firewall.update(True)
                    elif command == 'black':
                        firewall.update(False)
                    elif command.split(' ')[0] == 'open' :
                        if firewall.state :

                            firewall.add_port(int(command.split(' ')[1]))
                        else :
                            firewall.drop_port(int(command.split(' ')[1]))
                    elif command.split(' ')[0] == 'close' :
                        if firewall.state :

                            firewall.drop_port(int(command.split(' ')[1]))
                        else :
                            firewall.add_port(int(command.split(' ')[1]))
                    else :
                        data = pickle.dumps('NACK')
                        client.send(data)
                        break
                    data = pickle.dumps('ACK')
                    client.send(data)
