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

global Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = img.load("img/player.png").convert()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.speed = 4
player = Player()

# Objects
class _object(pygame.sprite.Sprite):

    def __init__(self, type, location):
        self.type = type
        self.location = location
        # ADDNEW
        if type == 0:
            cobblestone.__init__(self)
        elif type == 1:
            empty.__init__(self)
        elif type == 2:
            dirt_1.__init__(self)
        elif type == 3:
            dirt_2.__init__(self)
        elif type == 4:
            dirt_3.__init__(self)
        elif type == 5:
            # player spawn marker, rendered as empty
            empty.__init__(self)
        elif type == 6:
            flag.__init__(self)
        elif type == 7:
            spike.__init__(self)
        elif type == 8:
            player_dead.__init__(self)

    def setup(self):
        self.size = self.image.get_rect().size
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

def addobj(name,num):
    exec("""class {}(_object):
        def __init__(self):
            self.image = img.load(object_list[{}]).convert_alpha()
            self.setup()
    """.format(name,num),globals())

    exec("object_{} = _object({}, (0, 0))".format(num,num),globals())

# Blocks
# ADDNEW
addobj("cobblestone", 0)
addobj("empty", 1)
addobj("dirt_1", 2)
addobj("dirt_2", 3)
addobj("dirt_3", 4)
addobj("player_marker", 5)
addobj("flag", 6)
addobj("spike", 7)
addobj("player_dead", 8)

def loadmap(file):
    global current_map
    global current_map_size
    f = open(file, "rb")
    current_map_size, current_map = pickle.load(f)
    f.close()
loadmap("levels/lvl_1.txt")

def check_collide(hit_list):
    # output a list containing all types of obj player has collided with
    global TILESIZE
    global hit_types
    for tile in hit_list:
        slot_x = int(tile.x/TILESIZE)
        slot_y = int(tile.y/TILESIZE)
        hit_types.append(check_collide_sub(slot_x,slot_y))
    

def check_collide_sub(slot_x,slot_y):
    global current_map
    global current_map_size
    temp = 0
    for obj in current_map:
        if current_map_size[0] > temp:
            tempx = temp
            tempy = 0
        else:
            tempx = (temp - current_map_size[0] * int(temp/current_map_size[0]))
            tempy = int(temp/current_map_size[0])
        if slot_x == tempx and slot_y == tempy:
            return int(obj)
        temp += 1
        

def player_death():
    global player_corpses
    global player
    global current_map
    global current_map_size
    global TILESIZE

    # Add players corpse to a list, blit separately from other things
    player_corpses.append(pygame.Rect(player.rect.x,player.rect.y,TILESIZE,TILESIZE))
    temp = 0
    for obj in current_map:
        if current_map_size[0] > temp:
            tempx = temp*TILESIZE
            tempy = 0
        else:
            tempx = (temp - current_map_size[0] * int(temp/current_map_size[0]))*TILESIZE
            tempy = int(temp/current_map_size[0])*TILESIZE
        if int(obj) == 5:
            player.rect.x = tempx
            player.rect.y = tempy
        temp += 1



def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect,movement,tiles,hit_types):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
    hit_list = collision_test(rect,tiles)
    check_collide(hit_list)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    check_collide(hit_list)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

while True: # game loop

    if game_state == "playing":
        display.fill(LIGHTBLUE) # clear screen by filling it with blue

        true_scroll[0] += (player.rect.x-true_scroll[0]-336)/20
        true_scroll[1] += (player.rect.y-true_scroll[1]-196)/20
        scroll[0] = int(true_scroll[0])
        scroll[1] = int(true_scroll[1])

        tile_rects = []
        hit_types = []
        temp = 0
        for obj in current_map:
            if current_map_size[0] > temp:
                tempx = temp*TILESIZE
                tempy = 0
            else:
                tempx = (temp - current_map_size[0] * int(temp/current_map_size[0]))*TILESIZE
                tempy = int(temp/current_map_size[0])*TILESIZE
            # If type is in collision_list, put in collision rect list
            if int(obj) in collision_list:
                tile_rects.append(pygame.Rect(tempx,tempy,TILESIZE,TILESIZE))
            exec("display.blit(object_{}.image, ({},{}))".format(obj, tempx-scroll[0], tempy-scroll[1]), globals())
            temp += 1
        for obj in player_corpses:
            display.blit(object_8.image, (obj.x-scroll[0],obj.y-scroll[1]))
            tile_rects.append(obj)
        player_movement = [0,0]
        if moving_right == True:
            player_movement[0] += player.speed
        if moving_left == True:
            player_movement[0] -= player.speed
        player_movement[1] += vertical_momentum
        vertical_momentum += 0.2
        if vertical_momentum > JUMPLENGTH*-1:
            vertical_momentum = JUMPLENGTH*-1

        player.rect,collisions = move(player.rect,player_movement,tile_rects,hit_types)
        if 7 in hit_types and collisions["bottom"] == True:
            player_death()

        if collisions['bottom'] == True:
            air_timer = 0
            vertical_momentum = 0
        else:
            air_timer += 1
        if collisions['top'] == True:
            vertical_momentum = 0
        
        # Check if player is touching flag and end level
        if 6 in hit_types:
            game_state = "new_level"
        

        display.blit(player.image,(player.rect.x-scroll[0],player.rect.y-scroll[1]))

        # Check if player is touching spike and kill player
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

    elif game_state == "load_level":
        exec("loadmap('levels/lvl_{}.txt')".format(current_level))
        player_corpses = []
        temp = 0
        for obj in current_map:
            if current_map_size[0] > temp:
                tempx = temp*TILESIZE
                tempy = 0
            else:
                tempx = (temp - current_map_size[0] * int(temp/current_map_size[0]))*TILESIZE
                tempy = int(temp/current_map_size[0])*TILESIZE
            if int(obj) == 5:
                player.rect.x = tempx
                player.rect.y = tempy
            temp += 1
        game_state = "playing"

    elif game_state == "new_level":
        game_state = "load_level"
        current_level+=1

    
    else:
        print("ERR: Invalid game_state #100")
    pygame.display.update()
    clock.tick(60)
