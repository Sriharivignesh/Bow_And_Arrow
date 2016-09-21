import pygame
import time
import os
import random
import numpy

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
BALLOON_GAME_WIDTH = 300


ARROW_HEIGHT = 10
ARROW_WIDTH = 10

GAME_CONTINUE = True
GAME_FPS = 30

pygame.init()
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
    game_canvas.fill(GREEN)
    BALLOON_GAME_COORDINATES_CONTAINER = []
    for y in range(17):
        game_canvas.fill(RED,rect = [BALLOON_GAME_WIDTH,BALLOON_GAME_HEIGHT,10,10])
        BALLOON_GAME_COORDINATES_CONTAINER.append(BALLOON_GAME_WIDTH)
        BALLOON_GAME_WIDTH += 30
    
    mouse_location = pygame.mouse.get_pos()[1]
    game_canvas.fill(RED,rect = [50,mouse_location,10,10])

    pygame.display.update()
    BALLOON_GAME_HEIGHT -= 5
    if BALLOON_GAME_HEIGHT <= 0:
        BALLOON_GAME_HEIGHT = SCREEN_HEIGHT
    BALLOON_GAME_WIDTH = 300
    game_clock.tick(GAME_FPS)



pygame.quit()
quit()

