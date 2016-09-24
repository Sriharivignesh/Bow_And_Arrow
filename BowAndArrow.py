import pygame
import time
import os
import random
import numpy
import bisect
import sys

pygame.init()

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,200,0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BALLOON_CONTAINER = []
BALLOON_GAME_COORDINATES_CONTAINER = []
BALLOON_HEIGHT = 30
BALLOON_WIDTH = 30
BALLOON_GAME_HEIGHT = 600
BALLOON_GAME_WIDTH = 280
BALLOON_IMAGE = pygame.image.load("balloon.png")
BALLOON_BURST_IMAGE = pygame.image.load("balloon_burst.png")

GAME_BACKGROUND_IMAGE = pygame.image.load("background.jpg")

MOUSE_CLICK_CURRENT = 0
MOUSE_CLICK_PREVIOUS = 0

ARROW_HEIGHT = 2
ARROW_WIDTH = 30
ARROW_IMAGE = pygame.image.load("arrow.png")
ARROW_SHOT = False
ARROW_COORDINATES = []
ARROW_CONTAINER = []

BOW_IMAGE = pygame.image.load("archer.gif")

GAME_CONTINUE = True
GAME_FPS = 30

class Balloons(pygame.sprite.Sprite):

    def __init__(self):

        super(Balloons, self).__init__()
        self.image = BALLOON_IMAGE
        self.rect = self.image.get_rect()
        self.Fallen_Balloon = False

    def set_balloon_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def balloon_move(self):
        if self.Fallen_Balloon == False:
            if self.rect.y <= 0:
                self.rect.y = SCREEN_HEIGHT
            else:
                self.rect.y -= 5
        else:
            if self.rect.y >= SCREEN_HEIGHT:
                self.kill()
            else:
                self.rect.y += 5
    
    def balloon_burst(self):
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
            self.kill()
        else:
            self.rect.x += 10

BALLOON_GROUP = pygame.sprite.Group()
ARROW_GROUP = pygame.sprite.Group()

for i in range(17):
    temp_balloon = Balloons()
    temp_balloon.set_balloon_position(BALLOON_GAME_WIDTH, BALLOON_GAME_HEIGHT)
    BALLOON_GAME_WIDTH += 30
    BALLOON_GROUP.add(temp_balloon)

game_canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('BOW AND ARROW - RECREATION')

game_canvas.fill(GREEN)
pygame.display.update()

game_clock = pygame.time.Clock()

while GAME_CONTINUE:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_CONTINUE = False


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
        #print("ONE MOUSE CLICK CYCLE DONE")
        ARROW_SHOT = True
        temp_arrow = Arrow()
        temp_arrow.set_arrow_position(30, bow_location + 35)
        ARROW_GROUP.add(temp_arrow)
        MOUSE_CLICK_PREVIOUS = 0

    for all_balloons in BALLOON_GROUP:
        all_balloons.balloon_move() 

    for all_arrows in ARROW_GROUP:
        all_arrows.arrow_move()
    
    BALLOON_GROUP.draw(game_canvas)
    ARROW_GROUP.draw(game_canvas)
    pygame.display.update()
    game_clock.tick(GAME_FPS)



pygame.quit()
quit()

