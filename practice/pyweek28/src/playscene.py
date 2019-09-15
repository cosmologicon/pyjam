import pygame, math
from . import scene, pview, state, things, draw

class PlayScene(scene.Scene):
	def __init__(self):
		state.balloon = things.Balloon((0, 10))
		state.castle = things.Castle((0, 0))

	def think(self, dt, kdown, kpressed):
		# TODO: also handle ASDF
		kx = (kpressed[pygame.K_RIGHT]) - (kpressed[pygame.K_LEFT])
		ky = (kpressed[pygame.K_UP]) - (kpressed[pygame.K_DOWN])
		if kx and ky:  # Diagonal motion is the same speed
			kx, ky = math.norm((kx, ky))
		state.balloon.move(kx, ky)
		state.balloon.think(dt)
		state.castle.think(dt)

	def draw(self):
		pview.fill((80, 80, 160))
		# TODO: clouds in the background
		draw.string()
		state.balloon.draw()
		state.castle.draw()
		# TODO: HUD that shows your current altitude

