import pygame
from pygame.locals import *
from src import window, ptext, enco, settings, media
from src.window import F

class Rectangular(enco.Component):
	def init(self, rect, bcolor=(40, 20, 0), **kwargs):
		self.rect = pygame.Rect(rect)
		self.bcolor = bcolor
	def draw(self):
		window.screen.fill(self.bcolor, F(self.rect))
	def contains(self, pos):
		return F(self.rect).collidepoint(pos)
class HasText(enco.Component):
	def init(self, text, **kwargs):
		self.text = text
	def draw(self):
		rect = F(pygame.Rect(self.rect).inflate(-10, -10))
		ptext.drawbox(self.text, rect, fontname = "Oregano", color = "white")
	def click(self):
		clickbutton(self.text)

@Rectangular()
@HasText()
class Button(object):
	def __init__(self, rect, text):
		self.init(rect=rect, text=text)

buttons = []
def init():
	buttons.append(Button((40, 40, 220, 70), "Play sound"))
#	buttons.append(Button((40, 120, 220, 70), "Play video"))
	buttons.append(Button((40, 120, 220, 70), "Toggle fullscreen"))
	media.getsound("sound")

def clickbutton(name):
	if name == "Play sound":
		media.playsound("sound")
	if name == "Play video":
		media.playvideo("ostrich")
	if name == "Toggle fullscreen":
		settings.fullscreen = not settings.fullscreen
		window.init()

def think(dt, events):
	for event in events:
		if event.type == MOUSEBUTTONDOWN and event.button == 1:
			for button in buttons:
				if button.contains(event.pos):
					button.click()

def draw():
	window.screen.fill((0, 0, 100))
	ptext.draw("Press Esc to quit", fontname = "Oregano", fontsize = F(40),
		bottomleft = window.screen.get_rect().inflate(*F((-20, -20))).bottomleft,
		color = "#00AAFF", shadow = (1, 1))
	for button in buttons:
		button.draw()
	pygame.draw.circle(window.screen, (255, 255, 255), F((420, 120)), F(100))
	media.drawimage(media.colorfilter(media.getimage("earth.jpg")), F((640, 120)), 2.1 * window.sf)
	media.drawimage("egg.png", F((640, 320)), 0.3 * window.sf)

