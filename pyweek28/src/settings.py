import sys
gamename = "Nerdozog's Ascent"

# Baseline resolution (also default resolution)
resolution = 1280, 720
resolution0 = 720
resolutions = 480, 588, 720, 880, 1080
fullscreen = "--fullscreen" in sys.argv
for arg in sys.argv:
	if arg.startswith("--res="):
		resolution0 = int(arg[6:])
forceres = "--forceres" in sys.argv


minfps = 10
maxfps = 120

savename = "savegame.pkl"
reset = "--reset" in sys.argv


DEBUG = "--DEBUG" in sys.argv
showhelp = False

# TODO: command-line flags to change settings

audio = "--noaudio" not in sys.argv
music = audio and "--nomusic" not in sys.argv
sound = audio and "--nosound" not in sys.argv

# TODO: retain settings that are changed in-game, e.g. resolution and sound volume, between startups.

