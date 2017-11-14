from socket import socket, AF_INET,SOCK_DGRAM,gethostname,gethostbyname,getfqdn
from menu import *
import Display
import sys
import threading
import IPaddress        #this module is for getting the ip address of all the computers connected to the system

import threading
from queue import Queue
import socket





####################################################################################################
def portscan(host):             #this funtion returns the socket object with the port connected to the given host
    print_lock = threading.Lock()

    q = Queue()
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #this type of socket is for local lan connections
    def portScan(port):                             #this is a basic funtion
        try:
            s.connect((host,port))
            return s
        except socket.error as err:
            print(str(err))
        with print_lock:
            print('the port:',port,'is connected to this computer')

    for port in range(1000,1100):        # the range of ports used in this porgram range from 1000 to 1100
        q.put(port)

    def threader():                 #invoking the portScanner funtion using the threader
        while True:
            port = q.get()
            portScan(port)
            q.task_done()

    for x in range(10):     #have 10 threads
        t = threading.Thread(target= threader)
        t.daemon = True             #the thread dies when the main thread dies
        t.start()

    q.join()        #the program will go beyond this line if all the taskes are over
                    #i.e. the queue becomes empty
############################################################################################################



#code for stoping a thread
def getcard(cardNumbers,s):
    for i in range(len(cardNumbers)):
        cardNumbers[i] = int(cardNumbers[i])
    if s == 1:
        cardNumbers = sorted(cardNumbers)
    return cardNumbers
isServer = False
SIZE = 2048
myname = 'admin'
currnetmenue = ['JOIN','CREATE','HELP','EXIT']
menu = Menu()
myIP = gethostbyname(getfqdn())
print('computer IP : ' + myIP)
while True:
    select = menu.menu_UI(currnetmenue)
    if select == 1:
        isServer = True
    elif select == 0:
        isServer = False
    elif select == 2:
        #Display.displayText_help()
        continue
    else:
        sys.exit()
    PORTS = []
    IPs = []
    mySocket = []
    serverIP = ''
    PORT = 0 # the port to the server from the currnet client
    thread = threading.Thread(target=Display.loading)
    serverPORT = 1000
    if isServer:    #the code for connecting to all the other computer goes here
        IPs = IPaddress.doRangeScan()       #now IPs will contain all the ip address of the other computers
        print(IPs,'these are all the ip addresses connected to this computer')
        for host in IPs:
            mySocket.append(portscan(host))
            print(mySocket)     #all the sockets created to the other computers connected to this computer
    else:
        text = Display.getText('ENTER CODE')
        text = list(text)
        for t in range(len(text)):
            if text[t] != '.':
                text[t] = str(ord(text[t])-65)
        serverIP = ''.join(text)
        mySocket = socket(AF_INET,SOCK_DGRAM)
        PORT = 0    #the port is set to 0 so that at the run time it will be assigned to any free port
        thread.start()
        while True:
            try:
                print(PORT,serverIP)
                print('trying to connect to the server. . .')
                mySocket.connect((serverIP,PORT))
                mySocket.sendto('hello'.encode('utf-8'),serverIP)
                print('sent hello to the server')
                break
            except:
                pass
    Display.bootUp()
    START = 1
    myTurn = False
    numberOfCardWithPlayers = []
    mycards = ''
    incards = ''
    WIN = False
    gameover = False
    while(True):
        if isServer:
            #code for the computer which acts as a server
            pass
        else:
            from_the_server = mySocket.recv(SIZE)
            from_the_server = from_the_server.decode()
            if START == 1:
                START = 0
                numberOfCardWithPlayers,mycards = from_the_server.split('/')
                mycards = mycards.split(' ')
                numberOfCardWithPlayers = numberOfCardWithPlayers.split(' ')
            else:
                numberOfCardWithPlayers,incards = from_the_server.split('/')
                incards = from_the_server.split(' ')
                if incards[-1] == 'lose':
                    gameover = True
                    WIN = False
                elif incards[-1] == 'won':
                    gameover = True
                    WIN = True
                if incards[-1] == 'play':
                    incards.pop()
                    myTurn = True
                else:
                    myTurn = False

        numberOfCardWithPlayers = getcard(numberOfCardWithPlayers,0)
        mycards = getcard(mycards,1)
        incards = getcard(incards,1)
        Display.displayCards(mycards,numberOfCardWithPlayers,incards)
        if myTurn == True:
            takenCard,mycards = Display.selectCard()      #this funtion will display the cards and make the player choose a card from his pile
            mySocket.sendto(str(takenCard).encode('utf-8'),(serverIP,PORT))
        if(gameover):
            print(WIN)
            break