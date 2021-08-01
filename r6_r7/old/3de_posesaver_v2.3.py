# 3DE4.script.name: Pose Saver/Loader
# 3DE4.script.version: v2.3
# 3DE4.script.gui.config_menus: true		
# 3DE4.script.gui:Main Window::3DE4
# 3DE4.script.comment: Import/Export 3D rot/pos channels from/to a .pose file.
# 28 Nov 2016(Mumbai)
# Updated April 2018(Montreal)
# Patcha Saheb (patchasaheb@gmail.com)


from vl_sdv import *
import math
import os, sys
import os.path

window_title = "Patcha Pose Saver/Loader v2.3"

if 'linux' in sys.platform:
    HOME = os.environ['HOME']
    paramFile = HOME + "/Pose_3de.pose"

if 'darwin' in sys.platform:
    HOME = os.environ['HOME']
    paramFile = HOME + "/Pose_3de.pose"
else:
    if 'win' in sys.platform:
        HOME = os.environ['TEMP']
        paramFile = HOME + "\\Pose_3de.pose"

def Frame_Update(req):
	pg	= tde4.getCurrentPGroup()
	cam     = tde4.getCurrentCamera()
	frame   = tde4.getCurrentFrame(cam)
	offset = tde4.getCameraFrameOffset(cam)-1
	tde4.setWidgetValue(req,"from",str(frame+offset))
	tde4.setWidgetValue(req,"to",str(frame+offset))


def Show(req,widget,action):
	path = tde4.getWidgetValue(req,"file_browser")
	if path != None:
		show_req = tde4.createCustomRequester()
		tde4.addTextAreaWidget(show_req,"textarea","",0,0)
		tde4.setWidgetAttachModes(show_req,"textarea","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_WINDOW")
		tde4.setWidgetOffsets(show_req,"textarea",2,2,2,2)
		with open(path,"r") as ins:
			array = []
			for line in ins:
				array.append(line)
		for i in array:
			tde4.appendTextAreaWidgetString(show_req,"textarea",str(i))
		tde4.postCustomRequesterAndContinue(show_req,window_title,750,100)			
	else:
		tde4.postQuestionRequester(window_title,"Error, first please browse .pose file.","Ok")


def Write_Old_Pose():
	l = []
	pg	= tde4.getCurrentPGroup()
	cam     = tde4.getCurrentCamera()
	frame   = tde4.getCurrentFrame(cam)
	frames = tde4.getCameraNoFrames(cam)
	offset = tde4.getCameraFrameOffset(cam)-1
	pg_type = tde4.getPGroupType(pg)
	if pg_type == "CAMERA":
		pos = tde4.getPGroupPosition3D(pg,cam,frame)
		r3d = tde4.getPGroupRotation3D(pg,cam,frame)
		l.append(pos)
		rot	= rot3d(mat3d(r3d)).angles(VL_APPLY_ZXY)
		rx	= (rot[0]*180.0)/3.141592654
		ry	= (rot[1]*180.0)/3.141592654
		rz	= (rot[2]*180.0)/3.141592654
		r3d = (rx,ry,rz)
		l.append(r3d)
	if pg_type == "OBJECT":
		pos = tde4.getPGroupPosition3D(pg,cam,frame)
		r3d = tde4.getPGroupRotation3D(pg,cam,frame)
		rot	= rot3d(mat3d(r3d)).angles(VL_APPLY_ZXY)
		rx	= (rot[0]*180.0)/3.141592654
		ry	= (rot[1]*180.0)/3.141592654
		rz	= (rot[2]*180.0)/3.141592654
		r3d = (rx,ry,rz)
		l.append(pos)
		l.append(r3d)
	path = paramFile
	f = open(path,"w")
	f.write("%.15f %.15f %.15f %.15f %.15f %.15f "%(l[0][0],l[0][1],l[0][2],l[1][0],l[1][1],l[1][2]))
	f.close()

