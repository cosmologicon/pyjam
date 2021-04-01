import math
import pygame
from . import ptext, pview, state, progress, levels
from . import scene
from .pview import T


buttons = {
	levelname: ((200 + 100 * j, 200), 50)
	for j, levelname in enumerate(levels.data)
}

def control(cstate):
	if "click" in cstate.events:
		for bname, (bpos, br) in buttons.items():
			if bname in progress.unlocked and math.distance(cstate.mposV, T(bpos)) < T(br):
				goto(bname)
	if "quit" in cstate.kdowns:
		scene.pop()

def goto(levelname):
	from . import scene, playscene
	state.currentlevel = levelname
	scene.push(playscene)
	playscene.init()

def think(dt):
	pass


def draw():
	pview.screen.fill((30, 30, 60))
	for bname, (bpos, br) in buttons.items():
		if bname in progress.unlocked:
			pygame.draw.circle(pview.screen, (50, 50, 100), T(bpos), T(br))
			ptext.draw(bname, center = T(bpos), fontsize = T(30))

