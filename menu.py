
import pygame
from pygame.locals import *

pygame.init()
pygame.mixer.init()

sound_select = pygame.mixer.Sound("sound.wav")  # this is the sound given for seleciton
background = pygame.image.load('Assets\\Board.png')
screenx = 600          # this will be the screen size
screeny = 600

screen2 = pygame.display.set_mode((screenx,screeny))
background = pygame.transform.scale(background,(screenx,screeny))
class Menu():
    menu = [];  #will be used to enter the requires list for a particular task

    # the codes for different colors are initialised over here
    black = (100,0,0)
    blue = (200, 70, 10)
    white = (220,70,80)
    default_screen_color = white

    def __init__(self,set_screen = screen2,screen_color = default_screen_color):
        screen = set_screen
        self.default_screen_color = screen_color

    def menu_UI(self,current_menu):
        pos = 0
        screen2.blit(background, (0, 0))
        blitBackground = True
        while(True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        blitBackground = True
                        if pos != len(current_menu) - 1:
                            sound_select.play()
                        pos += 1
                    elif event.key == pygame.K_UP:
                        blitBackground = True
                        if pos != 0:
                            sound_select.play()
                        pos -= 1
                    elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        return(pos)
                else:
                    blitBackground = False
                if pos ==len(current_menu):
                    blitBackground = False
                    pos = len(current_menu) - 1
                if pos<0:
                    blitBackground = False
                    pos = 0
                if(blitBackground):
                    screen2.blit(background,(0,0))
                #pygame.display.update()
                for menu_pos in range(len(current_menu)):
                    if pos == menu_pos:
                        myfont = pygame.font.SysFont("arial", 70)
                        label = myfont.render(current_menu[menu_pos], 2, self.black)
                        screen2.blit(label,(screenx//2-80,screeny//2 - 50))
                    else:
                        myfont = pygame.font.SysFont("arial", 50)
                        label = myfont.render(current_menu[menu_pos], 2, self.blue)
                        screen2.blit(label, (screenx//2-60,screeny//2 + (menu_pos - pos)*65 - 50))
                    #pygame.display.update()