def Read_Old_Pose(req,widget,action):
	pg	= tde4.getCurrentPGroup()
	cam     = tde4.getCurrentCamera()
	frame   = tde4.getCurrentFrame(cam)
	pg_type = tde4.getPGroupType(pg)
	try:
		path = paramFile
		f = open(path,"r")
		string	= f.readline()
		a	= string.split()
		if len(a) == 6:
			# read values from .pose file..
			pos_x	= float(a[0])
			pos_y	= float(a[1])
			pos_z	= float(a[2])
			rot_x	= float(a[3])
			rot_y	= float(a[4])
			rot_z	= float(a[5])
			# matrix 3D...
			rot_x	= (rot_x*3.141592654)/180.0
			rot_y	= (rot_y*3.141592654)/180.0
			rot_z	= (rot_z*3.141592654)/180.0
			r3d	= mat3d(rot3d(rot_x,rot_y,rot_z,VL_APPLY_ZXY))
			r3d0	= [[r3d[0][0],r3d[0][1],r3d[0][2]],[r3d[1][0],r3d[1][1],r3d[1][2]],[r3d[2][0],r3d[2][1],r3d[2][2]]]		
			if pg_type == "CAMERA":
				tde4.setPGroupPosition3D(pg,cam,frame,[pos_x,pos_y,pos_z])
				tde4.setPGroupRotation3D(pg,cam,frame,r3d0)
				pf_mode  = tde4.getPGroupPostfilterMode(pg)
				tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
				tde4.filterPGroup(pg,cam)
				tde4.setPGroupPostfilterMode(pg,pf_mode)				
			if pg_type == "OBJECT":
				pg = tde4.getCurrentPGroup()
				for i_pg in tde4.getPGroupList():
					if tde4.getPGroupType(i_pg) == "CAMERA":				
						id_cpg = i_pg
						break
				id_opg = pg	
				rot_cpg = mat3d(tde4.getPGroupRotation3D(id_cpg,cam,frame))
				pos_cpg = vec3d(tde4.getPGroupPosition3D(id_cpg,cam,frame))
				rot_pos_base = igl3d(rot_cpg,pos_cpg)
				rot_opg_global = r3d
				pos_opg_global = vec3d(pos_x,pos_y,pos_z)
				scale = tde4.getPGroupScale3D(id_opg)								
				rot_pos_opg_new = igl3d(rot_opg_global,pos_opg_global).invert() * rot_pos_base
				tde4.setPGroupRotation3D(id_opg,cam,frame,rot_pos_opg_new.m.list())
				tde4.setPGroupPosition3D(id_opg,cam,frame,rot_pos_opg_new.v.list())
				tde4.setPGroupScale3D(id_opg,scale)
				pf_mode  = tde4.getPGroupPostfilterMode(id_opg)
				tde4.setPGroupPostfilterMode(id_opg,"POSTFILTER_OFF")
				tde4.filterPGroup(id_opg,cam)
				tde4.setPGroupPostfilterMode(id_opg,pf_mode)		
	except:
		pass

