# This module extends ptext to work on OpenGL surfaces.
# This module is not required to use the basic ptext module on regular pygame Surfaces.
# ptext.py must be in the same directory.

# ptextgl.draw(text, pos=None, **options)

# https://github.com/cosmologicon/pygame-text

import pygame, math
from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.arrays import vbo
import numpy
from . import ptext, pview

AUTO_PREP = True

class _DrawOptions(ptext._DrawOptions):
	_fields = tuple(field for field in ptext._DrawOptions._fields if field not in
		("surf", "cache"),
	) + (
		"prep",
	)
	_defaults = { k: v for k, v in ptext._DrawOptions._defaults.items() if k not in
		("surf", "cache")
	}
	def __init__(self, **kwargs):
		ptext._DrawOptions.__init__(self, **kwargs)
		if self.prep is None:
			self.prep = AUTO_PREP
	def resolvesurf(self):
		pass



_vertex_shader_source = """
#version 120
attribute vec2 p;
uniform vec4 rect;
uniform vec2 viewsize;
uniform float angle;
varying vec2 tcoord;
void main() {
	float C = cos(angle), S = sin(angle);
	mat2 R = mat2(C, S, -S, C);
	vec2 p0 = rect.xy;
	vec2 size = rect.zw;
	gl_Position = vec4((p0 + R * (p * size)) / viewsize * 2.0 - 1.0, 0.0, 1.0);
	tcoord = p;
}
"""
_fragment_shader_source = """
#version 120
uniform float alpha;
uniform sampler2D texture;
varying vec2 tcoord;
void main() {
	gl_FragColor = texture2D(texture, tcoord);
	gl_FragColor.a *= alpha;
}
"""

_shader = None
def init():
	global _shader, _locations, _pdata
	if _shader: return
	# Generate shaders
	vertex_shader = shaders.compileShader(_vertex_shader_source, GL_VERTEX_SHADER)
	fragment_shader = shaders.compileShader(_fragment_shader_source, GL_FRAGMENT_SHADER)
	_shader = shaders.compileProgram(vertex_shader, fragment_shader)
	_locations = {
		"p": glGetAttribLocation(_shader, "p"),
		"rect": glGetUniformLocation(_shader, "rect"),
		"viewsize": glGetUniformLocation(_shader, "viewsize"),
		"angle": glGetUniformLocation(_shader, "angle"),
		"alpha": glGetUniformLocation(_shader, "alpha"),
		"texture": glGetUniformLocation(_shader, "texture"),
	}
	_pdata = numpy.array([0, 0, 1, 0, 1, 1, 0, 1], numpy.float32)


def prep():
	init()
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glUseProgram(_shader)
	glEnableVertexAttribArray(_locations["p"])
	glVertexAttribPointer(_locations["p"], 2, GL_FLOAT, GL_FALSE, 0, _pdata)
	glUniform2f(_locations["viewsize"], *pview.size)
	glUniform1i(_locations["texture"], 0)

def unprep(state):
	glDisable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	shaders.glUseProgram(0)

_surf_cache = {}
def gettexture(text, **kwargs):
	options = ptext._GetsurfOptions(**kwargs)
	key = text, options.key()
	if key in _surf_cache:
		return _surf_cache[key]
	surf = ptext.getsurf(text, **kwargs)
	w, h = surf.get_size()
	texture = glGenTextures(1)
	glPixelStorei(GL_UNPACK_ALIGNMENT,1)
	glBindTexture(GL_TEXTURE_2D, texture)
	data = pygame.image.tostring(surf, "RGBA", 1)
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
	glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	_surf_cache[key] = surf, texture
	print(len(_surf_cache))
	return surf, texture
	

def draw(text, pos=None, **kwargs):
	options = _DrawOptions(pos = pos, **kwargs)
	if options.prep:
		state = prep()
	alpha = options.alpha
	options.alpha = 1
	angle = options.angle
	options.angle = 0



	glUniform1f(_locations["alpha"], alpha)
	glUniform1f(_locations["angle"], math.radians(angle))

	tsurf, texture = gettexture(text, **options.togetsurfoptions())

	w, h = tsurf.get_size()
	x, y = ptext._blitpos(options.angle, options.pos, options.anchor, (w, h), text)
	y = pview.h - y - h
	glUniform4f(_locations["rect"], x, y, w, h)
	glEnable(GL_TEXTURE_2D)
	glActiveTexture(GL_TEXTURE0)
	glBindTexture(GL_TEXTURE_2D, texture)
	glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
	if options.prep:
		unprep(state)
#	return tsurf, pos





