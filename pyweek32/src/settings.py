import pickle, os, sys, pygame

# Command line editable.

height = 720  # Current resolution
fullscreen = False
directcontrol = True
fixedcamera = False
autochomp = False
sfxvolume = 60
musicvolume = 60


def save():
	obj = height, fullscreen, directcontrol, fixedcamera, autochomp, sfxvolume, musicvolume
	pickle.dump(obj, open("settings.pkl", "wb"))
def load():
	global height, fullscreen, directcontrol, fixedcamera, autochomp, sfxvolume, musicvolume
	if not os.path.exists("settings.pkl"): return
	obj = pickle.load(open("settings.pkl", "rb"))
	height, fullscreen, directcontrol, fixedcamera, autochomp, sfxvolume, musicvolume = obj

size0 = 1280, 720  # Do not change

# EDIT HERE IF DESIRED
gamename = "Neverending"
savename = "savegame.pkl"
heights = 480, 540, 720, 1080
volumes = 0, 20, 40, 60, 80, 100
volumegamma = 1.6
DEBUG = True
reset = "--reset" in sys.argv
minfps, maxfps = 10, 120


keys = {
	"up": [pygame.K_UP, pygame.K_w, pygame.K_COMMA],
	"left": [pygame.K_LEFT, pygame.K_a],
	"right": [pygame.K_RIGHT, pygame.K_d, pygame.K_e],
	"down": [pygame.K_DOWN, pygame.K_s, pygame.K_o],
	"act": [pygame.K_SPACE, pygame.K_RETURN],
	"quit": [pygame.K_ESCAPE],
	"cheatwin": [pygame.K_1],
	"cheatgrow": [pygame.K_2],
	"controls": [pygame.K_F1],
	"camera": [pygame.K_F2],
	"chomp": [pygame.K_F3],
	"sfx": [pygame.K_F4],
	"music": [pygame.K_F5],
	"resize": [pygame.K_F10],
	"fullscreen": [pygame.K_F11],
	"screenshot": [pygame.K_F12],
}
def remapkeys(kdowns0, kpressed0):
	kdowns = set()
	kpressed = {}
	for keyname, values in keys.items():
		if any(value in kdowns0 for value in values):
			kdowns.add(keyname)
		kpressed[keyname] = any(kpressed0[value] for value in values)
	return kdowns, kpressed

