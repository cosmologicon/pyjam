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
	"tip": "You must be within the line of sight of the statue when you step on the plate for it to count. Move the statue in the middle of the room, then activate each of the numbered plates.",
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
	"tip": "You must be visible to the statue three times, including through the mirrors, when you stand on the plate. Move the statue or the mirrors or both, so that the statue has three lines of sight to the plate.",
}


data[4] = {
	"zoom": 20,
	"youpos": (-8, -8),
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
	"plates": [((8, -8), 2), ((-8, 8), 2)],
	"caption": "The last thing I remember, I was in my office late at night, working on my latest Treatise on Opticks. I was staring at myself in the mirror, pondering the nature of reflections.",
	"tip": "Move the statue and the mirrors so that the statue has two lines of sight to each plate. Hold Ctrl to zoom out and see the big picture.",
}


data[5] = {
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
	"caption": "I imagined my mirror image to be my evil twin, blocking my path and countering my every move. If only I could convince him to step aside for a moment, there would be nothing in my way to prevent me from passing through the mirror.",
	"tip": "Each plate needs a line of sight from the statue, and you have two mirrors to work with. Start by moving the statue so that it has a direct line of sight to two of the plates.",
}


data[6] = {
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
	"caption": "Is that what I did? Have I entered the mirror realm? But how? My evil twin is relentless and unerring. How could I ever hope to outmaneuver or outsmart him?",
	"tip": "The statue needs 7 lines of sight to the plate. This calls for two mirrors close together facing each other.",
}


data[7] = {
	"zoom": 12,
	"youpos": (8, -8),
	"lookpos": (-8, 8),
	"roomps": [
		(-11, 11),
		(-12.5, -12.5),
		(11, -11),
		(12.5, 12.5),
	],
	"mirrors": [
		(2, 0.5, 4),
		(3, 0.5, 4),
	],
	"plates": [
		((0, -5), 1),
		((0, 5), 1),
		((5, 0), 1),
		((-5, 0), 1),
		((0, 0), 3),
	],
	"caption": "What if my mirror image is not my adversary, but my accomplice? After all, we're perfectly in sync. Ah, I finally see how to end my treatise....",
	"tip": "You need two lines of sight that hit the center plate but none of the surrounding plates. You get narrower lines of sight when the mirror is further from the statue.",
}


data[8] = {
	"zoom": 12,
	"youpos": (0, 2),
	"lookpos": (0, 0),
	"roomps": [
		(20 * x, 14 * y * (0.5 + abs(x)))
		for x, y in math.CSround(24)
	],
	"mirrors": [(jwall, 0.5, 3) for jwall in (0, 4, 8, 12, 16, 20)],
	"plates": [
		((11, 5.2), 2),
		((-11, 5.2), 3),
		((-11, -5.2), 3),
		((11, -5.2), 4),
	],
	"caption": """This book is dedicated to my "evil" twin: Thank you for showing me the nature of reflections. The End.""",
	"tip": "This stage is extremely optional, so feel free to skip it! There's no ending cutscene or anything. Thanks for playing.",
}

