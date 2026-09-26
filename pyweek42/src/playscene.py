import pygame
from . import pview, thing, state, settings
from .pview import T

class self: pass

def init():
	state.you = thing.You((0, 0))
#	state.hazards = [thing.CircleHazard((3, 1), 2), thing.RectangleHazard((-4, 2), (2, 2))]
	state.spawners = []
	state.salvos = []

def control(kpressed, kdowns):
	dx = int("right" in kpressed) - int("left" in kpressed)
	dy = int("down" in kpressed) - int("up" in kpressed)
	state.you.control(dx, dy)
	if settings.DEBUG and "spawn" in kdowns:
		state.salvos.append(thing.TopSalvo5())
	if "act" in kdowns:
		state.activate()

def think(dt):
	state.you.think(dt)
	for obj in state.salvos:
		obj.think(dt)
	for obj in state.spawners:
		obj.think(dt)
		if not obj.alive:
			obj.spawn()
	for obj in state.hazards:
		obj.think(dt)
	state.hazards = [obj for obj in state.hazards if obj.alive]
	state.spawners = [obj for obj in state.spawners if obj.alive]
	state.salvos = [obj for obj in state.salvos if obj.alive]
	state.ouch = any(hazard.hitsyou(state.you) for hazard in state.hazards)
	state.device.think(dt)

def draw():
	pview.fill((20, 20, 20))
	state.draw_room()
	state.you.draw()
	for obj in state.spawners:
		obj.draw()
	for obj in state.hazards:
		obj.draw()
	if state.ouch:
		pview.fill((255, 0, 0, 60))

