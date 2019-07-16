from __future__ import division
import pygame, random
import settings, vista, img
from settings import F

def offset(edge, p0 = (0, 0)):
	x0, y0 = p0
	return x0 + [0, -1, 0, 1][edge], y0 + [1, 0, -1, 0][edge]

def clamp(x, a, b):
	return a if x < a else b if x > b else x
		
class Part(object):
	ismodule = True
	color = 100, 100, 100
	def __init__(self, name, blocks, inputs, outputs):
		self.name = name
		self.blocks = list(blocks)
		xs, ys = zip(*blocks)
		self.center = (max(xs) + min(xs) + 1) / 2, (max(ys) + min(ys) + 1) / 2
		self.inputs = list(inputs)
		self.outputs = list(outputs)
		self.color = random.randint(100, 200), random.randint(100, 200), random.randint(100, 200)
		self.dull = tuple(c // 2 for c in self.color)

	def shift(self, (dx, dy)):
		blocks = [(x + dx, y + dy) for x, y in self.blocks]
		inputs = [(x0 + dx, y0 + dy, x1 + dx, y1 + dy) for x0, y0, x1, y1 in self.inputs]
		outputs = [(x0 + dx, y0 + dy, x1 + dx, y1 + dy) for x0, y0, x1, y1 in self.outputs]
		p = Part(self.name, blocks, inputs, outputs)
		return p

	def nearest(self, (x, y)):
		xs, ys = zip(*self.blocks)
		xmin, xmax = -min(xs), settings.shipw - max(xs) - 1
		ymin, ymax = -min(ys), settings.shiph - max(ys) - 1
		dx = clamp(int(round(x - self.center[0])), xmin, xmax)
		dy = clamp(int(round(y - self.center[1])), ymin, ymax)
		return self.shift((dx, dy))

	def draw(self, screenpos0, blocksize, bad = False, on = True):
		x0, y0 = screenpos0
		d = int(blocksize * 0.03)
		for x, y in self.blocks:
			px = x0 + blocksize * x + d
			py = y0 + blocksize * y + d
			rect = px, py, blocksize - 2 * d, blocksize - 2 * d
			color = (100, 0, 0) if bad else self.color if on else self.dull
			vista.screen.fill(color, rect)
		for ix0, iy0, ix1, iy1 in self.inputs:
			dx, dy = ix1 - ix0, iy1 - iy0
			rot = {
				(0, 1): 180,
				(1, 0): -90,
				(0, -1): 0,
				(-1, 0): 90,
			}[(dx, dy)]
			pos = int(x0 + (ix1 + 0.5) * blocksize), int(y0 + (iy1 + 0.5) * blocksize)
			img.draw("outflow", pos, scale = blocksize / 64, angle = rot)

		px = int(x0 + blocksize * self.center[0])
		py = int(y0 + blocksize * self.center[1])
		img.drawtext(self.name, 14, center = (px, py))

	def drawoutline(self, screenpos0, blocksize):
		x0, y0 = screenpos0
		px = int(x0 + blocksize * self.center[0])
		py = int(y0 + blocksize * self.center[1])
		pygame.draw.circle(vista.screen, (255, 0, 255), (px, py), int(1.3 * blocksize), F(2))

	def contains(self, (x, y)):
		return (int(x), int(y)) in self.blocks

class Conduit(Part):
	ismodule = False
	def __init__(self, oedges, rot = 0, p0 = (0, 0)):
		self.p0 = p0
		self.oedges = oedges
		self.rot = rot
		name = "conduit-%s" % ("".join(map(str, oedges)))
		blocks = [p0]
		inputs = [offset(rot, p0) + p0]
		outputs = [p0 + offset((rot + oedge) % 4, p0) for oedge in oedges]
		Part.__init__(self, name, blocks, inputs, outputs)

	def draw(self, screenpos0, blocksize, bad = False, on = True):
		x0, y0 = screenpos0
		x0 += (self.p0[0] + 0.5) * blocksize
		y0 += (self.p0[1] + 0.5) * blocksize
		img.draw(self.name, (x0, y0), scale = blocksize / 64, angle = -90 * self.rot, bad = bad)

	def shift(self, (dx, dy)):
		dx0, dy0 = self.p0
		return Conduit(self.oedges, self.rot, (dx + dx0, dy + dy0))

	def rotate(self, n = 1):
		return Conduit(self.oedges, (self.rot + n) % 4)

def Module(modulename):
	return Part(modulename, settings.moduleblocks[modulename], settings.moduleinputs[modulename], [])



