import pygame
import time
import pygame_textinput
import threading

pygame.init()
FPS = 60        #the frams per second is initialised to 30

def drawing():
    while True:
        time.sleep(1/FPS)
        pygame.display.update()

screenx = 600
screeny = 600    #these are the size of the screen for the game

textColour = (100,150,250)
white = (200,200,200)
black = (0,0,0)
red = (220,70,80)     #all the colours used in this game
cards = []
LOADING = False
class TestSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(TestSprite, self).__init__()
        self.images = []
        for i in range(24):
            self.images.append('Assets\\loading\\745-' + str(i) + '.jpg')    # assuming both images are 64x64 pixels
        self.index = 0
        self.image = self.images[self.index]

    def update(self):
        '''This method iterates through the elements inside self.images and
        displays the next one each tick. For a slower animation, you may want to
        consider using a timer of some sort so it updates slower.'''
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        return self.image
for i in range(1,54):
    card = 'Assets\\'+ str(i) +'.png'
    cards.append(card)

background = pygame.image.load('Assets\\Board.png')
screen = pygame.display.set_mode((screenx, screeny))
background = pygame.transform.scale(background,(screenx,screeny))
#screen.blit(background, (0, 0))

#pygame.display.update()
def loading():
    myfont = pygame.font.SysFont("arial", 30)
    my_sprite = TestSprite()
    while LOADING:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
        img = my_sprite.update()
        img = pygame.image.load(img)
        screen.blit(img,(screenx//2-130,screeny//2+50))
        #pygame.display.update()
        time.sleep(0.04)
def getText(string):
    textinput = pygame_textinput.TextInput()
    clock = pygame.time.Clock()
    flag = 0
    screen.blit(background, (0, 0))
    while flag == 0:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # Feed it with events every frame
            temp = textinput.update(events)
            # Blit its surface onto the screen
            screen.blit(textinput.get_surface(), (10, 10))
            #pygame.display.update()
            if temp:
                flag = 1
                return textinput.get_text()
def displayServerCode(string):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('quit')
            pygame.quit()
    myfont = pygame.font.SysFont("arial", 30)
    screen.blit(background,(0,0))

    pygame.draw.rect(screen, white, (screenx // 2 - 170, screeny // 2 - 30, 370, 50))

    label = myfont.render('USE THE CODE TO', 2, textColour)
    screen.blit(label, (screenx//2-130, screeny//2-150))

    label1 = myfont.render('JOIN THE GAME', 2, textColour)
    screen.blit(label1, (screenx // 2 - 110, screeny // 2 - 100))

    myfont = pygame.font.SysFont("arial", 50)
    label2 = myfont.render(string, 2, textColour)
    screen.blit(label2, (screenx // 2 - 164, screeny // 2-32))
    #pygame.display.update()
def displayMsg(string):
    count = 0
    TextC = textColour
    msglist = list(string)
    X = screenx // 2 - len(msglist)*7
    Y = screeny // 2
    k = 0
    textsize = 30
    while(True):
        k += 0.1
        count += 1
        screen.blit(background,(0,0))
        Y -= int(k)
        myfont = pygame.font.SysFont("arial", textsize)
        label = myfont.render(string, 2, TextC)
        screen.blit(label, (X,Y))
        #pygame.display.update()
        time.sleep(0.01)
        if count == 70:
            break
def getBoard():
    pass
def bootUp():
    screen.blit(background, (0, 0))
    space = 20
    x = screenx // 2 - (space*13 // 2 + 35)
    y = 70
    for card in range(1,53):
        x += space
        locCard = pygame.image.load(cards[52]).convert()
        locCard = pygame.transform.scale(locCard, (80, 105))
        screen.blit(locCard, (x, y))
        #pygame.display.update()
        if(card%13 == 0):
            y += 100
            x = screenx // 2 - (space * 13 // 2 + 35)
    y = 70
    for card in range(1,53):
        x += space
        locCard = pygame.image.load(cards[card - 1]).convert()
        locCard = pygame.transform.scale(locCard, (80, 105))
        screen.blit(locCard, (x, y))
        #pygame.display.update()
        if(card%13 == 0):
            y += 100
            x = screenx // 2 - (space * 13 // 2 + 35)
    time.sleep(1.2)
def displayCards(cardNumbers,cardsWithPlayers,incards):
    screen.blit(background, (0, 0))
    space = 30
    y = 10
    lenc = len(cardNumbers)
    if lenc > 5:
        space = 20
    if lenc > 10:
        space = 17
    x = 10
    for n in cardsWithPlayers:
        x = 10
        for i in range(n):
            locCard = pygame.image.load(cards[52]).convert()
            locCard = pygame.transform.scale(locCard, (30, 40))
            screen.blit(locCard, (x, y))
            #pygame.display.update()
            x += space
        y += 20
    x = screenx//2-(len(incards)*space//2+35)
    y = 260
    for card in incards:
        x+=space
        locCard = pygame.image.load(cards[card-1]).convert()
        locCard = pygame.transform.scale(locCard,(80,105))
        screen.blit(locCard,(x,y))
        #pygame.display.update()
    x = screenx//2-(len(cardNumbers)*space//2+35)
    y = 450
    for card in cardNumbers:
        x+=space
        locCard = pygame.image.load(cards[card-1]).convert()
        locCard = pygame.transform.scale(locCard,(80,105))
        screen.blit(locCard,(x,y))
        #pygame.display.update()
    #pygame.display.update()
    time.sleep(10)
def selectCard(cardNumbers,cardsWithPlayers,incards): #code for selecting the card from the cards of the player
    index = 0
    cardno = -10
    screen.blit(background, (0, 0))
    change = True
    flag = 1
    while True:
        change = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    change = True
                    index -= 1
                    if index < 0:
                        index = len(cardNumbers) - 1
                if event.key == pygame.K_RIGHT:
                    change = True
                    index += 1
                    if index >= len(cardNumbers):
                        index = 0
                if event.key == pygame.K_SPACE:
                    change = True
                    return cardno,cardNumbers
        space = 20
        y = 10
        x = 10
        if change or flag == 1:
            screen.blit(background, (0, 0))
            flag = 0
            for n in cardsWithPlayers:
                x = 10
                for i in range(n):
                    locCard = pygame.image.load(cards[52]).convert()
                    locCard = pygame.transform.scale(locCard, (30, 40))
                    screen.blit(locCard, (x, y))
                    x += space
                y += 20
            x = screenx // 2 - (len(incards) * space // 2 + 35)
            y = 260
            for card in incards:
                x += space
                locCard = pygame.image.load(cards[card - 1]).convert()
                locCard = pygame.transform.scale(locCard, (80, 105))
                screen.blit(locCard, (x, y))
                # pygame.display.update()
            x = screenx // 2 - (len(cardNumbers) * space // 2 + 35)
            y = 450
            count = 0
            for card in cardNumbers:
                x += space
                locCard = pygame.image.load(cards[card - 1]).convert()
                locCard = pygame.transform.scale(locCard, (80, 105))
                if count == index:
                    screen.blit(locCard, (x, y-20))
                    cardno = card
                else:
                    screen.blit(locCard, (x, y))
                count += 1
