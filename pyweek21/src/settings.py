from pygame.locals import *


maxfps = 60
fullscreen = False
resolution = 480
savename = "data/savegame.pkl"
mixerfreq = 44100
mixerbuffer = 0
keys = {
	"quit": [K_ESCAPE],
	"cycle": [K_TAB],
	"assemble": [K_a],
}


resolution0 = 480  # do not change - logical (not actual) resolution of screen
gamename = "pyweek21"
DEBUG = True


shadecolor = 40, 40, 40
yscalefactor = 0.5  # 0.5 = isometric
shipframes = 16
blocksize = 50

