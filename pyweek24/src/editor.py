from __future__ import division, print_function
import pygame, math, json, os.path, sys
from . import maff, view, pview, ptext, hill
from .pview import T

filename = sys.argv[1] if len(sys.argv) > 1 else "/tmp/hills.json"
hills = []
if os.path.exists(filename):
	hills = json.load(open(filename, "r"))
jcursor = -1

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
	if pygame.K_RETURN in kdowns:
		jcursor = len(hills)
		hills.append({
			"specname": "oval",
			"x": 0,
			"y": 0,
			"z": 0,
			"sx": 0,
			"sy": 0,
			"xflip": False,
		})
	if pygame.K_TAB in kdowns:
		jcursor += -1 if kpressed[pygame.K_LSHIFT] else 1
		jcursor %= len(hills)
	if pygame.K_SPACE in kdowns:
		names = sorted(hill.specs)
		hills[jcursor]["specname"] = names[(names.index(hills[jcursor]["specname"]) + 1) % len(names)]
	if pygame.K_DELETE in kdowns:
		del hills[jcursor]
		jcursor = -1
	if pygame.K_a in kdowns:
		hills[jcursor]["x"] -= step
	if pygame.K_e in kdowns:
		hills[jcursor]["x"] += step
	if pygame.K_o in kdowns:
		hills[jcursor]["y"] -= step
	if pygame.K_COMMA in kdowns:
		hills[jcursor]["y"] += step
	if pygame.K_QUOTE in kdowns:
		hills[jcursor]["z"] -= step
	if pygame.K_PERIOD in kdowns:
		hills[jcursor]["z"] += step
	if pygame.K_h in kdowns:
		hills[jcursor]["sx"] -= step
	if pygame.K_n in kdowns:
		hills[jcursor]["sx"] += step
	if pygame.K_t in kdowns:
		hills[jcursor]["sy"] -= step
	if pygame.K_c in kdowns:
		hills[jcursor]["sy"] += step
	if pygame.K_BACKSPACE in kdowns:
		hills[jcursor]["xflip"] = not hills[jcursor]["xflip"]
	if kpressed[pygame.K_RIGHT]:
		view.X0 += 16 * step * dt
	if kpressed[pygame.K_LEFT]:
		view.X0 -= 16 * step * dt
	pview.fill((0, 0, 0))
	for jhill in sorted(range(len(hills)), key = lambda jhill: hills[jhill]["z"]):
		if jhill == jcursor and pygame.time.get_ticks() % 500 > 400:
			continue
		h = hills[jhill]
		hill.drawhill((h["x"], h["y"], h["z"]), hill.getspec(h))
	for h in hills:
		px, py = view.toscreen(h["x"], h["y"], h["z"])
		pygame.draw.circle(pview.screen, (255, 255, 255), (px, py), T(2))
		ptext.draw(h["specname"], fontsize = T(16), centerx = px, bottom = py - T(4))
		ptext.draw("%s,%s,%s\n%s/%s" % (h["x"], h["y"], h["z"], h["sx"], h["sy"]),
			fontsize = T(16), centerx = px, top = py + T(4))

	pygame.draw.line(pview.screen, (255, 128, 0), view.toscreen(view.X0, -30, 0), view.toscreen(view.X0, 30, 0), 1)
	pygame.draw.line(pview.screen, (255, 128, 0), view.toscreen(view.X0 - 30, -30, 0), view.toscreen(view.X0 - 30, 30, 0), 1)
	text = "%s,%s\n%s\n%.1fps" % (view.X0, view.Y0, filename, clock.get_fps())
	ptext.draw(text, bottomleft = T(10, 470), fontsize = T(20))

	pygame.display.flip()
	if pygame.K_ESCAPE in kdowns:
		playing = False

json.dump(hills, open(filename, "w"))


