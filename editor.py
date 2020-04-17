
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
fontbasic = pygame.font.SysFont('Calibri', 30)

menu_page = 1
menu_slots = ((10,15),(10,62),(10,109),(10,156),(10,203),(10,250),(10,297),(10,344),(10,391),(10,438),(10,485),(10,532),(10,579),(10,626),(10,673),(10,720),(10,767),(10,814),(10,861),(10,908),(10,955))

menu_pages_img = img.load("img_editor/menu_pages.png").convert_alpha()
menu_sidebar_img = img.load("img_editor/menu_sidebar.png").convert_alpha()

scroll_tracker = (0,0)
scroll_vel = 5
selected = 0

temp = 0

object_list = [

              "img/cobble.png", "img_editor/empty.png"

              ]

current_map = []
current_map_size = [10,10]

# Takes the current map size and fills in current_map based on it
for i in range(current_map_size[0]*current_map_size[1]):
    current_map.append("1")
print(current_map)

# Adds tuples, stolen from here: https://stackoverflow.com/questions/5607284/how-to-add-with-tuples
# USE LIKE THIS:
# tupleadd((1,0),foo(a-b,b))
def tupleadd(x,y):
    z = []
    for i in range(len(x)):
        z.append(x[i]+y[i])
    return tuple(z)

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
        

cobblestone_menu = _object(0, menu_slots[0])
cobblestone_txt = fontbasic.render('Cobblestone', True, (255, 255, 255))

def updates_and_draw():
    global scroll_tracker
    global mouse_x
    global mouse_y
    global selected
    global temp
    global mouse_1

    win.fill((0,0,0))
    win.blit(menu_sidebar_img, (-5,-5))

    # Insert editor tiles
    temp = 0
    for obj in current_map:
        if current_map_size[0] > temp:
            tempx = temp*32+scroll_tracker[0]+250
            tempy = scroll_tracker[1]
        else:
            tempx = (temp - current_map_size[0] * int(temp/current_map_size[0]))*32+scroll_tracker[0]+250
            tempy = int(temp/current_map_size[0])*32
        
        exec("object_{} = _object({},({},{}))".format(temp, obj, tempx, tempy))
        exec("win.blit(object_{}.image, object_{}.location)".format(temp, temp))
        temp+=1
    
    # Update and draw menu sidebar
    if menu_page == 1:
        # Blitting cobblestone and text besides it
        win.blit(cobblestone_menu.image, cobblestone_menu.location)
        win.blit(cobblestone_txt, tupleadd(cobblestone_menu.location, (40, 2)))

    if keys[pygame.K_UP]:
        scroll_tracker = tupleadd(scroll_tracker,(0,scroll_vel))
    if keys[pygame.K_DOWN]:
        scroll_tracker = tupleadd(scroll_tracker,(0,-scroll_vel))
    if keys[pygame.K_LEFT]:
        scroll_tracker = tupleadd(scroll_tracker,(scroll_vel,0))
    if keys[pygame.K_RIGHT]:
        scroll_tracker = tupleadd(scroll_tracker,(-scroll_vel,0))
    
    # FORMAT: win.blit(cobblestone_menu.image, tupleadd(scroll_tracker,(500,500)))

    mouse_1, mouse_2, mouse_3 = pygame.mouse.get_pressed()
    if mouse_1:
        temp = 0
        for slot in menu_slots:
            # if click is inside of slot
            if slot[0] <= mouse_x <= (slot[0]+232) and slot[1] <= mouse_y <= (slot[1]+32):
                selected = temp
            temp+=1

        # if click is inside editing area
        if 250 < mouse_x:
            # Tricky code that figures out which "slot" you have clicked
            temp1 = int(mouse_x-250-scroll_tracker[1]/32)
            temp2 = int(mouse_y-scroll_tracker[0]/32)
            print(temp2*current_map_size[0]+temp1)
            print(temp1)
            print(temp2)
            current_map[temp2*current_map_size[0]+temp1] = selected


    



                    


        

        

   


run = True
while run:
    clock.tick(60)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_1 = False
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