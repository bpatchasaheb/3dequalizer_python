#
# 3DE4.script.name:	3DE Export Pose...
# 3DE4.script.version:	v1.0
# 3DE4.script.gui:	Main Window::3DE4::File::Export
# 3DE4.script.comment:	It exports camera or object pose to .pose file.

#Author : Patcha Saheb (patchasaheb@gmail.com)
#Date : 06-03-2014

# import sdv's python vector lib...
from vl_sdv import *
import os,sys

pg 	= tde4.getCurrentPGroup()
cam	= tde4.getCurrentCamera()
frame	= tde4.getCurrentFrame(cam)
typ	= tde4.getPGroupType(pg)

# converting to angles...
def convertToAngles(r3d):
		rot	= rot3d(mat3d(r3d)).angles(VL_APPLY_ZXY)
		rx	= (rot[0]*180.0)/3.141592654
		ry	= (rot[1]*180.0)/3.141592654
		rz	= (rot[2]*180.0)/3.141592654
		return(rx,ry,rz)
if pg !=None and cam !=None:
		
	if typ == "CAMERA" or typ == "OBJECT":
		sellist = tde4.getCameraList(1)
		if len(sellist) < 2:
			p3d = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
			r3d = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
			path	= tde4.postFileRequester("Pose Saver...","*.pose")
			f = open(path,"w")
			f.write("%.15f %.15f %.15f %.15f %.15f %.15f "%(p3d[0],p3d[1],p3d[2],convertToAngles(r3d)[0],convertToAngles(r3d)[1],convertToAngles(r3d)[2]))
			f.close()
			tde4.postQuestionRequester("3DE Export Pose...",tde4.getPGroupName(pg)+"exported successfully","ok")
		else:
			tde4.postQuestionRequester("3DE Export Pose...","Error, there must be exactly one camera or object selected.","ok")
	else:
		tde4.postQuestionRequester("3DE Export Pose...","Error, CAMERA or OBJECT PGroup must be selected","ok")		
		










		
