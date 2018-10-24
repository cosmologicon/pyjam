from math import *
import os
from OpenGL.GL import *
from OpenGL.GLU import *
from . import state
#from . import modelloader, settings, section
from . import modelloader, settings

import numpy as np

class Animations(object):
	def __init__(self):
		self.water_flow = 0
		self.init_trigger = True
		self.fadepipe = 1.0
	def cycle(self):
		"""
		faderate = 0.01
		if state.you.section.label == 'pool':
			self.fadepipe = min(1.0,self.fadepipe+faderate)
		else:
			self.fadepipe = max(0.5,self.fadepipe-faderate)
		"""
		self.water_flow += 1
		"""
		if self.init_trigger: # hackish thing to print out OpenSCAD function calls from section objects
			count = 0
			for sect in state.sections:
				if sect.label == 'pool':
					exit_points = []
					for c in sect.connections:
						if sqrt(pow(sect.pos[0]-c.pos0[0],2)+pow(sect.pos[1]-c.pos0[1],2)) > sect.r:
							exit_points.append([c.pos0[0],c.pos0[1],c.width])
						else:
							exit_points.append([c.pos1[0],c.pos1[1],c.width])
					con_str = ", ".join(['[%.4f,%.4f,%.4f]'%(p[0]-sect.pos[0],p[1]-sect.pos[1],p[2]) for p in exit_points])
					print('pool(diameter=%.4f, wall_height=%.4f, connections=[%s]); // sect: %d'%(sect.r,max([p[2] for p in exit_points])+1.0,con_str,count))
					#print('pool')
				elif sect.label == 'straight' or sect.label == 'slope':
					if sect.connections[0].label == 'pool':
						dy1 = sqrt(pow(sect.connections[0].r,2)-pow(sect.width,2))
					else:
						dy1 = 0
					if sect.connections[1].label == 'pool':
						dy2 = sqrt(pow(sect.connections[1].r,2)-pow(sect.width,2))
					else:
						dy2 = 0
					print('straight(length=%.4f, width=%.4f, dy1=%.4f, dy2=%.4f, dz=%.4f); // sect: %d'%(sect.length,sect.width,dy1,dy2,sect.dz,count))
					#print('straight')
				elif sect.label == 'curve':
					#print('curve')
					print('curve(p0=[%.4f, %.4f], center=[%.4f, %.4f], dir=%d, angle=%.4f, width=%.4f); // sect: %d'%(sect.p0[0],sect.p0[1],sect.center[0],sect.center[1],sect.right,2*sect.beta*180.0/pi,sect.width,count))
				count += 1
			self.init_trigger = False
		"""

animation = Animations()

def init():
	global quadric
	quadric = gluNewQuadric()
	gluQuadricNormals(quadric, GLU_SMOOTH)
	gluQuadricTexture(quadric, GL_TRUE)
	
	# load in model files
	global model_fish, model_tail
	model_fish = modelloader.Model3D(os.path.join('models','fish001_tailfree_colour.obj'))
	model_tail = modelloader.Model3D(os.path.join('models','fish001_tail_colour.obj'))
	
	# Load in water texture
	global water_texture
	water_texture = modelloader.TextureSurf(os.path.join('models','water_texture_darkgreen.png'))
	global water_texture_pool
	water_texture_pool = modelloader.TextureSurf(os.path.join('models','water_texture_darkgreen_pool.png'))
	
	# Load in Environment model files
	global model3d_sections
	model3d_sections = []
	model3d_sections.append([])
	model_paths = [i for i in os.listdir(os.path.join('models','level_new')) if "obj" in i]
	max_ind = max([int(path[-7:-4]) for path in model_paths])
	for i in range(max_ind+1):
		model3d_sections[-1].append([])
	for path in model_paths:
		ind = int(path[-7:-4])
		model3d_sections[-1][ind] = modelloader.Model3D(os.path.join('models','level_new',path),alpha=0.3)
	
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

def drawmodel_watersurface():
	for sect in state.sections:
		if sect.label == 'pool':
			drawmodel_sect_pool_water(sect)
		elif sect.label == 'straight' or sect.label == 'slope':
			drawmodel_sect_straight_water(sect)
		elif sect.label == 'curve':
			drawmodel_sect_curve_water(sect)

def drawmodel_section_pools():
	for sect in state.sections:
		if sect.label == 'pool':
			drawmodel_sect_pool(sect)

def drawmodel_section_tubes():
	for sect in state.sections:
		if sect.label == 'straight' or sect.label == 'slope':
			drawmodel_sect_straight(sect)
		elif sect.label == 'curve':
			drawmodel_sect_curve(sect)

def drawmodel_sect_pool_water(sect):
	
	# draw water surface
	glEnable(GL_TEXTURE_2D)
	glPushMatrix()
	glColor4f(1, 1, 1, 0.3)
	glTranslate(*sect.pos)
	glBindTexture(GL_TEXTURE_2D, water_texture_pool.texture)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glBegin(GL_POLYGON)
	for x, y in math.CSround(int(round(10 * sect.r)), r = sect.r):
		glVertex(x, y, 0.1)
		dx = 0.5*sin(animation.water_flow/100.0)+1.0*cos(animation.water_flow/80.0)
		dy = 0.5*cos(animation.water_flow/100.0)+1.0*sin(animation.water_flow/80.0)
		glTexCoord2f((x+dx)/10, (y+dy)/10)
	glEnd()
	glPopMatrix()
	glDisable(GL_TEXTURE_2D)