def ImportCameraPose():
	pg	= tde4.getCurrentPGroup()
	cam     = tde4.getCurrentCamera()
	frame   = tde4.getCurrentFrame(cam)
	frames = tde4.getCameraNoFrames(cam)
	offset = tde4.getCameraFrameOffset(cam)-1
	f_from = tde4.getWidgetValue(req,"from")
	f_to = tde4.getWidgetValue(req,"to")
	if pg!=None and cam !=None:
		if tde4.getPGroupType(pg)=="CAMERA" or tde4.getCameraType(cam) =="REF_FRAME":
			path	= tde4.getWidgetValue(req,"file_browser")
			if path!=None:
				f	= open(path,"r")
				if not f.closed:
					string	= f.readline()
					a	= string.split()
					if len(a) == 6:
						Write_Old_Pose()
						# read values from .pose file..
						pos_x	= float(a[0])
						pos_y	= float(a[1])
						pos_z	= float(a[2])
						rot_x	= float(a[3])
						rot_y	= float(a[4])
						rot_z	= float(a[5])
						# matrix 3D...
						rot_x	= (rot_x*3.141592654)/180.0
						rot_y	= (rot_y*3.141592654)/180.0
						rot_z	= (rot_z*3.141592654)/180.0
						r3d	= mat3d(rot3d(rot_x,rot_y,rot_z,VL_APPLY_ZXY))
						r3d0	= [[r3d[0][0],r3d[0][1],r3d[0][2]],[r3d[1][0],r3d[1][1],r3d[1][2]],[r3d[2][0],r3d[2][1],r3d[2][2]]]
						# setting point group position and rotation...
						if f_from != None and f_to != None and (int(f_from)-offset) >= 1 and (int(f_from)-offset) <= frames and (int(f_to)-offset) >= 1 and (int(f_to)-offset) <= frames:
							for i in range(int(f_from)-offset,(int(f_to)+1)-offset):
								tde4.setPGroupPosition3D(pg,cam,i,[pos_x,pos_y,pos_z])
								tde4.setPGroupRotation3D(pg,cam,i,r3d0)
								tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
								tde4.filterPGroup(pg,cam)
						else:
							tde4.postQuestionRequester(window_title,"Error, please enter correct frame range.","ok")
					else: 
						tde4.postQuestionRequester(window_title,"there must be exactly 6 values in a row","ok")
		else:
			tde4.postQuestionRequester(window_title,"CameraPGroup/REF Camera must be selected.", "ok")						
	else:
		tde4.postQuestionRequester(window_title, "there must be a Camera and PointGroup.", "ok")			

def convertToAngles(r3d):
		rot	= rot3d(mat3d(r3d)).angles(VL_APPLY_ZXY)
		rx	= (rot[0]*180.0)/3.141592654
		ry	= (rot[1]*180.0)/3.141592654
		rz	= (rot[2]*180.0)/3.141592654
		return(rx,ry,rz)
		
def ExportCameraPose():
	pg 	= tde4.getCurrentPGroup()
	cam	= tde4.getCurrentCamera()
	frame= tde4.getCurrentFrame(cam)
	typ	= tde4.getPGroupType(pg)
	if pg !=None and cam !=None:
		if typ == "CAMERA" or typ == "REF_FRAME":
			sellist = tde4.getCameraList(1)
			if len(sellist) < 2:
				#getting PGroup position and rotation...
				p3d = tde4.getPGroupPosition3D(pg,cam,frame)
				r3d = tde4.getPGroupRotation3D(pg,cam,frame)
				path	= tde4.getWidgetValue(req,"file_browser")
				#writing values to file...
				f = open(path,"w")
				f.write("%.15f %.15f %.15f %.15f %.15f %.15f "%(p3d[0],p3d[1],p3d[2],convertToAngles(r3d)[0],convertToAngles(r3d)[1],convertToAngles(r3d)[2]))
				f.close()
			else:
				tde4.postQuestionRequester(window_title,"CameraPGroup/REF Camera must be selected.", "ok")
	else:
		tde4.postQuestionRequester(window_title, "there must be a Camera and PointGroup.", "ok")	
		
