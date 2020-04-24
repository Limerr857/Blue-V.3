import pygame 
from pygame import image as img

# game options/settings
TITLE = "Blue V.3"
WIDTH = 1920
HEIGHT = 1080
FPS = 60
object_list = [

    "img/cobble.png", "img/empty.png", "img/dirt_1.png", "img/dirt_2.png", "img/dirt_3.png", "img/empty.png", "img/flag.png"

]
TILESIZE = 32
JUMPLENGTH = -6
collision_list = [0,2,3,4,6]
true_scroll = [0,0]
scroll = [0,0]
current_level = 1
game_state = "load_level"

# player
moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (146,244,255)


