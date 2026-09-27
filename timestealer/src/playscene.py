import pygame, math
from . import pview, thing, state, settings, hud
from .pview import T

class self: pass

def init():
	state.current_stage = 1
	state.won = False
	state.health = 3
	state.you = thing.You((0, 0))
	state.load_stage()

def control(kpressed, kdowns):
	dx = int("right" in kpressed) - int("left" in kpressed)
	dy = int("down" in kpressed) - int("up" in kpressed)
	state.you.control(dx, dy)
	if settings.DEBUG and "spawn" in kdowns:
		state.salvos.append(thing.TopSalvo5())
	if "act" in kdowns:
		state.activate()
	if "skip" in kdowns:
		state.advance()

def think(dt):
	state.think(dt)
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
	if any(hazard.hitsyou(state.you) for hazard in state.hazards):
		state.you.hurt()
	state.device.think(dt)

def draw():
	pview.fill((20, 60, 60))
	state.draw_room()
	state.you.draw()
	for obj in state.spawners:
		obj.draw()
	for obj in state.hazards:
		obj.draw()
	if state.you.touch:
		alpha = math.mixI(20, 80, state.you.touch)
		pview.fill((255, 0, 0, alpha))
	hud.draw()

