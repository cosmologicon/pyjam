"""
testmodel.py - Script to test loading/rendering different 3D models
"""

import os, sys
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from math import *
import numpy as np

from . import modelloader, state, section, graphics

# Initialise pygame
pygame.init()
pygame.mixer.init()

# start up display
fps = 30
window_size = (854, 480)
screen = pygame.display.set_mode(window_size, OPENGL | DOUBLEBUF)
pygame.display.set_caption("Test Model: Click to Rotate")
clock = pygame.time.Clock()
quit_flag = False

# Load models
model_fish = modelloader.Model3D(os.path.join('models','fish001_tailfree_colour.obj'))

# create sections
state.sections.append(section.Pool(pygame.math.Vector3(5, 5, 0), 10))
state.sections.append(section.Pool(pygame.math.Vector3(40, 40, 0), 6))
state.sections.append(section.Pool(pygame.math.Vector3(80, 0, 0), 12))
state.sections.append(section.Pool(pygame.math.Vector3(-30, 10, 0), 8))
state.sections.extend(section.connectpools(state.sections[0], state.sections[1], waypoints = [pygame.math.Vector3(0, 40, 0)]))
state.sections.extend(section.connectpools(state.sections[1], state.sections[2], waypoints = [pygame.math.Vector3(40, 20, 0), pygame.math.Vector3(100, 30, 0)]))
state.sections.extend(section.connectpools(state.sections[2], state.sections[0], waypoints = [], rate = 20, width = 8))
state.sections.extend(section.connectpools(state.sections[0], state.sections[3], waypoints = []))

# ModelScene: simple scene class for viewing a 3D model
class ModelScene(object):
	
	def __init__(self, window_size):
		self.window_size = window_size
		
		# init camera variables
		self.yaw = 0.0
		self.pitch = 0.0
		self.mouse_click_held = False
		self.mouse_sensitivity = 0.005
		
		self.tail_ani_step = 0
		
		# Build models
		self.str_model = graphics.create_section_straight(state.sections[4])
		
		# Init Open GL lighting
		glLightfv(GL_LIGHT0, GL_POSITION,  (100, 200, 100, 0.0))
		glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
		glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
		glEnable(GL_LIGHT0)
		glEnable(GL_LIGHTING)
		glEnable(GL_COLOR_MATERIAL)
		glEnable(GL_DEPTH_TEST)
		glShadeModel(GL_SMOOTH)
	
	def on_event(self, events):
		for event in events:
			if event.type == MOUSEBUTTONDOWN:
				self.mouse_click_held = True
				pygame.mouse.set_visible(False)
				pygame.mouse.set_pos([self.window_size[0]/2,self.window_size[1]/2])
			elif event.type == MOUSEBUTTONUP:
				self.mouse_click_held = False
				pygame.mouse.set_visible(True)
	
	def on_update(self):
		
		self.tail_ani_step += 1
		if self.tail_ani_step > 15:
			self.tail_ani_step = 0
		
		if self.mouse_click_held:
			mp = pygame.mouse.get_pos()
			pygame.mouse.set_pos([self.window_size[0]/2,self.window_size[1]/2])
			rel = [mp[0]-self.window_size[0]/2,mp[1]-self.window_size[1]/2]
			self.pitch -= self.mouse_sensitivity*rel[1]
			if self.pitch >= pi/2:
				self.pitch = pi/2-0.0001
			elif self.pitch <= -pi/2:
				self.pitch = -pi/2+0.0001
			self.yaw += self.mouse_sensitivity*rel[0]
	
	def on_draw(self, screen):
	
		# Initialise view
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(60.0, self.window_size[0]/float(self.window_size[1]), 0.1, 1000.0)
		
		# setup camera perspective on the world
		vx_rot = cos(self.yaw+pi/2)
		vy_rot = sin(self.yaw+pi/2)
		glRotate(self.yaw*180/pi, 0, 1, 0)
		glRotate(-self.pitch*180/pi, vy_rot, 0, -vx_rot)
		DCM = np.array([[cos(self.pitch)*cos(self.yaw),-sin(self.yaw),sin(self.pitch)*cos(self.yaw)],[cos(self.pitch)*sin(self.yaw),cos(self.yaw),sin(self.pitch)*sin(self.yaw)],[-sin(self.pitch),0.0,cos(self.pitch)]])
		dist = 30.0
		dpx = -DCM[0][0]*dist
		dpy = -DCM[1][0]*dist
		dpz = -DCM[2][0]*dist
		glTranslate(-dpy, dpz, dpx)
		
		# clear screen
		glMatrixMode(GL_MODELVIEW)
		glClearColor(*(0.0,0.0,0.0,0.0))
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		
		# render model (fish)
		glLoadIdentity()
		glPushMatrix()
		glScale(1.0, 1.0, 1.0)
		glCallList(model_fish.gl_list)
		glPopMatrix()

scene = ModelScene(window_size)

# run a bare bones pygame loop
while not quit_flag:
	time = clock.tick(fps)
	filtered_events = []
	for event in pygame.event.get():
		if event.type == pygame.QUIT: # Check for window close
			quit_flag = True
		else:
			filtered_events.append(event)
	scene.on_event(filtered_events) # Run game events events
	scene.on_update() # Update scene
	scene.on_draw(screen) # Draw the screen
	pygame.display.flip()

