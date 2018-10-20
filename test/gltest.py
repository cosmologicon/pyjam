from __future__ import division
import pygame, numpy
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.GLU import *
from OpenGL.arrays import vbo

pygame.init()
pygame.display.set_mode((600, 400), DOUBLEBUF | OPENGL)

glClearColor(0.1, 0.1, 0.1, 1)


# Generate shaders
vertex_shader = shaders.compileShader("""
#version 120
void main() {
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}
""",
GL_VERTEX_SHADER)

fragment_shader = shaders.compileShader("""
#version 120
void main() {
    gl_FragColor = vec4( 0, 1, 0, 1 );
}
""", GL_FRAGMENT_SHADER)
shader = shaders.compileProgram(vertex_shader, fragment_shader)

# create a VBO
buffobj = vbo.VBO(
    numpy.array( [
        [  0, 1, 0 ],
        [ -1,-1, 0 ],
        [  1,-1, 0 ],
        [  2,-1, 0 ],
        [  4,-1, 0 ],
        [  4, 1, 0 ],
        [  2,-1, 0 ],
        [  4, 1, 0 ],
        [  2, 1, 0 ],
    ],'f')
)

# Generate a texture
img = pygame.font.Font(None, 50).render("Hello", True, (255, 255, 255))
w, h = img.get_size()
texture = glGenTextures(1)
glPixelStorei(GL_UNPACK_ALIGNMENT,1)
glBindTexture(GL_TEXTURE_2D, texture)
glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
data = pygame.image.tostring(img, "RGBA", 1)
glTexImage2D(GL_TEXTURE_2D, 0, 4, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)


playing = True
clock = pygame.time.Clock()
while playing:
	dt = 0.001 * clock.tick(40)
	for event in pygame.event.get():
		if event.type in (MOUSEBUTTONDOWN, KEYDOWN):
			playing = False

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


	glLoadIdentity()
	shaders.glUseProgram(shader)
	buffobj.bind()
	glEnableClientState(GL_VERTEX_ARRAY)
	glVertexPointerf(buffobj)
	glDrawArrays(GL_TRIANGLES, 0, 9)
	buffobj.unbind()
	glDisableClientState(GL_VERTEX_ARRAY)
	shaders.glUseProgram( 0 )

	# Display texture
	glBindTexture(GL_TEXTURE_2D, texture)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glTranslate(-1, -1, 0)
	glScale(2 / 600, 2 / 400, 1)
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glEnable(GL_TEXTURE_2D)
	glDisable(GL_DEPTH_TEST)
	glDisable(GL_CULL_FACE)
	glDisable(GL_LIGHTING)
	glBegin(GL_QUADS)
	x0, y0 = 10, 10
	w, h = img.get_size()
	for dx, dy in [(0, 0), (0, 1), (1, 1), (1, 0)]:
		glVertex(x0 + dx * w, y0 + dy * h, 0)
		glTexCoord(dy, 1 - dx)
	glEnd()


	pygame.display.flip()




