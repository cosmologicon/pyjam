from pygame.locals import *

gamename = "Beyond the horizon"

# Must have a 16x9 aspect ratio.
windowsize = 854, 480
# windowsize = 1280, 720
# windowsize = 1920, 1080

# Whether to start up in fullscreen mode. Can enter fullscreen in-game with F11.
fullscreen = False
# Maximum horizontal resolution to use in fullscreen mode (e.g. 1280). None to use maximum resolution.
fullscreenmaxwidth = None

maxfps = 60
drawbackground = True

DEBUG = True
autosave = False
savename = "data/savegame.json"


jumpcombotime = 0.08
tactivate = 0.25
maxjump = 30

usershipsize = 1.5
beacondetect = 12
# rshield = 14
vqteleport = 25
rqteleport = 50
twarpinvulnerability = 3
thurtinvulnerability = 1
tcutsceneinvulnerability = 5

musiccrossfadetime = 1

keycodes = {
	"left": [K_LEFT, K_a],
	"right": [K_RIGHT, K_d, K_e],
	"up": [K_UP, K_w, K_COMMA],
	"down": [K_DOWN, K_s, K_o],
	"go": [K_SPACE, K_RETURN, K_LSHIFT, K_RSHIFT, K_z],
	"abort": [K_BACKSPACE],
	"quit": [K_ESCAPE],
	"save": [K_F5],
	"screenshot": [K_F12],
}


regionbuffer = 10




