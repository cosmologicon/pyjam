from src import window, ptext
from window import F

lines = []

def clear():
	del lines[:]

def show(line):
	lines.append(line)

def think(dt):
	clear()

def draw():
	for line in lines:
		ptext.draw(line, fontsize = F(40), midtop = F(window.sx / 2, 10), color = "gray",
			owidth = 1)

