import socket
ClientSocket = socket.socket()
host = socket.gethostname()
port = 9999
print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))
address=[]
ad=[]
while True:
    Input = input('Say Something: ')
    ClientSocket.send(str.encode(Input))
    address.append(ClientSocket.recv(1048476))
    address.clear()
    ad.append(str.encode(ClientSocket.recv(1048476)))
    for element in ad:
        print(element)


ClientSocket.close()