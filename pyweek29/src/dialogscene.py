import pygame, math, numpy
from . import scene, pview, ptext, progress, sound
from . import draw as D
from .pview import T

lines = {
	"tutorial1": [
		"Y Another pleasant afternoon.",
		"Y On days like these, I can imagine I'm a butterfly floating on the wind.",
		"V My good lady! How do you do?",
		"Y Oh my, are you a fellow butterfly lover?",
		"V In a manner of speaking. My name is Professor Dame Victoria Winger.",
		"V I am the Chair of the Department of Mothematics at Eldbridge University.",
		"Y Goodness me! I'm Miranda Flutterbie. A pleasure to make your acquaintance!",
		"V Would you permit me to observe for a few moments?",
		"Y Certainly! It'll be good to have some company!",
	],
	"tutorial3": [
		"V Incredible movement! Just as I suspected!",
		"V Miranda, have you ever heard of the Butterfly Effect?",
		"Y I'm afraid not. Should I have?",
		"V It's a theory of lepidoptery that I've been studying for years,",
		"V but sadly, nobody has ever found any proof it actually exists.",
		"V Watching you play that last level, however, I'm convinced it's real!",
	],
	"tutorial3-post": [
		"Y So just what is this 'Butterfly Effect', Victoria?",
		"V I'll explain everything, but please come with me to the Ministry of Insects.",
		"V They must be informed of this!",
	],
	"tutorial4": [
		"rV Minister Buzzworthy!",
		"B Ah, Professor! What brings you to the Ministry of Insects?",
		"rV I finally have proof of The Butterfly Effect!",
		"B Heavens... after all this time.... Are you absolutely sure?",
		"rV Just watch this! Miranda, show him what you can do!",
	],
	"tutorial4-post": [
		"B Astounding! Yes, it must be the Butterfly Effect after all!",
		"B Of course you must begin the tracking down the Lines immediately.",
		"rV An expedition? Miranda, what do you think?",
		"Y Sure, I could do a few more levels.",
		"Y But how will we pay for an expedition?",
		"B The Ministry will provide everything you need! In fact I have just the man for your attaché.",
		"E Leftenant Elmer Wrightscoptch of the Royal Airship Battalion, at your service.",
		"Y Then it's settled!",
	],


	"A0": [
		"rV What brought you to the Ministry of Insects, Leftenant?",
		"E I was recently stationed on the good ship Argus, an airship in the Royal Sky Force.",
		"E En route back to Albion our engines died.",
		"E We were stranded in the middle of the ocean for days!",
		"E We surely would have perished when a miracle occurred!",
	],
	"A1": [
		"Y Don't leave us hanging, Elmer! What was the miracle that saved your doomed ship?",
		"E A great flock of butterflies! Larger than the largest stormcloud!",
		"rV The transcontinental migration! Incredible! What a sight that must have been!",
		"E The Argus was swept away like a leaf on the wind!",
		"E Within one day we were back on terra firma.",
	],
	"A2": [
		"Y So that's when you came to the Ministry of Insects?",
		"E Yes. Imagine the military applications if we could map the migrations.",
		"E Entire fleets could be carried across the ocean!",
		"Y That's what this is about for you? Transportation?",
		"E At first, yes. But having spent these days on the road with you, I'm starting to consider myself a lepidopterist as well!",
		"Y There's hope for you yet!",
	],

	"C0": [
		"E When did you first feel such a deep connection to butterflies, Miranda?",
		"Y As long as I can remember! I don't even notice it.",
		"Y In fact I only ever really notice it when they're gone.",
		"Y I once toured Borealis Island.",
		"E Ah, such a beautiful but desolate place.",
		"V No butterflies on the entire island.",
		"Y Yes. I could feel their absence. It was uncomfortable, like wearing ill-fitting clothes.",
		"E Or leaving the house without waxing your moustache!",
		"Y ... Sure...."
	],
	"C1": [
		"V Would it interest you to know that butterfly fossils have been found on Borealis Island?",
		"V Three millennia ago they all mysteriously vanished!",
		"E Perhaps they'll return one day!",
		"Y I don't know why, but I had a very bad feeling when you said that.",
	],


	"D0": [
		"Y Are you ready to tell me about the Butterfly Effect, Victoria?",
		"V Of course! How could I forget!",
		"V Throughout the countryside run invisible channels of supernatural energy known as Meadow Lines.",
		"V Their source and ultimate potential remain a mystery.",
		"V But I believe butterflies possess a sixth sense. They read the Meadow Lines.",
		"V By studying them we may unlock their potential!",
	],
	"D1": [
		"V I believe that as the Butterfly Effect ties butterflies to the Meadow Lines,",
		"V so too it ties you to the butterflies.",
		"V You can feel it, can't you? The butterflies guide you, showing you which way to go to catch the air currents.",
		"Y Yes, you could say that. It looks like arrows hanging in the air. And the orange ones are double arrows.",
		"Y Oh, and there's a map to the right, and everything fades to white when I've finished.",
		"V Fascinating! I must take notes.",
	],
	"D2": [
		"Y So wait, the Butterfly Effect doesn't have anything to do with chaos theory or the weather?",
		"V No, that won't be discovered until next century.",
		"V In this universe I'm calling dibs on the name first!",
	],


	"cpoint1": [
		"V Excellent data! It looks like the Line is leading to Nexus Point!",
		"Y I can see some butterflies flying off in that direction!",
	],
	"cpoint2": [
		"V Another Meadow Line mapped! This one also leads to Nexus Point!",
	],
	"cpoint3": [
		"V Another Meadow Line mapped! This one leads to....",
		"Y Let me guess. Nexus Point?",
		"V Hey, who's the mothematician here?!",
	],

	"nexus0": [
		"V There's a convergence of Meadow Lines here.",
		"Y Then why are there so few butterflies?",
		"V Perhaps there will be more later.",
	],
	"nexus1": [
		"V According to my calculations, we still need more butterflies to complete this stage.",
	],
	"nexus2": [
		"V According to my calculations, we just need a few more butterflies to complete this stage.",
	],
	"nexus3": [
		"V Looks like the butterflies we've found in our travels have congregated here.",
		"Y Does that mean I can finally beat this level now?",
		"V Yep. Go for it.",
	],

	"nexus-post": [
		"E Victoria! Miranda! I must confess something terrible!",
		"rV You're the one who pilfered my crumpets!",
		"Y Actually, that was me.",
		"E It's not about crumpets!",
		"E (Although if there are any left I wouldn't refuse....)",
		"E No, I was given a secret mission to spy on you, by the Minister of Insects!",
		"Y You lied to us!",
		"E Only by omission! The migration, my newfound love of butterflies. That much is true!",
		"E The Minister directed me to report all your findings to him!",
		"E He means to use the information to lure all the butterflies in Albion into a trap!",
		"Y A trap? No, it can't be!",
		"rV Leftenant, how could you?",
		"E It sounded so harmless! I thought he was just eccentric! How could butterflies hold such power?",
		"E I now see the error of my ways.... There is more to lepidoptery than I ever dreamed!",
		"rV We can't let it happen. I think I know where he might be headed. But we'll need some transportation.",
		"E We'll take the Argus! Come with me!",
	],

	"finale0": [
		"rV Can't this thing go any faster?",
		"E We may have bigger trouble. There's a stormcloud right behind us, and it's gaining.",
		"rV Did you say... a stormcloud?",
		"Y ....",
		"E ....",
		"Y .... That's no cloud.",
		"rV Bless my proboscis, it's every butterfly in Albion!",
		"Y They're flying into the trap!",
		"E STEAM POWER TO MAXIMUM!!!",
		"E Oh no...",
		"E The boiler's exploded! We're going down! Brace for impact!",
		"Xcrash",
		"Y Is everyone all right?",
		"V Well I for one am never getting in an airship again!",
		"B How nice of you all to drop in. Ah, and I see the first of the butterflies are arriving.",
		"Y Minister! Why are you doing this?!",
		"B It's quite simple, child.",
		"B I. Hate. Butterflies!",
		"Y Then why are you Minister of Insects?",
		"B To put an end to the reign of the butterfly once and for all!",
		"B Once they're gone, then all of Albion will recognise the true crown jewel of the insect kingdom:",
		"B Bumblebees!",
		"Y Not if we have anything to say about it!",
		"B Have at you!",
	],

	"finale0-post": [
		"B The colours... the motion... so hypnotic... I can't....",
		"Y Now, Elmer!",
		"rE Minister Buzzworthy, I'm placing you under arrest, for crimes against lepidoptery!",
		"B Curse you all! You may have me, but look! The butterflies are still flapping off to their doom!",
		"V He's right! Oh, we have to do something!",
		"E You two go ahead. I'll take him away.",
		"E Victoria, Miranda.... I'm sorry. And thank you for showing me the way of the butterfly.",
		"V Come on, Miranda. We have a disaster to stop.",
		"rE Was it worth it, Minister?",
		"B The likes of you could never comprehend my devotion to bumblebees.",
		"rE Any last words?",
		"B Long live the Queen.",
	],

	"finale1": [
		"Y I've been here before. This place was an observatory, abandoned three thousand years ago.",
		"V Right when the butterflies left. What will happen when they return?",
		"V All the Meadow Lines come together at this point.",
		"V This is where the Butterfly Effect has led us.",
	],
	"finale1-post": [
		"Y Yes! I can see the Lines! They extend from this moment through time and space!",
		"Y Not only can I see them, I can touch them, bend them.",
		"Y I can send the butterflies back and save them....",
		"Y I just need to....",
		"Xcrash",
		"Y W...what happened!",
		"V Miranda, you did it! They're leaving! It's going to be all right!",
		"Y Victoria, I saw it! The Butterfly Effect. It was incredible!",
		"V I've got time to hear all about it. I'm afraid we're stranded here.",
		"E Friends! The Argus repairs are complete. We're ready to board! Unless you'd rather walk, Victoria.",
		"V I suppose I can give it one more chance.",
		"V What do you say, Miranda, ready to follow the flock back home?",
		"Y Good idea. I have a son back at home I should probably check on.",
		"E I hope he hasn't gotten into too much trouble while you were away!",
		"Y Mortimer? Ha! He's not exactly the adventurous type.",
	],
}


