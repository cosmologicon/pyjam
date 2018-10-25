from math import *
import os
from OpenGL.GL import *
from OpenGL.GLU import *
from . import state
#from . import modelloader, settings, section
from . import modelloader, settings

import random
import numpy as np

class Splashes(object):
	def __init__(self, pos):
		self.n = 20
		self.pos = pos[:]
		self.x = [pos[0]+2.0*(random.random()-0.5) for i in range(self.n)]
		self.y = [pos[1]+2.0*(random.random()-0.5) for i in range(self.n)]
		self.z = [pos[2]+2.0*(random.random()-0.5) for i in range(self.n)]
		self.vx = [0.07*(random.random()-0.5) for i in range(self.n)]
		self.vy = [0.07*(random.random()-0.5) for i in range(self.n)]
		self.vz = [0.15*random.random() for i in range(self.n)]
		self.to = [random.randint(10,20) for i in range(self.n)]
		self.s = [0.5*random.random() for i in range(self.n)]
		self.c = [0.1*random.random()+0.3 for i in range(self.n)]
	
	def Update(self):
		for i in range(self.n):
			#self.to[i] -= 1
			#if self.to[i] < 0:
			if self.z[i] < self.pos[2]:
				#self.to[i] = random.randint(20,30)
				self.vz[i] = 0.15*random.random()
				self.x[i] = self.pos[0]+2.0*(random.random()-0.5)
				self.y[i] = self.pos[1]+2.0*(random.random()-0.5)
				self.z[i] = self.pos[2]+2.0*(random.random()-0.5)
			else:
				self.x[i] += self.vx[i]
				self.y[i] += self.vy[i]
				self.vz[i] -= 0.01
				self.z[i] += self.vz[i]
	
	def Draw(self):
		for i in range(self.n):
			glPushMatrix()
			glColor4f(self.c[i]/1.5, self.c[i], 0, 1)
			glTranslate(self.x[i],self.y[i],self.z[i])
			glDisable(GL_LIGHTING)
			drawsphere(self.s[i])
			glEnable(GL_LIGHTING)
			glPopMatrix()

class Vortex(object):
	def __init__(self, pos, radius=1.0, speed=1.0):
		self.pos = pos
		self.radius = radius
		self.speed = speed
		self.angle = 0
	
	def Update(self):
		self.angle = (self.angle+self.speed) % 360
	
	def Draw(self):
		glEnable(GL_TEXTURE_2D)
		glPushMatrix()
		glTranslate(self.pos[0],self.pos[1],self.pos[2]+0.5)
		glRotate(-self.angle, 0, 0, 1)
		if self.radius < 2.0:
			npoints = 10
			glBindTexture(GL_TEXTURE_2D, water_texture_vortex_small.texture)
		else:
			npoints = 20
			glBindTexture(GL_TEXTURE_2D, water_texture_vortex.texture)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		glBegin(GL_POLYGON)
		radius_text = 0.5
		for i in range(npoints):
			theta = i*2*pi/npoints
			glTexCoord2f(radius_text*sin(theta)+0.5, radius_text*cos(theta)+0.5)
			glVertex(self.radius*sin(theta), self.radius*cos(theta), 0)
		glEnd()
		glPopMatrix()
		glDisable(GL_TEXTURE_2D)

class Waterfall(object):
	def __init__(self, pos, drop_height, radius=1.0):
		self.pos = pos
		self.height = drop_height
		self.frame = 0
		self.radius = radius
		self.vortex_top = Vortex([pos[0],pos[1],pos[2]], radius=1.5, speed=2.5)
		self.splash_bottom = Splashes([pos[0],pos[1],pos[2]-drop_height+1.0])
	
	def Update(self):
		self.frame += 1
		self.vortex_top.Update()
		self.splash_bottom.Update()
	
	def Draw(self):
		glEnable(GL_TEXTURE_2D)
		glPushMatrix()
		glColor4f(1, 1, 1, 0.5)
		glTranslate(self.pos[0],self.pos[1],self.pos[2])
		glBindTexture(GL_TEXTURE_2D, water_texture.texture)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		steps = int(3*self.height)
		for i in range(10):
			theta1 = i*2*pi/10
			theta2 = (i+1)*2*pi/10
			glBegin(GL_QUADS)
			glTexCoord2f(i/10.0, (self.frame % steps)/steps)
			glVertex(self.radius*sin(theta1), self.radius*cos(theta1), -self.height)
			glTexCoord2f((i+1)/10.0, (self.frame % steps)/steps)
			glVertex(self.radius*sin(theta2), self.radius*cos(theta2), -self.height)
			glTexCoord2f((i+1)/10.0, 1.0+(self.frame % steps)/steps)
			glVertex(self.radius*sin(theta2), self.radius*cos(theta2), 0)
			glTexCoord2f(i/10.0, 1.0+(self.frame % steps)/steps)
			glVertex(self.radius*sin(theta1), self.radius*cos(theta1), 0)
			glEnd()
		glDisable(GL_BLEND)
		glPopMatrix()
		glDisable(GL_TEXTURE_2D)
		
		self.vortex_top.Draw()
		self.splash_bottom.Draw()

