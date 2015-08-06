import pygame
from pygame.locals import *
from src import window

pygame.mixer.pre_init(11000, -16, 1, 1)

sounds = {}

def getsound(name):
	if name not in sounds:
		sounds[name] = pygame.mixer.Sound("data/%s.ogg" % name)
	return sounds[name]
def playsound(name):
	getsound(name).play()


images = {}
def drawimage(name, pos, scale=1):
	if name not in images:
		img = pygame.image.load("data/%s" % name)
		if name.endswith(".jpg"):
			img = img.convert()
		else:
			img = img.convert_alpha()
		images[name] = img
	img = images[name]
	if scale != 1:
		w, h = img.get_rect().size
		img = pygame.transform.smoothscale(img, (int(w * scale), int(h * scale)))
	rect = img.get_rect()
	rect.center = pos
	window.screen.blit(img, rect)
