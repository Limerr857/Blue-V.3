import pygame
import sys
from variables import *
import pickle
from pygame.locals import *
import pygame.image as img

clock = pygame.time.Clock()


pygame.init() # initiates pygame

pygame.display.set_caption(TITLE)


win = pygame.display.set_mode((WIDTH,HEIGHT), pygame.FULLSCREEN) # initiate the window

display = pygame.Surface((640,360)) # used as the surface for rendering

moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0
true_scroll = [0,0]
scroll = [0,0]

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = img.load("img/player.png").convert()
        self.rect = self.image.get_rect()
        self.rect.x = 5*32
        self.rect.y = 3*32
        self.speed = 4
player = Player()

# Objects
class _object(pygame.sprite.Sprite):

    def __init__(self, type, location):
        self.type = type
        self.location = location

        if type == 0:
            # Cobblestone
            Cobblestone.__init__(self)
        elif type == 1:
            # Empty
            empty.__init__(self)
        elif type == 2:
            dirt_1.__init__(self)
        elif type == 3:
            dirt_2.__init__(self)
        elif type == 4:
            dirt_3.__init__(self)

    def setup(self):
        self.size = self.image.get_rect().size
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()


class Cobblestone(_object):
    def __init__(self):
        self.image = img.load(object_list[0]).convert_alpha()
        self.setup()


class empty(_object):
    def __init__(self):
        self.image = img.load(object_list[1]).convert_alpha()
        self.setup()


class dirt_1(_object):
    def __init__(self):
        self.image = img.load(object_list[2]).convert_alpha()
        self.setup()

class dirt_2(_object):
    def __init__(self):
        self.image = img.load(object_list[3]).convert_alpha()
        self.setup()

class dirt_3(_object):
    def __init__(self):
        self.image = img.load(object_list[4]).convert_alpha()
        self.setup()

# Blocks
object_0 = _object(0, (0, 0))
object_1 = _object(1, (0, 0))
object_2 = _object(2, (0, 0))
object_3 = _object(3, (0, 0))
object_4 = _object(4, (0, 0))

def loadmap(file):
    global current_map
    global current_map_size
    f = open(file, "rb")
    current_map_size, current_map = pickle.load(f)
    f.close()
loadmap("levels/lvl_1.txt")

def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect,movement,tiles):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

while True: # game loop
    display.fill(LIGHTBLUE) # clear screen by filling it with blue

    true_scroll[0] += (player.rect.x-true_scroll[0]-336)/20
    true_scroll[1] += (player.rect.y-true_scroll[1]-196)/20
    scroll[0] = int(true_scroll[0])
    scroll[1] = int(true_scroll[1])

    tile_rects = []
    temp = 0
    for obj in current_map:
        if current_map_size[0] > temp:
            tempx = temp*TILESIZE
            tempy = 0
        else:
            tempx = (temp - current_map_size[0] * int(temp/current_map_size[0]))*TILESIZE
            tempy = int(temp/current_map_size[0])*TILESIZE
        # If type is not empty, put in collision thing
        if int(obj) != 1:
            tile_rects.append(pygame.Rect(tempx,tempy,TILESIZE,TILESIZE))
        exec("display.blit(object_{}.image, ({},{}))".format(obj, tempx-scroll[0], tempy-scroll[1]), globals())
        temp += 1

    player_movement = [0,0]
    if moving_right == True:
        player_movement[0] += player.speed
    if moving_left == True:
        player_movement[0] -= player.speed
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > JUMPLENGTH*-1:
        vertical_momentum = JUMPLENGTH*-1

    player.rect,collisions = move(player.rect,player_movement,tile_rects)

    if collisions['bottom'] == True:
        air_timer = 0
        vertical_momentum = 0
    else:
        air_timer += 1
    if collisions['top'] == True:
        vertical_momentum = 0

    display.blit(player.image,(player.rect.x-scroll[0],player.rect.y-scroll[1]))

    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 6:
                    vertical_momentum = JUMPLENGTH
            if event.key == K_ESCAPE:
                # TODO REPLACE
                pygame.quit()
                sys.exit()
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
        
    win.blit(pygame.transform.scale(display,(WIDTH, HEIGHT)),(0,0))
    pygame.display.update()
    clock.tick(60)
