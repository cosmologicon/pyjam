import pygame, os.path
from src import ptext, window, sound
from src.window import F

lines = {}
for line in open(os.path.join("data", "dialog.txt")):
	line = line.strip()
	if line.endswith(":"):
		currentline = lines[line[:-1]] = []
	elif line:
		currentline.append(line)

played = {}
queue = []
def play(name):
	if name in played:
		return
	played[name] = True
	if name in lines:
		queue.extend([(line, "%sline%d" % (name, j+1)) for j, line in enumerate(lines[name])])
	else:
		print("Missing dialog: %s" % name)

def dump():
	return [played, queue]
def load(obj):
	global played, queue
	played, queue = obj

playing = None
currentline = None
def think(dt):
	global playing, currentline, playingends
	if not sound.lineplaying():
		currentline = None
		if queue:
			currentline, filename = queue.pop(0)
			sound.playline(filename)

style = {
	"A": ("NovaSquare", 38, "white"),
	"B": ("BlackOps", 20, "#AA4444"),
	"E": ("PermanentMarker", 38, "white"),
	"K": ("Exo", 20, "#AAAA77"),
}

def draw():
	if not currentline:
		return
	fontname, fontsize, color = style[currentline[0]]
	ptext.draw(currentline[2:], fontsize = F(fontsize), width = F(640), owidth = 0, shadow = (1, 1),
		left = F(180), bottom = window.sy - F(10), fontname = fontname, color = color)


