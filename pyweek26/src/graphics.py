import math
import os
from OpenGL.GL import *
from OpenGL.GLU import *
from . import state
from . import modelloader

import numpy as np

def init():
	global quadric
	quadric = gluNewQuadric()
	gluQuadricNormals(quadric, GLU_SMOOTH)
	gluQuadricTexture(quadric, GL_TRUE)
	
	# load in model files
	global model_fish, model_tail
	model_fish = modelloader.Model3D(os.path.join('models','fish001_tailfree_colour.obj'))
	model_tail = modelloader.Model3D(os.path.join('models','fish001_tail_colour.obj'))
	
	global model_sect_straight
	model_sect_straight = modelloader.Model3D(os.path.join('models','section_straight.obj'),flipz=True)
	
	# Init OpenGL lighting
	# TODO: figure out strange lighting directions
	glLightfv(GL_LIGHT0, GL_POSITION,  (0, 0, 200, 0.0))
	glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
	glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.1, 0.1, 0.1, 1.0))
	glEnable(GL_LIGHT0)
	glEnable(GL_LIGHTING)
	glEnable(GL_COLOR_MATERIAL)
	glEnable(GL_DEPTH_TEST)
	glShadeModel(GL_SMOOTH)

def drawmodel_sect_straight(pos0, length, width, angle):
	glPushMatrix()
	glColor4f(1.0, 1.0, 1.0, 1)
	glTranslate(*pos0)
	glRotate(math.degrees(-angle), 0, 0, 1)
	glRotate(90, 1, 0, 0)
	glCallList(model_sect_straight.gl_list)
	glPopMatrix()
	
def drawsphere(r = 1):
	gluSphere(quadric, r, 10, 10)

def drawcircle(center, r, axis, color):
	# note: axis doesn't work - all horizontal circles for now
	glPushMatrix()
	glColor4f(*color)
	glTranslate(*center)
	gluDisk(quadric, 0.95 * r, 1.05 * r, 10, 10)
	glPopMatrix()

def drawcylinder(p0, r, h, color):
	glPushMatrix()
	glColor4f(*color)
	glTranslate(*p0)
	gluCylinder(quadric, r, r, h, 10, 1)
	glPopMatrix()
	
def drawyou():
	glPushMatrix()
	#glColor4f(0.8, 0.5, 0, 1)
	glColor4f(1.0, 1.0, 1.0, 1)
	#glTranslate(*state.you.pos)
	glTranslate(state.you.pos[0], state.you.pos[1], state.you.pos[2]+0.5)
	angle = 20 * math.sin(state.you.Tswim * math.tau) - math.degrees(state.you.heading)
	angle_tail = 20 * math.cos(state.you.Tswim * math.tau) # tail waves out of phase
	glRotate(angle, 0, 0, 1)
	glRotate(90, 1, 0, 0)
	glScale(0.1, 0.1, 0.1)
	glCallList(model_fish.gl_list)
	glTranslate(0, 0, 7.0)
	glRotate(-angle_tail, 0, 1, 0)
	glCallList(model_tail.gl_list)
	glPopMatrix()

# Placeholder - for now everything's spheres
def drawobj(obj):
	glPushMatrix()
	glColor4f(*(list(obj.color) + [1]))
	glTranslate(*obj.pos)
	drawsphere(obj.r)
	glPopMatrix()

