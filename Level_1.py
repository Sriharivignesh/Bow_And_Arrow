import pygame
import time
import os
import random
import numpy
import bisect
import sys

pygame.init()

#Color variables
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,200,0)

#Set screen height and screen width
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#Set Balloon characteristics
BALLOON_HEIGHT = 30
BALLOON_WIDTH = 30
BALLOON_GAME_HEIGHT = 600
BALLOON_GAME_WIDTH = 280
BALLOON_IMAGE = pygame.image.load("Level_1_Sprites/balloon.png")
BALLOON_BURST_IMAGE = pygame.image.load("Level_1_Sprites/balloon_burst.png")

#Set game background
GAME_BACKGROUND_IMAGE = pygame.image.load("Common_Sprites/background.jpg")

#Variables to detect mouse click
MOUSE_CLICK_CURRENT = 0
MOUSE_CLICK_PREVIOUS = 0

#Set Arrow Characteristics
ARROW_HEIGHT = 2
ARROW_WIDTH = 30
ARROW_IMAGE = pygame.image.load("Common_Sprites/arrow.png")
ARROW_LIMIT = 20
ARROWS = ARROW_LIMIT

#Set Bow image
BOW_IMAGE = pygame.image.load("Common_Sprites/archer.gif")


GAME_CONTINUE = True #Game loop driver
game_canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('BOW AND ARROW - RECREATION')
game_canvas.fill(GREEN)
pygame.display.update()
game_clock = pygame.time.Clock()
GAME_FPS = 30 #Set Game FPS Rate
GAME_FONT = pygame.font.SysFont("comicsans", 50)
GAME_OVER = False

#Balloon class
class Balloons(pygame.sprite.Sprite):

    def __init__(self):

        super(Balloons, self).__init__()
        self.image = BALLOON_IMAGE
        self.rect = self.image.get_rect() #Get rect element for balloon sprite image
        self.Fallen_Balloon = False  #Variable to be set as True when balloon is struck by arrow

    def set_balloon_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def balloon_move(self): #Move the balloon up if it hasn't been burst yet. Otherwise move it down
        if self.Fallen_Balloon == False:
            if self.rect.y <= 0:
                self.rect.y = SCREEN_HEIGHT
            else:
                self.rect.y -= 5
        else:
            if self.rect.y >= SCREEN_HEIGHT:
                self.kill() #Kill the sprite when the burst balloon fully falls down
            else:
                self.rect.y += 5
    
    def balloon_burst(self): #Method called when collision between arrow and balloon is detected
        self.image = BALLOON_BURST_IMAGE
        self.Fallen_Balloon = True



class Arrow(pygame.sprite.Sprite):
    def __init__(self):
        super(Arrow, self).__init__()
        self.image = ARROW_IMAGE
        self.rect = self.image.get_rect()

    def set_arrow_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def arrow_move(self):
        if self.rect.x >= SCREEN_WIDTH:
            self.kill() #Kill arrow sprite when it reaches the width of the screen
        else:
            self.rect.x += 10


BALLOON_GROUP = pygame.sprite.Group() #Balloon sprite group
ARROW_GROUP = pygame.sprite.Group() #Arrow sprite group



def message_to_screen(message, color):
    game_canvas.blit(GAME_BACKGROUND_IMAGE, (0, 0))
    message_surface = GAME_FONT.render(message, 1, color)
    message_rect = message_surface.get_rect()
    message_rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    game_canvas.blit(message_surface, message_rect)
    pygame.display.update()


#Populate Bubble sprite group with Bubble sprites
def populate_balloons():
    BALLOON_GROUP.empty()
    global BALLOON_GAME_WIDTH
    for i in range(17):
        temp_balloon = Balloons()
        temp_balloon.set_balloon_position(BALLOON_GAME_WIDTH, BALLOON_GAME_HEIGHT)
        BALLOON_GAME_WIDTH += 30
        BALLOON_GROUP.add(temp_balloon)
    BALLOON_GAME_WIDTH = 280

populate_balloons()

while GAME_CONTINUE:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_CONTINUE = False
        elif GAME_OVER == True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    GAME_OVER = False
                    GAME_FPS = 30
                    populate_balloons()
                    ARROW_GROUP.empty()
                    ARROWS = ARROW_LIMIT
                elif event.key == pygame.K_n:
                    GAME_CONTINUE = False

    if len(BALLOON_GROUP) == 0:
        GAME_OVER = True
        message_to_screen("You won! Continue?  Press Y or N", BLACK)
        GAME_FPS = 5

    elif ARROWS <= 0 and len(ARROW_GROUP) == 0:
        GAME_OVER = True
        message_to_screen("Sorry you lost! Play again? Press Y or N", BLACK)
        GAME_FPS -= 5

    if GAME_OVER == False:
        game_canvas.blit(GAME_BACKGROUND_IMAGE, (0, 0))
        mouse_location = pygame.mouse.get_pos()[1]
        bow_location = mouse_location
        if bow_location > SCREEN_HEIGHT - 50:
            bow_location = SCREEN_HEIGHT - 50 
        game_canvas.blit(BOW_IMAGE, (10,bow_location))

        MOUSE_CLICK = pygame.mouse.get_pressed()
        if MOUSE_CLICK[0] == 1:
            MOUSE_CLICK_PREVIOUS = 1
        
        elif MOUSE_CLICK[0] == 0 and MOUSE_CLICK_PREVIOUS == 1:
            if ARROWS > 0:
                temp_arrow = Arrow() #When mouse is clicked create a new arrow sprite and add it to the arrow sprite group
                temp_arrow.set_arrow_position(30, bow_location + 35)
                ARROW_GROUP.add(temp_arrow)
                MOUSE_CLICK_PREVIOUS = 0
                ARROWS -= 1

        for balloon in BALLOON_GROUP:
            balloon.balloon_move() 

        for arrow in ARROW_GROUP:
            arrow.arrow_move()

        for balloon in pygame.sprite.groupcollide(BALLOON_GROUP, ARROW_GROUP, False, False): #Collision detection function of pygame
            balloon.balloon_burst()
  
        BALLOON_GROUP.draw(game_canvas)
        ARROW_GROUP.draw(game_canvas)
        pygame.display.update()

    game_clock.tick(GAME_FPS)

pygame.quit()
quit()

