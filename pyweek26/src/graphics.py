from math import *
import os
from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.GLU import *
import pygame
from . import state
from . import modelloader, settings

import random

class Splashes(object):
	def __init__(self, pos, section, lifetime = -1):
		self.n = 20
		self.pos = pos[:]
		self.section = section
		self.x = [pos[0]+2.0*(random.random()-0.5) for i in range(self.n)]
		self.y = [pos[1]+2.0*(random.random()-0.5) for i in range(self.n)]
		self.z = [pos[2]+2.0*(random.random()-0.5) for i in range(self.n)]
		self.vx = [0.07*(random.random()-0.5) for i in range(self.n)]
		self.vy = [0.07*(random.random()-0.5) for i in range(self.n)]
		self.vz = [0.15*random.random() for i in range(self.n)]
		self.to = [random.randint(10,20) for i in range(self.n)]
		self.s = [0.5*random.random() for i in range(self.n)]
		self.c = [0.1*random.random()+0.3 for i in range(self.n)]
		self.active = True
		self.lifetime = lifetime
	
	def Update(self):
		if self.lifetime > 0:
			self.lifetime -= 1
			if self.lifetime == 0:
				self.active = False
		for i in range(self.n):
			if self.z[i] < self.pos[2] and (self.lifetime == -1 or self.lifetime > 30):
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
	def __init__(self, pos, section, radius=1.0, speed=1.0):
		self.pos = pos
		self.section = section
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
		glColor4f(1, 1, 1, 0.5)
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
	def __init__(self, pos, section, drop_height, radius=1.0):
		self.pos = pos
		self.section = section
		self.height = drop_height
		self.frame = 0
		self.radius = radius
		self.vortex_top = Vortex([pos[0],pos[1],pos[2]], self.section, radius=1.5, speed=2.5)
		self.splash_bottom = Splashes([pos[0],pos[1],pos[2]-drop_height+1.0], self.section)
	
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
			glTexCoord2f(i/10.0, (self.frame % steps)/float(steps))
			glVertex(self.radius*sin(theta1), self.radius*cos(theta1), -self.height)
			glTexCoord2f((i+1)/10.0, (self.frame % steps)/float(steps))
			glVertex(self.radius*sin(theta2), self.radius*cos(theta2), -self.height)
			glTexCoord2f((i+1)/10.0, 1.0+(self.frame % steps)/float(steps))
			glVertex(self.radius*sin(theta2), self.radius*cos(theta2), 0)
			glTexCoord2f(i/10.0, 1.0+(self.frame % steps)/float(steps))
			glVertex(self.radius*sin(theta1), self.radius*cos(theta1), 0)
			glEnd()
		glDisable(GL_BLEND)
		glPopMatrix()
		glDisable(GL_TEXTURE_2D)
		
		self.vortex_top.Draw()
		self.splash_bottom.Draw()

