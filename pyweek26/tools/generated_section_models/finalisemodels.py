"""
finalisemodels.py - script to post-process stl files from OpenSCAD into final models
"""

import os, sys

import numpy
from stl import mesh

# paths to data/output
stl_dir = 'stl'
output_dir = 'obj'

# cycle through models and output objs
stl_paths = [i for i in os.listdir(stl_dir) if "stl" in i]
for file in stl_paths:
	stl_data = mesh.Mesh.from_file(os.path.join(stl_dir,file))
	if not "pool" in file:
		f = open(os.path.join(output_dir,file[:-3]+'obj'), "w");
		f.write('# Environment model file: %s\n'%(file))
		f.write('mtllib material_pipe.mtl\n')
		for i in range(stl_data.v0.shape[0]):
			vn = stl_data.normals[i]/numpy.linalg.norm(stl_data.normals[i])
			f.write('vn %.4f %.4f %.4f\n'%(vn[0],vn[1],vn[2]))
			f.write('v %.4f %.4f %.4f\n'%(stl_data.v0[i][0],stl_data.v0[i][1],stl_data.v0[i][2]))
			f.write('vn %.4f %.4f %.4f\n'%(vn[0],vn[1],vn[2]))
			f.write('v %.4f %.4f %.4f\n'%(stl_data.v1[i][0],stl_data.v1[i][1],stl_data.v1[i][2]))
			f.write('vn %.4f %.4f %.4f\n'%(vn[0],vn[1],vn[2]))
			f.write('v %.4f %.4f %.4f\n'%(stl_data.v2[i][0],stl_data.v2[i][1],stl_data.v2[i][2]))
		f.write('usemtl material_pipe\n')
		for i in range(stl_data.v0.shape[0]):
			f.write('f %d//%d %d//%d %d//%d\n'%(3*i+1,3*i+1,3*i+2,3*i+2,3*i+3,3*i+3))
		f.close()
	else:
		f = open(os.path.join(output_dir,file[:-3]+'obj'), "w");
		f.write('# Environment model file: %s\n'%(file))
		f.write('mtllib material_brick.mtl\n')
		xmin = min(min(stl_data.v0[:,0]),min(stl_data.v1[:,0]),min(stl_data.v2[:,0]))
		xmax = max(max(stl_data.v0[:,0]),max(stl_data.v1[:,0]),max(stl_data.v2[:,0]))
		ymin = min(min(stl_data.v0[:,1]),min(stl_data.v1[:,1]),min(stl_data.v2[:,1]))
		ymax = max(max(stl_data.v0[:,1]),max(stl_data.v1[:,1]),max(stl_data.v2[:,1]))
		zmin = min(min(stl_data.v0[:,2]),min(stl_data.v1[:,2]),min(stl_data.v2[:,2]))
		zmax = max(max(stl_data.v0[:,2]),max(stl_data.v1[:,2]),max(stl_data.v2[:,2]))
		for i in range(stl_data.v0.shape[0]):
			vn = stl_data.normals[i]/numpy.linalg.norm(stl_data.normals[i])
			f.write('v %.4f %.4f %.4f\n'%(stl_data.v0[i][0],stl_data.v0[i][1],stl_data.v0[i][2]))
			f.write('v %.4f %.4f %.4f\n'%(stl_data.v1[i][0],stl_data.v1[i][1],stl_data.v1[i][2]))
			f.write('v %.4f %.4f %.4f\n'%(stl_data.v2[i][0],stl_data.v2[i][1],stl_data.v2[i][2]))
			
			f.write('vn %.4f %.4f %.4f\n'%(vn[0],vn[1],vn[2]))
			f.write('vn %.4f %.4f %.4f\n'%(vn[0],vn[1],vn[2]))
			f.write('vn %.4f %.4f %.4f\n'%(vn[0],vn[1],vn[2]))
			
			if vn[2] == 1.0:
				f.write('vt %.4f %.4f\n'%((stl_data.v0[i][0]-xmin)/(xmax-xmin),(stl_data.v0[i][1]-ymin)/(ymax-ymin)))
				f.write('vt %.4f %.4f\n'%((stl_data.v1[i][0]-xmin)/(xmax-xmin),(stl_data.v1[i][1]-ymin)/(ymax-ymin)))
				f.write('vt %.4f %.4f\n'%((stl_data.v2[i][0]-xmin)/(xmax-xmin),(stl_data.v2[i][1]-ymin)/(ymax-ymin)))
			else:
				f.write('vt %.4f %.4f\n'%(0,0))
				f.write('vt %.4f %.4f\n'%(0,0))
				f.write('vt %.4f %.4f\n'%(0,0))
			
		f.write('usemtl material_brick\n')
		for i in range(stl_data.v0.shape[0]):
			f.write('f %d/%d/%d %d/%d/%d %d/%d/%d\n'%(3*i+1,3*i+1,3*i+1,3*i+2,3*i+2,3*i+2,3*i+3,3*i+3,3*i+3))
		f.close()
