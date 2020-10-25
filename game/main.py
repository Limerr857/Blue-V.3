import pygame
import sys
from variables import *
import pickle
from pygame.locals import *
import pygame.image as img
import math

clock = pygame.time.Clock()


pygame.init()  # initiates pygame

pygame.display.set_caption(TITLE)


win = pygame.display.set_mode(
    (WIDTH, HEIGHT), pygame.FULLSCREEN)  # initiate the window

display = pygame.Surface((640, 360))  # used as the surface for rendering
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

enemy_group = pygame.sprite.Group()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, type, location_x, location_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = exec("{}.__init__(self)".format(object_name_list[type]))
        self.rect.x = location_x
        self.rect.y = location_y
        self.type = type
        self.movement_tracker = -1
        enemy_group.add(self)

    def setup(self):
        self.size = self.image.get_rect().size
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

# Objects


class _object(pygame.sprite.Sprite):

    def __init__(self, type, location):
        self.type = type
        self.location = location

        if type != 5:
            exec("{}.__init__(self)".format(object_name_list[type]))
        elif type == 5:
            # player spawn marker, rendered as empty
            empty.__init__(self)
        # elif type in enemy_list:
        #     # enemy spawn marker, rendered as empty and enemies are then rendered separately
        #     empty.__init__(self)

    def setup(self):
        self.size = self.image.get_rect().size
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()


def addobj(name, num):
    exec("""class {}(_object):
        def __init__(self):
            self.image = img.load('img/' + object_name_list[{}] + '.png').convert_alpha()
            self.setup()
    """.format(name, num), globals())

    exec("object_{} = _object({}, (0, 0))".format(num, num), globals())


# blit all blocks
temp = 0
for obj in object_name_list:
    exec("addobj('{}', {})".format(obj, temp), globals())
    temp += 1


def loadmap(file):
    global current_map
    global current_map_size
    global current_enemies
    global enemy_list
    global enemy_group
    f = open(file, "rb")
    current_map_size, current_map = pickle.load(f)
    f.close()

    # Reset the current enemy count
    current_enemies = []
    current_enemies_rect = []
    enemy_group.empty()

    # Adds enemies in map to enemy list
    temp = 0
    temp2 = 0
    for obj in current_map:
        if current_map_size[0] > temp:
            tempx = temp*TILESIZE
            tempy = 0
        else:
            tempx = (temp - current_map_size[0] *
                     int(temp/current_map_size[0]))*TILESIZE
            tempy = int(temp/current_map_size[0])*TILESIZE
        # If type is enemy, put in current_enemies
        if int(obj) in enemy_list:
            # Enemy type , Enemy rect , Bounce reverse factor
            current_enemies.append(
                [int(obj), pygame.Rect(tempx, tempy, TILESIZE, TILESIZE), 1])
            current_enemies_rect.append(
                pygame.Rect(tempx, tempy, TILESIZE, TILESIZE))
            exec("enemy_{} = Enemy({},{},{})".format(
                temp2, int(obj), tempx, tempy))
            temp2 += 1
        temp += 1


loadmap("levels/lvl_1.txt")


def check_collide(hit_list):
    # output a list containing all types of obj player has collided with
    global TILESIZE
    global hit_types
    global current_clone
    for tile in hit_list:
        slot_x = int(tile.x/TILESIZE)
        slot_y = int(tile.y/TILESIZE)
        hit_types.append(check_collide_sub(slot_x, slot_y))
        # if player is colliding with a clone machine block
        for i in range(9, 20):
            if i == current_map[current_map_size[0]*slot_y+slot_x]:
                current_clone = [tile.x, tile.y]


def check_collide_sub(slot_x, slot_y):
    global current_map
    global current_map_size
    temp = 0
    for obj in current_map:
        if current_map_size[0] > temp:
            tempx = temp
            tempy = 0
        else:
            tempx = (temp - current_map_size[0]
                     * int(temp/current_map_size[0]))
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
    print("DEAD")

    # if player has died with no cloning machine to clone from
    if current_clone == []:
        game_state = "game_over"
        return None
    tilex = int(current_clone[0]/TILESIZE)
    tiley = int(current_clone[1]/TILESIZE)
    # if the cloning machine is empty before removing a level
    if current_map[current_map_size[0]*tiley+tilex] >= 21:
        # empty current_clone
        current_clone = []
    # if player has died with no cloning machine to clone from
    if current_clone == []:
        game_state = "game_over"
        return None
    # Add players corpse to a list, blit separately from other things
    if generate_corpse:
        player_corpses.append(pygame.Rect(
            player.rect.x, player.rect.y, TILESIZE, TILESIZE))
    player.rect.x = current_clone[0]
    player.rect.y = current_clone[1]-TILESIZE
    # Removes one level from the clone machine
    current_map[current_map_size[0]*tiley+tilex] += 1


