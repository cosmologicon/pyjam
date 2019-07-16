# THESE ARE NOT USER-EDITABLE SETTINGS, PEOPLE. DON'T MESS WITH THESE.

from __future__ import division
import pygame

DEBUG = False
gamename = "The Forgotten Angel"
minfps, maxfps = 10, 60

quickstart = False
pauseondialog = True

#ssize = sx, sy = 854, 480
ssize = sx, sy = 1138, 640
#ssize = sx, sy = 854 // 2, 480 // 2
def F(*args):
	if len(args) == 1:
		return int(round(args[0] * sy / 480))
	else:
		return [int(round(arg * sy / 480)) for arg in args]

# main gameplay area
grect = pygame.Rect(F(0, 0, 480, 480))
# side panel area
prect = pygame.Rect(F(480, 0, 374, 480))


# navmap
nrect = pygame.Rect(F(557, 260, 220, 220))
nscale = F(5)

# status indicators
statpos = [
	F(667 - 100, 240),
	F(667 + 100, 240),
]
statfontsize = F(20)

alertfontsize = 40

imgscale = 30  # image pixels per game unit for assets

shipsize = shipw, shiph = 4, 5

# Distance from the player before a fadeable object fades.
fadedistance = 16
vsize = 8

burndamagetime = 0.3
oortdamagetime = 0.3

modulecosts = {
	"engine": 0,
	"drill": 0,
	"laser": 3,
	"scope": 20,
	"gun": 100,
	"turbo": 80,
	"heatshield": 80,
	"deflector": 80,
	"hyperdrive": 200,
	"conduit-1": 3,
	"conduit-2": 3,
	"conduit-3": 3,
	"conduit-12": 10,
	"conduit-13": 10,
	"conduit-23": 10,
#	"conduit-cross": 40,
}

moduleinfo = {
	"engine": "Standard efficiency engine. Slightly better than getting out and pushing.",
	"drill": "Spacebuck extraction drill. Activates automatically in the presence of a passing asteroid.",
	"laser": "Short-range laser. Activates automatically in the presence of hostile units.",
	"scope": "Survey scope. Activate while on top of a planet to conduct a survey. Collects resources and adds the planet to your map.",
	"gun": "Strong weapon. Will fire when facing the target.",
	"turbo": "Medium-power engine. Faster than standard engine.",
	"heatshield": "Extreme heat shield. Pass across stars without taking damage.",
	"deflector": "Micrometeorite deflector. Travel through the Oort without taking damage.",
	"hyperdrive": "High-power engine. Much faster than standard engine. Immune to weapons while traveling. Consumes Starbucks.",
}

moduleblocks = {
	"engine": [(0,0), (1,0), (0,1), (1,1)],
	"drill": [(0,0), (1,0)],
	"laser": [(0,0), (1,0), (0,1)],
	"gun": [(0,0), (0,1), (0,2)],
	"scope": [(0,0), (1,0)],
	"turbo": [(0,1), (1,0), (1,1)],
	"heatshield": [(0,0), (1,0), (2,0)],
	"deflector": [(0,0), (0,1)],
	"hyperdrive": [(0,1), (1,0), (1,1), (2,1)],
}

moduleinputs = {
	"engine": [(-1,0,0,0)],
	"drill": [(2,0,1,0)],
	"laser": [(2,0,1,0)],
	"gun": [(0,1,1,1)],
	"scope": [(1,-1,1,0)],
	"turbo": [(-1,1,0,1)],
	"heatshield": [(-1,0,0,0)],
	"deflector": [(-1,1,0,1)],
	"hyperdrive": [(3,1,2,1)],
}



inames = {
	"mother": "Exelu",
	"supply": "Supply Ship",
	"baron": "Baroness",
	"angel0": "Angel",
	"angel1": "Angel",
	"angel2": "Angel",
	"angel3": "Angel",
	"angel4": "Angel",
	"angel6": "Angel",
	"angel7": "Angel",
	"angel8": "Angel",
	"angel9": "Angel",
}



