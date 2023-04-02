import sys

gamename = "BurgleCast"

minfps, maxfps = 5, 120

size0 = 1280, 720
height = None
heights = 240, 480, 720, 1080
fullscreen = False
forceres = False

savefile = "save.pkl"

reset = False
unlockall = False


DEBUG = False


if "--reset" in sys.argv:
	reset = True
if "--unlockall" in sys.argv:
	unlockall = True
if "--fullscreen" in sys.argv:
	fullscreen = True
for arg in sys.argv:
	if arg.startswith("--res="):
		height = int(arg[6:])

