import sys

gamename = "Project X"
wsize = 854, 480
minfps = 5
maxfps = 60
screenshotpath = "screenshots"
progresspath = "save/progress.pkl"
statepath = "save/quicksave.pkl"
fullscreen = False

# Effects options
cellshading = 0


# Debug settings
showbox = False
showfps = True
reset = True
quickstart = "--qstart" in sys.argv
unlockall = "--unlockall" in sys.argv
pulltower = True  # Whether the whole tower comes with it when you pluck an organelle

