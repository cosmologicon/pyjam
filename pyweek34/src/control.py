import pygame

xV, yV = 0, 0
pressed_ = False
click_ = False

def init():
	pass

def think(dt):
	global xV, yV, click_, pressed_
	xV, yV = pygame.mouse.get_pos()
	pressed = pygame.mouse.get_pressed()
	if pressed and not pressed_:
		click_ = True
	pressed_ = pressed
		

def hasclick():
	global click_
	ret = click_
	click_ = False
	return ret

