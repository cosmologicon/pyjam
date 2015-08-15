import pygame, os.path
from src import ptext, window, sound
from src.window import F

lines = {}
for line in open(os.path.join("data", "dialog.txt")):
	line = line.strip()
	if line.endswith(":"):
		currentline = lines[line[:-1]] = []
	else:
		currentline.append(line)

played = {}
queue = []
def play(name):
	if name in played:
		return
	played[name] = True
#	queue.extend(lines[name])
	queue.append("K dialogue: " + name)

def dump():
	return [played, queue]
def load(obj):
	global played, queue
	played, queue = obj

playing = None
playingends = 0
currentline = None
def think(dt):
	global playing, currentline, playingends
	if playing is None or playingends < pygame.time.get_ticks():
		currentline = None
		if queue:
			currentline = queue.pop(0)
			t = 0.5 + len(currentline) * 0.05
			playing = sound.playstatic(t)
			playingends = pygame.time.get_ticks() + 1000 * playing.get_length()

style = {
	"A": ("NovaSquare", 38, "white"),
	"B": ("BlackOps", 38, "white"),
	"E": ("PermanentMarker", 38, "white"),
	"K": ("Exo", 38, "white"),
}

def draw():
	if not currentline:
		return
	fontname, fontsize, color = style[currentline[0]]
	ptext.draw(currentline[2:], fontsize = F(fontsize), width = F(500), owidth = 0, shadow = (1, 1),
		centerx = window.sx / 2, bottom = window.sy - F(20), fontname = fontname, color = color)


