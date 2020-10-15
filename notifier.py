from plyer import notification
import socket
def sockets():
    global s 
    global host
    global port
    s=socket.socket()
    host=socket.gethostbyname(input("Enter the sender name"))
    port=9999
def connect():
    try:
        s.connect((host,port))
        print("Running")
    except Exception as msg:
        print(f"Connection didn't establish: {msg}")
        sockets()
        s.connect((host,port))
def receiver():
    address=[]
    while True:
        cmd=s.recv(1048576) 
        address.append(s.recv(1048576))
        address.clear()
        msg=cmd.decode("utf-8")
        #recv=s.recv(562109)
        #fo = open("foo.PNG", "wb")
        #fo.write(recv)
        #fo.close()
        notification.notify(
            title="Office notification",
            message=msg,
            app_icon='',  # e.g. 'C:\\icon_32x32.ico'
            app_name="notifier",
            ticker="lol",
            timeout=20,  # seconds
        )

def main():
    sockets()
    connect()
    receiver()
main()