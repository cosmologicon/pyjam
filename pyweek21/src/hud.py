import pygame
from . import ptext, state
from .util import F

showing = []
def clear():
	del showing[:]
def show(text):
	showing.append(text)
def draw():
	if showing:
		ptext.draw("\n".join(showing), midtop = F(427, 140), color = "#FF7777", owidth = 1.5,
			fontsize = F(32))
	if state.state.bank:
		ptext.draw("$%d" % state.state.bank, topright = F(844, 10), color = "white", owidth = 1.3,
			fontsize = F(28))

