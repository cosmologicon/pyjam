import sys

gamename = "Dr. Zome's Laboratory"
wsize = None  # will default to 480 in window mode and max available in fullscreen
minfps = 5
maxfps = 240
screenshotpath = "screenshots"
progresspath = "save/progress.pkl"  # Updated when you beat a level or unlock anything.
statepath = "save/quicksave.pkl"  # Updated at autosave time or when you quit the game.
backupstatepath = "save/quicksave-%s.pkl"  # Timestamped copy of the save state when you quit or press F5.
fullscreen = False
acolors = "--acolors" in sys.argv  # Whether to use the alternate, high-contrast color scheme for organelles

if "--fullscreen" in sys.argv:
	fullscreen = True
for arg in sys.argv:
	if arg.startswith("--res="):
		wsize = int(arg.split("=")[1])
if "--big" in sys.argv:
	wsize = 900

autosavetime = 10  # seconds between autosaves. Set to 0 to disable.
if "--noautosave" in sys.argv:
	autosavetime = 0

grabfactor = 1.3

# Effects options
cellshading = 1
background = 0.2
virusbounce = True
drawblob = True
n2collision = False

if "--loweffect" in sys.argv:
	cellshading = 0
	virusbounce = False
if "--noeffect" in sys.argv:
	cellshading = 0
	background = 0
	virusbounce = False
	drawblob = False
cellshading = 1

# Debug settings
DEBUG = "--debug" in sys.argv
showbox = False
showfps = "--showfps" in sys.argv or DEBUG
reset = "--reset" in sys.argv
quickstart = "--qstart" in sys.argv
unlockall = "--unlockall" in sys.argv
pulltower = True  # Whether the whole tower comes with it when you pluck an organelle

