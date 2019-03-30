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

forceres = False

reset = "--reset" in sys.argv


DEBUG = "--DEBUG" in sys.argv
unlockall = "--unlockall" in sys.argv



