import os.path

gamename = "They're Behind Everything"
DEBUG = True

minfps, maxfps = 10, 60

# The uniform motion of the camera.
# Don't change this. It will mis-calibrate the position of everything.
speed = 24
# Default position of the player to the left of the center.
lag = 30
# Pixels per game unit at the baseline resolution
gamescale = 10

# Duration before you land when we'll still register a jump if you press and hold jump
# until landing.
prejumptime = 0.2

# Approximate time to reach the cliff when jump is pressed when we'll hold off on jumping
# until the cliff is reached.
cliffhangtime = 0.3

savename = os.path.join("save", "progress.txt")

