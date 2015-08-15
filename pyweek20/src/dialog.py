import pygame, os.path
from src import ptext, window, sound, image
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
			volume = 0.25 if currentline[0] == "C" else 0.25 if currentline[0] == "A" else 1
			sound.playline(filename, volume = volume)

style = {
	"A": ("NovaSquare", 20, "#77AAAA"),
	"B": ("BlackOps", 20, "#AA4444"),
	"E": ("PermanentMarker", 38, "white"),
	"K": ("Exo", 20, "#AAAA77"),
	"C": ("BlackOps", 20, "#AA4444"),
}

def draw():
	if not currentline:
		return
	if currentline[0] == "E" or currentline[0] == "C":
		return
	fontname, fontsize, color = style[currentline[0]]
	ptext.draw(currentline[2:], fontsize = F(fontsize), width = F(640), owidth = 0, shadow = (1, 1),
		left = F(180), bottom = window.sy - F(10), fontname = fontname, color = color)
	img = image.get("avatar-" + currentline[0] + ".bmp", s = F(150))
	window.screen.blit(img, img.get_rect(center = F(90, 390)))


