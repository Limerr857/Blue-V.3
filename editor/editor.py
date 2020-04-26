
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
              (10, 485), (10, 532), (10, 579), (10, 626), (10, 673), (10, 720), (10, 767), (10, 814), (10, 861), (10, 908))

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

    "img_editor/cobble.png", "img_editor/empty.png", "img_editor/dirt_1.png", "img_editor/dirt_2.png", "img_editor/dirt_3.png",
    "img_editor/player.png", "img_editor/flag.png", "img_editor/spike.png", "img_editor/player_dead.png", "img_editor/clone_1.png",
    "img_editor/clone_2.png", "img_editor/clone_3.png", "img_editor/clone_4.png", "img_editor/clone_5.png", "img_editor/clone_6.png",
    "img_editor/clone_7.png", "img_editor/clone_8.png", "img_editor/clone_9.png", "img_editor/clone_10.png", "img_editor/clone_11.png",
    "img_editor/clone_12.png", "img_editor/clone_13.png"
 
]
objects = [
    "cobblestone", "empty", "dirt_1", "dirt_2", "dirt_3", "player", "flag", "spike", "player_dead", "clone_1",
    "clone_2", "clone_3", "clone_4", "clone_5", "clone_6", "clone_7", "clone_8", "clone_9", "clone_10", "clone_11",
    "clone_12", "clone_13"
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
# tupleadd((1,0),(a,b))


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


class _object(pygame.sprite.Sprite):

    def __init__(self, type, location):
        self.type = type
        self.location = location
        # ADDNEW
        exec("{}.__init__(self)".format(objects[type]))
        # TODO: DELETE THIS:
        # if type == 0:
        #     cobblestone.__init__(self)
        # elif type == 1:
        #     empty.__init__(self)
        # elif type == 2:
        #     dirt_1.__init__(self)
        # elif type == 3:
        #     dirt_2.__init__(self)
        # elif type == 4:
        #     dirt_3.__init__(self)
        # elif type == 5:
        #     player.__init__(self)
        # elif type == 6:
        #     flag.__init__(self)
        # elif type == 7:
        #     spike.__init__(self)
        # elif type == 8:
        #     player_dead.__init__(self)
        # elif type == 9:
        #     clone_1.__init__(self)
        # elif type == 10:
        #     clone_2.__init__(self)
        # elif type == 11:
        #     clone_3.__init__(self)
        # elif type == 12:
        #     clone_4.__init__(self)
        # elif type == 13:
        #     clone_5.__init__(self)
        # elif type == 14:
        #     clone_6.__init__(self)
        # elif type == 15:
        #     clone_7.__init__(self)
        # elif type == 16:
        #     clone_8.__init__(self)
        # elif type == 17:
        #     clone_9.__init__(self)
        # elif type == 18:
        #     clone_10.__init__(self)
        # elif type == 19:
        #     clone_11.__init__(self)
        # elif type == 20:
        #     clone_12.__init__(self)
        # elif type == 21:
        #     clone_13.__init__(self)


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

    if num < len(menu_slots):
        exec("{}_menu = _object({}, menu_slots[{}])".format(name,num,num),globals())
        exec("{}_txt = fontbasic.render('{}', True, (255, 255, 255))".format(name,name),globals())
    else:
        loops = int(num/len(menu_slots))
        temp = num-int(len(menu_slots)*loops)
        exec("{}_menu = _object({}, menu_slots[{}])".format(name,num,temp),globals())
        exec("{}_txt = fontbasic.render('{}', True, (255, 255, 255))".format(name,name),globals())

    exec("object_{} = _object({}, (0, 0))".format(num,num),globals())

def blitobj(name,num):
    loops = int(num/len(menu_slots))
    if menu_page == loops+1:
        # if the obj is in the current menu_page, blit it
        exec("win.blit({}_menu.image, {}_menu.location)".format(name,name),globals())
        exec("win.blit({}_txt, tupleadd({}_menu.location, (40, 2)))".format(name,name),globals())
    else:
        # Don't blit
        pass

# ADDNEW
temp = 0
for obj in objects:
    exec("addobj('{}', {})".format(obj,temp),globals())
    temp+=1
# TODO: DELETE THIS:
# addobj("cobblestone", 0)
# addobj("empty", 1)
# addobj("dirt_1", 2)
# addobj("dirt_2", 3)
# addobj("dirt_3", 4)
# addobj("player", 5)
# addobj("flag", 6)
# addobj("spike", 7)
# addobj("player_dead", 8)
# addobj("clone_1", 9)
# addobj("clone_2", 10)
# addobj("clone_3", 11)
# addobj("clone_4", 12)
# addobj("clone_5", 13)
# addobj("clone_6", 14)
# addobj("clone_7", 15)
# addobj("clone_8", 16)
# addobj("clone_9", 17)
# addobj("clone_10", 18)
# addobj("clone_11", 19)
# addobj("clone_12", 20)
# addobj("clone_13", 21)



def updates_and_draw():
    global scroll_tracker
    global mouse_x
    global mouse_y
    global selected
    global temp
    global mouse_1
    global new_object
    global menu_page

    win.fill((0, 0, 0))

    # Insert editor tiles
    # TODO: Delete if nothing breaks
    # if new_object:
    #     temp = 0
    #     for obj in current_map:
    #         if current_map_size[0] > temp:
    #             tempx = temp*32+scroll_tracker[0]+250
    #             tempy = scroll_tracker[1]
    #         else:
    #             tempx = (
    #                 temp - current_map_size[0] * int(temp/current_map_size[0]))*32+scroll_tracker[0]+250
    #             tempy = int(temp/current_map_size[0])*32+scroll_tracker[1]
    #         try:
    #             exec("win.blit(object_{}.image, ({},{}))".format(
    #                 obj, tempx, tempy), globals())
    #         except NameError:
    #             print("User has probably selected non-existant block from sidebar")
    #         temp += 1
    #     new_object = False
    temp = 0
    for obj in current_map:
        if current_map_size[0] > temp:
            tempx = temp*32+scroll_tracker[0]+250
            tempy = scroll_tracker[1]
        else:
            tempx = (temp - current_map_size[0] * int(temp/current_map_size[0]))*32+scroll_tracker[0]+250
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
    win.blit(menu_pages_img, (75, 977))
    # Blitting cobblestone and text besides it
    # ADDNEW
    temp = 0
    for obj in objects:
        exec("blitobj('{}', {})".format(obj,temp),globals())
        temp+=1
    # TODO: DELETE THIS:
    # blitobj("cobblestone", 0)
    # blitobj("empty", 1)
    # blitobj("dirt_1", 2)
    # blitobj("dirt_2", 3)
    # blitobj("dirt_3", 4)
    # blitobj("player", 5)
    # blitobj("flag", 6)
    # blitobj("spike", 7)
    # blitobj("player_dead", 8)
    # blitobj("clone_1", 9)
    # blitobj("clone_2", 10)
    # blitobj("clone_3", 11)
    # blitobj("clone_4", 12)
    # blitobj("clone_5", 13)
    # blitobj("clone_6", 14)
    # blitobj("clone_7", 15)
    # blitobj("clone_8", 16)
    # blitobj("clone_9", 17)
    # blitobj("clone_10", 18)
    # blitobj("clone_11", 19)
    # blitobj("clone_12", 20)
    # blitobj("clone_13", 21)

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
                selected = temp+len(menu_slots)*(menu_page-1)
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
        # if clock is on page changer area
        elif 75 <= mouse_x <= 163 and 977 <= mouse_y <= 1012:
            # 1
            if 75 <= mouse_x <= 90:
                menu_page = 1
            # 2
            elif 91 <= mouse_x <= 109:
                menu_page = 2
            # 3
            elif 110 <= mouse_x <= 127:
                menu_page = 3
            # 4
            elif 128 <= mouse_x <= 147:
                menu_page = 4


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
