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
	"snap": [K_SPACE],
	"map": [K_m],
	"kleft": [K_a, K_LEFT],
	"kright": [K_d, K_e, K_RIGHT],
	"kup": [K_w, K_COMMA, K_UP],
	"kdown": [K_s, K_o, K_DOWN],
	"assemble": [K_BACKSPACE],
}
ncolors = [
	Color("yellow"),
	Color("red"),
	Color("blue"),
]
minimapscale = 0.3



resolution0 = 480  # do not change - logical (not actual) resolution of screen
gamename = "The Aftermath"
DEBUG = True


shadecolor = 40, 40, 40
yscalefactor = 0.5  # 0.5 = isometric
blocksize = 50

