import sys
gamename = "PyWeek 28: Tower"

# Baseline resolution (also default resolution)
resolution = 1280, 720
resolutions = 360, 480, 720, 1080
fullscreen = False

minfps = 10
maxfps = 120

# TODO: change to False before uploading
DEBUG = True
showhelp = False

# TODO: command-line flags to change settings

audio = "--noaudio" not in sys.argv
music = audio and "--nomusic" not in sys.argv
sfx = audio and "--nosfx" not in sys.argv

# TODO: retain settings that are changed in-game, e.g. resolution and sound volume, between startups.

