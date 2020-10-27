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
map_danger = img.load('img/map_img/danger.png').convert_alpha()

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
            self.image = img.load(
                'img/' + object_name_list[{}] + '.png').convert_alpha()
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
    global air_timer
    global vertical_momentum
    global moving_right
    global moving_left

    air_timer = 0
    vertical_momentum = 0
    moving_right = False
    moving_left = False

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
    print("DEAD")
    print(player.rect.x)
    print(player.rect.y)
    player.rect.x = current_clone[0]
    player.rect.y = current_clone[1]-TILESIZE
    print(player.rect.x)
    print(player.rect.y)
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
        # Adds tile to hit_list if rect is colliding with it unless they are the same,
        # basically stops things from colliding with themselves
        if rect.colliderect(tile) and tile != rect:
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
    already_died = False
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
            # if movement == [0, 0]:
            # if not secondpass:
            already_died = True
            player_death(True)
            # else:
            # if not secondpass:
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
            # player_death(True)
    if not already_died:
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
            # if movement == [0, 0]:
            #     if not secondpass:
            if not already_died:
                player_death(True)
            # else:
            #     if not secondpass:
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
                # player_death(True)
    if not already_died:
        for tile in hit_list:
            if movement[1] > 0:
                rect.bottom = tile.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                rect.top = tile.bottom
                collision_types['top'] = True

    return rect, collision_types


def reset_map():
    global player_corpses
    global current_clone
    global game_state
    # restart
    game_state = "load_level"
    player_corpses = []
    current_clone = []


def map_cycle():
    global scroll_tracker
    global mouse_x
    global mouse_y
    global temp
    global mouse_1
    global new_object
    global enemy_list

    blit_tracker = []

    win.fill(LIGHTBLUE)

    temp = 0
    for obj in current_map:
        if current_map_size[0] > temp:
            tempx = temp*32+scroll_tracker[0]+250
            tempy = scroll_tracker[1]
        else:
            tempx = (
                temp - current_map_size[0] * int(temp/current_map_size[0]))*32+scroll_tracker[0]+250
            tempy = int(temp/current_map_size[0])*32+scroll_tracker[1]
        exec("win.blit(object_{}.image, ({},{}))".format(
            obj, tempx, tempy), globals())
        if obj in enemy_list:
            if obj == 22 or obj == 24:
                # x
                attack_list = map_subcycle(0, temp)
            elif obj == 23 or obj == 25:
                # y
                attack_list = map_subcycle(1, temp)
            # # Removes duplicates from the list
            # temp2 = []
            # [temp2.append(x) for x in attack_list if x not in temp2]
            # attack_list = temp2
            # TODO: REMOVE THIS
            for attack_position in attack_list:
                temp1 = attack_position[1] * \
                    current_map_size[0]+attack_position[0]
                if current_map_size[0] > temp:
                    tempx = temp1*32+scroll_tracker[0]+250
                    tempy = scroll_tracker[1]
                else:
                    tempx = (
                        temp1 - current_map_size[0] * int(temp1/current_map_size[0]))*32+scroll_tracker[0]+250
                    tempy = int(temp1/current_map_size[0])*32+scroll_tracker[1]
                # Stops it from blitting two map_danger in the same place
                temp3 = [tempx, tempy]
                if temp3 not in blit_tracker:
                    # Stops it from blitting a map_danger over an enemy sprite
                    if current_map[temp1] not in enemy_list:
                        win.blit(map_danger, (tempx, tempy))
                        blit_tracker.append([tempx, tempy])

        temp += 1

    if keys[pygame.K_UP]:
        scroll_tracker = tupleadd(scroll_tracker, (0, scroll_vel))
        new_object = True
    if keys[pygame.K_DOWN]:
        scroll_tracker = tupleadd(scroll_tracker, (0, -scroll_vel))
        new_object = True
    if keys[pygame.K_LEFT]:
        scroll_tracker = tupleadd(scroll_tracker, (scroll_vel, 0))
        new_object = True
    if keys[pygame.K_RIGHT]:
        scroll_tracker = tupleadd(scroll_tracker, (-scroll_vel, 0))
        new_object = True


def tupleadd(x, y):
    # Adds tuples, stolen from here: https://stackoverflow.com/questions/5607284/how-to-add-with-tuples
    # USE LIKE THIS:
    # tupleadd((1,0),(a,b))
    z = []
    for i in range(len(x)):
        z.append(x[i]+y[i])
    return tuple(z)


