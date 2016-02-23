import pygame
from pygame.locals import *
from src import window
from src.window import F

pygame.mixer.pre_init(11000, -16, 1, 1)

media = {}

def getsound(name):
	if name not in media:
		media[name] = pygame.mixer.Sound("data/%s.ogg" % name)
	return media[name]
def playsound(name):
	getsound(name).play()

def getvideo(name):
	if name not in media:
		video = pygame.movie.Movie("data/%s.mp4" % name)
		media[name] = video
	return media[name]
def playvideo(name, loops=0):
	video = getvideo(name)
	rect = pygame.Rect(F((0, 0) + video.get_size()), center = window.screen.get_rect().center)
	video.set_display(window.screen, rect)
	video.play()


def getimage(name):
	if name not in media:
		img = pygame.image.load("data/%s" % name)
		if name.endswith(".jpg"):
			img = img.convert()
		else:
			img = img.convert_alpha()
		media[name] = img
	return media[name]

def drawimage(name, pos, scale=1):
	if isinstance(name, pygame.Surface):
		img = name
	else:
		img = getimage(name)
	if scale != 1:
		w, h = img.get_rect().size
		img = pygame.transform.smoothscale(img, (int(w * scale), int(h * scale)))
	rect = img.get_rect()
	rect.center = pos
	window.screen.blit(img, rect)

def colorfilter(img):
	img = img.copy()
	surf = pygame.surfarray.pixels3d(img)
	sx, sy = img.get_rect().size
	surf[sx//2:,:sy//2,2] *= 0
	surf[:sx//2,:sy//2,:3] = (surf[:sx//2,:sy//2,:3] * 0.5).astype(surf.dtype)
	surf[sx//2:,sy//2:,0] *= 0
	return img


