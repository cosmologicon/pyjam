import math

data = {}

data[1] = {
	"zoom": 20,
	"youpos": (0, 3),
	"lookpos": (0, -3),
	"roomps": [(x, y) for x, y in math.CSround(5, r = 16, jtheta0 = 1 / 4)],
	"mirrors": [],
	"plates": [((x, y), 1) for x, y in math.CSround(5, r = 12, jtheta0 = 1 / 4)],
	"caption": "Where am I? How did I get here?",
	"tip": "Leave the statue in the middle of the room and step on each of the numbered plates.",
}

data[2] = {
	"zoom": 20,
	"youpos": (0, 0),
	"lookpos": (0, 12),
	"roomps": [
		(-4, 16), (-4, 4), (-16, 4),
		(-16, -4), (-4, -4), (-4, -16),
		(4, -16), (4, -4), (16, -4),
		(16, 4), (4, 4), (4, 16),
	],
	"mirrors": [],
	"plates": [((-12, 0), 1), ((0, -12), 1), ((12, 0), 1)],
	"caption": "This curious statue's eyes seem to gaze in all directions. What all does it see?",
	"tip": "Move the statue in the middle of the room, then step on each of the numbered plates.",
}


