from pygame.locals import *

gamename = "Beyond the horizon"

fullscreen = False
windowsize0 = 854, 480  # Used for aspect ratio. Do not set manually. Set windowsize below instead.
maxfps = 60
drawbackground = True

DEBUG = True
autosave = False
savename = "data/savegame.json"

windowsize = windowsize0

jumpcombotime = 0.08
tactivate = 0.25
maxjump = 30

beacondetect = 8
rshield = 14
vqteleport = 25
rqteleport = 50

keycodes = {
	"left": [K_LEFT, K_a],
	"right": [K_RIGHT, K_d, K_e],
	"up": [K_UP, K_w, K_COMMA],
	"down": [K_DOWN, K_s, K_o],
	"go": [K_SPACE, K_RETURN],
	"abort": [K_BACKSPACE],
	"quit": [K_ESCAPE],
	"save": [K_F5],
}

