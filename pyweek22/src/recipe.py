from . import state

def reset(self):
	self.lastshot = self.t

def think(self, dt):
	from . import thing
	flavors = [obj.flavor for obj in self.slots]
	if flavors.count(0) == 2:
		if self.lastshot + 0.5 < self.t:
			for obj in state.shootables:
				dx = obj.x - self.x
				dy = obj.y - self.y
				if dx ** 2 + dy ** 2 < 30 ** 2:
					obj.shoot(1)
					thing.Laser(self, obj).addtostate()
					self.lastshot = self.t
					break

