import sys

gamename = "Snowcrafter"

savefilename = "save.json"
yourname = "Cosmologicon"

offline = False

serverurl = "http://universefactory.net/tools/pyweek27/"
# To switch to a local server. See server/README.md to set up.
#serverurl = "http://0.0.0.0:8000/"
gallerydir = "gallery"

ups = 120

size0 = 1280, 720
heights = 360, 480, 720, 1080
fullscreen = "--fullscreen" in sys.argv
forceres = False

lowres = "--lowres" in sys.argv
if lowres:
	forceres = True

reset = "--reset" in sys.argv
DEBUG = "--DEBUG" in sys.argv
unlockall = "--unlockall" in sys.argv

collapsepoints = False
closepoints = False
if "--easy" in sys.argv:
	collapsepoints = True
	closepoints = True



