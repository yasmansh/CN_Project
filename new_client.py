# Import socket module
import socket

def handle_s(server,ans) :

    if ans == choqondar :
        pass
    elif ans == shalqam :
        pass
    pass

def Main():
    # local host IP '127.0.0.1'
    host = '127.0.0.1'
    port = 12345

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host,port))
    message = "ack"
    while True:
        s.send(message.encode('ascii'))
        data = s.recv(1024)
        print('Received from the server :',str(data.decode('ascii')))
        ans = input()
        s.send(ans.encode('ascii'))
        data = s.recv(1024)
        print('Received from the server :',str(data.decode('ascii')))
        if str(data.decode('ascii')) == 'which server?' :
            ans = input()
            s.send(ans.encode('ascii'))
            data = s.recv(1024)
            print('Received from the server :',str(data.decode('ascii')))
            if str(data.decode('ascii')).split(' ')[0] == 'ACK' :
                s.close()
                s.connect(host,int(data.decode('ascii').split(' ')[1]))
                handle_server(s,ans)
            if str(data.decode('ascii')) == 'NACK' :
                print('server not available')

    s.close()
if __name__ == '__main__':
    Main()
