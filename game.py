import Display
import threading
import socket
import menu
import pygame
import server
import client
import random

def chunks(l, n):
    splitlist = []
    d = 52//n
    counter = 0
    c = 0
    minilist = []
    for item in l:
        counter+=1
        minilist.append(item)
        if counter % d == 0:
            splitlist.append(minilist)
            minilist = []
    k = 0
    while len(minilist)>0:
        counter+=1
        splitlist[k].append(minilist.pop())
        k+=1
    return splitlist
pygame.init()
#all the types of strings send  over the connection
#
#       1 - <name of the player> text           this is se
#       2 - <play>  text
#       3 - <display> text
AllTheCards = []
for x in range(1,53):
    AllTheCards.append(str(x)+' ')
random.shuffle(AllTheCards)
#this funtions will update the screen regularly with a particular FPS
def drawing():
    print('i am here')
    while True:
        Display.drawing()
drawingThread = threading.Thread(target=drawing)
drawingThread.start()



#this funtion will return the list of numbers if the string of the numbers are givem
def getcard(cardNumbers,s):
    print(cardNumbers)
    cardNumbers = cardNumbers.split()
    for i in range(len(cardNumbers)):
        print(cardNumbers[i])
        cardNumbers[i] = int(cardNumbers[i])
    if s == 1:
        cardNumbers = sorted(cardNumbers)
    return cardNumbers
#Display.bootUp()
players = 0

while(True):
    isServer = False
    main_menu = ['HOST','JOIN','HELP','EXIT']
    mainMenu = menu.Menu()
    select = mainMenu.menu_UI(main_menu)
    if select == 0:
        isServer = True
        server_menu = ['2 PLAYER', '3 PLAYER', '4 PLAYER', '5 PLAYER']
        server_Menu = menu.Menu()
        players = mainMenu.menu_UI(server_menu)
        players+=1
        while True:
            print('proces')
            host = socket.gethostbyname(socket.getfqdn())
            host = host.split('.')
            print(host)
            if '192' in host:
                break
        code = host[-1]
        code = list(code)
        for i,c in enumerate(code):
            code[i] = chr(int(c)+65)
        code = ''.join(code)
        Display.displayServerCode(code)
        t = threading.Thread(target=Display.loading)
        Display.LOADING = True
        t.start()
        server.main(players)
        Display.LOADING = False
        print('all the players are connected.')
        Display.bootUp()
    elif select == 1:
        CODE = Display.getText('enter the code')
        IP = '192.168.1.'
        CODE = list(CODE)
        for i,c in enumerate(CODE):
            CODE[i] = str(ord(CODE[i])-65)
        CODE = ''.join(CODE)
        CODE.replace(' ', '')
        IP += CODE
        client.main(IP)
    elif select == 2:
        #code for displaying help
        pass
    else:
        pygame.quit()
        break
    while True:
        play = False
        tempMenu = ['PLAY','EXIT']
        m = menu.Menu()
        select = m.menu_UI(tempMenu)
        mycards = ''
        if select == 0:
            play = True
            # shuffel the cards and do all the other initialisations for the game to begin
            if isServer:
                cards = chunks(AllTheCards,players+1)
                clients = server.All_connections
                for c in range(len(clients)):
                    cards[c] = ''.join(cards[c])
                    server.Send(cards[c],clients[c])
                cards[-1] = ''.join(cards[-1])
                mycards = cards[-1]
                print('My cards :',mycards)
                mycards = getcard(mycards,1)
            else:
                while True:
                    if len(client.all_recved_data)>0:
                        mycards = client.all_recved_data[-1]
                        break
                print('My cards :',mycards)
                mycards = getcard(mycards,1)
            Display.bootUp()
        elif select == 1:
            play = False
        while play:     #this is the main game loop
            #<my cards ,cards with players , in cards >
            Display.displayCards(mycards,[5,5,5,5],[1,2,3])
            S = input()
