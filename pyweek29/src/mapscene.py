import pygame, math
from . import scene, playscene, pview, ptext, progress, sound
from . import draw as D
from .pview import T

def pickany(objs):
	objs = list(objs)
	return objs[0] if objs else None

class self:
	pass

def init():
	pass

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
	for join in progress.joins:
		if at in join:
			target = pickany(stage for stage in join if stage != at)
			if getmove(progress.stages[at], progress.stages[target]) == (mx, my):
				return target
	return None

def control(keys):
	if "act" in keys:
		scene.push(playscene)
		sound.play("select")
	else:
		target = gettarget(progress.at, keys)
		if target and target in progress.unlocked:
			progress.at = target
			sound.play("move")
		else:
			sound.play("no")

def think(dt):
	pass

def screenpos(pos):
	x, y = pos
	return T(100 * x, 720 - 100 * y)

def draw():
	pview.fill((60, 100, 60))
	for s0, s1 in progress.joins:
		if s0 not in progress.unlocked or s1 not in progress.unlocked:
			continue
		pygame.draw.line(pview.screen, (200, 200, 200),
			screenpos(progress.stages[s0]), screenpos(progress.stages[s1]), T(5))
	for stagename, pos in progress.stages.items():
		if stagename not in progress.unlocked:
			continue
		color = (50, 50, 50) if stagename in progress.beaten else (200, 0, 0)
		pygame.draw.circle(pview.screen, color, screenpos(pos), T(25))
#	angle = 10 * math.sin(math.tau * 0.001 * pygame.time.get_ticks())
	angle = 0
	D.drawimg("token", screenpos(progress.stages[progress.at]), pview.f * 400, angle)
	ptext.draw("At: %s" % progress.at, T(20, 20), fontsize = T(32), owidth = 1)