def ImportObjPose():
	pg	= tde4.getCurrentPGroup()
	cam     = tde4.getCurrentCamera()
	frame   = tde4.getCurrentFrame(cam)
	frames = tde4.getCameraNoFrames(cam)
	offset = tde4.getCameraFrameOffset(cam)-1
	f_from = int(tde4.getWidgetValue(req,"from"))
	f_to = int(tde4.getWidgetValue(req,"to"))
	if pg!=None and cam !=None:
		if tde4.getPGroupType(pg)=="OBJECT":
			pg = tde4.getCurrentPGroup()
			for i_pg in tde4.getPGroupList():
				if tde4.getPGroupType(i_pg) == "CAMERA":				
					id_cpg = i_pg
					break
			id_opg = pg				
			path	= tde4.getWidgetValue(req,"file_browser")
			if path!=None:
				f	= open(path,"r")
				if not f.closed:
					string	= f.readline()
					a	= string.split()
					if len(a) == 6:
						Write_Old_Pose()
						# read values from .pose file..
						pos_x	= float(a[0])
						pos_y	= float(a[1])
						pos_z	= float(a[2])
						rot_x	= float(a[3])
						rot_y	= float(a[4])
						rot_z	= float(a[5])
						# matrix 3D...
						rot_x	= (rot_x*3.141592654)/180.0
						rot_y	= (rot_y*3.141592654)/180.0
						rot_z	= (rot_z*3.141592654)/180.0
						r3d	= mat3d(rot3d(rot_x,rot_y,rot_z,VL_APPLY_ZXY))
						r3d0	= [[r3d[0][0],r3d[0][1],r3d[0][2]],[r3d[1][0],r3d[1][1],r3d[1][2]],[r3d[2][0],r3d[2][1],r3d[2][2]]]
						# setting point group position and rotation...
						if f_from != None and f_to != None and (int(f_from)-offset) >= 1 and (int(f_from)-offset) <= frames and (int(f_to)-offset) >= 1 and (int(f_to)-offset) <= frames:
							for frame in range(f_from-offset,(f_to+1)-offset):						
								rot_cpg = mat3d(tde4.getPGroupRotation3D(id_cpg,cam,frame))
								pos_cpg = vec3d(tde4.getPGroupPosition3D(id_cpg,cam,frame))
								rot_pos_base = igl3d(rot_cpg,pos_cpg)
								rot_opg_global = r3d
								pos_opg_global = vec3d(pos_x,pos_y,pos_z)
								scale = tde4.getPGroupScale3D(id_opg)
								rot_pos_opg_new = igl3d(rot_opg_global,pos_opg_global).invert() * rot_pos_base
								tde4.setPGroupRotation3D(id_opg,cam,frame,rot_pos_opg_new.m.list())
								tde4.setPGroupPosition3D(id_opg,cam,frame,rot_pos_opg_new.v.list())
								tde4.setPGroupScale3D(id_opg,scale)
							pf_mode  = tde4.getPGroupPostfilterMode(id_opg)
							tde4.setPGroupPostfilterMode(id_opg,"POSTFILTER_OFF")
							tde4.filterPGroup(id_opg,cam)
							tde4.setPGroupPostfilterMode(id_opg,pf_mode)								
						else:
							tde4.postQuestionRequester(window_title,"Error, please enter correct frame range.","ok")								
		else:
			tde4.postQuestionRequester(window_title,"ObjectPGroup must be selected.", "ok")
	else:
		tde4.postQuestionRequester(window_title, "there must be a Camera and PointGroup.", "ok")	
		
def ExportObjPose():
	pg 	= tde4.getCurrentPGroup()
	cam	= tde4.getCurrentCamera()
	frame= tde4.getCurrentFrame(cam)
	typ	= tde4.getPGroupType(pg)
	if pg !=None and cam !=None:
		if typ == "OBJECT":
			#getting PGroup position and rotation...
			p3d = tde4.getPGroupPosition3D(pg,cam,frame)
			r3d = tde4.getPGroupRotation3D(pg,cam,frame)
			path	= tde4.getWidgetValue(req,"file_browser")
			#writing values to file...
			f = open(path,"w")
			f.write("%.15f %.15f %.15f %.15f %.15f %.15f "%(p3d[0],p3d[1],p3d[2],convertToAngles(r3d)[0],convertToAngles(r3d)[1],convertToAngles(r3d)[2]))
			f.close()
		else:
			tde4.postQuestionRequester(window_title,"ObjectPGroup must be selected.", "ok")
	else:
		tde4.postQuestionRequester(window_title, "there must be a Camera and PointGroup.", "ok")	
		
