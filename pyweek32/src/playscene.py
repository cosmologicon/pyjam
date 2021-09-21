import pygame, math, random
from . import view, pview, graphics, geometry, state, ptext, progress
from .pview import T

class self:
	pass


def init():
	self.t = 0
	self.twin = 0
	state.init()
	view.x0, view.y0 = state.you.pos
	view.scale = 40
	from . import gameoverscene
	gameoverscene.init()
	

def think(dt, kpressed):
	self.t += dt

	if kpressed[pygame.K_SPACE]:
		state.you.unchomp()
	
	dkx = (1 if kpressed[pygame.K_RIGHT] else 0) - (1 if kpressed[pygame.K_LEFT] else 0)
	dky = (1 if kpressed[pygame.K_UP] else 0) - (1 if kpressed[pygame.K_DOWN] else 0)

	if not state.winning() and not state.gameover():
		state.you.think(dt, dkx, dky)
	state.think(dt)

	if state.winning():
		vtarget = 0, 0
		starget = 300 / state.R
	elif state.gameover():
		vtarget = view.x0, view.y0
		starget = 200
	elif state.you.chompin:
		vtarget = state.you.vtarget
		starget = state.you.starget
	else:
		vtarget = state.you.pos
		starget = 40
	view.x0, view.y0 = math.softapproach((view.x0, view.y0), vtarget, 4 * dt, dymin=0.001)
	view.scale = math.softlogapproach(view.scale, starget, 1 * dt, dymin=0.001)

	if state.winning():
		self.twin += dt
	if self.twin > 2:
		progress.beatendless(state.stage)
		init()
		

def draw():
#	if self.chompin:
#		pview.fill((40, 0, 0))
	graphics.drawstars()
	state.you.draw()
	for wall in state.walls:
		wall.draw()
	for obj in state.objs:
		obj.draw()		

	a = math.smoothfadebetween(self.t, 1.5, 1, 2, 0)
	if a > 0:
		ptext.draw("Endless Stage %d" % state.stage, midbottom = T(640, 700), fontsize = T(60),
			owidth = 1, alpha = a)



