import pygame
from .util import debug

sounds = {}
def getsound(sname):
	if sname not in sounds:
		sounds[sname] = None
		debug("Missing sound:", sname)
	return sounds[sname]

def play(sname):
	sound = getsound(sname)
	if sound is None:
		return

