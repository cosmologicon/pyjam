import pygame, math
from . import scene, playscene, view, pview, ptext, settings, graphics, snek, geometry, sound, progress
from .pview import T


class self:
	pass

def init():
	self.t = 0
	self.jopt = 0
	self.done = False
	self.tdone = 0
	self.you = snek.You((0, 0))
	tilt = -0.5
	self.you.ps = []
	ps = [(4 * S / (1 + C ** 2), 4 * S * C / (1 + C ** 2)) for C, S in math.CSround(120, jtheta0 = 1)]
	ps = [math.R(tilt, p) for p in ps]
	thetas = [math.atan2(x1 - x0, y1 - y0) for (x0, y0), (x1, y1) in geometry.traversepoly(ps)]
	thetas = thetas[:-1] + thetas[-1:]
	d, p0 = 0, (0, 0)
	for p, theta in zip(ps, thetas):
		self.you.ps.append((d, p, theta))
		d += math.distance(p, p0)
		p0 = p
	self.you.length = d
	self.you.d = d
	self.you.pos = ps[-1]
	self.you.theta = thetas[-1]
	self.you.speed = 1
	self.you.chomp(quiet = True)
	self.you.tchomp = 100
	self.you.menu = True
	self.you.fixmovement = False
	for _ in range(120):
		self.you.think(1 / 120, 0, 0)
	sound.playmusic("brittle")

def reset():
	self.t = 0
	self.done = False
	self.tdone = 0

def think(dt, kpressed, kdowns):
	self.t += dt
	self.you.think(dt, 0, 0)
	
	if "quit" in kdowns:
		scene.current = None
	if self.done:
		self.tdone += dt
		if self.tdone > 0.5:
			finish()
	else:
		if "up" in kdowns:
			self.jopt -= 1
			sound.playsound("blip0")
		if "down" in kdowns:
			self.jopt += 1
			sound.playsound("blip0")
		self.jopt = math.clamp(self.jopt, 0, 2)
		if "act" in kdowns:
			self.done = True
			sound.playsound("blip1")

def finish():
	if self.jopt == 0:
		scene.setcurrent("adventure")
	if self.jopt == 1:
		scene.setcurrent("endless")
	if self.jopt == 2:
		scene.setcurrent("settings_menu")
	

def draw():
	pview.fill((0, 20, 50))
	view.x0, view.y0, view.scale = 0, 0, 150
	self.you.draw()
	pview.fill((0, 20, 50, 200))
	ptext.draw(settings.gamename, center = T(640, 180), fontsize = T(160), owidth = 0.5, shade = 1)
	optnames = [
		"Adventure/Tutorial",
		"Endless",
		"Settings",
	]
	angle = math.mix(-0.2, 0.2, math.cycle(0.4 * self.t))
	for j, optname in enumerate(optnames):
		y = 400 + 90 * j
		ptext.draw(optname, midleft = T(250, y), fontsize = T(80), owidth = 0.5, shade = 1)
		if j == self.jopt:
			imgtop = "head-top-0" if not progress.adventuredone else "head-top-3"
			graphics.drawimgscreen(T(160, y + 15), "head-bottom", pview.f * 10, angle)
			graphics.drawimgscreen(T(160, y + 15), imgtop, pview.f * 10, angle)
	ptext.draw("by Christopher Night\nmusic by Kevin MacLeod",
		midtop = T(960, 540), fontsize = T(40), owidth = 0.5, shade = 1)

	btext = None
	if self.jopt == 0:
		btext = "Adventure complete. Thank you for playing!" if progress.adventuredone else "Adventure progress %d%%" % (4 * progress.adventure)
	if self.jopt == 1:
		btext = "Endless stages completed: %d" % progress.endless
	if btext:
		ptext.draw(btext, midbottom = T(640, 700), fontsize = T(34), owidth = 0.5, shade = 1)

	alpha = math.imix(0, 255, math.fadebetween(self.tdone, 0, 0, 0.5, 1))
	if alpha > 0:
		pview.fill((20, 60, 120, alpha))


