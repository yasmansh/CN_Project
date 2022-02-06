import socket
import pickle



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
Shalqam_PORT = 8090
HEADER_LENGTH = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP_address = 'localhost'
print('IP Address:\t' + IP_address)
server.connect((IP_address, Admin_PORT))
print("Connected to Admin Server ... ")

while True :
    try:

        msg = pickle.loads(server.recv(HEADER_LENGTH))
        print(msg) # asking for admin or user
        command = input()
        server.send(command.encode())
        msg = pickle.loads(server.recv(HEADER_LENGTH))
        print(msg)
        if msg == 'which server?':
            command = input()

            if command == CHOQONDAR :
                command = command+ ' ' + str(Choqondar_PORT)
                server.send(command.encode())
                msg = pickle.loads(server.recv(HEADER_LENGTH))
                if msg = 'ACK' :
                    server.close()
                    server.connect((IP_address, Choqondar_PORT))
                    print("Connected to Choqondar Server ... ")
                else  :
                    continue


            elif command == SHALQAM :
                command = command+ ' ' + str(Shalqam_PORT)
                server.send(command.encode())
                msg = pickle.loads(server.recv(HEADER_LENGTH))
                if msg = 'ACK' :
                    server.close()
                    server.connect((IP_address, Shalqam_PORT))
                    print("Connected to Shalqam Server ... ")
                else  :
                    continue

        if msg == 'password' :
            print('please insert your password')
            command = input()
            server.send(command.encode())
            msg = pickle.loads(server.recv(HEADER_LENGTH))
            print(msg)

            if msg == 'Admin logged in' :
                command = input()
                while True :
                    server.send(command.encode())
                    msg = pickle.loads(server.recv(HEADER_LENGTH))
                    print(msg)
                    if msg == 'NACK' :

                        break


def client_post_box():
    global command, msg
    command = input()  # username2
    server.send(command.encode())
    if command == '0':
        return  # Back to Main Page

    msg = pickle.loads(server.recv(HEADER_LENGTH))  # chat page OR post box
    if msg[:6] == 'CHATS|':  # chat page(valid username2)
        print(msg[6:])  # show chats
        chatting()
    else:  # post box(invalid username2)
        print(msg)  # post box(invalid username2)
        client_post_box()


def chatting():
    global command, msg
    command = input()  # send pm or shortcut
    server.send(command.encode())
    if command == '/exit':
        msg = pickle.loads(server.recv(HEADER_LENGTH))
        print(msg)  # post box
        client_post_box()
    elif command.find("/load") != -1:
        msg = pickle.loads(server.recv(HEADER_LENGTH))
        print(msg)  # show last x pm
        chatting()
    elif command.find("/") == -1:  # pm
        chatting()


while True:  # check kon faqat recv and send ... okeye ya na
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
            client_post_box()


        elif command == EXIT:
            exit()


    except Exception as e:
        print("Exiting")
        break

server.close()
