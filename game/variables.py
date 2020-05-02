import pygame 
from pygame import image as img

# game options/settings
TITLE = "Blue V.3"
WIDTH = 1920
HEIGHT = 1080
FPS = 60
object_name_list = [

    "cobblestone", "empty", "dirt_1", "dirt_2", "dirt_3", "empty", "flag",
    "spike", "player_dead", "clone_1", "clone_2", "clone_3", "clone_4", 
    "clone_5", "clone_6", "clone_7", "clone_8", "clone_9", "clone_10", 
    "clone_11","clone_12", "clone_13", "enemy_bounce_x", "enemy_bounce_y"

]
TILESIZE = 32
JUMPLENGTH = -6
# 21 is clone_13
collision_list = [0,2,3,4,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
enemy_list = [22,23]
true_scroll = [0,0]
scroll = [0,0]
current_level = 1
game_state = "load_level"
current_enemies = []
current_enemies_rect = []
enemy_speed_x = [2,0]
enemy_speed_y = [0,2]

# player
moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0
player_corpses = []
# The current cloning machine, where player will be 
current_clone = []

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (146,244,255)

# every menu sprite is contained in this menu object
class menus():
    def __init__(self):
        pass
    def loadall(self):
        self.game_over_bg = img.load("img/game_over_bg.png").convert()
        self.game_over_restart = img.load("img/go_restart.png").convert_alpha()
        self.game_over_restart_select = img.load("img/go_restart_select.png").convert_alpha()
menu = menus()
