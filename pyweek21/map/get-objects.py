import pygame, random

data = {
	"b": [],
	"you": {},
	"p": [],  # objective P
	"q": [],  # objective Q
	"r": [],  # objective R
	"s": [],  # objective S
	"dec": [],  # decorations
	"smoke": [],
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

		if color == (0, 255, 255):
			data["b"].append([px, py, [0, 1], 1])
		if color == (100, 255, 255):
			data["b"].append([px, py, [0, 1], 10])

		if color == (0, 255, 0):
			data["b"].append([px, py, [0, 1, 2], 1])
		if color == (100, 255, 100):
			data["b"].append([px, py, [0, 1, 2], 10])

		if color == (255, 0, 255):
			data["you"]["a"] = px, py
		if color == (0, 100, 255):
			data["you"]["b"] = px, py
		if color == (255, 0, 100):
			data["you"]["c"] = px, py
		if color == (100, 255, 0):
			data["you"]["d"] = px, py
		if color == (255, 100, 0):
			data["you"]["e"] = px, py
		if color == (100, 0, 255):
			data["you"]["f"] = px, py

		if color == (0, 100, 100):
			data["p"].append((px, py))
		if color == (100, 100, 0):
			data["q"].append((px, py))
		if color == (0, 120, 120):
			data["r"].append((px, py))
		if color == (0, 140, 140):
			data["s"].append((px, py))
		if color == (255, 255, 255):
			data["x"] = px, py


elevation = open("data/elevation.data", "rb").read()

nsmoke = 100
ndec = 400
objs = set()
objs |= set((x, y) for x, y in data["you"].values())
objs |= set(tuple(p) for a in "pqrs" for p in data[a])
objs |= set([data["x"]])
objs |= set((x, y) for x, y, _, _ in data["b"])
while len(data["dec"]) < ndec:
	x, y = random.randint(0, 2047), random.randint(0, 2047)
	c = ord(elevation[y + x * 2048])
	if c < 10:
		continue
	x -= 1024
	y = 1024 - y
	if any((obj[0] - x) ** 2 + (obj[1] - y) ** 2 < 40 ** 2 for obj in objs):
		continue
	if any((data["x"][0] - x) ** 2 + (data["x"][1] - y) ** 2 < 100 ** 2 for obj in objs):
		continue
	data["dec"].append((x, y))
	objs.add((x, y))
while len(data["smoke"]) < nsmoke:
	x, y = random.randint(0, 2047), random.randint(0, 2047)
	c = ord(elevation[y + x * 2048])
	if c < 10:
		continue
	x -= 1024
	y = 1024 - y
	if any((obj[0] - x) ** 2 + (obj[1] - y) ** 2 < 40 ** 2 for obj in objs):
		continue
	if any((data["x"][0] - x) ** 2 + (data["x"][1] - y) ** 2 < 100 ** 2 for obj in objs):
		continue
	data["smoke"].append((x, y))
	objs.add((x, y))

import json
json.dump(data, open("../data/gamedata.json", "w"))