def blit_if_selected(name, module, x_start, x_end, y_start, y_end):
    if x_start <= mouse_x <= x_end and y_start <= mouse_y <= y_end:
        # mouse over [name]
        exec("win.blit({}.{}_select, ({},{}))".format(
            module, name, x_start, y_start))
    else:
        exec("win.blit({}.{}, ({},{}))".format(module, name, x_start, y_start))


def check_if_selected(x_start, x_end, y_start, y_end):
    if x_start <= mouse_x <= x_end and y_start <= mouse_y <= y_end:
        # mouse over [name]
        return True
    else:
        return False


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def enemy_collision_test(rect, enemies):
    enemy_hit_list = []
    for tile in enemies:
        if rect.colliderect(tile):
            enemy_hit_list.append(tile)
    return enemy_hit_list


def move(rect, movement, tiles, hit_types, isplayer, secondpass):
    global enemy_group
    collision_types = {'top': False, 'bottom': False,
                       'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    enemy_hit_list = []
    if isplayer:
        check_collide(hit_list)
        enemy_hit_list = enemy_collision_test(rect, enemy_group.sprites())
        # kills player if they are touching enemy
        if enemy_hit_list != []:
            rect.x -= movement[0]
            if movement == [0, 0]:
                if not secondpass:
                    player_death(True)
            else:
                if not secondpass:
                    # TODO: Delete if nothing breaks:
                    # if movement[0] < 0:
                    #     movement[0] += player.speed
                    # elif movement[0] > 0:
                    #     movement[0] -= player.speed
                    # if movement[1] < 0:
                    #     movement[1] += player.speed
                    # elif movement[1] > 0:
                    #     movement[1] -= player.speed
                    # rect, collisions = move(
                    #     rect, movement, tile_rects, hit_types, True, True)
                    player_death(True)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    if isplayer:
        check_collide(hit_list)
        enemy_hit_list = enemy_collision_test(rect, enemy_group.sprites())
        # kills player if they are touching enemy
        if enemy_hit_list != []:
            # Used to prevent a bug where the players corpse would be generated inside an enemy by 1 pixel
            if movement[1] < 0:
                rect.y -= int(math.floor(movement[1]))
            else:
                rect.y -= movement[1]
            if movement == [0, 0]:
                if not secondpass:
                    player_death(True)
            else:
                if not secondpass:
                    # TODO: Delete if nothing breaks:
                    # if movement[0] < 0:
                    #     movement[0] += player.speed
                    # elif movement[0] > 0:
                    #     movement[0] -= player.speed
                    # if movement[1] < 0:
                    #     movement[1] += player.speed
                    # elif movement[1] > 0:
                    #     movement[1] -= player.speed
                    # rect, collisions = move(
                    #     rect, movement, tile_rects, hit_types, True, True)
                    player_death(True)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True

    return rect, collision_types


while True:  # game loop
    mouse_x, mouse_y = pygame.mouse.get_pos()

    if game_state == "playing":
        display.fill(LIGHTBLUE)  # clear screen by filling it with blue

        true_scroll[0] += (player.rect.x-true_scroll[0]-336)/20
        true_scroll[1] += (player.rect.y-true_scroll[1]-196)/20
        scroll[0] = int(true_scroll[0])
        scroll[1] = int(true_scroll[1])

        tile_rects = []
        hit_types = []

        # Blit all objects to screen
        temp = 0
        for obj in current_map:
            if current_map_size[0] > temp:
                tempx = temp*TILESIZE
                tempy = 0
            else:
                tempx = (
                    temp - current_map_size[0] * int(temp/current_map_size[0]))*TILESIZE
                tempy = int(temp/current_map_size[0])*TILESIZE
            # If type is in collision_list, put in collision rect list
            if int(obj) in collision_list:
                tile_rects.append(pygame.Rect(
                    tempx, tempy, TILESIZE, TILESIZE))
            # only blit if object isn't an enemy
            if int(obj) not in enemy_list:
                # only blit if object is visible on screen
                if -TILESIZE <= tempx-scroll[0] <= 640 and -TILESIZE <= tempy-scroll[1] <= 360:
                    exec("display.blit(object_{}.image, ({},{}))".format(
                        obj, tempx-scroll[0], tempy-scroll[1]), globals())
            temp += 1

        # Blit the players corpses
        for obj in player_corpses:
            display.blit(object_8.image, (obj.x-scroll[0], obj.y-scroll[1]))
            tile_rects.append(obj)

        player_movement = [0, 0]
        if moving_right == True:
            player_movement[0] += player.speed
        if moving_left == True:
            player_movement[0] -= player.speed
        player_movement[1] += vertical_momentum
        vertical_momentum += 0.2
        if vertical_momentum > JUMPLENGTH*-1:
            vertical_momentum = JUMPLENGTH*-1

        player.rect, collisions = move(
            player.rect, player_movement, tile_rects, hit_types, True, False)
        if 7 in hit_types and collisions["bottom"] == True:
            player_death(True)
        # if 23 in hit_types or 22 in hit_types:
        #     print("AAAAAAAAAAAAAAA")
        #     print(player_movement)
        #     player_movement[0] *= -1
        #     player_movement[1] *= -1
        #     print(player_movement)
        #     player.rect,collisions = move(player.rect,player_movement,tile_rects,hit_types,True)
        #     player_death(True)

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

        templist = enemy_group.sprites()
        for obj in enemy_group:
            # update postition of enemies
            # if type is enemy_bounce_x
            if obj.type == 22:
                # neccesary for making the object reverse directions when hitting a wall
                tempx = 0
                tempx = enemy_speed_x.copy()
                tempx[0] *= obj.movement_tracker

                obj.rect, collisions = move(
                    obj.rect, tempx, tile_rects, hit_types, False, False)
                # if the enemy hits a wall
                if collisions["left"] or collisions["right"]:
                    # reverse movement
                    if obj.movement_tracker == -1:
                        obj.movement_tracker = 1
                    elif obj.movement_tracker == 1:
                        obj.movement_tracker = -1

            # if type is enemy_bounce_y
            elif obj.type == 23:
                # neccesary for making the object reverse directions when hitting a wall
                tempy = 0
                tempy = enemy_speed_y.copy()
                tempy[1] *= obj.movement_tracker

                obj.rect, collisions = move(
                    obj.rect, tempy, tile_rects, hit_types, False, False)
                # if the enemy hits a wall
                if collisions["top"] or collisions["bottom"]:
                    # reverse movement
                    if obj.movement_tracker == -1:
                        obj.movement_tracker = 1
                    elif obj.movement_tracker == 1:
                        obj.movement_tracker = -1

            # Blit enemies wich are alive
            exec("display.blit(object_{}.image, ({},{}))".format(
                obj.type, obj.rect.x-scroll[0], obj.rect.y-scroll[1]))

        display.blit(player.image, (player.rect.x -
                                    scroll[0], player.rect.y-scroll[1]))

        win.blit(pygame.transform.scale(display, (WIDTH, HEIGHT)), (0, 0))

    elif game_state == "load_level":
        exec("loadmap('levels/lvl_{}.txt')".format(current_level))
        temp = 0
        for obj in current_map:
            if current_map_size[0] > temp:
                tempx = temp*TILESIZE
                tempy = 0
            else:
                tempx = (
                    temp - current_map_size[0] * int(temp/current_map_size[0]))*TILESIZE
                tempy = int(temp/current_map_size[0])*TILESIZE
            if int(obj) == 5:
                player.rect.x = tempx
                player.rect.y = tempy
            temp += 1
        game_state = "playing"

    elif game_state == "new_level":
        game_state = "load_level"
        current_level += 1
        player_corpses = []
        current_clone = []

    elif game_state == "game_over":
        win.blit(menu.game_over_bg, (0, 0))
        blit_if_selected("game_over_restart", "menu", 738, 1182, 498, 580)

        mouse_1, mouse_2, mouse_3 = pygame.mouse.get_pressed()
        if mouse_1:
            if check_if_selected(738, 1182, 498, 580):
                # restart
                game_state = "load_level"
                player_corpses = []
                current_clone = []
        # TODO: make a game over screen with restart, quit, and quit and save

    else:
        print("ERR: Invalid game_state #100")

    for event in pygame.event.get():  # event loop
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
            if event.key == K_k:
                # TODO REPLACE
                player_death(False)
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    pygame.display.update()
    clock.tick(60)
