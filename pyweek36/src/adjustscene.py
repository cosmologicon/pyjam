import pygame, math
from . import pview, ptext, quest, state, graphics, progress, hud, view, settings, sound, thing
from . import scene
from .pview import T

class self:
	pass

def init(oldscene):
	self.oldscene = oldscene
	self.oldvis = pygame.mouse.get_visible()
	pygame.mouse.set_visible(True)
	self.t = 0
	cols = [
		["starsdown", "nebuladown", "objsizedown"],
		["starsup", "nebulaup", "objsizeup"],
	]
	self.buttons = [
		(bname, pygame.Rect(796 + 220 * x, 100 + 50 * y, 70, 40))
		for x, col in enumerate(cols) for y, bname in enumerate(col) if bname is not None
	]
	self.DMs = [
		thing.ExampleDM((-6, 0), 4, j * math.tau / 3)
		for j in range(3)
	]
	view.xG0 = 0
	view.yG0 = 0
	view.VscaleG = 50

def think(dt, kdowns = [], kpressed = [0] * 128, mpos = (0, 0), mdowns = set()):
	self.t += dt
	if self.t > 0.1 and pygame.K_F9 in kdowns:
		pygame.mouse.set_visible(self.oldvis)
		scene.current = self.oldscene
	if 1 in mdowns:
		for bname, rect in self.buttons:
			visible, active, text = bstate(bname)
			if visible and T(rect).collidepoint(mpos):
				if active:
					sound.play("click")
					onclick(bname)
				else:
					sound.play("no")
	for DM in self.DMs:
		DM.think(dt)


def bstate(bname):
	if bname == "starsdown":
		return True, settings.stars > 0, "LESS"
	if bname == "starsup":
		return True, settings.stars < 20, "MORE"
	if bname == "nebuladown":
		return True, settings.nebula > 0, "LESS"
	if bname == "nebulaup":
		return True, settings.nebula < 20, "MORE"
	if bname == "objsizedown":
		return True, settings.objsize > 0, "LESS"
	if bname == "objsizeup":
		return True, settings.objsize < 20, "MORE"
	return False, False, ""
	
def onclick(bname):
	if bname == "starsdown":
		settings.stars -= 1
	if bname == "starsup":
		settings.stars += 1
	if bname == "nebuladown":
		settings.nebula -= 1
	if bname == "nebulaup":
		settings.nebula += 1
	if bname == "objsizedown":
		settings.objsize -= 1
	if bname == "objsizeup":
		settings.objsize += 1
	settings.save()
		

def draw():
	pview.fill((0, 0, 0))
#	view.xG0 = self.t * 0.5
	graphics.drawnebula()
	graphics.drawstars()
	for DM in self.DMs:
		DM.r = (0.05 + 0.4 * (settings.objsize / 10) ** 1.4) * settings.viewscale / 50
		DM.draw()

	text = "\n".join([
		"This game is about locating black objects on a dark background. It's supposed to be challenging, but how difficult this is depends a lot on your monitor and lighting conditions. This screen lets you adjust the background settings to make the game easier or harder. You should be able to barely make out the nebula in the background, and see a few stars wink out here and there as an object passes in front of them. If you can easily see the objects at a glance, it's probably too easy. Ideally it's challenging without being frustrating.",
		"",
		"Press F9 to resume the game.",
	])
	ptext.draw(text, center = T(940, 440), width = T(480), fontsize = T(18),
		shade = 1)
	ptext.draw(f"STARS: {settings.stars}", center = T(940, 120), fontsize = T(20), shade = 1)
	ptext.draw(f"NEBULA: {settings.nebula}", center = T(940, 170), fontsize = T(20), shade = 1)
	ptext.draw(f"OBJSIZE: {settings.objsize}", center = T(940, 220), fontsize = T(20), shade = 1)

	for bname, rect in self.buttons:
		visible, active, text = bstate(bname)
		if visible:
			bcolor = (50, 50, 150) if active else (20, 20, 20)
			pygame.draw.rect(pview.screen, bcolor, T(rect), 0, border_radius = T(8))
			bcolor = math.imix(bcolor, (255, 255, 255), 0.05)
			pygame.draw.rect(pview.screen, bcolor, T(rect), T(6), border_radius = T(8))
			if active:
				bcolor = math.imix(bcolor, (255, 255, 255), 0.5)
			rect = rect.inflate(-T(12), -T(12))
			ptext.drawbox(text, T(rect), color = bcolor, owidth = 0.5)

