# 3DE4.script.name: Pose Saver/Loader
#
# 3DE4.script.version:	v1.4.4
# 		
# 3DE4.script.gui:Main Window::3DE4
#
# 3DE4.script.comment: Imports 3D rot/pos channels from a .pose file.
#
#04-June-2015.
#
#Patcha Saheb (patchasaheb@gmail.com)


from vl_sdv import *
import math

window_title = "Patcha Pose Saver/Loader v1.4.4"

def Update(req):
	pg	= tde4.getCurrentPGroup()
	cam     = tde4.getCurrentCamera()
	frame   = tde4.getCurrentFrame(cam)
	offset = tde4.getCameraFrameOffset(cam)-1
	tde4.setWidgetValue(req,"from",str(frame+offset))
	tde4.setWidgetValue(req,"to",str(frame+offset))

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
			path	= tde4.getWidgetValue(req,"file_browser")
			if path!=None:
				f	= open(path,"r")
				if not f.closed:
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
						# setting point group position and rotation...
						if f_from != None and f_to != None and (int(f_from)-offset) >= 1 and (int(f_from)-offset) <= frames and (int(f_to)-offset) >= 1 and (int(f_to)-offset) <= frames:
							for i in range(f_from-offset,(f_to+1)-offset):						
								newvalues = tde4.convertObjectPGroupTransformationWorldTo3DE(cam, i, r3d0, [pos_x,pos_y,pos_z], 1.0, 0)
								tde4.setPGroupPosition3D(pg,cam,i,newvalues[1])
								tde4.setPGroupRotation3D(pg,cam,i,newvalues[0])
								tde4.filterPGroup(pg,cam)
								tde4.setPGroupScale3D(pg,1.0)
								tde4.updateGUI()
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
			#new_values = tde4.convertObjectPGroupTransformation3DEToWorld(cam,frame,r3d,p3d,1.0,0)
			#r3d = new_values[0]
			#p3d = new_values[1]
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
		
def Close(req,widget,action):
	tde4.unpostCustomRequester(req)	
	
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
			#focal = tde4.getCameraFocalLength(cam,frame)
			tde4.setPGroupPosition3D(pg,cam,frame,pos.list())
			tde4.setPGroupRotation3D(pg,cam,frame,rot.list())
			tde4.setPGroupScale3D(pg,scale)
			#tde4.setCameraFocalLength(cam,frame,focal)
			tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
	if pg_type == "OBJECT":
		for i in range(1,frames+1):
			tde4.setCurrentFrame(cam,i)
			frame = tde4.getCurrentFrame(cam)
			obj_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
			obj_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
			scale = tde4.getPGroupScale3D(pg)
			#focal = tde4.getCameraFocalLength(cam,frame)
			new_values = tde4.convertObjectPGroupTransformationWorldTo3DE(cam, frame, obj_rot.list(), obj_pos.list(), 1.0, 0)
			tde4.setPGroupPosition3D(pg,cam,frame,new_values[1])
			tde4.setPGroupRotation3D(pg,cam,frame,new_values[0])
			tde4.setPGroupScale3D(pg,scale)
			#tde4.setCameraFocalLength(cam,frame,focal)
			tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
	#only change from public, returns to parked frame
	tde4.setCurrentFrame(cam,currentFrame)
			

#build GUI...

req	= tde4.createCustomRequester()

pg	= tde4.getCurrentPGroup()
cam     = tde4.getCurrentCamera()
frame   = tde4.getCurrentFrame(cam)
offset = tde4.getCameraFrameOffset(cam)-1
tde4.addFileWidget(req,"file_browser","Browse...","*.pose")
tde4.addOptionMenuWidget(req,"mode_menu1","Select Type","Camera/REF Camera","ObjectPGroup","3D Model")
tde4.setWidgetAttachModes(req,"mode_menu1","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"mode_menu1",30,95,45,0)	
tde4.addOptionMenuWidget(req,"mode_menu2","Import/Export","Import","Export")
tde4.setWidgetAttachModes(req,"mode_menu2","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"mode_menu2",30,95,85,0)
tde4.addTextFieldWidget(req,"from","Import start frame ",str(frame+offset))
tde4.setWidgetAttachModes(req,"from","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"from",30,45,120,0)
tde4.addTextFieldWidget(req,"to","Import end frame",str(frame+offset))
tde4.setWidgetAttachModes(req,"to","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"to",80,95,120,0)
tde4.addSeparatorWidget(req,"sep")
tde4.setWidgetAttachModes(req,"sep","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"sep",2,98,140,0)
tde4.addButtonWidget(req,"apply","Apply",70,10)
tde4.setWidgetAttachModes(req,"apply","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"apply",65,80,160,0)
tde4.addButtonWidget(req,"close","Close",70,10)
tde4.setWidgetAttachModes(req,"close","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"close",82,97,160,0)
#widget callbacks...
tde4.setWidgetCallbackFunction(req,"apply","Apply")
tde4.setWidgetCallbackFunction(req,"close","Close")
tde4.setWidgetCallbackFunction(req,"mode_menu1","Disable_Widgets")	
tde4.setWidgetCallbackFunction(req,"mode_menu2","Disable_Widgets")	

tde4.postCustomRequesterAndContinue(req,window_title,500,190,"Update")	


