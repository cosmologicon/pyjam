import pygame, math, random
from . import view, pview, graphics, geometry, state
from .pview import T

class self:
	pass


def init():
	self.t = 0
	state.init()

def think(dt, kpressed):
	self.t += dt

	if kpressed[pygame.K_SPACE]:
		state.you.unchomp()
	
	dkx = (1 if kpressed[pygame.K_RIGHT] else 0) - (1 if kpressed[pygame.K_LEFT] else 0)
	dky = (1 if kpressed[pygame.K_UP] else 0) - (1 if kpressed[pygame.K_DOWN] else 0)

	state.you.think(dt, dkx, dky)
	state.think(dt)

	if state.you.chompin:
		vtarget = state.you.vtarget
		starget = state.you.starget
	else:
		vtarget = state.you.pos
		starget = math.mix(40, 42, math.cycle(0.0002 * pygame.time.get_ticks()))
	view.x0, view.y0 = math.softapproach((view.x0, view.y0), vtarget, 4 * dt, dymin=0.001)
	view.scale = math.softlogapproach(view.scale, starget, 1 * dt, dymin=0.001)



def draw():
#	if self.chompin:
#		pview.fill((40, 0, 0))
	graphics.drawstars()
	state.you.draw()
	for obj in state.objs:
		obj.draw()		