def ExportModelPose():
	currentpg	= tde4.getCurrentPGroup()
	cam     = tde4.getCurrentCamera()
	frame   = tde4.getCurrentFrame(cam)
	pgl = tde4.getPGroupList()
	for pg in pgl:
		tde4.setCurrentPGroup(pg)
		mlist = tde4.get3DModelList(pg,1)
		if len(mlist) == 1:
			model = mlist[0]
			name = tde4.get3DModelName(pg,model)
			pgname = tde4.getPGroupName(pg)
			break	
	mlist = tde4.get3DModelList(pg,1)
	if len(mlist) == 1:
		model = mlist[0]						
		pg_type = tde4.getPGroupType(pg)
		if pg!=None and cam !=None:
			model = mlist[0]
			if pg_type == "CAMERA":
				mpos = tde4.get3DModelPosition3D(pg,model,cam,frame)
				mrot  = tde4.get3DModelRotationScale3D(pg,model)
			if pg_type == "OBJECT":
				pos = tde4.get3DModelPosition3D(pg,model,cam,frame)
				rot  = tde4.get3DModelRotationScale3D(pg,model)				
				p = tde4.getPGroupPosition3D(pg,cam,frame)
				m = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
				mpos = (mat3d(m)*vec3d(pos)) + vec3d(p)
				mrot = mat3d(m) * mat3d(rot)
			rot	= rot3d(mat3d(mrot)).angles(VL_APPLY_ZXY)
			rx	= (rot[0]*180.0)/3.141592654
			ry	= (rot[1]*180.0)/3.141592654
			rz	= (rot[2]*180.0)/3.141592654
			path	= tde4.getWidgetValue(req,"file_browser")
			#writing values to file...
			f = open(path,"w")
			f.write("%.15f %.15f %.15f %.15f %.15f %.15f "%(mpos[0],mpos[1],mpos[2],rx,ry,rz))
			f.close()
			tde4.setCurrentPGroup(currentpg)
		else:
			tde4.postQuestionRequester(window_title, "there must be a Camera and PointGroup.", "ok")						
	else:
		tde4.postQuestionRequester(window_title, "Error, exactly one 3DModel must be selected.", "ok")
		
