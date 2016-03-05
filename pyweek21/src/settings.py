import sys
from pygame.locals import *


maxfps = 60
minfps = 10
fullscreen = "--fullscreen" in sys.argv
resolution = 480
for arg in sys.argv:
	if arg.startswith("--res="):
		resolution = int(arg[6:])
if "--small" in sys.argv or "--360" in sys.argv:
	resolution = 360
if "--large" in sys.argv or "--720" in sys.argv:
	resolution = 720
if "--huge" in sys.argv or "--1080" in sys.argv:
	resolution = 1080
savename = "data/savegame.pkl"
keys = {
	"quit": [K_ESCAPE],
	"remulate": [K_RETURN],            # keys that emulate a right click
	"cycle": [K_TAB],                  # cycle selection
	"snap": [K_SPACE],                 # move camera to current selection
	"kmulti": [K_LSHIFT, K_LCTRL],     # hold this key to select multiple when clicking
	"map": [K_m],                      # bring up map
	"kleft": [K_a, K_LEFT],
	"kright": [K_d, K_e, K_RIGHT],
	"kup": [K_w, K_COMMA, K_UP],
	"kdown": [K_s, K_o, K_DOWN],
	"assemble": [K_BACKSPACE],         # for debugging
}
mixerfreq = 44100
mixerbuffer = 0
volumes = {
	"ack": 0.5,
	"music": 0.5,
	"dialogue": 1,
	"narrator": 1,
	"sfx": 1,
	"ssh": 0.5,  # music volume factor when dialogue is playing
}
ncolors = [
	Color("yellow"),
	Color("red"),
	Color("blue"),
]
minimapscale = 0.3
shipheight = 1
shipspacing = 12
buildingspacing = 14
restart = "--restart" in sys.argv  # delete existing saved game on startup
lowres = "--lowres" in sys.argv  # avoid some of the more CPU intensive special effects
dialogueext = "ogg"
musicext = "ogg"
sfxext = "ogg"
sbox = 50  # selection box size
doubleclicktime = 0.4


resolution0 = 480  # do not change - logical (not actual) resolution of screen
gamename = "The Aftermath"
DEBUG = "--DEBUG" in sys.argv


shadecolor = 40, 40, 40
yscalefactor = 0.5  # 0.5 = isometric
blocksize = 50

