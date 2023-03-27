
class Obstacle:
	def __init__(self, pH):
		self.pH = pH

class Light:
	def __init__(self, pH, dirHs):
		self.pH = pH
		self.dirHs = dirHs

	def monitored(self, cells):
		hitcells = []
		for dxH, dyH in self.dirHs:
			xH, yH = self.pH
			while True:
				xH, yH = xH + dxH, yH + dyH
				if xH, yH not in cells:
					break
				hitcells.append((xH, yH))
		return hitcells


