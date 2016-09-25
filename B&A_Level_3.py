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

#Set Bubble characteristics
BUBBLE_HEIGHT = 30
BUBBLE_WIDTH = 30
BUBBLE_IMAGE = pygame.image.load("Level_3_Sprites/bubble.png")
BUBBLE_IMAGE = pygame.transform.scale(BUBBLE_IMAGE, (30, 30))
BUBBLE_BURST_IMAGE = pygame.image.load("Level_3_Sprites/bubble_burst.png")
BUBBLE_BURST_IMAGE = pygame.transform.scale(BUBBLE_BURST_IMAGE, (BUBBLE_WIDTH, BUBBLE_HEIGHT))
BUBBLE_GROUP = pygame.sprite.Group() #Bubble sprite group

#Set game background
GAME_BACKGROUND_IMAGE = pygame.image.load("Common_Sprites/background.jpg")
GAME_OVER = False
game_canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('BOW AND ARROW - Level 3 - Bubbles --- ARROWS: %d' %30)

game_canvas.fill(GREEN)
pygame.display.update()

game_clock = pygame.time.Clock()

#Variables to detect mouse click
MOUSE_CLICK_CURRENT = 0
MOUSE_CLICK_PREVIOUS = 0

#Set Arrow Characteristics
ARROW_HEIGHT = 2
ARROW_WIDTH = 30
ARROW_IMAGE = pygame.image.load("Common_Sprites/arrow.png")
ARROW_LIMIT = 30
ARROWS = ARROW_LIMIT
ARROW_GROUP = pygame.sprite.Group() #Arrow sprite group

#Set Bow image
BOW_IMAGE = pygame.image.load("Common_Sprites/archer.gif")

#Game loop driver
GAME_CONTINUE = True

#Set Game FPS Rate
GAME_FPS = 30

GAME_FONT = pygame.font.SysFont("comicsans", 50)

#Bubble class
class Bubbles(pygame.sprite.Sprite):

    def __init__(self):

        super(Bubbles, self).__init__()
        self.image = BUBBLE_IMAGE
        self.rect = self.image.get_rect() #Get rect element for Bubble sprite image
        self.Fallen_Bubble = False  #Variable to be set as True when Bubble is struck by arrow

    def set_bubble_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def bubble_move(self): #Move the Bubble up if it hasn't been burst yet. Otherwise move it down
        if self.Fallen_Bubble == False:
            if self.rect.y <= 0:
                self.rect.y = SCREEN_HEIGHT
            else:
                self.rect.y -= 5
        else:
            if self.rect.y <= 0 or self.rect.x <= 0:
                self.kill() #Kill the sprite when the burst Bubble fully falls down
            else:
                self.rect.x -= 5
                self.rect.y -= 5
    
    def bubble_burst(self): #Method called when collision between arrow and Bubble is detected
        self.image = BUBBLE_BURST_IMAGE
        self.Fallen_Bubble = True



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

def message_to_screen(message, color):
    game_canvas.blit(GAME_BACKGROUND_IMAGE, (0, 0))
    message_surface = GAME_FONT.render(message, 1, color)
    message_rect = message_surface.get_rect()
    message_rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    game_canvas.blit(message_surface, message_rect)
    pygame.display.update()


#Populate Bubble sprite group with Bubble sprites
def populate_bubbles():
    for i in range(17):
        temp_bubble = Bubbles()
        while True:
            temp_bubble.set_bubble_position(random.randrange(280, 800, 50), random.randrange(0, 600, 50))
            if pygame.sprite.spritecollideany(temp_bubble, BUBBLE_GROUP) == None:
                break
        BUBBLE_GROUP.add(temp_bubble)
        ARROW_GROUP.empty()


populate_bubbles()


while GAME_CONTINUE:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_CONTINUE = False
        elif GAME_OVER == True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    GAME_OVER = False
                    GAME_FPS = 30
                    populate_bubbles()
                    ARROWS = ARROW_LIMIT
                elif event.key == pygame.K_n:
                    GAME_CONTINUE = False
    
    if len(BUBBLE_GROUP) == 0:
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
                ARROWS -= 1
            MOUSE_CLICK_PREVIOUS = 0

        for bubble in BUBBLE_GROUP:
            bubble.bubble_move() 

        for arrow in ARROW_GROUP:
            arrow.arrow_move()

        for bubble in pygame.sprite.groupcollide(BUBBLE_GROUP, ARROW_GROUP, False, False): #Collision detection function of pygame
            bubble.bubble_burst()

        BUBBLE_GROUP.draw(game_canvas)
        ARROW_GROUP.draw(game_canvas)
        pygame.display.set_caption('BOW AND ARROW - Level 3 - Bubbles --- ARROWS LEFT: %d' %ARROWS)
        pygame.display.update()

    game_clock.tick(GAME_FPS)






pygame.quit()
quit()