import pygame, math
from . import scene, playscene, pview, ptext
from .pview import T

def pickany(objs):
	objs = list(objs)
	return objs[0] if objs else None

class self:
	pass

def init():
	self.stages = {
		"backyard": (2, 3),
		"stage 2": (3, 2),
		"lair": (4, 2),
		"boss": (4, 3),
	}
	self.joins = [
		("backyard", "stage 2"),
		("stage 2", "lair"),
		("stage 2", "boss"),
		("lair", "boss"),
		("backyard", "boss"),
	]
	self.at = "backyard"

def getmove(p0, p1):
	x0, y0 = p0
	x1, y1 = p1
	dx, dy = x1 - x0, y1 - y0
	return math.sign(dx), math.sign(dy)

def gettarget(at, keys):
	mx = int("right" in keys) - int("left" in keys)
	my = int("up" in keys) - int("down" in keys)
	if not mx and not my:
		return None
	for join in self.joins:
		if at in join:
			target = pickany(stage for stage in join if stage != at)
			if getmove(self.stages[at], self.stages[target]) == (mx, my):
				return target
	return None

def control(keys):
	if "act" in keys:
		scene.push(playscene)
	else:
		target = gettarget(self.at, keys)
		if target:
			self.at = target

def think(dt):
	pass

def screenpos(pos):
	x, y = pos
	return T(100 * x, 720 - 100 * y)
	
def draw():
	pview.fill((60, 100, 60))
	for s0, s1 in self.joins:
		pygame.draw.line(pview.screen, (200, 200, 200),
			screenpos(self.stages[s0]), screenpos(self.stages[s1]), T(5))
	for stagename, pos in self.stages.items():
		pygame.draw.circle(pview.screen, (40, 40, 40), screenpos(pos), T(25))
	pygame.draw.circle(pview.screen, (255, 200, 100), screenpos(self.stages[self.at]), T(20))
	ptext.draw("At: %s" % self.at, T(20, 20), fontsize = T(32), owidth = 1)