class self:
	pass


def init(track):
	self.track = track
	self.jline = -1
	self.t = 0
	self.tline = 0
	self.a = 0
	self.switching = True
	self.ready = False
	
	if track == "nexus":
		n = sum(stage in progress.beaten for stage in ("A2", "C2", "D2"))
		track = "nexus%d" % n
	elif track in ("A2-post", "C2-post", "D2-post"):
		n = sum(stage in progress.beaten for stage in ("A2", "C2", "D2"))
		track = "cpoint%d" % n

	if track in lines and track not in progress.dseen:
		self.lines = list(lines[track])
		progress.dseen.add(track)
		for who in "YEVB":
			for rev in [False, True]:
				drawwho(who, -1, 1, rev)
	else:
		scene.pop()
		self.lines = []

def control(keys):
	if "act" in keys and not self.switching:
		self.switching = True
		self.ready = False
	if "forfeit" in keys:
		self.jline = len(self.lines)
		scene.pop()

def think(dt):
	if not self.switching:
		D.killtime(0.02)
	if self.ready:
		self.t += dt
	if self.switching:
		self.tline = 0
		self.a = math.approach(self.a, 1, 3.5 * dt)
		if self.a == 1:
			self.switching = False
			self.a = 0
			self.jline += 1
			if self.jline == len(self.lines):
				scene.pop()
			if self.jline < len(self.lines) and self.lines[self.jline] == "Xcrash":
				sound.play("crash")
	else:
		self.tline += dt
	if not self.switching and 0 <= self.jline < len(self.lines):
		t = 1 + 0.08 * len(self.lines[self.jline])
		if self.lines[self.jline] == "Xcrash":
			t = 3
		if self.tline > t:
			self.switching = True
			self.ready = False

