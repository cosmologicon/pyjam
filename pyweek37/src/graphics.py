import math
from . import ptext, view, settings

def drawsymbolatD(symbol, pD, fontsizeD, beta = 1):
	color = math.imix((0, 0, 0), settings.colorcodes[symbol], beta)
	ptext.draw(symbol, center = pD, color = color,
		fontsize = fontsizeD, owidth = 2)
def drawsymbolat(symbol, pD, fontsizeG, beta = 1):
	drawsymbolatD(symbol, pD, view.DscaleG(fontsizeG), beta)

