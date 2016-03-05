import sys
from pygame.locals import *


maxfps = 60
minfps = 10
fullscreen = False
resolution = 480
savename = "data/savegame.pkl"
mixerfreq = 44100
mixerbuffer = 0
keys = {
	"quit": [K_ESCAPE],
	"cycle": [K_TAB],
	"snap": [K_SPACE],
	"kmulti": [K_LSHIFT, K_LCTRL],
	"map": [K_m],
	"kleft": [K_a, K_LEFT],
	"kright": [K_d, K_e, K_RIGHT],
	"kup": [K_w, K_COMMA, K_UP],
	"kdown": [K_s, K_o, K_DOWN],
	"assemble": [K_BACKSPACE],
}
volumes = {
	"ack": 0.5,
	"music": 0.5,
	"dialogue": 1,
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
dialogueext = "wav"
musicext = "wav"
sbox = 50  # selection box size



resolution0 = 480  # do not change - logical (not actual) resolution of screen
gamename = "The Aftermath"
DEBUG = "--DEBUG" in sys.argv


shadecolor = 40, 40, 40
yscalefactor = 0.5  # 0.5 = isometric
blocksize = 50

