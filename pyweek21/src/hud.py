import pygame
from . import ptext
from .util import F

showing = []
def clear():
	del showing[:]
def show(text):
	showing.append(text)
def draw():
	if not showing:
		return
	ptext.draw("\n".join(showing), midtop = F(427, 140), color = "#FF7777", owidth = 1.5,
		fontsize = F(32))

