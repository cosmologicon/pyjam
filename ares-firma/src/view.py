import pygame
from . import pview
from . import settings
VconvertS = pview.T


SscaleG = None

def init():
	pview.set_mode(settings.size0, fullscreen = settings.fullscreen)
	pygame.display.set_caption(settings.gamename)

def VconvertG(aG):
	return VconvertS(SscaleG * aG)

def GconvertV(aV):
	VscaleS = pview.f
	return aV / (VscaleS * SscaleG)

def GconvertVs(aV):
	return [GconvertV(xV) for xV in aV]


