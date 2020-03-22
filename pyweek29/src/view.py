import pygame
from . import pview, settings
from .pview import T


def init():
	pview.set_mode(size0 = settings.size0, height = settings.height0,
		fullscreen = settings.fullscreen, forceres = settings.forceres)