class Animations(object):
	def __init__(self):
		self.water_flow = 0
		self.init_trigger = True
		self.fadepipe = 1.0
		#self.splashes = [Splashes([-30.0,30.0,3.0])]
		self.splashes = []
		#self.waterfalls = [Waterfall([0.0,0.0,0.0],20.0)]
		self.waterfalls = []
	def cycle(self):
		"""
		faderate = 0.01
		if state.you.section.label == 'pool':
			self.fadepipe = min(1.0,self.fadepipe+faderate)
		else:
			self.fadepipe = max(0.5,self.fadepipe-faderate)
		"""
		self.water_flow += 1
		for splash in self.splashes:
			splash.Update()
		for waterfall in self.waterfalls:
			waterfall.Update()
		
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
				elif sect.label == 'pipe':
					print('// pipe // sect %d'%(count))
				count += 1
			self.init_trigger = False
		"""
	def draw(self):
		for splash in self.splashes:
			splash.Draw()
		for waterfall in self.waterfalls:
			waterfall.Draw()

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
	global water_texture_vortex
	water_texture_vortex = modelloader.TextureSurf(os.path.join('models','water_texture_vortex.png'))
	global water_texture_vortex_small
	water_texture_vortex_small = modelloader.TextureSurf(os.path.join('models','water_texture_vortex_small.png'))
	
	# Load in Environment model files
	global model3d_pipe
	model3d_pipe = modelloader.Model3D(os.path.join('models','pipe.obj'),alpha=0.3)
	
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
		if sect.label == 'pipe':
			drawmodel_sect_pipe(sect)
	for sect in state.sections:
		if sect.label == 'straight' or sect.label == 'slope':
			drawmodel_sect_straight(sect)
		elif sect.label == 'curve':
			drawmodel_sect_curve(sect)

def drawmodel_sect_pipe(sect):
	# render structure
	glPushMatrix()
	glColor4f(1.0, 1.0, 1.0, 1)
	glTranslate(sect.pos0[0],sect.pos0[1],sect.pos0[2]+1.5)
	glRotate(math.degrees(-sect.angle), 0, 0, 1)
	glTranslate(0,sect.connections[0].r,0)
	glRotate(90, 1, 0, 0)
	glRotate(180, 0, 0, 1)
	glCallList(model3d_pipe.gl_list)
	glPopMatrix()

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
		dx = 0.5*sin(animation.water_flow/100.0)+1.0*cos(animation.water_flow/80.0)
		dy = 0.5*cos(animation.water_flow/100.0)+1.0*sin(animation.water_flow/80.0)
		glTexCoord2f((x+dx)/10, (y+dy)/10)
		glVertex(x, y, 0.1)
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
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glCallList(model3d_sections[0][sect_ind].gl_list)
		glDisable(GL_BLEND)
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
	if fabs(sect.getflowrate()) > 0:
		steps = ceil(sect.length/(sect.getflowrate()/float(settings.maxfps)))
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
	angle = sect.z[2]*(animation.water_flow*(0.2*sect.getflowrate()/settings.maxfps) % (2*pi))
	for vertex in sect.vertices:
		vx = vertex[0]*cos(angle) - vertex[1]*sin(angle)
		vy = vertex[0]*sin(angle) + vertex[1]*cos(angle)
		glTexCoord2f((vx)/10+0.5, (vy)/10+0.5)
		glVertex(vertex[0],vertex[1],vertex[2]+0.1)
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
	glRotate(90 + state.you.rangle(), 1, 0, 0)
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

