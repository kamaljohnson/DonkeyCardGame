import Display
import threading
import socket
import menu
import pygame
import server
import client

pygame.init()

#this funtions will update the screen regularly with a particular FPS
def drawing():
    print('i am here')
    while True:
        Display.drawing()
drawingThread = threading.Thread(target=drawing)
drawingThread.start()



#this funtion will return the list of numbers if the string of the numbers are givem
def getcard(cardNumbers,s):
    for i in range(len(cardNumbers)):
        cardNumbers[i] = int(cardNumbers[i])
    if s == 1:
        cardNumbers = sorted(cardNumbers)
    return cardNumbers
Display.bootUp()

while(True):
    main_menu = ['HOST','JOIN','HELP','EXIT']
    mainMenu = menu.Menu()
    select = mainMenu.menu_UI(main_menu)
    if select == 0:
        server_menu = ['2 PLAYER', '3 PLAYER', '4 PLAYER', '5 PLAYER']
        server_Menu = menu.Menu()
        players = mainMenu.menu_UI(server_menu)
        players+=1
        host = socket.gethostbyname(socket.gethostname())
        host = host.split('.')
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
