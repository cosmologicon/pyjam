from . import pview, ptext, progress, settings
from . import scene, playscene, mapscene, dialogscene
from . import draw as D
from .pview import T

def init():
	pass

def control(keys):
	if "act" in keys:
		if "finale1" in progress.beaten:
			scene.pop()
		else:
			scene.push(mapscene)
			if len(progress.unlocked) == 1:
				scene.push(playscene)
				scene.push(dialogscene, progress.at)

def think(dt):
	D.killtime(0.12)

def draw():
	D.drawimg("title-back", pview.center, pview.size)
	ptext.draw("Miranda the", center = T(640, 230),
		fontname = "CarterOne", fontsize = T(80),
		color = (200, 200, 255), shade = 1, owidth = 0.5, shadow = (0.5, 0.5))
	ptext.draw("Lepidopterist", center = T(640, 360),
		fontname = "Bevan", fontsize = T(160),
		color = (200, 200, 255), shade = 1, owidth = 0.5, shadow = (0.5, 0.5))

	ptext.draw("by Christopher Night", center = T(640, 520),
		fontname = "ChangaOne", fontsize = T(48),
		color = (200, 200, 200), shade = 1, owidth = 0.5, shadow = (0.5, 0.5))
	ptext.draw("music by Kevin MacLeod", center = T(640, 570),
		fontname = "ChangaOne", fontsize = T(32),
		color = (200, 200, 200), shade = 1, owidth = 0.5, shadow = (0.5, 0.5))

	text = "Space: play    F10: toggle fullscreen"
	if not settings.fullscreen:
		text += "     F11: pick resolution [%dp]" % pview.h
	if "finale1" in progress.beaten:
		text = "Thank you for playing"

	ptext.draw(text,
		center = T(640, 690),
		fontname = "ChangaOne", fontsize = T(40),
		color = (200, 200, 200), shade = 1, owidth = 0.5, shadow = (0.5, 0.5))