class Stalker(object):
	def __init__(self, pos, section):
		self.pos = pos[:]
		self.section = section
		self.inds = [random.randint(1,100),random.randint(1,100),random.randint(1,100)]
		
		self.armpos = [[0,0],[0,0],[0,0]]
		self.angle_body = 0
		self.angle_eye = 0
		
		tdist = 5.0
		self.splashes = []
		for i in range(3):
			ang = i*(2*pi/3.0)
			self.MoveArms(i, tdist, ang)
			self.splashes.append(Splashes([self.armpos[i][0], self.armpos[i][1], self.pos[2]], self.section))
	
	def MoveArms(self, arm_ind, tdist, ang):
		ang_nom = arm_ind*(2*pi/3.0)
		self.armpos[arm_ind][0] = self.pos[0]+tdist*sin(ang)
		self.armpos[arm_ind][1] = self.pos[1]+tdist*cos(ang)
	
	def UpdateHeadEye(self):
		self.angle_eye = -atan2(state.you.pos[1]-self.pos[1], state.you.pos[0]-self.pos[0])*180/pi-90
		self.angle_body = self.angle_eye
	
	def Update(self):
		self.inds[0] += 1
		self.inds[1] += 1
		self.inds[2] += 1
		self.UpdateHeadEye()
		for splash in self.splashes:
			splash.Update()
	
	def get_normal(self, p0, p1, p3):
		u = [p3[0]-p0[0], p3[1]-p0[1], p3[2]-p0[2]]
		v = [p1[0]-p0[0], p1[1]-p0[1], p1[2]-p0[2]]
		n = [u[1]*v[2]-u[2]*v[1], u[2]*v[0] - u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
		return n
	
	def Draw(self):
		
		steps_h = 3
		steps_w = 5
		
		height = 5.0
		trad_base = 0.5
		
		sway_distx = 1.0
		curvynessx = 2.0
		sway_speedx = 0.1
		
		sway_disty = 1.0
		curvynessy = 2.0
		sway_speedy = 0.1
		
		# draw body
		glPushMatrix()
		glTranslate(self.pos[0], self.pos[1], self.pos[2])
		glRotate(-90, 1, 0, 0)
		glRotate(self.angle_body, 0, 1, 0)
		glScale(0.3, 0.3, 0.3)
		glCallList(model_stalkerbody.gl_list)
		glTranslate(0, -10.0, 0)
		#glRotate(self.angle_eye, 0, 1, 0)
		glCallList(model_stalkereye.gl_list)
		glPopMatrix()
		
		# draw arms
		for arm_ind in range(3):
			glPushMatrix()
			glColor(1.0, 0.5, 1.0, 1)
			glTranslate(self.armpos[arm_ind][0],self.armpos[arm_ind][1],self.pos[2])
			for i in range(steps_h):
				off_x1 = sway_distx*sin(curvynessx*(i/steps_h)-sway_speedx*self.inds[arm_ind])
				off_y1 = sway_disty*cos(curvynessy*(i/steps_h)-sway_speedy*self.inds[arm_ind])
				if i == (steps_h-1):
					off_x2 = off_x1
					off_y2 = off_y1
				else:
					off_x2 = sway_distx*sin(curvynessx*((i+1)/steps_h)-sway_speedx*self.inds[arm_ind])
					off_y2 = sway_disty*cos(curvynessy*((i+1)/steps_h)-sway_speedy*self.inds[arm_ind])
				for j in range(steps_w):
					if j % 2 == 0:
						glColor(1.0, 0.5, 1.0, 1)
					else:
						glColor(1.0, 0.3, 1.0, 1)
					rad1 = trad_base*(1-pow((i/(steps_h)),2))
					rad2 = trad_base*(1-pow(((i+1)/(steps_h)),2))
					theta1 = j*2*pi/steps_w
					theta2 = (j+1)*2*pi/steps_w
					if i == (steps_h-1):
						h2 = (i)*height/float(steps_h)
					else:
						h2 = (i+1)*height/float(steps_h)
					glBegin(GL_QUADS)
					p0 = [rad1*sin(theta1)+off_x1, rad1*cos(theta1)+off_y1, i*height/float(steps_h)]
					p1 = [rad1*sin(theta2)+off_x1, rad1*cos(theta2)+off_y1, i*height/float(steps_h)]
					p2 = [rad2*sin(theta2)+off_x2, rad2*cos(theta2)+off_y2, h2]
					p3 = [rad2*sin(theta1)+off_x2, rad2*cos(theta1)+off_y2, h2]
					n = self.get_normal(p0, p1, p3)
				
					glNormal3fv(n)
					glVertex3fv(p0)
					glNormal3fv(n)
					glVertex3fv(p1)
					glNormal3fv(n)
					glVertex3fv(p2)
					glNormal3fv(n)
					glVertex3fv(p3)
					glEnd()
			glPopMatrix()
		
		for splash in self.splashes:
			splash.Draw()

def build_openscad_commands():
	
	f = open(os.path.join('tools','generated_section_models','scad','openscad_script.sh'), "w");
	f.write('#!/bin/bash\n')
	count = 0
	for sect in state.sections:
		f.write('echo Building section %d of %d\n'%(count+1,len(state.sections)))
		if sect.label == 'pool':
			exit_points = []
			step_width = 3.0
			for sect2 in state.sections:
				if sect2 == sect or not sect2.label == 'pool':
					continue
				if fabs(sect2.pos[2]-sect.pos[2]) < 5.0:
					wall_margin = (sqrt(pow(sect2.pos[0]-sect.pos[0],2)+pow(sect2.pos[1]-sect.pos[1],2))-sect2.r-sect.r)
					if wall_margin < 2.5:
						step_width = 0.0
					elif wall_margin < 7.0:
						step_width = min(1.0,step_width)
			for c in sect.connections:
				if c.label == 'pipe':
					continue
				if sqrt(pow(sect.pos[0]-c.pos0[0],2)+pow(sect.pos[1]-c.pos0[1],2)) > sect.r:
					exit_points.append([c.pos0[0],c.pos0[1],c.width])
				else:
					exit_points.append([c.pos1[0],c.pos1[1],c.width])
			con_str = ", ".join(['[%.4f,%.4f,%.4f]'%(p[0]-sect.pos[0],p[1]-sect.pos[1],p[2]) for p in exit_points])
			f2 = open(os.path.join('tools','generated_section_models','scad','pool_%03d.scad'%(count)), "w");
			f2.write('use <../build_environments.scad>;\n')
			f2.write('pool(diameter=%.4f, wall_height=%.4f, step_width=%.4f, connections=[%s]);\n'%(sect.r,max([p[2] for p in exit_points])+1.0,step_width,con_str))
			f2.close()
			f.write('%s -o ../stl/pool_%03d.stl pool_%03d.scad\n'%(settings.openscad_path,count,count))
		elif sect.label == 'straight' or sect.label == 'slope':
			if sect.connections[0].label == 'pool':
				dy1 = sqrt(pow(sect.connections[0].r,2)-pow(sect.width,2))
			else:
				dy1 = 0
			if sect.connections[1].label == 'pool':
				dy2 = sqrt(pow(sect.connections[1].r,2)-pow(sect.width,2))
			else:
				dy2 = 0	
			f2 = open(os.path.join('tools','generated_section_models','scad','section_%03d.scad'%(count)), "w");
			f2.write('use <../build_environments.scad>;\n')
			f2.write('straight(length=%.4f, width=%.4f, dy1=%.4f, dy2=%.4f, dz=%.4f);\n'%(sect.length,sect.width,dy1,dy2,sect.dz))
			f2.close()
			f.write('%s -o ../stl/section_%03d.stl section_%03d.scad\n'%(settings.openscad_path,count,count))
		elif sect.label == 'curve':
			f2 = open(os.path.join('tools','generated_section_models','scad','section_%03d.scad'%(count)), "w");
			f2.write('use <../build_environments.scad>;\n')
			f2.write('curve(p0=[%.4f, %.4f], center=[%.4f, %.4f], dir=%d, angle=%.4f, width=%.4f);\n'%(sect.p0[0],sect.p0[1],sect.center[0],sect.center[1],sect.right,2*sect.beta*180.0/pi,sect.width))
			f2.close()
			f.write('%s -o ../stl/section_%03d.stl section_%03d.scad\n'%(settings.openscad_path,count,count))
			
		count += 1
	f.close()

class Animations(object):
	def __init__(self):
		self.water_flow = 0
		self.init_trigger = True
		self.fadepipe = 1.0
		self.splashes = []
		self.vortexes = []
		self.waterfalls = []
		self.stalker = []
		
	def cycle(self):
		
		self.water_flow += 1
		for splash in self.splashes:
			splash.Update()
			if splash.active == False:
				self.splashes.remove(splash)
		for vortex in self.vortexes:
			vortex.Update()
		for waterfall in self.waterfalls:
			waterfall.Update()
		for stalker in self.stalker:
			stalker.Update()
				
	def draw(self):
		for splash in self.splashes:
			if splash.section in get_sections_to_draw():
				splash.Draw()
		for vortex in self.vortexes:
			vortex.Draw()
		for waterfall in self.waterfalls:
			if waterfall.section in get_sections_to_draw():
				waterfall.Draw()
		for stalker in self.stalker:
			stalker.Update()
			if stalker.section in get_sections_to_draw():
				stalker.Draw()
		
#animation = Animations()

def init():
	global quadric
	quadric = gluNewQuadric()
	gluQuadricNormals(quadric, GLU_SMOOTH)
	gluQuadricTexture(quadric, GL_TRUE)
	
	print('loading model files ...')
	
	# load in model files
	global model_fish, model_tail
	model_fish = modelloader.Model3D(os.path.join('models','fish001_tailfree_colour.obj'))
	model_tail = modelloader.Model3D(os.path.join('models','fish001_tail_colour.obj'))
	
	global model_stalkerbody, model_stalkereye
	model_stalkerbody = modelloader.Model3D(os.path.join('models','stalker_body.obj'))
	model_stalkereye = modelloader.Model3D(os.path.join('models','stalker_eye.obj'))
	
	global model_fishfood
	model_fishfood = modelloader.Model3D(os.path.join('models','fishfood.obj'))
	
	# Load in water textures
	global water_texture
	water_texture = modelloader.TextureSurf(os.path.join('models','textures','water_texture_darkgreen.png'))
	global water_texture_pool
	water_texture_pool = modelloader.TextureSurf(os.path.join('models','textures','water_texture_darkgreen_pool.png'))
	global water_texture_vortex
	water_texture_vortex = modelloader.TextureSurf(os.path.join('models','textures','water_texture_vortex.png'))
	global water_texture_vortex_small
	water_texture_vortex_small = modelloader.TextureSurf(os.path.join('models','textures','water_texture_vortex_small.png'))
	
	# Load in Environment model files
	global model3d_pipe
	model3d_pipe = modelloader.Model3D(os.path.join('models','pipe.obj'),alpha=0.3)
	global model3d_arrowup
	model3d_arrowup = modelloader.Model3D(os.path.join('models','arrow_up.obj'),alpha=0.3)
	global model3d_arrowdown
	model3d_arrowdown = modelloader.Model3D(os.path.join('models','arrow_down.obj'),alpha=0.3)
	global model3d_arrowdown_yellow
	model3d_arrowdown_yellow = modelloader.Model3D(os.path.join('models','arrow_down_yellow.obj'),alpha=0.3)
	
	global model3d_sections
	model3d_sections = []
	model3d_sections.append([])
	level_name = settings.leveldataname
	model_paths = [i for i in os.listdir(os.path.join('models',level_name)) if "obj" in i]
	max_ind = max([int(path[-7:-4]) for path in model_paths])
	for i in range(max_ind+1):
		model3d_sections[-1].append([])
	c = 0
	for path in model_paths:
		ind = int(path[-7:-4])
		if c % 20 == 0:
			print('Loading 3D Models: %d of %d'%(c+1,len(model_paths)))
		c += 1
		model3d_sections[-1][ind] = modelloader.Model3D(os.path.join('models',level_name,path),alpha=0.3)
	
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

def get_sections_to_draw():
	if state.you.section.label == 'pool':
		draw_sections = [state.you.section]+state.you.section.connections
	else:
		draw_sections = [state.you.section]
		while draw_sections[-1].label != "pool":
			if draw_sections[-1].label == 'pipe':
				break
			draw_sections.append(draw_sections[-1].connections[0])
		if draw_sections[-1].label == "pool":
			draw_sections.extend(draw_sections[-1].connections)
		draw_sections.append(state.you.section.connections[1])
		while draw_sections[-1].label != "pool":
			if draw_sections[-1].label == 'pipe':
				break
			draw_sections.append(draw_sections[-1].connections[1])
		if draw_sections[-1].label == "pool":
			draw_sections.extend(draw_sections[-1].connections)
	return draw_sections

def drawmodel_watersurface():
	#for sect in state.sections:
	for sect in get_sections_to_draw():
		if sect.label == 'pool':
			dist2you = sqrt(pow(state.you.pos[0]-sect.pos[0],2)+pow(state.you.pos[0]-sect.pos[0],2))
			if dist2you < 20 and (state.you.pos[2]-sect.pos[2]) < -8:
				continue
			drawmodel_sect_pool_water(sect)
		elif sect.label == 'straight' or sect.label == 'slope':
			dist2you = sqrt(pow(state.you.pos[0]-sect.pos0[0],2)+pow(state.you.pos[0]-sect.pos0[0],2))
			if dist2you < 20 and (state.you.pos[2]-sect.pos0[2]) < -8:
				continue
			drawmodel_sect_straight_water(sect)
		elif sect.label == 'curve':
			dist2you = sqrt(pow(state.you.pos[0]-sect.center[0],2)+pow(state.you.pos[0]-sect.center[0],2))
			if dist2you < 20 and (state.you.pos[2]-sect.center[2]) < -8:
				continue
			drawmodel_sect_curve_water(sect)

def drawmodel_section_pools():
	#for sect in state.sections:
	for sect in get_sections_to_draw():
		if sect.label == 'pool':
			dist2you = sqrt(pow(state.you.pos[0]-sect.pos[0],2)+pow(state.you.pos[0]-sect.pos[0],2))
			if dist2you < 20 and (state.you.pos[2]-sect.pos[2]) < -8:
				continue
			drawmodel_sect_pool(sect)

def drawmodel_section_tubes():
	#for sect in state.sections:
	for sect in get_sections_to_draw():
		if sect.label == 'pipe':
			dist2you = sqrt(pow(state.you.pos[0]-sect.pos0[0],2)+pow(state.you.pos[0]-sect.pos0[0],2))
			if dist2you < 20 and (state.you.pos[2]-sect.pos0[2]) < -8:
				continue
			drawmodel_sect_pipe(sect)
	#for sect in state.sections:
	for sect in get_sections_to_draw():
		if sect.label == 'straight' or sect.label == 'slope':
			dist2you = sqrt(pow(state.you.pos[0]-sect.pos0[0],2)+pow(state.you.pos[0]-sect.pos0[0],2))
			if dist2you < 20 and (state.you.pos[2]-sect.pos0[2]) < -8:
				continue
			drawmodel_sect_straight(sect)
		elif sect.label == 'curve':
			dist2you = sqrt(pow(state.you.pos[0]-sect.center[0],2)+pow(state.you.pos[0]-sect.center[0],2))
			if dist2you < 20 and (state.you.pos[2]-sect.center[2]) < -8:
				continue
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
		dx = 0.5*sin(state.animation.water_flow/100.0)+1.0*cos(state.animation.water_flow/80.0)
		dy = 0.5*cos(state.animation.water_flow/100.0)+1.0*sin(state.animation.water_flow/80.0)
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
	#if fabs(state.you.pos[2]-sect.pos[2]) > 5.0:
	if False:
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glCallList(model3d_sections[0][sect_ind].gl_list)
		glDisable(GL_BLEND)
	else:
		glCallList(model3d_sections[0][sect_ind].gl_list)
	glPopMatrix()
	if sect.hasfood:
		glPushMatrix()
		glTranslate(*sect.pos)
		glColor4f(1, 1, 0, 1)
		glPointSize(5)
		glBegin(GL_POINTS)
		for jfood in range(50):
			x, y = math.CS(jfood * math.phi, sect.r / 2 * (jfood ** 2 * math.phi % 1))
			z = 3 * ((jfood ** 3 * math.phi + pygame.time.get_ticks() * 0.001) % 1) ** 2
			glVertex(x, y, z)
		glEnd()
		glPopMatrix()
		drawfishfood(sect.pos)

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
		steps = ceil(sect.length/(3*sect.getflowrate()/float(settings.maxfps)))
		glTexCoord2f(0, -(state.animation.water_flow % steps)/steps)
		glVertex(-sect.width, dy1, 0.1)
		glTexCoord2f(0, (0.2*(sect.length-dy1-dy2)/sect.width)-(state.animation.water_flow % steps)/steps)
		glVertex(-sect.width, sect.length-dy2, sect.dz+0.1)
		glTexCoord2f(1, (0.2*(sect.length-dy1-dy2)/sect.width)-(state.animation.water_flow % steps)/steps)
		glVertex(sect.width, sect.length-dy2, sect.dz+0.1)
		glTexCoord2f(1, -(state.animation.water_flow % steps)/steps)
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
	
	# adjust length for connections
	if sect.connections[0].label == 'pool':
		dy1 = sqrt(pow(sect.connections[0].r,2)-pow(sect.width,2))
	else:
		dy1 = 0
	if sect.connections[1].label == 'pool':
		dy2 = sqrt(pow(sect.connections[1].r,2)-pow(sect.width,2))
	else:
		dy2 = 0
	
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
	
	# render arrows
	if sect.connections[0].label == 'pool':
		glPushMatrix()
		glColor4f(1.0, 1.0, 1.0, 1)
		glTranslate(sect.pos0[0],sect.pos0[1],sect.pos0[2]+sect.width+1.0)
		glRotate(math.degrees(-sect.angle), 0, 0, 1)
		glRotate(90, 1, 0, 0)
		glRotate(180, 0, 0, 1)
		glTranslate(0,0,-dy1)
		if not state.you.section.label == 'pool':
			glEnable(GL_BLEND)
			glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		if sect.pool0.pos.z > sect.pool1.pos.z:
			glCallList(model3d_arrowdown.gl_list)
		elif sect.pool0.pos.z < sect.pool1.pos.z:
			glCallList(model3d_arrowup.gl_list)
		else:
			if (sect.pool0.pressure() - sect.pool1.pressure()) > -1:
				glCallList(model3d_arrowdown.gl_list)
			elif (sect.pool0.pressure() - sect.pool1.pressure()) == -1:
				glCallList(model3d_arrowdown_yellow.gl_list)
			else:
				glCallList(model3d_arrowup.gl_list)
		if not state.you.section.label == 'pool':
			glDisable(GL_BLEND)
		glPopMatrix()
	
	if sect.connections[1].label == 'pool':
		glPushMatrix()
		glColor4f(1.0, 1.0, 1.0, 1)
		glTranslate(sect.pos0[0],sect.pos0[1],sect.pos0[2]+sect.width+1.0+sect.dz)
		glRotate(math.degrees(-sect.angle), 0, 0, 1)
		glRotate(90, 1, 0, 0)
		glRotate(180, 0, 0, 1)
		glTranslate(0,0,-sect.length+dy2)
		glRotate(180, 0, 1, 0)
		if not state.you.section.label == 'pool':
			glEnable(GL_BLEND)
			glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		if sect.pool1.pos.z > sect.pool0.pos.z:
			glCallList(model3d_arrowdown.gl_list)
		elif sect.pool1.pos.z < sect.pool0.pos.z:
			glCallList(model3d_arrowup.gl_list)
		else:
			if (sect.pool1.pressure() - sect.pool0.pressure()) > -1:
				glCallList(model3d_arrowdown.gl_list)
			elif (sect.pool1.pressure() - sect.pool0.pressure()) == -1:
				glCallList(model3d_arrowdown_yellow.gl_list)
			else:
				glCallList(model3d_arrowup.gl_list)
		if not state.you.section.label == 'pool':
			glDisable(GL_BLEND)
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
	angle = sect.z[2]*(state.animation.water_flow*(0.2*sect.getflowrate()/settings.maxfps) % (2*pi))
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

def drawdisk(center, r, color):
	glPushMatrix()
	glColor4f(*color)
	glTranslate(*center)
	gluDisk(quadric, 0, r, 20, 1)
	glPopMatrix()

def drawcylinder(p0, r, h, color):
	glPushMatrix()
	glColor4f(*color)
	glTranslate(*p0)
	gluCylinder(quadric, r, r, h, 10, 1)
	glPopMatrix()

def drawcone(p0, r, h, color):
	glPushMatrix()
	glColor4f(*color)
	glTranslate(*p0)
	gluCylinder(quadric, r, 0, h, 10, 1)
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

def drawfishfood(pos):
	glPushMatrix()
	glColor4f(1.0, 1.0, 1.0, 1)
	glTranslate(pos[0], pos[1], pos[2])
	glRotate(180, 1, 0, 0)
	glRotate(20, 0, 0, 1)
	glScale(2.0, 2.0, 2.0)
	if not state.food:
		glDisable(GL_LIGHTING)
	glCallList(model_fishfood.gl_list)
	if not state.food:
		glEnable(GL_LIGHTING)
	glPopMatrix()

# Placeholder - for now everything's spheres
def drawobj(obj):
	glPushMatrix()
	glColor4f(*(list(obj.color) + [1]))
	glTranslate(*obj.pos)
	drawsphere(obj.r)
	glPopMatrix()


