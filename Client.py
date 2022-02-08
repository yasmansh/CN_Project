import socket
import pickle
from vidgear.gears import NetGear
import cv2

SIGN_UP = "1"
LOGIN = "2"
EXIT = "3"
ACK = "ACK"

CHOQONDAR = "choqondar"
SHALQAM = "shalqam"
ADMIN_PASSWORD = "0"
ACTIVATE_BLACK_FIREWALL = 'black'
ACTIVATE_WHITE_FIREWALL = 'white'

ADMIN_PORT = 8088
Choqondar_PORT = 8089
Shalqam_PORT = 9090
HEADER_LENGTH = 1024


def client_post_box(server):
    global command, msg
    command = input()  # username2
    server.send(command.encode())
    if command == '0':
        return  # Back to Main Page

    msg = pickle.loads(server.recv(HEADER_LENGTH))  # chat page OR post box
    if msg[:6] == 'CHATS|':  # chat page(valid username2)
        print(msg[6:])  # show chats
        chatting(server)
    else:  # post box(invalid username2)
        print(msg)  # post box(invalid username2)
        client_post_box(server)


def chatting(server):
    global command, msg
    command = input()  # send pm or shortcut
    server.send(command.encode())
    if command == '/exit':
        msg = pickle.loads(server.recv(HEADER_LENGTH))
        print(msg)  # post box
        client_post_box(server)
    elif command.find("/load") != -1:
        msg = pickle.loads(server.recv(HEADER_LENGTH))
        print(msg)  # show last x pm
        chatting(server)
    elif command.find("/") == -1:  # pm
        chatting(server)


def handle_s(server, ans):
    if ans == 'choqondar':
        while True:
            try:
                menu = pickle.loads(server.recv(HEADER_LENGTH))
                print(menu)
                command = input()
                server.send(command.encode())

                if command == SIGN_UP:
                    msg = pickle.loads(server.recv(HEADER_LENGTH))
                    print(msg)
                    command = input()
                    server.send(command.encode())
                    while msg != ACK:
                        msg = pickle.loads(server.recv(HEADER_LENGTH))
                        if msg != ACK:
                            print(msg)
                            command = input()
                            server.send(command.encode())
                    continue  # Back to Main Page


                elif command == LOGIN:
                    msg = pickle.loads(server.recv(HEADER_LENGTH))
                    print(msg)
                    command = input()  # username
                    server.send(command.encode())
                    msg = pickle.loads(server.recv(HEADER_LENGTH))
                    print(msg)
                    command = input()  # password
                    server.send(command.encode())
                    msg = pickle.loads(server.recv(HEADER_LENGTH))
                    print(msg)
                    if msg == 'Incorrect username or password.':
                        continue  # Back to Main Page
                    # Login successful
                    # Post Box
                    client_post_box(server)


                elif command == EXIT:
                    exit()


            except Exception as e:
                print("Exiting")
                break

    elif ans == 'shalqam':
        while True:
            try:
                menu = pickle.loads(server.recv(HEADER_LENGTH))
                print(menu)
                command = input()
                server.send(command.encode())

                if command == '1' or command == '2':
                    ################----------#################
                    pass
                elif command == EXIT:
                    exit()


            except Exception as e:
                print("Exiting")
                break
    pass


def Main():
    # local host IP '127.0.0.1'
    host = '127.0.0.1'
    port = 12345

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    message = "ack"
    while True:
        s.send(message.encode('ascii'))
        data = s.recv(1024)
        print('Received from the server :', str(data.decode('ascii')))
        ans = input()
        s.send(ans.encode('ascii'))
        data = s.recv(1024)
        print('Received from the server :', str(data.decode('ascii')))
        if str(data.decode('ascii')) == 'which server?':
            ans = input()
            s.send(ans.encode('ascii'))
            data = s.recv(1024)
            print('Received from the server :', str(data.decode('ascii')))
            if str(data.decode('ascii')).split(' ')[0] == 'ACK':
                s.close()
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((host, int(data.decode('ascii').split(' ')[1])))
                handle_s(s, ans)
                break
            if str(data.decode('ascii')) == 'NACK':
                print('server not available')
        if str(data.decode('ascii')) == 'password':
            print('please insert your password')
            command = input()
            s.send(command.encode('ascii'))
            data = s.recv(1024)
            print('Received from the server :', str(data.decode('ascii')))

            if str(data.decode('ascii')) == 'Admin logged in':

                while True:
                    command = input()
                    s.send(command.encode('ascii'))
                    data = s.recv(1024)
                    print('Received from the server :', str(data.decode('ascii')))
                    if str(data.decode('ascii')) == 'NACK':
                        break

    s.close()


if __name__ == '__main__':
    Main()
