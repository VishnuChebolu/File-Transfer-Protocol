import threading
import socket
import hashlib
import getpass
import os


host = '192.168.167.25'
port = 5050

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

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


def handle(client):
    while True:
        code_word = input('ftp>')
        client.send(code_word.encode('ascii'))
        if code_word == 'help':
            print(client.recv(1024).decode('ascii'))
            continue
        if code_word == 'quit':
            break
        number = client.recv(1024).decode('ascii')
        if number == '0':
            filename = input("enter filename : ")
            if not (os.path.isfile(filename)):
                print(f'%Error ftp://{host}/? (No such file)')
                print('550- Requested action not taken. File unavailable')
                continue
            client.send(filename.encode('ascii'))
            upload_file(filename, client)
            
        elif number == '1':
            file = input("enter filename : ")
            client.send(file.encode('ascii'))
            download_file(file,client)

        elif number == '2':
            lst = client.recv(1024).decode('ascii')
            print(lst)
        elif number == '3':
            filename = input("enter filename : ")
            client.send(filename.encode('ascii'))
        else:
            print("command not matched.")
            break


def receive():
    uname = input('Username : ')
    print('331- Username ok, need password')
    pwd = getpass.getpass()
    print('230- Logged in')
    print('passive mode On')
    pwd = hashlib.md5(pwd.encode()).hexdigest()
    client.send(uname.encode('ascii'))
    client.send(pwd.encode('ascii'))
    sf = client.recv(1024).decode('ascii')
    if sf == '1':
        print(f'\nTrying to connect...{host}')
        print(f'Connected to {host}')
        print('220- Welcome to Ftp server')
        handle(client)
    else:
        print("Invalid credentials !")
        client.close()


receive()
