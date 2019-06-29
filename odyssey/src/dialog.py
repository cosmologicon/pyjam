from __future__ import print_function

from . import settings, sound, ptext, pview
from .pview import T

# play dialog
def trigger(convo):
	sound.manager.current_dialog = convo
	sound.manager.current_dind = 0
	sound.manager.PlayVoice(convo+'1')

def pause():
	sound.manager.PauseVoice()

def get_current_dialog():
	if sound.manager.current_dialog == None:
		return None
	else:
		return (sound.manager.current_dialog, sound.manager.current_dind+1) # (dialog letter A-B-C, number 1,2,3)

def draw_current_dialog():
	current = get_current_dialog()
	if current is None:
		return
	convo, line = current
	key = "%s%d" % (convo, line)
	if key not in texts:
		return
	who, _, line = texts[key].partition(" ")
	font, color = {
		"P": ("Chicle", "orange"),
		"K": ("Schoolbell", "yellow"),
		"S": ("Creepster", "red"),
		"F": ("Chicle", "yellow"),
	}[who]
	ptext.draw(line, midbottom = T(640, 20), width = T(800), fontsize = T(60),
		color = color, fontname = font,
		owidth = 1, ocolor = "black", shade = 1,
	)

texts = {
	"A1": "P I always wanted to see the world beyond the fishtank...",
	"A2": "K Fishy! No!!!",
	"A3": "P What was I thinking?!",
	"A4": "P What is this place?",
	"A5": "K Fishy! Can you hear me?",
	"A6": "K I'm sorry you got sick, and I'm sorry I....",
	"A7": "P I never thought I'd miss the tank.",
	"A8": "P Looks like I'm on my own now.",
	"A9": "S I wouldn't be so sure about that, little morsel!",
	"A10": "P Who said that?!",
	"A11": "S Hahaha....",
	"A12": "P I've got a bad feeling about this....",

	"B1": "S Looks like dinner is served!",
	"B2": "S Tell me, are you sweet, or savory?",
	"B3": "S Where are you?!",
	"B4": "S Right behind you! Slow down and you'll see!",

	"C1": "P That was close.",
	"C2": "S Catch you later, little morsel.",
	"C3": "P I've got to find a way out of here.",
	"C4": "S All this water has to go somewhere... I hope.",

	"D1": "S Swim, swim, swim!",
	"D2": "S Taste my wake!",

	"E1": "S Look at you go.",
	"E2": "S Not this time!",

	"F1": "S Well, well, well. How nice of you to drop in!",
	"F2": "S And I must say, your timing is perfect -- I'm starving!",
	"F3": "S Hahaha!",
	"F4": "P Yikes! I've got to find a way out of here, and fast!",

	"G1": "S You think you can get away from me? You haven't escaped! There is no escape! I'll still get you! I'll get you!!! I'll...",

	"H1": "F Hey.",
	"H2": "P ...Hello? You're not going to eat me... are you?",
	"H3": "F Nah. You... wanna swim with us?",
	"H4": "P Yes. Yes, I'd like that.",
	"H5": "P I wanted a life of my own. I thought I'd been given it, but all I'd been given was a chance. The real thing, that I had to win for myself.",
}	

