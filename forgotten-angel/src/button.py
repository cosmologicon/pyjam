import pygame
import vista, state, img

class Button(object):
	def __init__(self, name, rect, fontsize = 22, fontname = "viga", bcolor = (0, 0, 255, 100), color = (255, 255, 255), text = None):
		self.name = name
		self.text = text or name
		self.color = color
		self.bcolor = bcolor
		self.rect = pygame.Rect(rect)
		self.fontsize = fontsize
		self.fontname = fontname
		self.makeimg()

	def makeimg(self):
		self.img = pygame.Surface(self.rect.size).convert_alpha()
		self.img.fill(self.bcolor)
		timg = img.gettext(" \n%s\n " % self.text, self.fontsize, self.color, (0, 0, 0, 0), self.fontname)
		p = self.img.get_rect().move(0, -self.fontsize // 6).center
		self.img.blit(timg, timg.get_rect(center = p))

	def within(self, screenpos):
		return self.rect.collidepoint(screenpos)

	def click(self):
		click(self.text)

	def draw(self):
		vista.screen.blit(self.img, self.rect)

class ModuleButton(Button):
	def __init__(self, *args, **kwargs):
		Button.__init__(self, *args, **kwargs)
		self.img1 = self.img
		self.img0 = self.img1.copy()
		mask = self.img1.copy()
		mask.fill((0,0,0,200))
		self.img0.blit(mask, (0, 0))

	def think(self, dt):
		self.img = self.img1 if state.state.active[self.text] else self.img0

def click(buttonname):
	if state.state.handlebutton(buttonname):
		return
	print("unhandled button: %s" % buttonname)

