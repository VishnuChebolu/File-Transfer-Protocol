import threading
import socket
import os
import json

host = '192.168.167.25'  # localhost
port = 5050

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

menu = ["upload", "download", "show", "remove", "quit"]
clients = []

a = open(r"credentials.json", 'r')
cred = json.load(a)


def show(client):
    lst = os.listdir()
    client.send(str(lst).encode('ascii'))

def upload_file(file_name,target):
    f = open(file_name, 'rb')
    target.send(f.read())

def download_file(file_name,target):
    f = open(file_name, 'wb')
    target.settimeout(1)
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close()


def upload(client): # upload in client side => download in server side
    filename = client.recv(1024).decode('ascii')
    download_file(filename, client)
    print(f'{filename} received.')


def download(client): 
    filename = client.recv(1024).decode('ascii')
    upload_file(filename, client)

    


def remove(client):
    filename = client.recv(1024).decode('ascii')
    os.remove(filename)
    print(f'{filename} deleted.')


def handle(client):
    while True:
        message = client.recv(1024).decode('ascii')
        if message in menu:
            number = menu.index(message)
            client.send(str(number).encode('ascii'))
            if number == 0:
                upload(client)
            elif number == 1:
                download(client)
            elif number == 2:
                show(client)
            elif number == 3:
                remove(client)
            elif number == 4:
                print(f'client has disconnected.')
                client.close()
        elif message == 'help':
            client.send(str(menu).encode('ascii'))
            continue
        elif message == 'quit':
            client.close()


def receive():
    while True:
        client, address = server.accept()
        uname = client.recv(1024).decode('ascii')
        pwd = client.recv(1024).decode('ascii')
        if cred[uname][0] == pwd:
            print(f'Connected with {str(address)}')
            client.send('1'.encode('ascii'))
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        else:
            client.send('2'.encode('ascii'))
            client.close()


if __name__ == "__main__":
    print("FTP server has started!")
    receive()
