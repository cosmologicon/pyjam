"""
modelloader.py - reads in obj and mtl files for 3D models, materials and textures

modified from code found at:
https://www.pygame.org/wiki/OBJFileLoader
"""

import pygame, os
from OpenGL.GL import *
from OpenGL.raw import GL
from OpenGL.arrays import ArrayDatatype as ADT

# TextureSurf: load in image file for use as textur
class TextureSurf(object):
	def __init__(self, path):
		surf = pygame.image.load(path)
		self.w, self.h = surf.get_width(), surf.get_height()
		surf_data = pygame.image.tostring(surf, 'RGBA', 1)
		self.texture = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, self.texture)
		glPixelStorei(GL_UNPACK_ROW_LENGTH, 0)
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.w, self.h, 0, GL_RGBA, GL_UNSIGNED_BYTE, surf_data)

# Material: loads a mtl material description file
def Material(mtl_dir, filename, wrap_type):
    contents = {}
    mtl = None
    for line in open(filename, "r"):
        if line.startswith('#'): continue
        values = line.split()
        if not values: continue
        if values[0] == 'newmtl':
            mtl = contents[values[1]] = {}
        elif mtl is None:
            raise ValueError
        elif values[0] == 'map_Kd':
            # load the texture referred to by this declaration
            mtl[values[0]] = values[1]
            #surf = pygame.image.load(os.path.join(mtl_dir,mtl['map_Kd']))
            surf = pygame.image.load(os.path.join('models','textures',mtl['map_Kd']))
            image = pygame.image.tostring(surf, 'RGBA', 1)
            ix, iy = surf.get_rect().size
            texid = mtl['texture_Kd'] = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texid)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                GL_LINEAR)
            
            if wrap_type == 'repeat':
            	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            elif wrap_type == 'mirror':
            	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT)
            	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT)
            
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA,
                GL_UNSIGNED_BYTE, image)
        else:
            #mtl[values[0]] = map(float, values[1:])
            mtl[values[0]] = values[1:]
    return contents

# model3d: load in obj file and creates vertex, face, texture buffers of OpenGL rendering
class Model3D(object):
	
    def __init__(self, filename, wrap_type='repeat', flipz=False, coltex=False, alpha=1.0):
        
        self.filename = filename
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []
        self.mtl = None

        material = None
        path = os.path.split(filename)[0]
        use_texture = False
        
        # parse in obj
        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'v':
                v = [float(values[2]), -float(values[3]), -float(values[1])]
                if flipz:
                	v[1] = -v[1]
                self.vertices.append(v)
            elif values[0] == 'vn':
                v = [float(values[2]), -float(values[3]), -float(values[1])]
                if flipz:
                	v[1] = -v[1]
                self.normals.append(v)
            elif values[0] == 'vt':
                self.texcoords.append([float(values[1]),float(values[2])])
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'mtllib':
                #self.mtl = Material(path, os.path.join(path, values[1]), wrap_type)
                self.mtl = Material(path, os.path.join('models','materials', values[1]), wrap_type)
                for name in self.mtl:
                    if 'texture_Kd' in self.mtl[name]:
                        use_texture = True
            elif values[0] == 'f':
                face = []
                texcoords = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    vert = int(w[0])
                    if vert < 0:
                        # refers to -ve indexed verts defined up to this
                        # point
                        vert += len(self.vertices)
                    face.append(vert)
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                self.faces.append((face, norms, texcoords, material))
            else:
                continue
        
        # setup buffers and call list
        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        if use_texture: glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)
        
        for face in self.faces:
            vertices, normals, texture_coords, material = face

            if material:
                mtl = self.mtl[material]
                if 'texture_Kd' in mtl:
                    # use diffuse texmap
                    glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
                    if coltex:
                    	#glColor(*mtl['Kd'])
                    	kd = [float(i) for i in mtl['Kd']]
                    	glColor(kd[0], kd[1], kd[2], alpha)
                    else:
                    	glColor(1,1,1,alpha)
                else:
                    # just use diffuse colour
                    #glColor(*mtl['Kd'])
                    kd = [float(i) for i in mtl['Kd']]
                    glColor(kd[0], kd[1], kd[2], alpha)
            else:
                glColor(1,1,1,alpha)

            glBegin(GL_POLYGON)
            for i in range(0, len(vertices)):
                if normals[i]:
                    glNormal3fv(self.normals[normals[i] - 1])
                if texture_coords[i]:
                    glTexCoord2fv(self.texcoords[texture_coords[i] - 1])
                glVertex3fv(self.vertices[vertices[i] - 1])
            glEnd()
        
        if use_texture: glDisable(GL_TEXTURE_2D)
        glEndList()

        """
        index_list = [[]]
        a, b, c, prev_mat = self.faces[0]
        material_list = [prev_mat]
        for face in self.faces:
        	vertices, normals, texture_coords, material = face
        	if not material == prev_mat:
        		prev_mat = material
        		material_list.append(material)
        		index_list.append([])
        	index_list[-1].append([v-1 for v in vertices])
        self.numpy_verts = np.array(self.vertices, dtype=np.float32)
        self.numpy_norms = np.array(self.normals, dtype=np.float32)
        self.numpy_texcoords = np.array(self.texcoords, dtype=np.float32)
        self.tri_index_numpy = []
        for i in xrange(len(index_list)):
        	self.tri_index_numpy.append(np.array(index_list[i], dtype=np.uint))
        
        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glVertexPointerf(self.numpy_verts)
        glNormalPointerf(self.numpy_norms)
        glTexCoordPointerf(self.numpy_texcoords)
        for i in xrange(len(index_list)):
        	mtl = self.mtl[material_list[i]]
        	if 'texture_Kd' in mtl:
        		# use diffuse texmap
        		glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
        		if coltex:
        			glColor(*mtl['Kd'])
        		else:
        			glColor(1,1,1)
        	else:
        		# just use diffuse colour
        		glColor(*mtl['Kd'])
        	glDrawElementsui(GL_TRIANGLES, self.tri_index_numpy[i])
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        glDisable(GL_TEXTURE_2D)
        glEndList()
        """
