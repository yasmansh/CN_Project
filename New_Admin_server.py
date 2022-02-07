import socket
from _thread import *
import threading

ch_port = 8080
sh_port = 9090


class Firewall():
    state = True
    port_list = []

    def __init__(self):
        self.state = False
        self.port_list = []

    def update(self, mode):
        self.state = mode
        self.port_list = []

    def add_port(self, port):
        self.port_list.append(port)

    def drop_port(self, port):
        self.port_list = self.port_list.remove(port)


CONNECT_TO_EXTERNAL_SERVER = "server"
lOGIN_AS_ADMIN = "admin"
print_lock = threading.Lock()


def threaded(c):
    firewall = Firewall()
    while True:
        command = c.recv(1024)
        print(str(command.decode('ascii')))
        c.send('menu:\n *Connect to external servers \n *login as admin'.encode('ascii'))
        command = str(c.recv(1024).decode('ascii'))
        print(command)
        if command == CONNECT_TO_EXTERNAL_SERVER:
            c.send('which server?'.encode('ascii'))
            command = str(c.recv(1024).decode('ascii'))
            print(command)
            if command == 'choqondar':
                if firewall.state:
                    if ch_port in firewall.port_list:
                        msg = 'ACK ' + str(ch_port)
                        c.send(msg.encode('ascii'))
                    else:
                        c.send('NACK'.encode('ascii'))
                else:
                    if ch_port in firewall.port_list:
                        c.send('NACK'.encode('ascii'))
                    else:
                        msg = 'ACK ' + str(ch_port)
                        c.send(msg.encode('ascii'))
            if command == 'shalqam':

                if firewall.state:
                    if sh_port in firewall.port_list:
                        msg = 'ACK ' + str(sh_port)
                        c.send(msg.encode('ascii'))
                    else:
                        c.send('NACK'.encode('ascii'))
                else:
                    if sh_port in firewall.port_list:
                        c.send('NACK'.encode('ascii'))

                    else:
                        cmsg = 'ACK ' + str(sh_port)
                        c.send(msg.encode('ascii'))
        if not command:
            print('Bye')
            print_lock.release()
            break

    c.close()


def Main():
    host = ""
    port = 1234
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)
    s.listen(5)
    print("socket is listening")
    while True:
        c, addr = s.accept()
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
        start_new_thread(threaded, (c,))
    s.close()


if __name__ == '__main__':
    Main()
