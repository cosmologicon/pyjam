import math, pygame
from . import pview, ptext
from .lru_cache import lru_cache
from .pview import T

# How long to show a line of dialog by default.
def tline(line):
	return 0.3 + 0.05 * len(line)

@lru_cache(1000)
def whoimg(who, size):
	if size is not None:
		return pygame.transform.smoothscale(whoimg(who, None), (size, size))
	return pygame.image.load("img/%s.png" % who)
	

class Dialog:
	def __init__(self):
		self.current = None
		self.currenthelp = ""
		self.t = 0
		self.convolines = []
		self.tconvo = 0
		self.cclicked = False
	def run(self, line):
		# TODO: allow for different colors and fonts
		self.current = line
		self.t = 0
	def helptext(self, line):
		self.currenthelp = line
	def startconvo(self, convoname):
		self.cclicked = False
		self.convolines.extend(convos[convoname])
	def think(self, dt):
		if self.convolines:
			self.tconvo += dt
			if self.tconvo >= tline(self.convolines[0]):
				self.tconvo = 0
				self.convolines.pop(0)
		else:
			self.tconvo = 0
			self.t += dt
		if self.current and self.t > tline(self.current) * 2:
			self.current = None
	def draw(self):
		if self.convolines:
			pview.fill((10, 10, 10, 120))
			line = self.convolines[0]
			alpha = math.dsmoothfade(self.tconvo, 0, tline(line), 0.3)
			who = line[:line.index(":")]
			line = line[line.index(":") + 2:]
			ptext.draw(line, bottomleft = T(400, 720), width = T(640), fontsize = T(44),
				color = (100, 100, 255), owidth = 2, alpha = alpha, fontname = "Teko-SemiBold", lineheight = 0.7)
			surf = whoimg(who, T(300))
			pview.screen.blit(surf, surf.get_rect(center = T(300, 660)))
		else:
			if self.current is not None:
				alpha = math.dsmoothfade(self.t, 0, tline(self.current), 0.3)
				ptext.draw(self.current, midtop = pview.midtop, width = T(720), fontsize = T(50),
					color = "red", owidth = 1, alpha = alpha, fontname = "Teko-SemiBold")
			if self.currenthelp:
				ptext.draw(self.currenthelp, midtop = T(640, 200), width = T(720), fontsize = T(50),
					color = "lightblue", owidth = 1, fontname = "Teko-SemiBold")
			

dialog = Dialog()

# Module-level functions for shorthand
def run(line):
	dialog.run(line)
def think(dt):
	dialog.think(dt)
def draw():
	dialog.draw()
def helptext(line = ""):
	dialog.helptext(line)
def startconvo(convoname):
	dialog.startconvo(convoname)
def clickthrough():
	if not dialog.convolines:
		return
	if dialog.cclicked or dialog.tconvo > 0.3:
		dialog.cclicked = True
		dialog.convolines.pop(0)
	
		


convos = {
	"test": [
		"Herzud: This stupid thing cost 200 billion zoltons!",
		"Dorgaz: You hear that, Nerdozog? If you can't get it to work, it's coming out of your paycheck!",
		"Nerdozog: Geez, bite my head off why don't you?!",
		"Dorgaz: Believe me, I've considered it....",
		"Dorgaz: BUT YOU'RE ALL HEAD!",
		"Alitwon: Let me help you before you hurt yourself.",
	],
	"intro": [
		"Dorgaz: So, you're the sucker they sent me to get this thing operational, huh?",
		"Nerdozog: Nerdozog, reporting for duty!",
		"Dorgaz: Is this your first time working on a space elevator, Nerdz?",
		"Nerdozog: Wh... uh... this is the first space elevator in the world!",
		"Dorgaz: Ugh, I asked for someone with 10 moltons' experience in space elevators! You'll have to do!",
	],
	"chat1": [
		"Herzud: How runs my little space elevator today, Dorgaz?",
		"Dorgaz: Dr. Herzud, there was no need to come down here yourself. Everything is going perfectly smoothly, I assure you.",
		"Nerdozog: Aaaahhhh!!! I stuck my head out the window and a space bug got in my eye!!!",
		"Herzud: Hmmm.... Perhaps I will be taking closer look at operation.",
		"Dorgaz: Nerdozog, I swear to Glorg...",
	],
	"chat2": [
		"Alitwon: You have to stand up for yourself, you know.",
		"Nerdozog: You must not have met me. I'm Nerdozog.",
		"Alitwon: Alitwon. And I've had my eye on you. You've got potential.",
		"Alitwon: See this project through and I see big things for you in the future.",
		"Nerdozog: I think you must have me confused with some other Nerdozog.",
	],
	"chat3": [
		"Dorgaz: Hey Nerdz, I forgot my Slurmee in Skyburg. If you stop by there, pick it up for me, will ya?",
		"Nerdozog: Your Slurmee? Oh... well... I guess it's not too far out of my way....",
		"Dorgaz: It's an extra large zargleberry flavor. I spilled most of it on the window. You can't miss it.",
		"Alitwon: Don't you think he has more important work to do?",
	],
	"chat4": [
		"Herzud: Ha ha! From the ground we go up, up, up, and up!",
		"Herzud: Ten thousand krelmars above Xenophoton! What fun!",
		"Herzud: Oooh, I can see some of my houses from here.",
	],
	"chat5": [
		"Nerdozog: Dr. Herzud, are you really the one who came up with the Fermi Paradox?",
		"Herzud: Idea that statistically speaking, aliens must be existing?",
		"Herzud: Why yes! In fact that's the very reason I have sunk my fortune into building the space elevator!",
		"Nerdozog: Oh.... well then why isn't it called the Herzud Paradox?",
		"Herzud: ....                  ",
		"Alitwon: That's a sensitive subject, Nerdozog.",
	],
	"chat6": [
		"Alitwon: Keep those missions coming, Nerd-O!",
		"Alitwon: And make it quick! There's increased gamma ray activity.",
		"Herzud: According to calculation, if we fail to leave planet in next 16 millieons, we will be destined for oblivion!",
		"Alitwon: We need your help Nerd-O, it looks like you're the only one who can save us now.",
		"Nerdozog: No pressure, I guess...",
	],
	"chat7": [
		"Alitwon: Just a few more missions and we can launch the first spaceships!",
		"Nerdozog: Is this a bad time to mention I'm afraid of heights???",
	],
	"end": [
		"Herzud: Looks like our ships are ready to set sail, and sail it will be.",
		"Herzud: The scientists have told me that with just a little bit of solar current it turns out that we won't need any source of fuel here at all.",
		"Dorgaz: Yup, I hate to say it, but you are the hero of the day.",
		"Alitwon: I know it seems like lightyears away, but we are going to send a crew over to Alphazion 35 for a inter-galactic recruitment trip.",
		"Herzud: Alphazion 35? Isn't that the home of the hu-mons? Those guys are so weird looking!",
		"Alitwon: Agreed, but it actually looks like this could turn into a big business venture for us across the galaxy.",
		"Alitwon: Nerdozog, can you lead the way on this one?",
		"Nerdozog: Since you asked, certainly.",
		"Nerdozog: Captain Nerdozog.... I like the sound of that!",
		"Alitwon: The end! Thank you for playing!",
	],
}




