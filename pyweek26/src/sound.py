import os
import pygame
from . import settings, state

pygame.mixer.init()

class SoundManager(object):
	def __init__(self):
		self.channels = []
		for i in range(6):
			self.channels.append(pygame.mixer.Channel(i+2))
		
		self.voice_channel = pygame.mixer.Channel(0) # channel 0 dedicated for voice
		self.ambient_channel = pygame.mixer.Channel(1) # channel 2 dedicated for ambient sounds
		self.next_sound_chan = 2
		
		# Load up voice/dialogue samples
		voice_files = [i for i in os.listdir(os.path.join('data','voice')) if "ogg" in i]
		self.voice_samples = {}
		for file in voice_files:
			self.voice_samples[file] = pygame.mixer.Sound(os.path.join('data','voice',file))
		
		# Load sound samples
		sound_files = [i for i in os.listdir(os.path.join('data','sound')) if "ogg" in i]
		self.sound_samples = {}
		for file in sound_files:
			name = file[:-4]
			self.sound_samples[name] = pygame.mixer.Sound(os.path.join('data','sound',file))
		
	# play sounds on other channels
	def PlaySound(self,name):
		self.channels[self.next_sound_chan].play(self.sound_samples[name])
		self.next_sound_chan += 1
		if self.next_sound_chan == 6:
			self.next_sound_chan = 0
	
	# Function for playing voice on dedicated channel
	def PlayVoice(self,name):
		self.voice_channel.play(self.voice_samples[name])
	
	def PauseVoice(self):
		self.voice_channel.pause()
	
	def ResumeVoice(self):
		self.voice_channel.unpause()
	
	def StopVoice(self):
		self.voice_channel.stop()
	
	def CheckVoice(self):
		return self.voice_channel.get_busy()
	
	def Update_Ambient(self):
		pass
	
	def Update_Voice(self):
		pass
	
	def Update(self):
		self.Update_Ambient()
		self.Update_Voice()
		
manager = SoundManager()
