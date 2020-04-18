
import pygame
from pygame import image as img
import time
import pickle

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

win = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
pygame.display.set_caption("Blue V.3")
clock = pygame.time.Clock()


def updates_and_draw():
    pass


run = True
while run:
    clock.tick(60)
    x, y = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if keys[pygame.K_ESCAPE]:
        run = False

    updates_and_draw()
    pygame.display.update()


pygame.quit()