import pygame
from pygame import image as img

# game options/settings
TITLE = "Blue V.3"
WIDTH = 1920
HEIGHT = 1080
FPS = 60
# ADDNEW
object_name_list = [

    "cobblestone", "empty", "dirt_1", "dirt_2", "dirt_3", "empty", "flag",
    "spike", "player_dead", "clone_1", "clone_2", "clone_3", "clone_4",
    "clone_5", "clone_6", "clone_7", "clone_8", "clone_9", "clone_10",
    "clone_11", "clone_12", "clone_13", "enemy_bounce_x", "enemy_bounce_y",
    "enemy_bounce_x_invert", "enemy_bounce_y_invert", "spike_left", "spike_centre",
    "spike_right", "stalactite"

]
TILESIZE = 32
# Default: -6
JUMPLENGTH = -6
# 21 is clone_13
collision_list = [0, 2, 3, 4, 6, 7, 8, 9, 10,
                  11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 26, 27, 28, 29]
enemy_list = [22, 23, 24, 25]
true_scroll = [0, 0]
scroll = [0, 0]
current_level = 1
game_state = "load_level"
current_enemies = []
current_enemies_rect = []
enemy_speed_x = [2, 0]
enemy_speed_x_invert = [-2, 0]
enemy_speed_y = [0, 2]
enemy_speed_y_invert = [0, -2]

# map variables
scroll_tracker = (0, 0)
scroll_vel = 7

# player
moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0
player_corpses = []
# The current cloning machine, where the player will respawn
current_clone = []

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (146, 244, 255)


# every menu sprite is contained in this menu object
class menus():
    def __init__(self):
        pass

    def loadall(self):
        # Items in bglist must be fully rectangular with no alpha parts
        bglist = [
            "game_over_bg", "escape_menu_bg"
        ]
        # Items in itemlist must have a _select version in the /img folder
        itemlist = [
            "go_restart", "esc_reset", "esc_resume", "esc_quit"
        ]
        # Items in textlist have no requirements
        textlist = [
            "map_instructions"
        ]
        for name in bglist:
            exec(f"self.{name} = img.load('img/{name}.png').convert()")
        for name in itemlist:
            exec(f"self.{name} = img.load('img/{name}.png').convert_alpha()")
            exec(
                f"self.{name}_select = img.load('img/{name}_select.png').convert_alpha()")
        for name in textlist:
            exec(f"self.{name} = img.load('img/{name}.png').convert_alpha()")


menu = menus()
