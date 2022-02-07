import socket
import pickle
import datetime
from _thread import start_new_thread

import new_client

SIGN_UP = "1"
LOGIN = "2"
EXIT = "3"
ACK = "ACK"
NACK = "NACK"
HEADER_LENGTH = 1024
record_username_password = {}
record_all_messages = {}
# {'username': [('from_username', 'pm', datetime]}


record_username_chatWith_lastTime = {}  # { 'username1|'username2' :datetime } - user1 akharin bar dar datetime username2 ro exit karde


class Client:

    def __init__(self, client_address, client_socket):
        self.socket = client_socket
        self.address = client_address
        self.messages = []
        print(f"{client_address} connected to Choqondar")


    def send(self, data):
        self.socket.send(data)

    def recv(self):
        return self.socket.recv(HEADER_LENGTH).decode()


def run(client):

    while True:

        data = pickle.dumps('1. Sign Up\n2. Login\n3. Exit')
        client.send(data)

        command = client.recv()

        if not command:
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
            continue  # Back to Main Page

        elif command == LOGIN:
            data = pickle.dumps('Please enter your username.')
            client.send(data)
            username = client.recv()
            data = pickle.dumps('Please enter your password.')
            client.send(data)
            password = client.recv()
            if username in record_username_password and record_username_password[username] == password:
                # Login successful
                # Post Box
                post_box(client, username)
            else:
                data = pickle.dumps('Incorrect username or password.')
                client.send(data)
                continue  # Back to Main Page


        elif command == EXIT:
            print(str(client_address) + " disconnected.")
            new_client.Main()
            break
        else:
            print("Not understand")


def post_box(client, username):
    rest_of_contacts = list(record_username_password.keys())
    rest_of_contacts.remove(username)
    chat_contacts = []  # (name , number of new messages, time_of_last_pm)
    if username in record_all_messages:  # Has at least one chat
        for msg in record_all_messages[username]:
            if msg[0] in rest_of_contacts:  # msg[0] = from username
                rest_of_contacts.remove(msg[0])
                chat_contacts.append((msg[0], 0, datetime.datetime.min))

    for i in range(len(chat_contacts)):  # Updating number of new messages
        last_seen = datetime.datetime.min
        if str(username + "|" + chat_contacts[i][0]) in record_username_chatWith_lastTime:
            last_seen = record_username_chatWith_lastTime[username + "|" + chat_contacts[i][0]]
        for msg in record_all_messages[username]:
            if msg[0] == chat_contacts[i][0] and msg[2] > last_seen:
                chat_contacts[i] = (chat_contacts[i][0], chat_contacts[i][1] + 1, chat_contacts[i][2])
            if msg[0] == chat_contacts[i][0] and msg[2] > chat_contacts[i][2]:
                chat_contacts[i] = (chat_contacts[i][0], chat_contacts[i][1], msg[2])

    chat_contacts.sort(key=lambda x: x[2], reverse=True)
    rest_of_contacts.sort()
    contacts = ''
    for chat_contact in chat_contacts:
        if chat_contact[1] == 0:
            contacts += chat_contact[0] + '\n'
        else:
            contacts += chat_contact[0] + ' (' + str(chat_contact[1]) + ')\n'
    for c in rest_of_contacts:
        contacts += c + '\n'
    data = pickle.dumps(contacts.rstrip('\n'))
    client.send(data)

    while True:
        username2 = client.recv()
        if username2 == '0':  # Back to Main Page
            return
        elif username2 != username and username in record_username_password:  # Chat page
            chat_page(client, username, username2)
            return
        else:  # Invalid username2
            post_box(client, username)


def chat_page(client, username, username2):
    chats = load_x(username, username2, 5)
    data = pickle.dumps('CHATS|' + chats)
    client.send(data)
    while True:
        pm = client.recv()
        if pm.find("/") == -1:  # send pm to username2
            current_time = datetime.datetime.now()
            if username2 in record_all_messages:
                record_all_messages[username2].append((username, pm, current_time))
            else:
                record_all_messages[username2] = [(username, pm, current_time)]

            if username in record_all_messages:
                record_all_messages[username].append((username, pm, current_time))
            else:
                record_all_messages[username] = [(username, pm, current_time)]

        elif pm == "/exit":  # shortcut
            record_username_chatWith_lastTime[username + '|' + username2] = datetime.datetime.now()
            post_box(client, username)
            return
        elif pm.find("/load") != -1:  # shortcut
            x = int(pm.split()[1])
            chats = load_x(username, username2, x)
            data = pickle.dumps(chats)
            client.send(data)


def load_x(username, username2, x):
    if username not in record_all_messages:
        return 'No message here yet...'
    chat_msg = []
    for m in record_all_messages[username]:
        if m[0] == username2:
            chat_msg.append(m)

    if username2 in record_all_messages:
        for m in record_all_messages[username2]:
            if m[0] == username and m not in chat_msg:
                chat_msg.append(m)

    chat_msg.sort(key=lambda x: x[2])  # Sort based on the third column(datetime)
    if len(chat_msg) == 0:
        return 'No message here yet...'
    chats = ''
    for m in chat_msg[-x:]:
        if m[0] == username2:
            chats += '(' + m[0] + ') ' + m[1] + '\n'
        else:
            chats += m[1] + '\n'
    return chats.rstrip('\n')


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP Server
IP_address = 'localhost'
Port = '8080'
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