def ImportModelPose():
	currentpg	= tde4.getCurrentPGroup()
	cam     = tde4.getCurrentCamera()
	frame   = tde4.getCurrentFrame(cam)
	pgl = tde4.getPGroupList()
	for pg in pgl:
		tde4.setCurrentPGroup(pg)
		mlist = tde4.get3DModelList(pg,1)
		if len(mlist) == 1:
			model = mlist[0]
			name = tde4.get3DModelName(pg,model)
			pgname = tde4.getPGroupName(pg)
			break
	mlist = tde4.get3DModelList(pg,1)
	if len(mlist) == 1:
		model = mlist[0]					
		pg_type = tde4.getPGroupType(pg)
		mlist = tde4.get3DModelList(pg,1)		
		if pg!=None and cam !=None:
			tde4.set3DModelSurveyFlag(pg,model,0)
			path	= tde4.getWidgetValue(req,"file_browser")
			if path!=None:
				f	= open(path,"r")
				if not f.closed:
					string	= f.readline()
					a	= string.split()
					if len(a) == 6:
						# read values from .pose file..
						if pg_type == "CAMERA":
							pos_x	= float(a[0])
							pos_y	= float(a[1])
							pos_z	= float(a[2])						
							rot_x	= (float(a[3])*3.141592654)/180.0
							rot_y	= (float(a[4])*3.141592654)/180.0
							rot_z	= (float(a[5])*3.141592654)/180.0
						if pg_type == "OBJECT":
							x	= float(a[0])
							y	= float(a[1])
							z	= float(a[2])	
							p = tde4.getPGroupPosition3D(pg,cam,frame)
							m1 = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
							l = mat3d(m1).invert()*(vec3d(x,y,z) - vec3d(p))
							pos_x	= l[0]
							pos_y	= l[1]
							pos_z	= l[2]
							rot_x	= (float(a[3])*3.141592654)/180.0
							rot_y	= (float(a[4])*3.141592654)/180.0
							rot_z	= (float(a[5])*3.141592654)/180.0					
						m = mat3d(tde4.get3DModelRotationScale3D(pg,model))
						m1 = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))		
						rot_matrix	= mat3d(rot3d(rot_x,rot_y,rot_z,VL_APPLY_ZXY))
						s0 = vec3d(m[0][0],m[1][0],m[2][0]).norm2()
						s1 = vec3d(m[0][1],m[1][1],m[2][1]).norm2()
						s2 = vec3d(m[0][2],m[1][2],m[2][2]).norm2()
						scale_matrix = mat3d(s0,0.0,0.0,0.0,s1,0.0,0.0,0.0,s2)
						if pg_type == "CAMERA":
							f = rot_matrix * scale_matrix					
						if pg_type == "OBJECT":
							f = mat3d(m1).invert()*(rot_matrix * scale_matrix)
						tde4.set3DModelPosition3D(pg,model,[pos_x,pos_y,pos_z])
						tde4.set3DModelRotationScale3D(pg,model,f.list())
						tde4.setCurrentPGroup(currentpg)
				else: 
					tde4.postQuestionRequester(window_title,"there must be exactly 6 values in a row","ok")
		else:
			tde4.postQuestionRequester(window_title, "there must be a Camera and PointGroup.", "ok")	
	else:
		tde4.postQuestionRequester(window_title, "Error, exactly one 3DModel must be selected.", "ok")			

def Apply(req,widget,action):
	pg = tde4.getCurrentPGroup()
	cam = tde4.getCurrentCamera()
	frame = tde4.getCurrentFrame(cam)
	pg_type = tde4.getPGroupType(pg)
	if widget == "apply":
		menu1_value = tde4.getWidgetValue(req,"mode_menu1")
		menu2_value = tde4.getWidgetValue(req,"mode_menu2")
		if menu1_value == 1 and menu2_value == 1:
			ImportCameraPose()
			bake_post_filtered_curves()
		if menu1_value == 1 and menu2_value == 2:
			ExportCameraPose()
		if menu1_value == 2 and menu2_value == 1:
			ImportObjPose()
			bake_post_filtered_curves()
		if menu1_value == 2 and menu2_value == 2:
			ExportObjPose()
		if menu1_value == 3 and menu2_value == 1:	
			ImportModelPose()				
		if menu1_value == 3 and menu2_value == 2:	
			ExportModelPose()
		
def Disable_Widgets(req,widget,action):
	menu1_value = tde4.getWidgetValue(req,"mode_menu1")
	menu2_value = tde4.getWidgetValue(req,"mode_menu2")
	if menu1_value == 1 or menu1_value == 2:
		if  menu2_value == 1:
			tde4.setWidgetSensitiveFlag(req,"from",1)
			tde4.setWidgetSensitiveFlag(req,"to",1)
	if menu1_value == 1 or menu1_value == 2:
		if menu2_value == 2:
			tde4.setWidgetSensitiveFlag(req,"from",0)
			tde4.setWidgetSensitiveFlag(req,"to",0)		
	if menu1_value == 3:
		if menu2_value == 1 or menu2_value == 2:
			tde4.setWidgetSensitiveFlag(req,"from",0)
			tde4.setWidgetSensitiveFlag(req,"to",0)
	if menu1_value == 1 or menu1_value == 2:
		tde4.setWidgetSensitiveFlag(req,"revert",1)
	else:
		tde4.setWidgetSensitiveFlag(req,"revert",0)

