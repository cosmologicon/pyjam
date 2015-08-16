from pygame.locals import *
import sys

gamename = "Beyond the Horizon"

# Must have a 16x9 aspect ratio.
windowsize = 854, 480
# windowsize = 1280, 720
# windowsize = 1920, 1080

if "--720" in sys.argv:
	windowsize = 1280, 720
if "--1080" in sys.argv:
	windowsize = 1920, 1080

# Whether to start up in fullscreen mode. Can enter fullscreen in-game with F11.
fullscreen = "--fullscreen" in sys.argv
# Maximum horizontal resolution to use in fullscreen mode (e.g. 1280). None to use maximum resolution.
fullscreenmaxwidth = None

maxfps = 60
minfps = 6
drawbackground = True

DEBUG = "--debug" in sys.argv
saveonquit = True
saveonemergency = True
# Set it to savegame.json if you prefer to save as json. I think it's slower, though.
savename = "data/savegame.pkl"

musicvolume = 0.2, 0.5
musiccrossfadetime = 1

# Set lower for higher-resolution lava lamp effects (takes more CPU).
backgroundfactor = 16

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
beaconsforfinale = 10
logicalscreensize = 54

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




