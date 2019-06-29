import os
import pygame
from . import settings

pygame.mixer.init()

class SoundManager(object):
	def __init__(self):
		self.channels = []
		for i in range(5):
			self.channels.append(pygame.mixer.Channel(i+3))
		
		self.voice_channel = pygame.mixer.Channel(0) # channel 0 dedicated for voice
		self.ambient_channel_a = pygame.mixer.Channel(1) # channel 1-2 dedicated for ambient sounds
		self.ambient_channel_b = pygame.mixer.Channel(2)
		self.next_sound_chan = 3
		
		# Load up voice/dialogue samples
		voice_files = [i for i in os.listdir(os.path.join('data','voice')) if "ogg" in i]
		self.voice_samples = {}
		for file in voice_files:
			name = file[:-4]
			self.voice_samples[name] = pygame.mixer.Sound(os.path.join('data','voice',file))
		
		self.current_dialog = None
		self.current_dind = -1
		self.paused = False
		
		# Load sound samples
		sound_files = [i for i in os.listdir(os.path.join('data','sound')) if "ogg" in i]
		self.sound_samples = {}
		for file in sound_files:
			name = file[:-4]
			self.sound_samples[name] = pygame.mixer.Sound(os.path.join('data','sound',file))
		
		# start-up ambient sound
		self.ambient_channel_a.play(self.sound_samples['water_ambient'],loops=-1)
		self.ambient_channel_a.set_volume(0.0)
		self.ambient_channel_b.play(self.sound_samples['water_ambient_tube'],loops=-1)
		self.ambient_channel_b.set_volume(0.0)
		
		self.vol_a = 0.0
		self.vol_b = 0.0
		self.mixrate = 0.005
		
		# Music
		self.music_tracks = {}
		self.music_tracks['levelA'] = [os.path.join('data','music','levelA0.ogg'),os.path.join('data','music','levelA1.ogg')]
		self.music_tracks['levelB'] = [os.path.join('data','music','levelB0.ogg'),os.path.join('data','music','levelB1.ogg')]
		self.music_tracks['intro'] = os.path.join('data','music','intro.ogg')
		self.music_tracks['boss'] = os.path.join('data','music','boss.ogg')
		self.music_tracks['end'] = os.path.join('data','music','end.ogg')
		
		self.current_music = None
		self.playing_intro = False
		
	# play sounds on other channels
	def PlaySound(self,name):
		self.channels[self.next_sound_chan].play(self.sound_samples[name])
		self.next_sound_chan += 1
		if self.next_sound_chan == 5:
			self.next_sound_chan = 0
	
	# Function for playing voice on dedicated channel
	def PlayVoice(self,name):
		self.voice_channel.play(self.voice_samples[name])
	
	def PauseVoice(self):
		self.voice_channel.pause()
		self.paused = True
	
	def ResumeVoice(self):
		self.voice_channel.unpause()
		self.paused = False
	
	def StopVoice(self):
		self.voice_channel.stop()
	
	def CheckVoice(self):
		return self.voice_channel.get_busy()
	
	def StopMusic(self):
		pygame.mixer.music.stop()
		self.current_music = None
		self.playing_intro = False
	
	def Update_Ambient(self):
		from . import state
		if self.CheckVoice() == True:
			pygame.mixer.music.set_volume(0.3)
			self.vol_a = 0.0
			self.vol_b = 0.05
			vol_a_target = self.vol_a
			vol_b_target = self.vol_b
		else:
			pygame.mixer.music.set_volume(0.7)
			if state.you.section.label in ['straight','slope','pipe','curve']:
				vol_a_target = 0.0
				vol_b_target = 0.5
			elif state.you.section.label == 'pool':
				if len(state.you.section.drainers) > 0:
					vol_a_target = 0.4
					vol_b_target = 0.0
				else:
					vol_a_target = 0.2
					vol_b_target = 0.0
			else:
				vol_a_target = 0
				vol_b_target = 0
		
		if vol_a_target > self.vol_a:
			self.vol_a = min((self.vol_a+self.mixrate),vol_a_target)
		elif vol_a_target < self.vol_a:
			self.vol_a = max((self.vol_a-self.mixrate),vol_a_target)
		if vol_b_target > self.vol_b:
			self.vol_b = min((self.vol_b+self.mixrate),vol_b_target)
		elif vol_b_target < self.vol_b:
			self.vol_b = max((self.vol_b-self.mixrate),vol_b_target)
			
		self.ambient_channel_a.set_volume(self.vol_a)
		self.ambient_channel_b.set_volume(self.vol_b)
	
	def Update_Voice(self):
		if self.current_dialog == None:
			return
		if self.CheckVoice() == False and self.paused == False:
			self.current_dind += 1
			next_stub = self.current_dialog+'%d'%(self.current_dind+1)
			if next_stub in self.voice_samples.keys():
				self.PlayVoice(next_stub)
			else:
				self.current_dialog = None
				self.current_dind = -1
	
	def Update_Music(self):
		from . import state
		new_track = state.currentmusic()
		if new_track == 'level': # whats 'level' ???
			new_track = 'levelA' 
		if not new_track == self.current_music:
			self.current_music = new_track
			if new_track in ['levelA','levelB']:
				self.playing_intro = True
				pygame.mixer.music.load(self.music_tracks[self.current_music][0])
				pygame.mixer.music.play()
			else:
				self.playing_intro = False
				pygame.mixer.music.load(self.music_tracks[self.current_music])
				pygame.mixer.music.play(-1)
		if self.playing_intro:
			if not pygame.mixer.music.get_busy():
				pygame.mixer.music.stop()
				self.playing_intro = False
				pygame.mixer.music.load(self.music_tracks[self.current_music][1])
				pygame.mixer.music.set_volume(0.0)
				pygame.mixer.music.play(-1)
	
	def Update(self):
		self.Update_Music()
		self.Update_Ambient()
		self.Update_Voice()
		
manager = SoundManager()
