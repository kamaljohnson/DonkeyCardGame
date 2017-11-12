from socket import socket, AF_INET,SOCK_DGRAM,gethostname,gethostbyname,getfqdn
from menu import *
import Display
import sys
import threading

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
    serverPORT = 5000
    if isServer:
        myIPread = list(myIP)
        for i in range(len(myIPread)):
            if myIPread[i] == '.':
                pass
            else:
                myIPread[i] = chr(int(myIPread[i])+65)
        myIPread = ''.join(myIPread)
        sip = '0.0.0.0'
        serverMenu = ['2 Players','3 Players','4 Players','5 Players']
        select = menu.menu_UI(serverMenu)
        thread.start()
        Display.displayServerCode(myIPread)
        mySocket = socket(AF_INET,SOCK_DGRAM)
        mySocket.bind((sip,serverPORT))
        clientAddr = [] #this list will store all the address of the players connected to the server
        print(select)
        for i in range(select+1):
            #PORTS.append(5000 + i)
            #mySocket.append(socket(AF_INET, SOCK_DGRAM))
            #mySocket[i].bind((sip, PORTS[i]))
            #try:
            print('waiting for the client to send messgae to the server. . .')
            data,addr = mySocket.recvfrom(SIZE)
            if addr not in clientAddr:
                clientAddr.append(addr)
            print(addr + ' is connected')
            print(clientAddr)
            msgthread = threading.Thread(target=Display.displayMsg,args=data + ' joined to the game')
            msgthread.start()
            #except:
            #    pass
        #print(PORTS)
        #while len(IPs) < len(PORTS):               #use clientAddr for sending to individual clients connected to the server
        #    data,addr = mySocket.recvfrom(SIZE)
        #    IPs.append(addr)
    else:
        text = Display.getText('ENTER CODE')
        text = list(text)
        for t in range(len(text)):
            if text[t] != '.':
                text[t] = str(ord(text[t])-65)
        serverIP = ''.join(text)
        mySocket = socket(AF_INET,SOCK_DGRAM)
        PORT = 5000    #the port is set to 0 so that at the run time it will be assigned to any free port
        thread.start()
        while True:
            try:
                print(PORT,serverIP)
                print('trying to connect to the server. . .')
                mySocket.bind((serverIP,PORT))
                mySocket.setblocking(0)
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