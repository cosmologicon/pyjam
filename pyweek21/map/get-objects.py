import pygame

data = {
	"b": [],
	"you": {},
	"p": [],  # objective P
}

pygame.display.set_mode((100, 100))
objmap = pygame.image.load("map-objects.png")
mx, my = objmap.get_size()
for x in range(mx):
	for y in range(my):
		color = objmap.get_at((x, y))
		px, py = x - mx // 2, my // 2 - y

		if color == (255, 255, 0):
			data["b"].append([px, py, [0], 1])
		if color == (255, 255, 100):
			data["b"].append([px, py, [0], 10])

		if color == (255, 0, 0):
			data["b"].append([px, py, [1], 1])
		if color == (255, 100, 100):
			data["b"].append([px, py, [1], 10])

		if color == (0, 0, 255):
			data["b"].append([px, py, [2], 1])
		if color == (100, 100, 255):
			data["b"].append([px, py, [2], 10])

		if color == (255, 0, 255):
			data["you"]["a"] = px, py
		if color == (0, 100, 255):
			data["you"]["b"] = px, py

		if color == (0, 100, 100):
			data["p"].append((px, py))
		if color == (255, 255, 255):
			data["x"] = px, py

import json
json.dump(data, open("../data/gamedata.json", "w"))
			
