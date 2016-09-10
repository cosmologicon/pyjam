import sys

gamename = "Dr. Zome's Laboratory"
wsize = 854, 480
minfps = 5
maxfps = 60
screenshotpath = "screenshots"
progresspath = "save/progress.pkl"
statepath = "save/quicksave.pkl"
fullscreen = False

autosavetime = 10  # seconds between autosaves. Set to 0 to disable.


# Effects options
cellshading = 1
background = 1
virusbounce = True
drawblob = True
n2collision = False

# Debug settings
showbox = False
showfps = True
reset = "--reset" in sys.argv
quickstart = "--qstart" in sys.argv
unlockall = "--unlockall" in sys.argv
pulltower = True  # Whether the whole tower comes with it when you pluck an organelle

