from . import state, view, pview, settings, ptext

scenes = []
def push(s):
	scenes.append(s)
	s.init()
def top():
	return scenes[-1] if scenes else None

class Play(object):
	def init(self):
		state.load()
		self.player = "X"
	def think(self, dt, control):
		self.pointedG = view.GnearesttileV(control.mposV)
		if control.down:
			if state.canmoveto(self.player, self.pointedG):
				state.moveto(self.player, self.pointedG)
		for piece in state.getpieces():
			piece.think(dt)
	def draw(self):
		pview.fill((0, 50, 120))
		ptext.draw(settings.gamename, center = pview.T(400, 100), color = "white", shade = 2,
			scolor = "black", shadow = (1, 1), angle = 10,
			fontsize = pview.T(120))
		for color, pG in state.gettiles():
			if pG == self.pointedG and state.canmoveto(self.player, self.pointedG):
				color = "white"
			view.drawtile(color, pG)
		for piece in state.getpieces():
			piece.draw()
play = Play()