def layout(jline):
	if not 0 <= jline < len(self.lines):
		color = 0, 0, 0
		line = None
		who = None
		dpos = 0
		rev = False
	else:
		who, _, line = self.lines[jline].partition(" ")
		rev = who.startswith("r")
		dpos = -1 if who == "Y" else 1
		if who.startswith("X"):
			who = None
			dpos = 0
		if rev:
			who = who[1:]
		color = {
			"Y": (0, 255, 255),
			"E": (255, 200, 100),
			"V": (255, 0, 255),
			"B": (240, 200, 160),
			None: (128, 128, 128),
		}[who]
	if rev:
		dpos = -dpos
	return line, who, dpos, color, rev

def drawback(color, dpos):
	w, h = pview.size
	w //= 8
	h //= 8
	xs = numpy.arange(float(w)).reshape([w, 1, 1]) / w - 0.5
	ys = numpy.arange(float(h)).reshape([1, h, 1]) / h - 0.5
	ys = ys / (1.0 - 1.4 * dpos * xs)
	t = 0.001 * pygame.time.get_ticks()
	f = 0.25 + sum([
		0.06 * numpy.sin(20 * ys + 4 * t),
		0.05 * numpy.sin(30 * ys - 7 * t),
		0.04 * numpy.sin(43 * ys - 10 * t),
		0.03 * numpy.sin(55 * ys + 13 * t),
	])
	img = pygame.Surface((w, h)).convert()
	img.fill(color)
	arr = pygame.surfarray.pixels3d(img)
	arr[:,:,:] = (arr * f).astype(arr.dtype)
	del arr
	pview.screen.blit(pygame.transform.smoothscale(img, pview.size), (0, 0))
	
