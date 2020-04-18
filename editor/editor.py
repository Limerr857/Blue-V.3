
import pygame
from pygame import image as img
import pickle
import random

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

win = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
pygame.display.set_caption("Blue V.3 Editor")
clock = pygame.time.Clock()
fontbasic = pygame.font.SysFont('Calibri', 30)

menu_page = 1
menu_slots = ((10, 15), (10, 62), (10, 109), (10, 156), (10, 203), (10, 250), (10, 297), (10, 344), (10, 391), (10, 438),
              (10, 485), (10, 532), (10, 579), (10, 626), (10, 673), (10, 720), (10, 767), (10, 814), (10, 861), (10, 908), (10, 955))

menu_pages_img = img.load("img_editor/menu_pages.png").convert_alpha()
menu_sidebar_img = img.load("img_editor/menu_sidebar.png").convert_alpha()
menu_y = img.load("img_editor/menu_y.png").convert_alpha()
menu_x = img.load("img_editor/menu_x.png").convert_alpha()

scroll_tracker = (0, 0)
scroll_vel = 7
selected = 0
new_object = True

temp = 0

# ADDNEW
object_list = [

    "img_editor/cobble.png", "img_editor/empty.png", "img_editor/dirt_1.png", "img_editor/dirt_2.png", "img_editor/dirt_3.png"

]

current_map = []
current_map_size = [50, 20]

# Takes the current map size and fills in current_map based on it


def reloadmap():
    global current_map_size
    global current_map
    current_map = []
    for i in range(current_map_size[0]*current_map_size[1]):
        current_map.append("1")


reloadmap()

# Adds tuples, stolen from here: https://stackoverflow.com/questions/5607284/how-to-add-with-tuples
# USE LIKE THIS:
# tupleadd((1,0),foo(a-b,b))


def tupleadd(x, y):
    z = []
    for i in range(len(x)):
        z.append(x[i]+y[i])
    return tuple(z)

# Saves the current map to editor_saves


def savemap():
    global current_map
    global current_map_size
    f = open("editor_saves/save.txt", "wb+")
    pickle.dump((current_map_size, current_map), f)
    f.close()


def loadmap():
    global current_map
    global current_map_size
    global new_object
    f = open("editor_saves/save.txt", "rb")
    current_map_size, current_map = pickle.load(f)
    f.close()
    new_object = True

# ADDNEW


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


# ADDNEW
cobblestone_menu = _object(0, menu_slots[0])
cobblestone_txt = fontbasic.render('Cobblestone', True, (255, 255, 255))
empty_menu = _object(1, menu_slots[1])
empty_txt = fontbasic.render('Empty', True, (255, 255, 255))
dirt_1_menu = _object(2, menu_slots[2])
dirt_1_txt = fontbasic.render('Dirt_1', True, (255, 255, 255))
dirt_2_menu = _object(3, menu_slots[3])
dirt_2_txt = fontbasic.render('Dirt_2', True, (255, 255, 255))
dirt_3_menu = _object(4, menu_slots[4])
dirt_3_txt = fontbasic.render('Dirt_3', True, (255, 255, 255))

# ADDNEW
# Each object is represented by their _object.type value
object_0 = _object(0, (0, 0))
object_1 = _object(1, (0, 0))
object_2 = _object(2, (0, 0))
object_3 = _object(3, (0, 0))
object_4 = _object(4, (0, 0))