#bake buffer curves...
def bake_post_filtered_curves():
	pg = tde4.getCurrentPGroup()
	cam = tde4.getCurrentCamera()
	frames = tde4.getCameraNoFrames(cam)
	pg_type = tde4.getPGroupType(pg)
	currentFrame = tde4.getCurrentFrame(cam)
	if pg_type == "CAMERA":
		for i in range(1,frames+1):
			tde4.setCurrentFrame(cam,i)
			frame = tde4.getCurrentFrame(cam)	
			pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
			rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
			scale = tde4.getPGroupScale3D(pg)
			focal = tde4.getCameraFocalLength(cam,frame)
			tde4.setPGroupPosition3D(pg,cam,frame,pos.list())
			tde4.setPGroupRotation3D(pg,cam,frame,rot.list())
			tde4.setPGroupScale3D(pg,scale)
			tde4.setCameraFocalLength(cam,frame,focal)
		pf_mode  = tde4.getPGroupPostfilterMode(pg)
		tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
		tde4.filterPGroup(pg,cam)
		tde4.setPGroupPostfilterMode(pg,pf_mode)
	if pg_type == "OBJECT":
		pg = tde4.getCurrentPGroup()
		for i_pg in tde4.getPGroupList():
			if tde4.getPGroupType(i_pg) == "CAMERA":				
				id_cpg = i_pg
				break
		id_opg = pg		
		for i in range(1,frames+1):
			tde4.setCurrentFrame(cam,i)
			frame = tde4.getCurrentFrame(cam)
			rot_cpg = mat3d(tde4.getPGroupRotation3D(id_cpg,cam,frame))
			pos_cpg = vec3d(tde4.getPGroupPosition3D(id_cpg,cam,frame))
			rot_pos_base = igl3d(rot_cpg,pos_cpg)
			rot_opg_global = mat3d(tde4.getPGroupRotation3D(id_opg,cam,frame))
			pos_opg_global = vec3d(tde4.getPGroupPosition3D(id_opg,cam,frame))
			scale = tde4.getPGroupScale3D(pg)
			rot_pos_opg_new = igl3d(rot_opg_global,pos_opg_global).invert() * rot_pos_base
			tde4.setPGroupRotation3D(id_opg,cam,frame,rot_pos_opg_new.m.list())
			tde4.setPGroupPosition3D(id_opg,cam,frame,rot_pos_opg_new.v.list())
			tde4.setPGroupScale3D(pg,scale)
		pf_mode  = tde4.getPGroupPostfilterMode(pg)
		tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
		tde4.filterPGroup(pg,cam)
		tde4.setPGroupPostfilterMode(pg,pf_mode)
	#only change from public, returns to parked frame
	tde4.setCurrentFrame(cam,currentFrame)


def Transfer_Pose(req,widget,action):
	pg = tde4.getCurrentPGroup()
	cam = tde4.getCurrentCamera()
	frame = tde4.getCurrentFrame(cam)
	frames = tde4.getCameraNoFrames(cam)
	pg_type = tde4.getPGroupType(pg)
	offset = tde4.getCameraFrameOffset(cam)-1
	f_from = int(tde4.getWidgetValue(req,"copy_frame")) - offset
	f_to = int(tde4.getWidgetValue(req,"paste_frame")) - offset
	if f_from != None and f_to != None and f_from >= 1 and f_from <= frames and f_to >= 1 and f_to <= frames:
		pos3d = tde4.getPGroupPosition3D(pg,cam,f_from)
		rot3d = tde4.getPGroupRotation3D(pg,cam,f_from)
		if pg_type == "CAMERA":
			tde4.setPGroupPosition3D(pg,cam,f_to,pos3d)
			tde4.setPGroupRotation3D(pg,cam,f_to,rot3d)
		if pg_type == "OBJECT":
			new_values = tde4.convertObjectPGroupTransformationWorldTo3DE(cam,f_to,rot3d,pos3d,1.0,0)
			tde4.setPGroupPosition3D(pg,cam,f_to,new_values[1])
			tde4.setPGroupRotation3D(pg,cam,f_to,new_values[0])
			#tde4.filterPGroup(pg,cam)
			tde4.setPGroupScale3D(pg,tde4.getPGroupScale3D(pg))
			tde4.updateGUI()
		pf_mode  = tde4.getPGroupPostfilterMode(pg)
		tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
		tde4.filterPGroup(pg,cam)
		tde4.setPGroupPostfilterMode(pg,pf_mode)
	else:
		tde4.postQuestionRequester(window_title,"Error, please enter correct frame range.","ok")			

