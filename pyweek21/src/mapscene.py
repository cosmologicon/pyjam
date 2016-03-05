from . import background, sound, scene


def onpush():
	sound.play("mapup")

def think(dt, estate):
	if estate["map"] or estate["lup"]:
		scene.pop()

def draw():
	background.drawmap()
	

