# hello_psg.py

import PySimpleGUI as sg
from PIL import Image, ImageTk
import io
import os
import socket
SEPARATOR = "<SEPARATOR>"
ClientSocket = socket.socket()
host = socket.gethostname()
port = 9999

# print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(e)

address=[]
def get_img_data(f, maxsize=(200, 200), first=False):
    """Generate image data using PIL
    """
    img = Image.open(f)
    img.thumbnail(maxsize)
    if first:                     # tkinter is inactive the first time
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()
    return ImageTk.PhotoImage(img)

sg.theme('Dark Purple 7')
#clients = ['Gone last', "Yoboii", "Sharma ji", "Bandu", "Mote dai"]
clients_column = [
    [sg.Text("Server", font='Courier 40')],
    [sg.Text(f'{socket.gethostname()}', font='Verdana 14', size=(30, 1))],
    [sg.Text(size=(30, 1), key="-SPACE1-")],
]

# for clients in client :
#     clients_column.append([sg.Text(f'{clients}', font='Verdana 11', size=(30, 1))])
    
message_column = [
    [sg.Text("Message", font='Courier 20')],
    [sg.Text(size=(60, 1), key="-SPACE2-")],
    [sg.Multiline(size=(60, 7), font='Times 13', border_width=0, background_color='#dedede', text_color='#131',
                  enable_events=True, key="-MESSAGE-")],
    [sg.Text(size=(60, 1), key="-SPACE3-")],
    [sg.In(size=(30, 1), enable_events=True, font='Verdana 13', key="-FILE_NAME-"), sg.FileBrowse('Upload Image',
                                                                                                  font='Calibri 15', key='_BUTTON_UPLOAD_')],
    [sg.Text(size=(60, 1), key="-UPLOAD_INFO-")],
    [sg.Image(key="-IMAGE-")],
    [sg.Text(size=(60, 1), key="-SPACE4-")],
    [sg.Button('Send', border_width=0, font='Calibri 16', key='_BUTTON_SEND_')]
]

layout = [
    [
        sg.Column(clients_column),
        sg.VSeparator(),
        sg.Column(message_column),
    ]
]

# Create the window
window = sg.Window("Demo", layout, margins=(50, 100), default_element_size=(12, 1),
                   text_justification='l',
                   auto_size_text=False,
                   auto_size_buttons=False,
                   default_button_element_size=(12, 1),
                   finalize=True)

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "_BUTTON_SEND_":
        val=values["-MESSAGE-"] 
        filename = values["-FILE_NAME-"]
        if filename=='':
            if val =="\n":
                sg.popup('Error', 'Please fill the message box')
            else:
                try:
                    msg = values["-MESSAGE-"]
                    ClientSocket.sendall(str.encode(msg))
                except socket.error as e1:
                    sg.popup("connection error",e1)
        else:
            File=open(filename,"rb")
            data_img=File.read(1073741824)
            File.close()
            if val =="\n":
                sg.popup('Error', 'Please fill the message box')
            else:
                try:
                    msg = values["-MESSAGE-"]
                    ClientSocket.sendall(f"{msg}{SEPARATOR}{data_img}".encode())
                except socket.error as e1:
                    sg.popup("connection error",e1)
        # ad.append((ClientSocket.recv(1048476)).decode("utf-8"))
    if event == "-FILE_NAME-":
        filename = values["-FILE_NAME-"]
        if filename.endswith(('.png', '.gif', '.jpg', 'jpeg')):
            window['-UPLOAD_INFO-'].update("")
            window["-IMAGE-"].update(data=get_img_data(filename, first=True))
        else:
            window['-UPLOAD_INFO-'].update("Please select valid image")
    if event == "OK" or event == sg.WIN_CLOSED:
        break

ClientSocket.close()
window.close()