def drawwho(who, dpos, a, rev):
	if who == "Y":
		x = 640 + dpos * (400 + 600 * a)
		D.drawimg("you", T(x, 400), T(1400), flip = rev)
	elif who == "E":
		x = 640 + dpos * (360 + 600 * a)
		D.drawimg("elmer", T(x, 400), T(1600), flip = rev)
	elif who == "V":
		x = 640 + dpos * (360 + 600 * a)
		D.drawimg("victoria", T(x, 400), T(1400), flip = rev)
	elif who == "B":
		x = 640 + dpos * (360 + 600 * a)
		D.drawimg("minister", T(x, 400), T(1400), flip = rev)
	

def drawline(line, who, color, dpos, a):
	fontname = {
		"Y": "SpicyRice",
		"E": "ChangaOne",
		"V": "CarterOne",
		"B": "Simonetta",
	}[who]
	lineheight = 0.8 if fontname == "CarterOne" else 1
	ptext.draw(line, midbottom = T(640 + (100 + 1200 * a) * dpos, 660), width = T(960),
		color = color, shade = 1, shadow = (1, 1.3), owidth = 0.25,
		fontsize = T(60), fontname = fontname,
		lineheight = lineheight)

def draw():
	self.ready = True
	line, who, dpos, color, rev = layout(self.jline)
	if not self.switching:
		drawback(color, dpos)
		if who:
			drawwho(who, dpos, 0, rev)
		if line:
			drawline(line, who, color, dpos, 0)
	else:
		line1, who1, dpos1, color1, rev1 = layout(self.jline + 1)
		acolor = math.imix(color, color1, self.a)
		drawback(acolor, math.mix(dpos, dpos1, self.a))
		if who and who1 and who == who1:
			drawwho(who, dpos, 0, rev)
		else:
			if who:
				drawwho(who, dpos, self.a, rev)
			if who1:
				drawwho(who1, dpos1, 1 - self.a, rev1)
		if line:
			drawline(line, who, color, dpos, self.a)
		if line1:
			drawline(line1, who1, color1, dpos1, 1 - self.a)
	ptext.draw("Space: next   Backspace: skip", fontname = "ChangaOne", color = (255, 220, 200),
		fontsize = T(22), bottomright = T(1270, 710),  shade = 1, owidth = 0.5, shadow = (1, 1))


