import pygame

gamename = "Dark Matter"

# DIFFICULTY SETTINGS - ADJUST THESE AS NECESSARY!
# These values control how prominent the background graphics are, which determines how
# hard it is to see the unmatter in the game. Lower values will make the game harder.
# You want seeing the unmatter to be challenging but not frustrating.
# 0: basically impossible
# 7: my preferred setting for fullscreen mode
# 10: my preferred setting for windowed mode
# 14: my preferred setting for small windows or poor lighting conditions
# 20: very easy on any resolution
stars = 10
nebula = 10


minfps, maxfps = 5, 120

height = 720
size0 = 1280, 720  # Do not change
heights = 480, 720, 1080, 1440  # Ok to add your own resolutions

fullscreen = False
forceres = False

sfxvolume = 0.5
musicvolume = 0.5

DEBUG = True

minimapradius = 50
mapradius = 1000
countradius = 25

keys = {
	"thrust": [pygame.K_UP, pygame.K_w, pygame.K_COMMA],
	"left": [pygame.K_LEFT, pygame.K_a],
	"right": [pygame.K_RIGHT, pygame.K_d, pygame.K_e],
	"stop": [pygame.K_DOWN, pygame.K_s, pygame.K_o],
	"gravnet": [pygame.K_SPACE, pygame.K_RETURN],
	"beam": [pygame.K_1],
	"ring": [pygame.K_2],
	"glow": [pygame.K_3],
	"drive": [pygame.K_4],
	"map": [pygame.K_5, pygame.K_m],
	"return": [pygame.K_6, pygame.K_BACKSPACE],
}



