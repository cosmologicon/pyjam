import pygame
from . import ptext, window, sound, scene, playscene
from .util import F

def onpush():
	global t
	t = 0
	sound.play("bomb")

def think(dt, estate):
	global t
	t += dt
	if t > 10:
		scene.swap(playscene)

def draw():
	window.screen.fill((255, 255, 255))


