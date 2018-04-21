import sys

gamename = "Universe Factory 25"
minfps, maxfps = 10, 60

DEBUG = True
# DEBUG = "--DEBUG" in sys.argv

# Screen resolution
size0 = 1280, 720
heights = 360, 480, 576, 720, 1080
height = 720
for arg in sys.argv:
	if arg.startswith("--res="):
		height = int(arg[6:])
forceres = "--forceres" in sys.argv
fullscreen = "--fullscreen" in sys.argv

savename = "savegame.pkl"
reset = "--reset" in sys.argv

