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

ARROW_HEIGHT = 2
ARROW_WIDTH = 30
ARROW_IMAGE = pygame.image.load("arrow.png")

GAME_CONTINUE = True
GAME_FPS = 30

game_canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('BOW AND ARROW - RECREATION')

for x in range(10):
    BALLOON_CONTAINER.append(1)

game_canvas.fill(GREEN)
pygame.display.update()

game_clock = pygame.time.Clock()


while GAME_CONTINUE:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_CONTINUE = False

    #game_canvas.fill(GREEN)
    game_canvas.blit(GAME_BACKGROUND_IMAGE, (0, 0))
    BALLOON_GAME_COORDINATES_CONTAINER = []
    
    for y in range(17):
        #game_canvas.fill(RED,rect = [BALLOON_GAME_WIDTH,BALLOON_GAME_HEIGHT,10,10])
        game_canvas.blit(BALLOON_IMAGE,(BALLOON_GAME_WIDTH,BALLOON_GAME_HEIGHT))
        BALLOON_GAME_COORDINATES_CONTAINER.append(BALLOON_GAME_WIDTH)
        BALLOON_GAME_WIDTH += 30
    
    mouse_location = pygame.mouse.get_pos()[1]
    game_canvas.fill(RED,rect = [50,mouse_location,10,10])

    pygame.display.update()
    BALLOON_GAME_HEIGHT -= 5
    if BALLOON_GAME_HEIGHT <= 0:
        BALLOON_GAME_HEIGHT = SCREEN_HEIGHT
    BALLOON_GAME_WIDTH = 280
    game_clock.tick(GAME_FPS)



pygame.quit()
quit()