def map_subcycle(direction, position):
    pos = [0, 0]
    result = []
    nothit = True
    pos[0] = math.floor(position/current_map_size[0])
    tempy = pos[0]
    pos[1] = position % current_map_size[0]
    tempx = pos[1]
    if direction == 0:
        # enemy moves on x-axis
        while nothit:
            tempx -= 1
            if current_map[tempy*current_map_size[0]+tempx] not in collision_list:
                result.append([tempx, tempy])
            else:
                nothit = False
        tempx = pos[1]
        nothit = True
        while nothit:
            tempx += 1
            if current_map[tempy*current_map_size[0]+tempx] not in collision_list:
                result.append([tempx, tempy])
            else:
                nothit = False
    elif direction == 1:
        # enemy moves on y-axis
        while nothit:
            tempy -= 1
            if current_map[tempy*current_map_size[0]+tempx] not in collision_list:
                result.append([tempx, tempy])
            else:
                nothit = False
        tempy = pos[0]
        nothit = True
        while nothit:
            tempy += 1
            if current_map[tempy*current_map_size[0]+tempx] not in collision_list:
                result.append([tempx, tempy])
            else:
                nothit = False
    return result


while True:  # game loop
    mouse_x, mouse_y = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()

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

        # Add all enemies to the collision rect list so that they can collide with each other
        for obj in enemy_group:
            tile_rects.append(obj.rect)

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
        # If player hits a spike
        if 7 in hit_types and collisions["bottom"] == True:
            player_death(True)
        if 26 in hit_types and collisions["bottom"] == True:
            player_death(True)
        if 27 in hit_types and collisions["bottom"] == True:
            player_death(True)
        if 28 in hit_types and collisions["bottom"] == True:
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

        templist = enemy_group.sprites()
        for obj in enemy_group:
            # update position of enemies
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

            # if type is enemy_bounce_x_invert
            elif obj.type == 24:
                # neccesary for making the object reverse directions when hitting a wall
                tempx = 0
                tempx = enemy_speed_x_invert.copy()
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

            # if type is enemy_bounce_y_invert
            elif obj.type == 25:
                # neccesary for making the object reverse directions when hitting a wall
                tempy = 0
                tempy = enemy_speed_y_invert.copy()
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
        blit_if_selected("go_restart", "menu", 738, 1182, 498, 580)

        mouse_1, mouse_2, mouse_3 = pygame.mouse.get_pressed()
        if mouse_1:
            if check_if_selected(738, 1182, 498, 580):
                reset_map()
        # TODO: make a game over screen with restart, quit, and quit and save

    elif game_state == "escape_menu":
        win.blit(menu.escape_menu_bg, (0, 0))
        blit_if_selected("esc_reset", "menu", 668, 1251, 282, 361)
        blit_if_selected("esc_resume", "menu", 643, 1303, 772, 851)
        blit_if_selected("esc_quit", "menu", 630, 1290, 576, 655)

        mouse_1, mouse_2, mouse_3 = pygame.mouse.get_pressed()
        if mouse_1:
            if check_if_selected(668, 1251, 282, 361):
                # esc_reset is clicked on
                reset_map()
            if check_if_selected(643, 1303, 772, 851):
                # esc_resume is clicked on
                game_state = "playing"
            if check_if_selected(630, 1290, 576, 668):
                # esc_quit is clicked on
                pygame.quit()
                sys.exit()

    elif game_state == "map":
        map_cycle()
        win.blit(menu.map_instructions, (0, 1021))

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
                if game_state == "playing":
                    if air_timer < 6:
                        vertical_momentum = JUMPLENGTH
            if event.key == K_F4 and pygame.KMOD_ALT:
                pygame.quit()
                sys.exit()
            if event.key == K_ESCAPE:
                if game_state == "playing":
                    game_state = "escape_menu"
                elif game_state == "escape_menu":
                    game_state = "playing"
            if event.key == K_k:
                # TODO Remove
                player_death(False)
            if event.key == K_m:
                if game_state == "playing":
                    game_state = "map"
                elif game_state == "map":
                    game_state = "playing"
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    pygame.display.update()
    clock.tick(60)
