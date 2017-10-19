from __future__ import division, print_function
import pygame, math, json, os.path, sys
from . import maff, view, pview, ptext, hill
from .pview import T

filename = sys.argv[1] if len(sys.argv) > 1 else "/tmp/hills.json"
hills = []
hazards = []
if os.path.exists(filename):
	hills, hazards = json.load(open(filename, "r"))
	for h in hills:
		h["a"] = h.get("a", 0)
jcursor = -1
cursorsets = ["hills", "hazards"]
cursorset = "hills"

view.init()
clock = pygame.time.Clock()
playing = True
while playing:
	dt = 0.001 * clock.tick(20)
	kdowns = []
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			kdowns.append(event.key)
		if event.type == pygame.QUIT:
			playing = False
	kpressed = pygame.key.get_pressed()
	step = 1
	if kpressed[pygame.K_LCTRL]:
		step *= 8
	if kpressed[pygame.K_LSHIFT]:
		step *= 0.125

	if pygame.K_F11 in kdowns:
		pview.toggle_fullscreen()
	if pygame.K_BACKQUOTE in kdowns:
		cursorset = cursorsets[(cursorsets.index(cursorset) + 1) % len(cursorsets)]
		jcursor = 0

	obj = None
	if cursorset == "hills" and 0 <= jcursor < len(hills):
		obj = hills[jcursor]
	if cursorset == "hazards" and 0 <= jcursor < len(hazards):
		obj = hazards[jcursor]

	if cursorset in ("hills", "hazards"):
		if pygame.K_a in kdowns:
			obj["x"] -= step
		if pygame.K_e in kdowns:
			obj["x"] += step
		if pygame.K_o in kdowns:
			obj["y"] -= step
		if pygame.K_COMMA in kdowns:
			obj["y"] += step
		if pygame.K_QUOTE in kdowns:
			obj["z"] -= step
		if pygame.K_PERIOD in kdowns:
			obj["z"] += step
	if cursorset == "hills":
		if pygame.K_TAB in kdowns:
			jcursor += -1 if kpressed[pygame.K_LSHIFT] else 1
			jcursor %= len(hills)
		if pygame.K_RETURN in kdowns:
			jcursor = len(hills)
			hills.append({
				"type": "hill",
				"specname": "oval",
				"x": 0,
				"y": 0,
				"z": 0,
				"a": 0,
				"sx": 0,
				"sy": 0,
				"xflip": False,
			})
		if pygame.K_SPACE in kdowns:
			names = sorted(hill.specs)
			obj["specname"] = names[(names.index(obj["specname"]) + 1) % len(names)]
		if pygame.K_DELETE in kdowns:
			del hills[jcursor]
			jcursor = -1
		if pygame.K_1 in kdowns:
			obj["a"] -= 0.125 * step
		if pygame.K_2 in kdowns:
			obj["a"] += 0.125 * step
		if pygame.K_h in kdowns:
			obj["sx"] -= step
		if pygame.K_n in kdowns:
			obj["sx"] += step
		if pygame.K_t in kdowns:
			obj["sy"] -= step
		if pygame.K_c in kdowns:
			obj["sy"] += step
		if pygame.K_BACKSPACE in kdowns:
			obj["xflip"] = not obj["xflip"]
	if cursorset == "hazards":
		if pygame.K_TAB in kdowns:
			jcursor += -1 if kpressed[pygame.K_LSHIFT] else 1
			jcursor %= len(hazards)
		if pygame.K_RETURN in kdowns:
			jcursor = len(hazards)
			hazards.append({
				"x": 0,
				"y": 0,
				"z": 0,
				"r": 2,
				"vx": 0,
				"vy": 0,
				"X0": 0,
			})
		if pygame.K_DELETE in kdowns:
			del hazards[jcursor]
			jcursor = -1
		if pygame.K_1 in kdowns:
			obj["r"] -= 0.5 * step
		if pygame.K_2 in kdowns:
			obj["r"] += 0.5 * step
		if pygame.K_h in kdowns:
			obj["vx"] -= step
		if pygame.K_n in kdowns:
			obj["vx"] += step
		if pygame.K_t in kdowns:
			obj["vy"] -= step
		if pygame.K_c in kdowns:
			obj["vy"] += step
		if obj:
			obj["X0"] = view.X0

	if kpressed[pygame.K_RIGHT]:
		view.X0 += 16 * step * dt
	if kpressed[pygame.K_LEFT]:
		view.X0 -= 16 * step * dt
	pview.fill((0, 0, 0))
	for jhill in sorted(range(len(hills)), key = lambda jhill: (hills[jhill]["z"], -hills[jhill]["x"])):
		if jhill == jcursor and cursorset == "hills" and pygame.time.get_ticks() % 500 > 400:
			continue
		h = hills[jhill]
		hill.drawhill((h["x"], h["y"], h["z"]), hill.getspec(h))
	for j, hazard in enumerate(hazards):
		if j == jcursor and cursorset == "hazards" and pygame.time.get_ticks() % 500 > 400:
			continue
		p0 = view.toscreen(hazard["x"], hazard["y"], hazard["z"])
		p1 = view.toscreen(hazard["x"] + hazard["vx"], hazard["y"] + hazard["vy"], hazard["z"])
		r = view.screenscale(hazard["r"], hazard["z"])
		pygame.draw.circle(pview.screen, (200, 100, 0), p0, r)
		pygame.draw.line(pview.screen, (200, 100, 0), p0, p1)
	for h in hills:
		px, py = view.toscreen(h["x"], h["y"], h["z"])
		pygame.draw.circle(pview.screen, (255, 255, 255), (px, py), T(2))
		ptext.draw(h["specname"], fontsize = T(16), centerx = px, bottom = py - T(4))
		ptext.draw("%s,%s,%s\n%s/%s/%.2f" % (h["x"], h["y"], h["z"], h["sx"], h["sy"], h["a"]),
			fontsize = T(16), centerx = px, top = py + T(4))
	for h in hazards:
		px, py = view.toscreen(h["x"], h["y"], h["z"])
		pygame.draw.circle(pview.screen, (0, 0, 0), (px, py), T(2))
		ptext.draw("%s,%s,%s\n%s/%s/%.2f" % (h["x"], h["y"], h["z"], h["vx"], h["vy"], h["r"]),
			fontsize = T(16), centerx = px, top = py + T(4))

	pygame.draw.line(pview.screen, (255, 128, 0), view.toscreen(view.X0, -30, 0), view.toscreen(view.X0, 30, 0), 1)
	pygame.draw.line(pview.screen, (255, 128, 0), view.toscreen(view.X0 - 30, -30, 0), view.toscreen(view.X0 - 30, 30, 0), 1)
	text = "%s,%s\n%s\n%.1fps" % (view.X0, view.Y0, filename, clock.get_fps())
	ptext.draw(text, bottomleft = T(10, 470), fontsize = T(20))

	pygame.display.flip()
	if pygame.K_ESCAPE in kdowns:
		playing = False

state = hills, hazards
json.dump(state, open(filename, "w"))


