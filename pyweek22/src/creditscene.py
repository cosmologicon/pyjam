import math
from . import view, menuscene, scene, ptext, img
from .util import F


fading = True
fade = 0
def init():
	global t, fading, fade
	t = 0
	fading = True
	fade = 0

def think(dt, mpos, mdown, *args):
	global t, fading, fade
	t += dt
	if mdown or t > 17.5:
		fading = False
	fade = math.clamp(fade + 2 * dt * (1 if fading else -1), 0, 1)
	if not fading and fade == 0:
		scene.pop()

def draw():
	if fade == 1:
		view.clear((80, 80, 80))
	else:
		menuscene.draw()
		view.drawoverlay(fade, (80, 80, 80))
		return
	lines = [
		(32, "yellow", "Dr. Zome's"),
		(60, "yellow", "Laboratory"),
		(32, "white", "PyWeek 22"),
		(),
		(60, "blue", "Team Universe Factory 22"),
		(),
		(40, "yellow", "Christopher Night"),
		(40, "white", "Team lead"),
		(40, "white", "Programming"),
		(40, "white", "Design"),
		(40, "white", "Writing"),
		(),
		(40, "yellow", "Charles McPillan"),
		(40, "white", "Design"),
		(40, "white", "Production"),
		(40, "white", "Story Lead"),
		(),
		(40, "yellow", "Mary Bichner"),
		(40, "white", "Music"),
		(40, "white", "Audio Production"),
		(),
		(40, "yellow", "Randy Parcel"),
		(40, "white", "Voice"),
		(),
		(40, "yellow", "Pat Bordenave"),
		(40, "white", "Voice"),
		(),
		(40, "yellow", "Samantha Thompson"),
		(40, "white", "Character Art"),
		(),
		(40, "yellow", "Jordan Gray"),
		(40, "white", "Sound Effects"),
		(),
		(60, "blue", "Thank you for playing!"),
	]
	y = 640 - 160 * t
	img.draw("zume", F(100, y + 1320 - 20 * abs(math.sin(2 * math.tau * t))), radius = F(65))
	img.draw("simon", F(754, y + 1475), radius = F(65), angle = 14 * math.sin(2 * math.tau * t))
	for line in lines:
		if not line:
			y += 60
			continue
		h, color, text = line
		ptext.draw(text, color = color, shadow = (1, 1), fontsize = F(h), fontname = "SansitaOne",
			midtop = F(854/2, y))
		y += h * 1.2 + 10

def abort():
	pass

