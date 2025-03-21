import sys
from . import pview
from pygame.locals import *

gamename = "The Final Choice"

minfps = 5
maxfps = 60

DEBUG = False

fullscreen = "--fullscreen" in sys.argv
portrait = "--portrait" in sys.argv
windowsize = 480  # 16:9 aspect ratio
forceres = False
for arg in sys.argv:
	if arg.startswith("--res="):
		windowsize = int(arg[6:])
		forceres = True
if "--big" in sys.argv:
	windowsize = 720
	forceres = True
if "--huge" in sys.argv:
	windowsize = 1080
lowres = "--lowres" in sys.argv
restart = "--restart" in sys.argv
nomusic = "--nomusic" in sys.argv
nosound = "--nosound" in sys.argv
vidcap = "--vidcap" in sys.argv

pview.SCREENSHOT_DIRECTORY = "screenshots"
savedir = "save"
quicksavefile = "qsave.pkl"
progressfile = "save.pkl"
miraclefile = "msave.pkl"

swapaction = False
miracle = "--miracle" in sys.argv
tquicksave = 0 if "--noquicksave" in sys.argv else 5

soundext = "ogg"

controls = {
	"left": [K_LEFT, K_a],
	"right": [K_RIGHT, K_d, K_e],
	"up": [K_UP, K_w, K_COMMA],
	"down": [K_DOWN, K_s, K_o],
	"action": [K_SPACE, K_RETURN, K_LCTRL, K_RCTRL, K_LSHIFT, K_RSHIFT, K_z],
	"swap": [K_CAPSLOCK, K_TAB],
	"quit": [K_ESCAPE],
	"fullscreen": [K_F11, K_f],
	"portrait": [K_F10],
	"screenshot": [K_F12],
	"quicksave": [K_F5],
	"quickload": [K_F6],
	"toggledebug": [K_F2],
}
def isdown(key, kdowns):
	return any(k in kdowns for k in controls[key])
def ispressed(key, kpressed):
	return any(kpressed[k] for k in controls[key])

