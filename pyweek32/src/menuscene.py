import pygame, math
from . import playscene, view, pview, ptext, settings, graphics, snek, geometry
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
	self.you.chomp()
	self.you.tchomp = 100
	self.you.menu = True
		

def think(dt, kpressed, kdowns):
	self.t += dt
	self.you.think(dt, 0, 0)
	
	if self.done:
		self.tdone += dt
		if self.tdone > 1:
			finish()
	else:
		if pygame.K_UP in kdowns:
			self.jopt -= 1
		if pygame.K_DOWN in kdowns:
			self.jopt += 1
		self.jopt = math.clamp(self.jopt, 0, 2)
		if pygame.K_SPACE in kdowns:
			self.done = True

def finish():
	if self.jopt == 0:
		scene.current = "adventure"
		playscene.init()
	if self.jopt == 1:
		scene.current = "endless"
		playscene.init()
	if self.jopt == 2:
		scene.current = "settings"	
	

def draw():
	pview.fill((0, 0, 50))
	view.x0, view.y0, view.scale = 0, 0, 150
	self.you.draw()
	pview.fill((0, 0, 50, 200))
	ptext.draw(settings.gamename, center = T(640, 180), fontsize = T(160), owidth = 0.5, shade = 1)
	optnames = [
		"Adventure",
		"Endless",
		"Settings",
	]
	angle = math.mix(-0.2, 0.2, math.cycle(0.4 * self.t))
	for j, optname in enumerate(optnames):
		y = 420 + 90 * j
		ptext.draw(optname, midleft = T(250, y), fontsize = T(80), owidth = 0.5, shade = 1)
		if j == self.jopt:
			graphics.drawimgscreen(T(160, y + 15), "head-bottom", pview.f * 10, angle)
			graphics.drawimgscreen(T(160, y + 15), "head-top", pview.f * 10, angle)
	ptext.draw("by Christopher Night\nmusic by Kevin MacLeod",
		midtop = T(900, 440), fontsize = T(50), owidth = 0.5, shade = 1)


