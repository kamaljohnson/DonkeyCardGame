import socket
import threading
from queue import Queue
dataQ = Queue()

all_recved_data = []
# Create a socket
def socket_create():
    try:
        global host
        global port
        global s
        host = '192.168.1.100'          #this is the server ip address
        port = 1000
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Connect to a remote socket
def socket_connect():
    try:
        global host
        global port
        global s
        s.connect((host, port))
        st = threading.Thread(target=sentdata)
        st.daemon = True
        st.start()
        rt = threading.Thread(target=recvdata)
        rt.daemon = True
        rt.start()
    except socket.error as msg:
        print("Socket connection error: " + str(msg))


# Receive commands from remote server and run on local machine
def recvdata():
    while True:
        print('ready to recv data from server')
        data = s.recv(1024)
        all_recved_data.append(data.decode())
def get_recved_data():
    return all_recved_data

def sentdata():
    while True:
        data = dataQ.get()
        s.send(str.encode(data))
        dataQ.task_done()
def main():
    socket_create()
    socket_connect()

def Send(data):
    dataQ.put(data)