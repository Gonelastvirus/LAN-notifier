from plyer import notification
import socket
import os
SEPARATOR = "<SEPARATOR>"
def sockets():
    global s 
    global host
    global port
    s=socket.socket()
    host= socket.gethostbyname(input("Enter the sender name"))#str(e2.get())
    port=9999
def connect():
    try:
        s.connect((host,port))
        print("Running")
        # messagebox.showerror("Connect", "Running")
    except Exception as msg:
        print(f"Connection didn't establish: {msg}")
        # messagebox.showerror("Connection didn't establish", msg)
def receiver():
    while True:
        try:
            global cmd
            cmd=(s.recv(1073741824)).decode('utf-8')
            msg,img=cmd.split(SEPARATOR)
            msg_en=msg.encode()
            img_en=bytes(img)
            print(f"{msg_en}")
            desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Downloads')
            print(desktop)
            filename=desktop+"\\LAN_received.png"
            fo = open(filename, "wb")
            fo.write(img_en)
            fo.close()
            notification.notify(
                title="Office notification",
                message=msg_en,
                app_icon='',  # e.g. 'C:\\icon_32x32.ico'
                app_name="notifier",
                ticker="lol",
                timeout=20,  # seconds
            )
        except:
            msg=cmd.decode('utf-8')
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