def drawmodel_sect_pool(sect):
	
	# draw structure
	glPushMatrix()
	glColor4f(1.0, 1.0, 1.0, 1)
	glTranslate(*sect.pos)
	glRotate(-90, 1, 0, 0)
	glRotate(-90, 0, 1, 0)
	sect_ind = state.sections.index(sect)
	#if sect == state.you.section or sect in state.you.section.connections:
	if False:
		glDisable(GL_DEPTH_TEST) # can I get around needing this?
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glCallList(model3d_sections[0][sect_ind].gl_list)
		glDisable(GL_BLEND)
		glEnable(GL_DEPTH_TEST)
	else:
		glCallList(model3d_sections[0][sect_ind].gl_list)
	glPopMatrix()

def drawmodel_sect_straight_water(sect):
	
	# adjust length for connections
	if sect.connections[0].label == 'pool':
		dy1 = sqrt(pow(sect.connections[0].r,2)-pow(sect.width,2))
	else:
		dy1 = 0
	if sect.connections[1].label == 'pool':
		dy2 = sqrt(pow(sect.connections[1].r,2)-pow(sect.width,2))
	else:
		dy2 = 0
	
	# draw water surface
	glEnable(GL_TEXTURE_2D)
	glPushMatrix()
	glColor4f(1, 1, 1, 0.3)
	glTranslate(*sect.pos0)
	glRotate(math.degrees(-sect.angle), 0, 0, 1)
	glBindTexture(GL_TEXTURE_2D, water_texture.texture)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glBegin(GL_QUADS)
	if fabs(sect.rate) > 0:
		steps = ceil(sect.length/(sect.rate/float(settings.maxfps)))
		glTexCoord2f(0, -(animation.water_flow % steps)/steps)
		glVertex(-sect.width, dy1, 0.1)
		glTexCoord2f(0, (0.2*(sect.length-dy1-dy2)/sect.width)-(animation.water_flow % steps)/steps)
		glVertex(-sect.width, sect.length-dy2, sect.dz+0.1)
		glTexCoord2f(1, (0.2*(sect.length-dy1-dy2)/sect.width)-(animation.water_flow % steps)/steps)
		glVertex(sect.width, sect.length-dy2, sect.dz+0.1)
		glTexCoord2f(1, -(animation.water_flow % steps)/steps)
		glVertex(sect.width, dy1, 0.1)
	else:
		glTexCoord2f(0, 0)
		glVertex(-sect.width, dy1, 0.1)
		glTexCoord2f(0, (0.2*(sect.length-dy1-dy2)/sect.width))
		glVertex(-sect.width, sect.length-dy2, sect.dz+0.1)
		glTexCoord2f(1, (0.2*(sect.length-dy1-dy2)/sect.width))
		glVertex(sect.width, sect.length-dy2, sect.dz+0.1)
		glTexCoord2f(1, 0)
		glVertex(sect.width, dy1, 0.1)
	glEnd()
	glPopMatrix()
	glDisable(GL_TEXTURE_2D)
	
def drawmodel_sect_straight(sect):
	# render structure
	glPushMatrix()
	glColor4f(1.0, 1.0, 1.0, 1)
	glTranslate(*sect.pos0)
	glRotate(math.degrees(-sect.angle), 0, 0, 1)
	glRotate(90, 1, 0, 0)
	glRotate(180, 0, 0, 1)
	sect_ind = state.sections.index(sect)
	#if (state.you.section.label == 'pool' and sect in state.you.section.connections) or (not state.you.section.label == 'pool'):
	#if sect == state.you.section or sect in state.you.section.connections:
	#if True:
	if not state.you.section.label == 'pool':
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glCallList(model3d_sections[0][sect_ind].gl_list)
		glDisable(GL_BLEND)
	else:
		glCallList(model3d_sections[0][sect_ind].gl_list)
	glPopMatrix()

def drawmodel_sect_curve_water(sect):
	
	# draw water surface
	glEnable(GL_TEXTURE_2D)
	glPushMatrix()
	glColor4f(1, 1, 1, 0.3)
	glTranslate(*sect.center)
	glBindTexture(GL_TEXTURE_2D, water_texture_pool.texture)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glBegin(GL_POLYGON)
	angle = sect.z[2]*(animation.water_flow*(0.2*sect.rate/settings.maxfps) % (2*pi))
	for vertex in sect.vertices:
		glVertex(vertex[0],vertex[1],vertex[2]+0.1)
		vx = vertex[0]*cos(angle) - vertex[1]*sin(angle)
		vy = vertex[0]*sin(angle) + vertex[1]*cos(angle)
		glTexCoord2f((vx)/10+0.5, (vy)/10+0.5)
	glEnd()
	glPopMatrix()
	glDisable(GL_TEXTURE_2D)

def drawmodel_sect_curve(sect):
	
	# render structure
	glPushMatrix()
	glColor4f(1.0, 1.0, 1.0, 1)
	glTranslate(*sect.center)
	if sect.right:
		angle = (180.0/pi)*atan2(sect.p0[1]-sect.center[1],sect.p0[0]-sect.center[0])-180
	else:
		angle = (180.0/pi)*atan2(sect.p0[1]-sect.center[1],sect.p0[0]-sect.center[0])
	glRotate(angle, 0, 0, 1)
	glRotate(90, 1, 0, 0)
	glRotate(180, 0, 0, 1)
	sect_ind = state.sections.index(sect)
	#if sect == state.you.section or sect in state.you.section.connections:
	#if True:
	if not state.you.section.label == 'pool':
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glCallList(model3d_sections[0][sect_ind].gl_list)
		glDisable(GL_BLEND)
	else:
		glCallList(model3d_sections[0][sect_ind].gl_list)
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

