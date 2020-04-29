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
# loads all menu images
global menu
menu.loadall()


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
        elif type == 9:
            clone_1.__init__(self)
        elif type == 10:
            clone_2.__init__(self)
        elif type == 11:
            clone_3.__init__(self)
        elif type == 12:
            clone_4.__init__(self)
        elif type == 13:
            clone_5.__init__(self)
        elif type == 14:
            clone_6.__init__(self)
        elif type == 15:
            clone_7.__init__(self)
        elif type == 16:
            clone_8.__init__(self)
        elif type == 17:
            clone_9.__init__(self)
        elif type == 18:
            clone_10.__init__(self)
        elif type == 19:
            clone_11.__init__(self)
        elif type == 20:
            clone_12.__init__(self)
        elif type == 21:
            clone_13.__init__(self)


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
addobj("clone_1", 9)
addobj("clone_2", 10)
addobj("clone_3", 11)
addobj("clone_4", 12)
addobj("clone_5", 13)
addobj("clone_6", 14)
addobj("clone_7", 15)
addobj("clone_8", 16)
addobj("clone_9", 17)
addobj("clone_10", 18)
addobj("clone_11", 19)
addobj("clone_12", 20)
addobj("clone_13", 21)

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
    global current_clone
    for tile in hit_list:
        slot_x = int(tile.x/TILESIZE)
        slot_y = int(tile.y/TILESIZE)
        hit_types.append(check_collide_sub(slot_x,slot_y))
        # if player is colliding with a clone machine block
        for i in range(9, 21): 
            if i in hit_types:
                current_clone = [tile.x,tile.y]


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
        

def player_death(generate_corpse):
    global player_corpses
    global player
    global current_map
    global current_map_size
    global TILESIZE
    global current_clone
    global game_state

    # if player has died with no cloning machine to clone from
    if current_clone == []:
        game_state = "game_over"
        return None
    # Add players corpse to a list, blit separately from other things
    if generate_corpse:
        player_corpses.append(pygame.Rect(player.rect.x,player.rect.y,TILESIZE,TILESIZE))
    tilex = int(current_clone[0]/TILESIZE)
    tiley = int(current_clone[1]/TILESIZE)
    player.rect.x = current_clone[0]
    player.rect.y = current_clone[1]+TILESIZE
    current_map[current_map_size[0]*tiley+tilex] += 1
    # if the cloning machine is empty after removing a level
    if current_map[current_map_size[0]*tiley+tilex] == 21:
        # empty current_clone
        current_clone = []


def blit_if_selected(name,module,x_start,x_end,y_start,y_end):
    if x_start <= mouse_x <= x_end and y_start <= mouse_y <= y_end:
        # mouse over [name]
        exec("win.blit({}.{}_select, ({},{}))".format(module,name,x_start,y_start))
    else:
        exec("win.blit({}.{}, ({},{}))".format(module,name,x_start,y_start))


def check_if_selected(x_start,x_end,y_start,y_end):
    if x_start <= mouse_x <= x_end and y_start <= mouse_y <= y_end:
        # mouse over [name]
        return True
    else:
        return False


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
    mouse_x, mouse_y = pygame.mouse.get_pos()

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
            # only blit if object is visible on screen
            if -TILESIZE <= tempx-scroll[0] <= 640 and -TILESIZE <= tempy-scroll[1] <= 360:
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
            player_death(True)
        
        # if player is below map
        if player.rect.y > current_map_size[1]*TILESIZE:
            player_death(False)
    
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

        
        win.blit(pygame.transform.scale(display,(WIDTH, HEIGHT)),(0,0))

    elif game_state == "load_level":
        exec("loadmap('levels/lvl_{}.txt')".format(current_level))
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
        player_corpses = []
        current_clone = []

    elif game_state == "game_over":
        win.blit(menu.game_over_bg, (0,0))
        blit_if_selected("game_over_restart","menu",738,1182,498,580)

        mouse_1, mouse_2, mouse_3 = pygame.mouse.get_pressed()
        if mouse_1:    
            if check_if_selected(738,1182,498,580):
                # restart
                game_state = "load_level"
                player_corpses = []
                current_clone = []
        # TODO: make a game over screen with restart, quit, and quit and save
    
    else:
        print("ERR: Invalid game_state #100")
    
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

    pygame.display.update()
    clock.tick(60)
