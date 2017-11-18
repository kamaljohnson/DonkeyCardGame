import socket
import threading
from queue import Queue

sendingQ = Queue()      #this queue will hold all the datas to be sent to different clients

All_connections = []
All_address = []
dataRecved = []             #this will keep track of all the datas recved from other computers

print_lock = threading.Lock()

cardsWithPeople = []

incards = []
isPlay = False  #if True then the server person is to play now else no
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

            #the '1' corresponds to the server
            All_address.append('1')
            All_connections.append('1')
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

def getMaxCard(tempData):
    tempList = []
    for d in tempData:
        tempList.append(int(t[0]))
    tempList = sorted(tempList)
    return tempList[-1]         #this will be the largest number in the list

#this funtion will return the address of the owner of the card
def getClientFromCard(card):
    for d in dataRecved:
        c = d[0]
        if card == c:
            return d[-1]            #this will return the add of the card owner

def Recv(conn):
    Strike = False
    print('ready to recv data from client')
    while True:
        data,addr = conn.recvfrom(1024)
        print('send by',addr)
        #the data is of the form :
        # <play card>:<1/-1>:addr
        # play card : this is the card which the current client choose to play
        # <1/-1> : 1 if the card is played straight / -1 if the player striked an oponent
        data = data.decode()
        data = data.split(':')
        data.append(addr)
        dataRecved.append(data)
        if data[-2] == '-1':
            print('Striked the round.')
            Strike = True
        else:
            Strike = False
        print(dataRecved)
        # this if condition checkes if a full round of play is ove or not
        if len(dataRecved) >= All_connections + 1 or Strike == True:
            print('a full round is over checking for max card')
            if Strike == True:
                tempData = dataRecved
                tempData.pop()
            else:
                tempData = dataRecved
            mcard = getMaxCard(tempData)
            tclient = getClientFromCard(mcard)
            for i, d in enumerate(All_address):         #this will change the address to conn type
                if d == tclient:
                    tclient = All_connections[i]
                    break
            allcards = []
            for i in dataRecved:
                allcards.append(i[0])
            allcards = ''.join(allcards)
            if Strike == True:
                Send('add:'+allcards,tclient)      #this makes the client receve all the cards just played
            Send('playnew:',tclient)       #this makes the client start a new round
            dataRecved = []
        else:
            allcards = []
            for i in dataRecved:
                allcards.append(i[0])
            allcards = ''.join(allcards)
            #the code for makeing the next player play the game is writen here
            d = dataRecved[-1]
            adr = d[-1]
            for i,a in All_address:
                if adr == a:
                    i+=1
                    break
            i = i%len(All_address)  #this code will make the cyclic effect
            adr = All_address[i]
            con = All_connections[i]
            if adr == '1':
                #the server is to play
                isPlay = True
                incards = allcards
            else:
                isPlay = False
                incards = allcards
                for c in All_connections:   #this code will send all the incards to all the clients and also tell which player to play next
                    if c == con:
                        Send('play:' + allcards, con)
                    else:
                        Send('just:'+ allcards,c)
#returns the list of data recved from the other computers
def getData():
    return(dataRecved)

def main(clients):
    numberOfClients = clients
    socket_create()
    socket_bind()
    socket_accept(clients)