import pygame, math
from . import scene, playscene, dialogscene, pview, ptext, progress, sound
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
#		scene.push(dialogscene, "backyard")
		sound.play("select")
	else:
		print(keys)
		target = gettarget(progress.at, keys)
		if target and target in progress.unlocked:
			progress.at = target
			sound.play("move")
		else:
			sound.play("no")

def think(dt):
	D.killtime(0.05)

def screenpos(pos):
	x, y = pos
	return T(100 * x, 720 - 100 * y)

def draw():
	pview.fill((60, 100, 60))
	for s0, s1 in progress.joins:
		if s0 not in progress.unlocked or s1 not in progress.unlocked:
			continue
		p0 = screenpos(progress.stages[s0])
		p1 = screenpos(progress.stages[s1])
		pygame.draw.line(pview.screen, (0, 0, 0), p0, p1, T(10))
		pygame.draw.line(pview.screen, (200, 200, 200), p0, p1, T(6))
	for stagename, pos in progress.stages.items():
		if stagename not in progress.unlocked:
			continue
		if stagename in progress.beaten:
			color = 50, 50, 50
		else:
			a = int(round(math.sin(5 * pygame.time.get_ticks() * 0.001) * 10)) / 10
			color = tuple(pview.I(180 + 60 * a, 40 + 20 * a, 40 + 20 * a))
		D.drawimg("lep-icon", screenpos(pos), T(420), colormask = color)
#	angle = 10 * math.sin(math.tau * 0.001 * pygame.time.get_ticks())
	angle = 0
	D.drawimg("token", screenpos(progress.stages[progress.at]), pview.f * 400, angle)
	ptext.draw("At: %s" % progress.at, T(20, 20), fontsize = T(32), owidth = 1)



