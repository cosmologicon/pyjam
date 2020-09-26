import pygame
from . import settings

def init():
	pass

def get():
	kdowns = set()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			kdowns.add("quit")
		if event.type == pygame.KEYDOWN:
			for key, kcodes in settings.keys.items():
				if event.key in kcodes:
					kdowns.add(key)
	pressed = pygame.key.get_pressed()
	kpressed = { key: any(pressed[code] for code in codes) for key, codes in settings.keys.items() }
	return kdowns, kpressed

def empty():
	return set(), { key: False for key in settings.keys.keys() }


