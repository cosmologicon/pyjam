import pygame, math
from . import ptext, window, sound, scene, bombscene
from .util import F

crawltext = " ".join("""
It is a time of political unrest. An underground group known as the Seekers have demonstrated 
increasingly brazen acts of power. Reports of a devastating weapon under Seeker control are 
unconfirmed, but the populace remains uneasy knowing that any day, an attack might come.
""".split())

def onpush():
	global t
	t = 0
	ptext.getsurf(crawltext, fontsize = F(60), widthem = 14, fontname = "Oswald")
	sound.play("dialogue/NARRATOR", 1)

def think(dt, estate):
	global t
	t += dt
	if t > 2 and not pygame.mixer.Channel(1).get_busy():
		scene.swap(bombscene)

def draw():
	window.screen.fill((0, 0, 0))
	top = 440 - 70 * t
	ptext.draw(crawltext, fontsize = F(60), fontname = "Oswald", widthem = 14, midtop = F(854 // 2, top))
	ptext.draw("Fullscreen: F", fontsize = F(18), fontname = "Righteous", bottomleft = F(10, 470))


