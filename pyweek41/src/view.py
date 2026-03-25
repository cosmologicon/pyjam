from . import settings, pview
import pygame

def init():
	pview.set_mode(settings.size)
	pygame.display.set_caption(settings.gamename)

def change_res():
	pview.cycle_height(settings.heights)

def toggle_fullscreen():
	pview.toggle_fullscreen()

def screenshot():
	pview.screenshot()


class camera:
	xG0 = 0
	yG0 = 0
	WscaleG = 14

def VsmoothscaleG(rG):
	VscaleG = pview.f
	return VscaleG * camera.WscaleG * rG

def VscaleG(rG):
	return pview.T(camera.WscaleG * rG)

def VconvertG(posG):
	xG, yG = posG
	xW = pview.centerx0 + camera.WscaleG * (xG - camera.xG0)
	yW = pview.centery0 - camera.WscaleG * (yG - camera.yG0)
	return pview.T(xW, yW)

def GconvertV(posV):
	xV, yV = posV
	xW, yW = xV / pview.f, yV / pview.f
	xG = camera.xG0 + (xW - pview.centerx0) / camera.WscaleG
	yG = camera.yG0 - (yW - pview.centery0) / camera.WscaleG
	return xG, yG

