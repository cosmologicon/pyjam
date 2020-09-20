import pygame
from . import settings

def init():
	pass

def get():
	kdowns = set()
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			for key, kcodes in settings.keys.items():
				if event.key in kcodes:
					kdowns.add(key)
	return kdowns

