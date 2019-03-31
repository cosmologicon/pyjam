from __future__ import division
import sys, json, os

gamename = "Snowcrafter"

savefilename = "progress.json"
yourname = ""

offline = False

serverurl = "http://universefactory.net/tools/pyweek27/"
# To switch to a local server. See server/README.md to set up.
#serverurl = "http://0.0.0.0:8000/"
gallerydir = "gallery"

ups = 120

collapsepoints = False
closepoints = False

size0 = 1280, 720
heights = 360, 480, 720, 1080
fullscreen = False
forceres = False
lowres = False
nomusic = False
nosfx = False

def save():
	obj = yourname, closepoints, collapsepoints
	json.dump(obj, open("settings.json", "w"))

def load():
	global yourname, closepoints, collapsepoints
	if os.path.exists("settings.json"):
		obj = json.load(open("settings.json", "r"))
		yourname, closepoints, collapsepoints = obj
load()


if "--fullscreen" in sys.argv:
	fullscreen = True

if "--lowres" in sys.argv:
	lowres = True
if lowres:
	forceres = True
if "--nomusic" in sys.argv or "--noaudio" in sys.argv:
	nomusic = True
if "--nosfx" in sys.argv or "--noaudio" in sys.argv:
	nosfx = True
	
reset = "--reset" in sys.argv
DEBUG = "--DEBUG" in sys.argv
unlockall = "--unlockall" in sys.argv
if "--easy" in sys.argv:
	collapsepoints = True
	closepoints = True


