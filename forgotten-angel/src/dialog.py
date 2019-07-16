from __future__ import division
import pygame
import settings, img, vista, state
from settings import F

avatarscale = F(80) / 256
textsize = F(24)

names = {
	"V": "Lieutenant Valdis",
	"B": "Baroness von Sussmeyer",
}

colors = {
	"V": (0, 255, 0),
	"B": (255, 128, 0),
}
fonts = {
	"V": "jockey",
	"B": "oleo",
}



def duration(line):
	return 1 + 0.05 * len(line)

def pause():
	pass

def resume():
	pass

def think(dt):
	if not state.state.playing:
		return
	who, _, line = state.state.playing[0].partition(": ")
	state.state.tline += dt
	if state.state.tline > duration(line):
		advance()

def advance():
	state.state.tline = 0
	del state.state.playing[0]

def draw():
	if not state.state.playing:
		return
	who, _, line = state.state.playing[0].partition(": ")
	imgname = "avatar%s" % who
	ipos = F(50, 480 - 50)
	img.draw(imgname, ipos, scale = avatarscale)
	pos = F(100, 480 - 90)
	img.drawtext(line + "\n ", fontname = fonts[who], fontsize = textsize, topleft = pos, maxwidth = F(480))
	pos = F(100, 480 - 95)
	img.drawtext(names[who] + "\n ", fontname = fonts[who], fontsize = textsize, color = colors[who], midleft = pos)

	rect = pygame.Rect(F(0, 0, 80, 80))
	rect.center = ipos
	pygame.draw.rect(vista.screen, colors[who], rect, F(2))

def playfirst(dname):
	if dname in state.state.played:
		return
	play(dname)

def play(dname):
	state.state.played.add(dname)
	if dname in lines:
		state.state.playing.extend(lines[dname])
	else:
		print "playing %s" % dname

def clear(dname):
	pass

lines = {
	"cometomother": [
		"V: You may have heard that the Sector of the Nine Angels was saved from certain doom by a single brave soul in a tiny, one-room capsule.",
		"V: Well... I was there at the Great Collapse... and there was a little more to the story....",
		"V: This is a distress call from Lieutenant Valdis of the Exelu, to anyone who can hear me. We've suffered heavy casualties.",
		"V: Our engines are completely destroyed. We're dead in space. You'll have to come to the Exelu. I'm uploading the coordinates to your navcom.",
		"V: Activate your engine by clicking on its icon. Then click on your screen to travel.",
		"V: We're reading a lot of hostile drone activity out there. Keep your distance and be careful.",
	],
	"hookupmodule": [
		"V: Looks like all but one of your power supplies are offline. You'll need to reroute the hookup for your drill module.",
		"V: Use a branching conduit to connect both the drill and the engine to the working supply.",
		"V: I'll be honest: you're in pretty bad shape.",
		"V: But that little one-room ship of yours might be the only spaceworthy thing left in the whole fleet.",
	],
	"howtodrill": [
		"V: You'll only be able to run one module at a time out there...",
		"V: ...but by switching back and forth, you should be able to mine a few asteroids, which will get things going.",
		"V: Move your ship into the path of an asteroid, and then activate your drill module.",
		"V: You'll automatically extract some resources as the asteroid passes by, if the drill is activated.",
		"V: Come back whenever you need repairs, or to save your progress.",
	],
	"buylaser": [
		"V: You've got enough Spacebucks now to build a weapon. I suggest you do so.",
		"V: Taking out drones should get you Spacebucks much faster than picking at asteroids.",
	],
	"cometobaron1": [
		"B: Howdy, suckers! Soldier of fortune, Baronness Svana von Sussmeyer here! You can call me the Baroness.",
		"B: I've come across something you might find interesting... the location of a fleet supply ship.",
		"B: All I ask is 50 Spacebucks. You can meet me at this location.",
	],
	"wheresmymoney": [
		"B: Well? Did you bring the 50 Spacebucks I dema...quested?",
	],
	"findthesupply": [
		"B: Well? Did you bring the 50 Spacebucks I dema...quested?",
		"B: Excellent! I'll add the location of the supply ship to your navcom.",
		"B: Just watch out for the uh... Never mind! Nothing! Have a nice day!",
	],
	"cometobaron2": [
		"B: Come find me! I've got another proposition for you, since it looks like the last one worked out so well.",
		"B: The cost this time is 200 Spacebucks.",
	],
	"wheresmymoney2": [
		"B: How about it? You got those 200 Spacebucks?",
	],
	"findboss2": [
		"B: How about it? You got those 200 Spacebucks?",
		"B: Right on! Hey look, I'm really sorry about the whole mixup last time, what with the whole battleship attacking you.",
		"B: I can almost definitely promise you won't find the exact same thing this time... almost.",
	],
	"cometobaron4": [
		"B: Hey look, I've got one more thing to tell you. No money this time. You can find me in the Oort.",
	],
	"findangel10": [
		"B: I just wanted to let you know, I'm leaving this system. I don't like the way things are going.",
		"B: But before I go, I've noticed you've been snooping around the stars, and there's something I wanted to tell you.",
		"B: There's a tenth Angel.",
		"B: It doesn't show up on any maps, but it's out there.",
		"B: I can't tell you exactly where. All I know is if you look at the Angels on your map, it makes sense.",
		"B: Anyway I'm out of here. You... stay safe, okay?",
	],

	"act2": [
		"V: I admit I was suspicious of this Baroness character, but the supply ship was right where she said,",
		"V: even if she did fail to warn you about the Hamisi cruiser guarding it.",
		"V: Most of the wreckage from the ship is unusable, but the power supply you brought back is intact.",
		"V: You can now have two modules active at once, if they're hooked to different supplies.",
		"V: Just remember that when you activate a module, any modules on the same supply will deactivate.",
	],
	"act3": [
		"V: We must find out why the Angel collapsed.",
		"V: I suggest you focus on surveying the Angels to determine their nature.",
		"V: The locations of all nine Angels has been added to your navcom. I'm certain that there must be something there....",
		"V: You'll need a heat shield as well as a scope.",
	],

	
}


