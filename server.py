import socket
import threading
from queue import Queue

sendingQ = Queue()      #this queue will hold all the datas to be sent to different clients

All_connections = []
All_address = []
dataRecved = []             #this will keep track of all the datas recved from other computers

print_lock = threading.Lock()

# Create socket (allows two computers to connect)
def socket_create():
    try:
        global host
        global port
        global s
        host = ''
        port = 1000
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error: " + str(msg))

# Bind socket to port (the host and port the communication will take place) and wait for connection from client
def socket_bind():
    try:
        global host
        global port
        global s
        print("Binding socket to port: " + str(port))
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print("Socket binding error: " + str(msg) + "\n" + "Retrying...")
        socket_bind()


# Establish connection with client (socket must be listening for them)
def socket_accept(numberOfClients):
    i = 0
    while True:
        conn, address = s.accept()
        print("Connection has been established | " + "IP " + address[0] + " | Port " + str(address[1]))
        All_connections.append(conn)
        All_address.append(address)
        t1 = threading.Thread(target = sendingthreader)
        t1.start()
        i += 1
        t2 = threading.Thread(target = Recv,args=(conn,))
        t2.start()
        if len(All_connections) == numberOfClients:
            print('connected to all',numberOfClients)
            return 1

def sendingthreader():
    while True:
        if not sendingQ.empty():
            data,conn = sendingQ.get()
            sendto(data,conn)
            sendingQ.task_done()

# Send commands
def sendto(data,conn):
    print(data)
    conn.send(str.encode(data))

#send data to a particular computer with the connIndex
def Send(data,conn):
    sendingQ.put([data,conn])

def Recv(conn):
    print('ready to recv data from client')
    while True:
        data,addr = conn.recvfrom(1024)
        print('send by',addr)
        dataRecved.append(data.decode())
        print(dataRecved)
#returns the list of data recved from the other computers
def getData():
    return(dataRecved)

def main(clients):
    numberOfClients = clients
    socket_create()
    socket_bind()
    socket_accept(clients)