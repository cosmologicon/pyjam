import math
from . import graphics

you = None
hazards = []
spawners = []
salvos = []

room_rect = -8, -5, 16, 10

def room_bounds():
	x, y, w, h = room_rect
	return (x, x + w), (y, y + h)


def draw_room():
	x, y, w, h = room_rect
	graphics.drawrectG((x, y), (w, h), (0, 60, 60))

def constrain_to_room(pos, r = 0):
	x, y = pos
	(x0, x1), (y0, y1) = room_bounds()
	return math.clamp(x, x0 + r, x1 - r), math.clamp(y, y0 + r, y1 - r)



	
	

