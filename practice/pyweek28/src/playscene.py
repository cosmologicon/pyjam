import pygame, math, random
from . import scene, pview, state, things, draw, ptext
from .pview import T

class PlayScene(scene.Scene):
	def __init__(self):
		state.balloon = things.Balloon((0, 10))
		state.castle = things.Castle((0, 0))
		state.meteors = []

	def think(self, dt, kdown, kpressed):
		# TODO: also handle ASDF
		kx = (kpressed[pygame.K_RIGHT]) - (kpressed[pygame.K_LEFT])
		ky = (kpressed[pygame.K_UP]) - (kpressed[pygame.K_DOWN])
		if kx and ky:  # Diagonal motion is the same speed
			kx, ky = math.norm((kx, ky))
		state.balloon.move(kx, ky)

		# Add 1 meteor per second at a random position
		if 0.3 * random.random() < dt:
			state.meteors.append(things.randommeteor())
		state.balloon.think(dt)
		state.castle.think(dt)
		for meteor in state.meteors:
			meteor.think(dt)
		state.meteors = [meteor for meteor in state.meteors if meteor.alive]

	def draw(self):
		pview.fill((80, 80, 160))
		# TODO: clouds in the background
		draw.string()
		for meteor in state.meteors:
			meteor.draw()
		state.balloon.draw()
		state.castle.draw()

		# TODO: use a more interesting font
		text = "\n".join([
			"Collect: %s/%s" % (state.score, state.goal),
			"Speed: %s" % (state.speed,),
		])
		ptext.draw(text, bottomleft = pview.bottomleft, fontsize = T(32), owidth = 1)
		
		text = "\n".join([
			"Collect meteors using the castle.",
			"Collect enough to upgrade the balloon speed.",
			"Beware: meteors that hit the balloon will reset your progress.",
		])
		ptext.draw(text, bottomright = pview.bottomright, fontsize = T(22), owidth = 1)


