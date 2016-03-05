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
		ptext.draw("upgradons: %d" % state.state.bank, topright = F(844, 10), color = "white", owidth = 1.3,
			fontsize = F(28))

def drawyouinfo(letter):
	name = {
		"A": "Mel Bovus",
		"B": "Martina Scamp",
		"C": "Ignatius Pturner",
		"D": "Ruby Jade",
		"E": "Hallan Waterby",
		"F": "Nicholas Pax",
	}[letter]
	byline = {
		"A": "Has their own ship. Pretty cool, huh?",
		"B": "Has their own ship. Pretty cool, huh?",
		"C": "Has their own ship. Pretty cool, huh?",
		"D": "Has their own ship. Pretty cool, huh?",
		"E": "Has their own ship. Pretty cool, huh?",
		"F": "Has their own ship. Pretty cool, huh?",
	}[letter]
	ptext.draw(name, topleft = F(28, 110), width = F(400), color = "#AAAAAA", owidth = 1.3,
		fontsize = F(32))
	ptext.draw(byline, topleft = F(28, 144), width = F(400), color = "red", owidth = 1.3,
		fontsize = F(32))

def drawup1info(letter, cost, canbuy):
	name = {
		"A": "Mel",
		"B": "Scamp",
		"C": "Ignatius",
		"D": "Ruby",
		"E": "Hallan",
		"F": "Pax",
	}[letter]
	color = "white" if canbuy else "#666666"
	ptext.draw("Click to purchase SPEED upgrade for " + name,
		topleft = F(28, 110), color = color, fontsize = F(32), owidth = 1)
	ptext.draw("Cost: %d upgradons" % cost,
		topleft = F(28, 144), color = "#AAAACC", fontsize = F(32), owidth = 1)

def drawup2info(letter, cost, canbuy):
	name = {
		"A": "Mel",
		"B": "Scamp",
		"C": "Ignatius",
		"D": "Ruby",
		"E": "Hallan",
		"F": "Pax",
	}[letter]
	color = "white" if canbuy else "#666666"
	ptext.draw("Click to purchase CHARGE RATE upgrade for " + name,
		topleft = F(28, 110), color = color, fontsize = F(32), owidth = 1)
	ptext.draw("Cost: %d upgradons" % cost,
		topleft = F(28, 144), color = "#AAAACC", fontsize = F(32), owidth = 1)