#build GUI...

req	= tde4.createCustomRequester()

pg	= tde4.getCurrentPGroup()
cam     = tde4.getCurrentCamera()
frame   = tde4.getCurrentFrame(cam)
offset = tde4.getCameraFrameOffset(cam)-1

tde4.addFileWidget(req,"file_browser","Browse...","*.pose")
tde4.addOptionMenuWidget(req,"mode_menu1","Select Type","Camera/REF Camera","ObjectPGroup","3D Model")
tde4.setWidgetAttachModes(req,"mode_menu1","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"mode_menu1",30,95,40,0)	

tde4.addOptionMenuWidget(req,"mode_menu2","Import/Export","Import","Export")
tde4.setWidgetAttachModes(req,"mode_menu2","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"mode_menu2",30,95,80,0)

tde4.addTextFieldWidget(req,"from","Import start frame ",str(frame+offset))
tde4.setWidgetAttachModes(req,"from","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"from",30,45,115,0)

tde4.addTextFieldWidget(req,"to","Import end frame",str(frame+offset))
tde4.setWidgetAttachModes(req,"to","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"to",80,95,115,0)

tde4.addButtonWidget(req,"show_file","Show '.pose' file",50,10)
tde4.setWidgetAttachModes(req,"show_file","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"show_file",5,33,151,0)

tde4.addButtonWidget(req,"revert","Undo import",50,10)
tde4.setWidgetAttachModes(req,"revert","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"revert",36,60,151,0)

tde4.addButtonWidget(req,"apply","Import/Export Pose",70,10)
tde4.setWidgetAttachModes(req,"apply","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"apply",63,95,151,0)

tde4.addSeparatorWidget(req,"sep")
tde4.setWidgetAttachModes(req,"sep","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"sep",2,98,170,0)

tde4.addTextFieldWidget(req,"copy_frame","Copy pose from ",str(frame+offset))
tde4.setWidgetAttachModes(req,"copy_frame","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"copy_frame",25,37,190,0)

tde4.addTextFieldWidget(req,"paste_frame","Paste pose to ",str(frame+offset))
tde4.setWidgetAttachModes(req,"paste_frame","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"paste_frame",59,71,190,0)

tde4.addButtonWidget(req,"transfer_pose_btn","Transfer Pose",70,10)
tde4.setWidgetAttachModes(req,"transfer_pose_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"transfer_pose_btn",74,98,190,0)

#widget callbacks...
tde4.setWidgetCallbackFunction(req,"apply","Apply")
tde4.setWidgetCallbackFunction(req,"revert","Apply")
tde4.setWidgetCallbackFunction(req,"mode_menu1","Disable_Widgets")	
tde4.setWidgetCallbackFunction(req,"mode_menu2","Disable_Widgets")
tde4.setWidgetCallbackFunction(req,"revert","Read_Old_Pose")	
tde4.setWidgetCallbackFunction(req,"show_file","Show")
tde4.setWidgetCallbackFunction(req,"transfer_pose_btn","Transfer_Pose")

tde4.postCustomRequesterAndContinue(req,window_title,580,230,"Frame_Update")	

