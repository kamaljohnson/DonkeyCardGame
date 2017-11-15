import Display
import threading
from queue import Queue
import socket
import menu
import pygame
import server
import client
import time

pygame.init()

#this funtions will update the screen regularly with a particular FPS
def drawing():
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

while(True):
    main_menu = ['CREATE','JOIN','HELP','EXIT']
    mainMenu = menu.Menu()
    select = mainMenu.menu_UI(main_menu)
    if select == 0:
        host = socket.gethostbyname(socket.gethostname())
        print(host)
        host = host.split('.')
        print(host)
        code = host[-1]
        code = list(code)
        print(code)
        for i,c in enumerate(code):
            code[i] = chr(int(c)+65)
        code = ''.join(code)
        print(code)
        Display.displayServerCode(code)
        t = threading.Thread(target=server.main)
        t.start()
        time.sleep(20)
    elif select == 1:
        CODE = Display.getText('text')
        print(CODE)
        IP = '192.168.1.'
        CODE = list(CODE)
        for i,c in enumerate(CODE):
            CODE[i] = str(ord(CODE[i])-65)
        CODE = ''.join(CODE)
        CODE.replace(' ', '')
        print(CODE)
        IP += CODE
        print(IP)
        client.main(IP)
    elif select == 2:
        #code for displaying help
        pass
    else:
        pygame.quit()
        break
