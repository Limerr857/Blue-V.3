
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

object_list = [

              "img/cobble.png"

              ]

class _object():

    def __init__(self, type, location):
        self.type = type
        self.location = location

        if type == 0:
            pass


def updates_and_draw():
    
    if 


run = True
while run:
    clock.tick(60)
    x, y = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    updates_and_draw()
    pygame.display.update()


pygame.quit()