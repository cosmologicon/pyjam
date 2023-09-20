import pygame, json, os.path, math
from collections import defaultdict

path = os.path.join("data", "sector.json")

def dist(p0, p1):
	x0, y0 = p0
	x1, y1 = p1
	return math.hypot(x1 - x0, y1 - y0)

def load():
	global spots, adjs
	data = json.load(open(path))
	spots = [tuple(spot) for spot in data["spots"]]
	adjs = { tuple(spot): [tuple(sadj) for sadj in sadjs] for spot, sadjs in data["adjs"] }

home_color = 255, 255, 255
spot_color = 0, 0, 255
SCALE = 20

def parse_image():
	img = pygame.image.load("img/sector.png")
	w, h = img.get_size()
	pixels = defaultdict(list)
	for y in range(h):
		for x in range(w):
			color = tuple(img.get_at((x, y)))[:3]
			if color != (0, 0, 0):
				pixels[color].append((x, y))
	assert len(pixels[home_color]) == 1
	(x0, y0), = pixels[home_color]
	def spos(p):
		x, y = p
		return (x - x0) * SCALE, -(y - y0) * SCALE
	spots = [(0, 0)] + [spos(p) for p in pixels[spot_color]]
	adjs = []
	for spot in spots:
		closest = min(dist(spot, s) for s in spots if s != spot)
		sadjs = [spot1 for spot1 in spots if spot1 != spot and dist(spot, spot1) < 2 * closest]
		adjs.append((spot, sadjs))
	sector_data = {
		"spots": spots,
		"adjs": adjs,
	}
	json.dump(sector_data, open(path, "w"))
	

if __name__ == "__main__":
	parse_image()

