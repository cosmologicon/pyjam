import math, pygame, os.path
from functools import cache
from . import ptext, pview, view, settings

@cache
def loadimg(filename):
	return pygame.image.load(filename)

@cache
def img0(iname, scale = 1):
	if scale != 1:
		img = img0(iname)
		w, h = img.get_rect().size
		return pygame.transform.rotozoom(img, 0, scale)
	return loadimg(os.path.join("img", iname + ".png"))

def drawimgat(img, pD):
	pview.screen.blit(img, img.get_rect(center = pD))

def drawsymbolatD(symbol, pD, fontsizeD, beta = 1):
	color = math.imix((0, 0, 0), settings.colorcodes[symbol], beta)
	ptext.draw(symbol, center = pD, color = color,
		fontsize = fontsizeD, owidth = 2)
def drawsymbolat(symbol, pD, fontsizeG, beta = 1):
	drawsymbolatD(symbol, pD, view.DscaleG(fontsizeG), beta)

def drawdomeat(pG):
	drawimgat(img0("dome", scale = view.VscaleG / 400), view.DconvertG(pG))

