from __future__ import division
import math
from . import ptext, playscene, view, scene, state
from .util import F

def init():
	global t
	t = 0

def think(dt, *args):
	global t
	t += dt
	if t > 2:
		scene.pop()

def draw():
	playscene.draw()
	if t < 2:
		alpha = math.clamp(2 * (2 - t), 0, 1) * 0.8
		view.drawoverlay(alpha)
	if t < 1.5:
		ptext.draw("Level start!", fontsize = F(150), center = F(854/2, 480/2),
			color = "yellow", gcolor = "orange", shadow = (1, 1))

def abort():
	state.save()

