import socket
import pickle

SIGN_UP = "1"
LOGIN = "2"
EXIT = "3"
ACK = "OK"

Choqondar_PORT = 8075
HEADER_LENGTH = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP_address = 'localhost'
print('IP Address:\t' + IP_address)
server.connect((IP_address, Choqondar_PORT))
print("Connected to Choqondar Server ... ")

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
            continue
            # back to main page

        elif command == LOGIN:
            msg = pickle.loads(server.recv(HEADER_LENGTH))
            print(msg)
            command = input()  #username
            server.send(command.encode())
            msg = pickle.loads(server.recv(HEADER_LENGTH))
            print(msg)
            command = input() #password
            server.send(command.encode())
            msg = pickle.loads(server.recv(HEADER_LENGTH))
            print(msg)
            if msg =='Incorrect username or password.':
                continue  # back to main page
            #post box

        elif command == EXIT:
            exit()


    except Exception as e:
        print("Exiting")
        break

server.close()
