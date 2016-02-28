import pygame

data = {
	"activated": []
}

pygame.display.set_mode((100, 100))
objmap = pygame.image.load("map-objects.png")
mx, my = objmap.get_size()
for x in range(mx):
	for y in range(my):
		color = objmap.get_at((x, y))
		pos = x - mx // 2, my // 2 - y
		if color == (0, 255, 0):
			data["start"] = pos
		elif color == (0, 127, 0):
			data["activated"].append(pos)

import json
json.dump(data, open("../data/gamedata.json", "w"))
			
