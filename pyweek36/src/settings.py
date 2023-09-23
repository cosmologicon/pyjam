import pygame, pickle, os.path

gamename = "Unmatter Hunter"

# DEFAULT DIFFICULTY SETTINGS
# If you update these be sure to delete settings.pkl too.
stars = 10
nebula = 10
objsize = 10


minfps, maxfps = 5, 120

height = 720
size0 = 1280, 720  # Do not change
heights = 480, 720, 1080, 1440  # Ok to add your own resolutions

fullscreen = False
forceres = False

sfxvolume = 0.5
musicvolume = 0.5

savepath = "save.pkl"
quicksavepath = "qsave.pkl"
settingspath = "settings.pkl"
tquicksave = 5
reset = False

DEBUG = True

minimapradius = 50
mapradius = 1000
countradius = 25
viewscale = 50

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

def save():
	obj = height, fullscreen, forceres, stars, nebula, objsize
	pickle.dump(obj, open(settingspath, "wb"))

def load():
	global height, fullscreen, forceres, stars, nebula, objsize
	if os.path.exists(settingspath):
		obj = pickle.load(open(settingspath, "rb"))
		height, fullscreen, forceres, stars, nebula, objsize = obj
load()		

