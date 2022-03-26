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
	"tip": "Leave the statue in the middle of the room and activate each of the numbered plates by stepping on them and pressing Space.",
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
	"tip": "You must be within the line of sight of the statue when you step on the plate for it to count. Move the statue in the middle of the room, then step on each of the numbered plates.",
}


data[3] = {
	"zoom": 20,
	"youpos": (0, 0),
	"lookpos": (0, 14),
	"roomps": [
		(-4, 16),
		(-4, -16),
		(4, -16),
		(4, 16),
	],
	"mirrors": [(0, 0.6, 4), (2, 0.2, 4)],
	"plates": [((0, -14), 3)],
	"caption": "Mirrors! But why don't I see the statue's reflection?",
	"tip": "You must be visible to the statue three times, including through the mirrors, when you stand on the plate. Move either the statue or the mirrors so that the statue has three lines of sight to the plate.",
}


data[4] = {
	"zoom": 20,
	"youpos": (0, 0),
	"lookpos": (8, 8),
	"roomps": [
		(-11, 11),
		(-11, -11),
		(11, -11),
		(11, 11),
	],
	"mirrors": [
		(0, 0.6, 4),
		(2, 0.2, 4),
	],
	"plates": [((0, -8), 3)],
	"caption": "The last thing I remember, I was in my office late at night, working on my latest Treatise on Opticks. I was staring in the mirror, pondering the nature of reflections.",
	"tip": "Move the statue and the mirrors so that the statue has two lines of sight to each plate. Hold Ctrl to zoom out.",
}


data[5] = {
	"zoom": 20,
	"youpos": (0, 0),
	"lookpos": (0, 4),
	"roomps": [
		(0, 7),
		(-7, 0),
		(0, -16),
		(7, 0),
	],
	"mirrors": [(0, 0.5, 6), (3, 0.5, 6)],
	"plates": [((0, -11), 7)],
	"caption": "I imagined my mirror image to be my evil twin, countering my every move and blocking my path. If only I could convince him to step aside for a moment, there would be nothing blocking me from passing through the mirror.",
	"tip": "Move either the statue or the mirrors so that the statue has the correct number of lines of sight to the plate. Hold Ctrl to zoom out.",
}


data[6] = {
	"zoom": 12,
	"youpos": (-8, -8),
	"lookpos": (8, 8),
	"roomps": [
		(-11, 11),
		(-12.5, -12.5),
		(11, -11),
		(12.5, 12.5),
	],
	"mirrors": [
		(0, 0.5, 4),
		(2, 0.5, 4),
	],
	"plates": [
		((0, -5), 1),
		((0, 5), 1),
		((5, 0), 1),
		((-5, 0), 1),
		((0, 0), 3),
	],
	"caption": "As adversaries go, my reflection may not be ambitious or destructive, but he is relentless and unerring. I know that I will never be able to outmaneuver or outsmart him.",
	"tip": "Move the statue and the mirrors so that the statue has 2 lines of sight to the center plate through the mirrors, but no lines of sight to the outer plates through the mirrors. Hold Ctrl to zoom out.",
}


data[7] = {
	"zoom": 12,
	"youpos": (0, 8),
	"lookpos": (0, 0),
	"roomps": [
		(0, 16), (-16, 2), (-4, 4), (-4, -4), (-16, -2),
		(0, -16), (16, -2), (4, -4), (4, 4), (16, 2),
	],
	"mirrors": [
		(0, 0.5, 4),
		(5, 0.5, 4),
	],
	"plates": [
		((9, 5.2), 1),
		((-9, 5.2), 1),
		((-9, -5.2), 1),
		((9, -5.2), 1),
	],
	"caption": "But perhaps I've been thinking about it all wrong. What if my mirror image is not my adversary, but my accomplice? We certainly seem to be able to work together.",
	"tip": "",
}


data[8] = {
	"zoom": 12,
	"youpos": (0, 2),
	"lookpos": (0, 0),
	"roomps": [
		(20 * x, 14 * y * (0.5 + abs(x)))
		for x, y in math.CSround(24)
	],
	"mirrors": [
		(0, 0.5, 3),
		(5, 0.5, 4),
	],
	"plates": [
		((9, 5.2), 1),
		((-9, 5.2), 1),
		((-9, -5.2), 1),
		((9, -5.2), 1),
	],
	"caption": "I believe I can now finish my treatise.",
	"tip": "",
}

