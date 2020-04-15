
import pygame
from pygame import image as img
import time
import math
import random
import pickle

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

win = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
pygame.display.set_caption("Blue V.3 Editor")
clock = pygame.time.Clock()

menu_page = 1

object_list = [

              "img/cobble.png"

              ]

current_map = []

class _object(pygame.sprite.Sprite):

    def __init__(self, type, location):
        self.type = type
        self.location = location

        if type == 0:
            # Cobblestone
            Cobblestone.__init__(self)

    def setup(self):
        self.size = self.image.get_rect().size
        self.mask = pygame.mask.from_surface(self.image)

class Cobblestone(_object):
    def __init__(self):
        self.image = img.load(object_list[0]).convert_alpha()
        self.setup()
        self.rect = self.image.get_rect()


def updates_and_draw():
    
    # Update and draw menu
    if menu_page == 1:
        import os
        print(os.getcwd())
        cbbl = img.load("cobble.png").convert()
        win.blit(cbbl, (10, 10))
        

   


run = True
while run:
    clock.tick(60)
    x, y = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    # TODO: replace with actual menu
    if keys[pygame.K_ESCAPE]:
        run = False

    updates_and_draw()
    pygame.display.update()


pygame.quit()