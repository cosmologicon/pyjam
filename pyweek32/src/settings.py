import pickle, os, sys

# Command line editable.

height = 720  # Current resolution
fullscreen = False
directcontrol = False
fixedcamera = True
autochomp = False



def save():
	obj = height, fullscreen
	pickle.dump(obj, open("settings.pkl", "wb"))
def load():
	global height, fullscreen
	if not os.path.exists("settings.pkl"): return
	obj = pickle.load(open("settings.pkl", "rb"))
	height, fullscreen = obj
def reset():
	if os.path.exists("settings.pkl"):
		os.remove("settings.pkl")
	save()

size0 = 1280, 720  # Do not change

# EDIT HERE IF DESIRED
gamename = "Neverending"
savename = "savegame.pkl"
heights = 480, 540, 720, 1080
DEBUG = True
reset = "--reset" in sys.argv
minfps, maxfps = 10, 120