def updates_and_draw():
    global scroll_tracker
    global mouse_x
    global mouse_y
    global selected
    global temp
    global mouse_1
    global new_object

    win.fill((0, 0, 0))

    # Insert editor tiles
    if new_object:
        temp = 0
        for obj in current_map:
            if current_map_size[0] > temp:
                tempx = temp*32+scroll_tracker[0]+250
                tempy = scroll_tracker[1]
            else:
                tempx = (
                    temp - current_map_size[0] * int(temp/current_map_size[0]))*32+scroll_tracker[0]+250
                tempy = int(temp/current_map_size[0])*32+scroll_tracker[1]

            try:
                exec("win.blit(object_{}.image, ({},{}))".format(
                    obj, tempx, tempy), globals())
            except NameError:
                print("User has probably selected non-existant block from sidebar")
            temp += 1
        new_object = False
    temp = 0
    for obj in current_map:
        if current_map_size[0] > temp:
            tempx = temp*32+scroll_tracker[0]+250
            tempy = scroll_tracker[1]
        else:
            tempx = (
                temp - current_map_size[0] * int(temp/current_map_size[0]))*32+scroll_tracker[0]+250
            tempy = int(temp/current_map_size[0])*32+scroll_tracker[1]
        try:
            exec("win.blit(object_{}.image, ({},{}))".format(
                obj, tempx, tempy), globals())
        except NameError:
            print("User has probably selected non-existant block from sidebar")
        temp += 1

    # Update and draw menu sidebar
    win.blit(menu_sidebar_img, (-5, -5))
    win.blit(menu_y, (93, 1017))
    win.blit(menu_x, (93, 1042))
    # Blitting cobblestone and text besides it
    # ADDNEW
    win.blit(cobblestone_menu.image, cobblestone_menu.location)
    win.blit(cobblestone_txt, tupleadd(cobblestone_menu.location, (40, 2)))
    win.blit(empty_menu.image, empty_menu.location)
    win.blit(empty_txt, tupleadd(empty_menu.location, (40, 2)))
    win.blit(dirt_1_menu.image, dirt_1_menu.location)
    win.blit(dirt_1_txt, tupleadd(dirt_1_menu.location, (40, 2)))
    win.blit(dirt_2_menu.image, dirt_2_menu.location)
    win.blit(dirt_2_txt, tupleadd(dirt_2_menu.location, (40, 2)))
    win.blit(dirt_3_menu.image, dirt_3_menu.location)
    win.blit(dirt_3_txt, tupleadd(dirt_3_menu.location, (40, 2)))

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

    # FORMAT: win.blit(cobblestone_menu.image, tupleadd(scroll_tracker,(500,500)))

    mouse_1, mouse_2, mouse_3 = pygame.mouse.get_pressed()
    if mouse_1:
        temp = 0
        for slot in menu_slots:
            # if click is inside of slot
            if slot[0] <= mouse_x <= (slot[0]+232) and slot[1] <= mouse_y <= (slot[1]+32):
                selected = temp
            temp += 1

        # if click is inside editing area
        if 250 < mouse_x:
            # Tricky code that figures out which "slot" you have clicked
            temp1 = int((mouse_x-250-scroll_tracker[0])/32)
            temp2 = int((mouse_y-scroll_tracker[1])/32)
            try:
                current_map[temp2*current_map_size[0]+temp1] = selected
                new_object = True
            except:
                print("User clicked outside of map area")
        # if click is on map size changer area
        elif 93 <= mouse_x <= 157 and 1017 <= mouse_y <= 1067:
            # -y
            if 93 <= mouse_x <= 125 and 1017 <= mouse_y <= 1042:
                current_map_size[1] -= 1
            # +y
            elif 125 <= mouse_x <= 157 and 1017 <= mouse_y <= 1042:
                current_map_size[1] += 1
            # -x
            elif 93 <= mouse_x <= 125 and 1042 <= mouse_y <= 1067:
                current_map_size[0] -= 1
            # +x
            elif 125 <= mouse_x <= 157 and 1042 <= mouse_y <= 1067:
                current_map_size[0] += 1
            reloadmap()


run = True
while run:
    clock.tick(60)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_1 = False
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # TODO: replace with actual menu?
    if keys[pygame.K_ESCAPE]:
        run = False

    if keys[pygame.K_c] and keys[pygame.K_LSHIFT]:
        reloadmap()

    if keys[pygame.K_s] and keys[pygame.K_LSHIFT]:
        savemap()

    if keys[pygame.K_l] and keys[pygame.K_LSHIFT]:
        loadmap()

    updates_and_draw()
    pygame.display.update()


pygame.quit()
