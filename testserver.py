import socket
import os
from threading import Thread
import threading
import sys
from colorama import init, Fore
init()
GREEN = Fore.GREEN
RED = Fore.RED
YELLOW = Fore.YELLOW
WHITE=Fore.WHITE
SEPARATOR = "<SEPARATOR>"
clients = set()
clients_lock = threading.Lock()

def listener(client, address):
    global clients
    print (f"Accepted connection from:{address}\n")
    with clients_lock:
        clients.add(client)
    while True:
        try:
            data=(client.recv(1073741824)).decode('utf-8')
            msg,img=data.split(SEPARATOR)
            with clients_lock:
                for c in clients:     
                    c.send(f"{msg}{SEPARATOR}{img}".encode())
        except:
            msg=data.encode()
            with clients_lock:
                for c in clients:
                    c.send(msg)
    client.close()
host =""
port = 9999
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host,port))
s.listen(20)
th = []

while True:
    try:
        print (f"{YELLOW}Server is listening for connections...")
        client, address = s.accept()
        print(f"{GREEN}")
        th.append(Thread(target=listener, args = (client,address)).start())
    except socket.error as msg:
        print(f"{RED}")
        print (f"{msg}")
    except KeyboardInterrupt:
        if client:  # <---
            client.close()
        break  # <---
s.close()