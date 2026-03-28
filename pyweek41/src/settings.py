import sys

gamename = "Nightfeel"
size = 1280, 720
heights = 480, 600, 720, 1280, 1440
minfps, maxfps = 5, 120

savename = "savegame.pkl"

editor = "--editor" in sys.argv  # Level editor mode
reset = "--reset" in sys.argv

