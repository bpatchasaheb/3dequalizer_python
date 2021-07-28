#
#
# 3DE4.script.name:	3D cones...
#
# 3DE4.script.version:	v1.2
#
# 3DE4.script.gui.button:	Lineup Controls::3D cones, align-bottom-left, 80, 20
# 3DE4.script.gui.button:	Orientation Controls::3D cones, align-bottom-left, 70, 20
#
# 3DE4.script.comment:	Create 3D cones on selected 3D points.
#
#16-12-2014.

# Written by Patcha Saheb(patchasaheb@gmail.com)
#copyright@2014 by Patcha Saheb.

from vl_sdv import *
import os,sys
import math

# Creating 3D Model...

window_title = "Patcha 3D cones v1.2"
def create_cone():
	pg = tde4.getCurrentPGroup()
	m = tde4.create3DModel(pg, 4)
	tde4.set3DModelName(pg, m, "3Dcone")
	i0 = tde4.add3DModelVertex(pg, m, [0.0, 0.0, 0.0])
	i1 = tde4.add3DModelVertex(pg, m, [-0.361,1.798, -0.358])
	i2 = tde4.add3DModelVertex(pg, m, [-0.361,1.798, 0.358])
	i3 = tde4.add3DModelVertex(pg, m, [0.361, 1.798, -0.358])
	i4 = tde4.add3DModelVertex(pg, m, [0.361, 1.798, 0.358])
	tde4.add3DModelLine(pg, m, [i0,i1])
	tde4.add3DModelLine(pg, m, [i0,i2])
	tde4.add3DModelLine(pg, m, [i0,i3])
	tde4.add3DModelLine(pg, m, [i0,i4])
	tde4.add3DModelLine(pg, m, [i1,i2])
	tde4.add3DModelLine(pg, m, [i1,i3])
	tde4.add3DModelLine(pg, m, [i2,i4])
	tde4.add3DModelLine(pg, m, [i3,i4])
	tde4.add3DModelFace(pg,m,[i0,i3,i4,i0])
	tde4.add3DModelFace(pg,m,[i0,i1,i3,i0])
	tde4.add3DModelFace(pg,m,[i0,i2,i1,i0])
	tde4.add3DModelFace(pg,m,[i0,i4,i2,i0])
	tde4.add3DModelFace(pg,m,[i1,i2,i4,i3,i1])
	tde4.set3DModelSurveyFlag(pg, m, 0)
	tde4.set3DModelPosition3D(pg, m, p3d)
	
#Functions...
	
def Naming():
	c = tde4.getCurrentCamera()
	pg = tde4.getCurrentPGroup()
	frame = tde4.getCurrentFrame(c)
	mlist = tde4.get3DModelList(pg,0)
	pl = tde4.getPointList(pg,1)
	for p in pl:
		if tde4.isPointCalculated3D(pg, p):
				p3d = tde4.getPointCalcPosition3D(pg, p)
		for m in mlist:
			name = tde4.get3DModelName(pg,m) 
			if name == "3Dcone":
				mpos = tde4.get3DModelPosition3D(pg,m,c,frame)
				if p3d == mpos:
					n = tde4.getPointName(pg,p)
					na = "3Dcone" + " " + n
					tde4.set3DModelName(pg,m,na)
					
def ConesList():
	pg = tde4.getCurrentPGroup()
	mlist = tde4.get3DModelList(pg,0)
	l = []
	for m in mlist:
		name = tde4.get3DModelName(pg,m)
		if name.startswith("3Dcone") == True:
			l.append(m)
	return l

def CreateModel(req,widget,action):
	global p3d
	c = tde4.getCurrentCamera()
	pg = tde4.getCurrentPGroup()
	if  c!=None and pg != None:
		frame = tde4.getCurrentFrame(c)
		pl = tde4.getPointList(pg,1)
		if len(pl) > 0:
			if len(ConesList())>0 and len(pl) >0:
				count = 0
				for p in pl:
					if tde4.isPointCalculated3D(pg, p):
						p3d = tde4.getPointCalcPosition3D(pg, p)
					for m in ConesList():
						mpos = tde4.get3DModelPosition3D(pg,m,c,frame)
						if p3d != mpos:
							count = count +1
						else:
							break
					if count == len(ConesList()):
						create_cone()
						Naming()
					count = 0
			else:
				if len(pl) > 0:
					for p in pl:
						if tde4.isPointCalculated3D(pg, p):
							p3d = tde4.getPointCalcPosition3D(pg, p)
							create_cone()
							Naming()
		else:
			tde4.postQuestionRequester(window_title, "Error, atleast one 3d point must be selected.", "Ok")
	else:
			tde4.postQuestionRequester(window_title, "Error, there is no point group or camera.", "OK")		

def Scaling(req,widget,action):
	pg = tde4.getCurrentPGroup()
	c = tde4.getCurrentCamera()
	if c!= None and pg!=None:
		mlist = tde4.get3DModelList(pg,1)
		if len(mlist) != 0:
			s = float(tde4.getWidgetValue(req,"scale_slider"))
			f = float(tde4.getWidgetValue(req,"scale_factor"))
			mode = tde4.getWidgetValue(req,"mode_menu")
			for model in mlist:
				#Extract scale & rotation matrices...
				m = mat3d(tde4.get3DModelRotationScale3D(pg,model))
				s0 = vec3d(m[0][0],m[1][0],m[2][0]).norm2()
				s1 = vec3d(m[0][1],m[1][1],m[2][1]).norm2()
				s2 = vec3d(m[0][2],m[1][2],m[2][2]).norm2()
				scale_Matrix = mat3d(s0,0.0,0.0,0.0,s1,0.0,0.0,0.0,s2)
				m_rot = m * mat3d(1.0/s0,0.0,0.0,0.0,1.0/s1,0.0,0.0,0.0,1.0/s2)
				rot_Matrix = mat3d(rot3d(m_rot),VL_APPLY_ZXY)
				if mode == 1:
					sm1= mat3d(s,0.0,0.0,0.0,s,0.0,0.0,0.0,s)
					f1 = rot_Matrix * sm1
					tde4.set3DModelRotationScale3D(pg,model,f1.list())
				if mode == 2:
					sm2 = mat3d(f,0.0,0.0,0.0,f,0.0,0.0,0.0,f)
					f2 = rot_Matrix * sm2
					tde4.set3DModelRotationScale3D(pg,model,f2.list())
		else:
			tde4.postQuestionRequester(window_title, "Error, atleast one 3d model must be selected.", "Ok")
	else:
			tde4.postQuestionRequester(window_title, "Error, there is no point group or camera.", "OK")	

def Sensitivity(req,widget,action):
	j = tde4.getWidgetValue(req,"mode_menu")
	tde4.setWidgetSensitiveFlag(req,"scale_slider",(1-j)+1)
	tde4.setWidgetSensitiveFlag(req,"scale_factor",j-1)
	
def SelectAll(req,widget,action):
	pg = tde4.getCurrentPGroup()
	c = tde4.getCurrentCamera()
	if c!=None and pg!=None:
		if len(ConesList()) > 0:
			for m in ConesList():
				tde4.set3DModelSelectionFlag(pg,m,1)
		else:
			tde4.postQuestionRequester(window_title,"Error, there are no 3D cones.","OK")
	else:
			tde4.postQuestionRequester(window_title, "Error, there is no point group or camera.", "OK")	
			
def DeSelectAll(req,widget,action):
	pg = tde4.getCurrentPGroup()
	c = tde4.getCurrentCamera()
	if c!=None and pg!=None:
		mlist = tde4.get3DModelList(pg,1)
		for m in mlist:
			name = tde4.get3DModelName(pg,m)
			tde4.set3DModelSelectionFlag(pg,m,0)
	else:
			tde4.postQuestionRequester(window_title, "Error, there is no point group or camera.", "OK")	
	
def GetCones(req,widget,action):
	pg = tde4.getCurrentPGroup()
	c = tde4.getCurrentCamera()
	mlist = tde4.get3DModelList(pg,0)
	if c!=None and pg!=None:
		for m in mlist:
			name = tde4.get3DModelName(pg,m)
			tde4.set3DModelSelectionFlag(pg,m,0)
		frame = tde4.getCurrentFrame(c)
		pl = tde4.getPointList(pg, 1)
		if len(pl) > 0: 
			for p in pl:
				if tde4.isPointCalculated3D(pg, p):
					p3d = tde4.getPointCalcPosition3D(pg, p)
					for m in ConesList():
						mpos = tde4.get3DModelPosition3D(pg,m,c,frame)
						if p3d == mpos:
							tde4.set3DModelSelectionFlag(pg,m,1)
		else:
			tde4.postQuestionRequester(window_title, "Error, atleast one 3d point must be selected.", "Ok")
	else:
			tde4.postQuestionRequester(window_title, "Error, there is no point group or camera.", "OK")				
	
def DeleteCones(req,widget,action):
	pg = tde4.getCurrentPGroup()
	c = tde4.getCurrentCamera()
	if c!=None and pg!=None:
		if len(ConesList()) > 0:		
			for m in ConesList():	
				tde4.delete3DModel(pg,m)
		else:
			tde4.postQuestionRequester(window_title,"Error, there are no 3D cones.","OK")
	else:
			tde4.postQuestionRequester(window_title, "Error, there is no point group or camera.", "OK")	
			
def Color(req,widget,action):
	pg = tde4.getCurrentPGroup()
	c = tde4.getCurrentCamera()
	mlist = tde4.get3DModelList(pg,1)
	if c!=None and pg!=None:
		frame = tde4.getCurrentFrame(c)
		alp = tde4.getWidgetValue(req,"alpha_slider")
		if len(mlist) > 0:
			for m in mlist:
				if tde4.getWidgetValue(req,"red") == 1:
					tde4.set3DModelColor(pg,m,1.0,0.0,0.0,alp)
				if tde4.getWidgetValue(req,"green") == 1:
					tde4.set3DModelColor(pg,m,0.0,1.0,0.0,alp)		
				if tde4.getWidgetValue(req,"blue") == 1:
					tde4.set3DModelColor(pg,m,0.0,0.0,1.0,alp)				
				if tde4.getWidgetValue(req,"purple") == 1:
					tde4.set3DModelColor(pg,m,1.0,0.0,1.0,alp)
				if tde4.getWidgetValue(req,"yellow") == 1:
					tde4.set3DModelColor(pg,m,1.0,1.0,0.0,alp)
				if tde4.getWidgetValue(req,"black") == 1:
					tde4.set3DModelColor(pg,m,0.0,0.0,0.0,alp)	
				if tde4.getWidgetValue(req,"white") == 1:
					tde4.set3DModelColor(pg,m,1.0,1.0,1.0,alp)
				if tde4.getWidgetValue(req,"cyan") == 1:
					tde4.set3DModelColor(pg,m,0.22,0.45,0.65,alp)
		else:
			tde4.postQuestionRequester(window_title, "Error, atleast one 3d model must be selected.", "Ok")
	else:
			tde4.postQuestionRequester(window_title, "Error, there is no point group or camera.", "OK")	
		
def Show(req,widget,action):
	c = tde4.getCurrentCamera()
	pg = tde4.getCurrentPGroup()
	mlist = tde4.get3DModelList(pg,1)	
	if c!=None and pg!=None:
		frame = tde4.getCurrentFrame(c)
		pl = tde4.getPointList(pg, 1)
		i0 = tde4.getWidgetValue(req,"showall")
		i1 = tde4.getWidgetValue(req,"hideall")
		i2 = tde4.getWidgetValue(req,"showselected")
		i3 = tde4.getWidgetValue(req,"hideselected")
		if i0 == 1:
			for m in ConesList():
				tde4.set3DModelVisibleFlag(pg,m,1)
		if i1 == 1:
			for m in ConesList():
				tde4.set3DModelVisibleFlag(pg,m,0)
		if i2 == 1:
			if len(mlist) > 0:
				for cone in ConesList():
					tde4.set3DModelVisibleFlag(pg,cone,0)
				for m in mlist:
					tde4.set3DModelVisibleFlag(pg,m,1)
			else:
				tde4.postQuestionRequester(window_title,"Error, atleast one 3D model must be selected","OK")					
		if i3 == 1:
			if len(mlist) > 0:
				for cone in ConesList():
					tde4.set3DModelVisibleFlag(pg,cone,1)
				for m in mlist:
					tde4.set3DModelVisibleFlag(pg,m,0)
			else:
				tde4.postQuestionRequester(window_title,"Error, atleast one 3D model must be selected","OK")
	else:
			tde4.postQuestionRequester(window_title, "Error, there is no point group or camera.", "OK")	

def Snaping(req,widget,action):
	pg = tde4.getCurrentPGroup()
	c = tde4.getCurrentCamera()
	if c!=None and pg!=None:
		frame = tde4.getCurrentFrame(c)
		mlist = tde4.get3DModelList(pg,0)
		pl = tde4.getPointList(pg, 0)
		l = []
		for m in mlist:
			name = tde4.get3DModelName(pg,m)
			if name.startswith("3Dcone") == True:
				l.append(name)
		n0 = []
		for n in l:
			i = n[7:]
			n0.append(i)
		for p in pl:
			pname = tde4.getPointName(pg,p)
			if tde4.isPointCalculated3D(pg, p):
				p3d = tde4.getPointCalcPosition3D(pg, p)
				for n1 in n0:
					if pname == n1:
						n2 = "3Dcone"+ " " + n1
						for m2 in ConesList():
							if tde4.get3DModelName(pg,m2) == n2:
								tde4.set3DModelPosition3D(pg,m2,p3d)
	else:
			tde4.postQuestionRequester(window_title, "Error, there is no point group or camera.", "OK")	
							
def Rotate(req,widget,action):
	pg = tde4.getCurrentPGroup()
	c = tde4.getCurrentCamera()
	if c!=None and pg!=None:
		mlist = tde4.get3DModelList(pg,1)
		frame = tde4.getCurrentFrame(c)
		if len(mlist) > 0:
			for model in mlist:
				#Convert to Angles...
				rot_x = float(tde4.getWidgetValue(req,"rotx")) *  math.pi /180.0
				rot_y = float(tde4.getWidgetValue(req,"roty")) *  math.pi /180.0
				rot_z = float(tde4.getWidgetValue(req,"rotz")) *  math.pi /180.0
				rot_Matrix = mat3d(rot3d(rot_x,rot_y,rot_z,VL_APPLY_ZXY))
				m = mat3d(tde4.get3DModelRotationScale3D(pg,model))
				s0 = vec3d(m[0][0],m[1][0],m[2][0]).norm2()
				s1 = vec3d(m[0][1],m[1][1],m[2][1]).norm2()
				s2 = vec3d(m[0][2],m[1][2],m[2][2]).norm2()
				scale_Matrix = mat3d(s0,0.0,0.0,0.0,s1,0.0,0.0,0.0,s2)
				f = rot_Matrix * scale_Matrix					
				tde4.set3DModelRotationScale3D(pg,model,f.list())
		else:
			tde4.postQuestionRequester(window_title, "Error, atleast one 3d model must be selected.", "Ok")
	else:
			tde4.postQuestionRequester(window_title, "Error, there is no point group or camera.", "OK")	
			
def Translate(req,widget,action):
	pg = tde4.getCurrentPGroup()
	c = tde4.getCurrentCamera()
	x = float(tde4.getWidgetValue(req,"posx"))
	y = float(tde4.getWidgetValue(req,"posy"))
	z = float(tde4.getWidgetValue(req,"posz"))
	if c!=None and pg!=None:
		mlist = tde4.get3DModelList(pg,1)
		frame = tde4.getCurrentFrame(c)
		if len(mlist) > 0:
			for model in mlist:
				pos = vec3d(tde4.get3DModelPosition3D(pg,model,c,frame))
				pos_x = float(pos[0] + x)
				pos_y = float(pos[1] + y)
				pos_z = float(pos[2] + z)
				tde4.set3DModelPosition3D(pg,model,[pos_x,pos_y,pos_z])
		else:
			tde4.postQuestionRequester(window_title, "Error, atleast one 3d model must be selected.", "Ok")
	else:
			tde4.postQuestionRequester(window_title, "Error, there is no point group or camera.", "OK")					
			
def copyright(req,widget,action):
	print "copyright@2014 by Patcha Saheb."	
		
	
#Build UI....		
			
try:
	req	= _scale_requester
except (ValueError,NameError,TypeError):
	req	= tde4.createCustomRequester()
	_scale_requester	= req

	tde4.addMenuBarWidget(req,"menu_bar")
	tde4.setWidgetAttachModes(req,"menu_bar","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
	tde4.setWidgetOffsets(req,"menu_bar",0,100,1,0)
	#view menu
	tde4.addMenuWidget(req,"view_menu","View","menu_bar",1)
	tde4.addMenuToggleWidget(req,"showall","Show all 3D cones","view_menu", 1)
	tde4.addMenuToggleWidget(req,"hideall","Hide all 3D cones","view_menu", )
	tde4.addMenuToggleWidget(req,"showselected","Show selected 3D cones","view_menu", 0)
	tde4.addMenuToggleWidget(req,"hideselected","Hide selected 3D cones","view_menu", 0)
	#color menu
	tde4.addMenuWidget(req,"color_menu","Color","menu_bar",1)
	tde4.addMenuToggleWidget(req,"red","Red","color_menu",0)
	tde4.addMenuToggleWidget(req,"green","Green","color_menu",0)
	tde4.addMenuToggleWidget(req,"blue","Blue","color_menu",0)
	tde4.addMenuToggleWidget(req,"purple","Purple","color_menu",0)
	tde4.addMenuToggleWidget(req,"yellow","Yellow","color_menu",0)
	tde4.addMenuToggleWidget(req,"black","Black","color_menu",0)
	tde4.addMenuToggleWidget(req,"white","White","color_menu",0)
	tde4.addMenuToggleWidget(req,"cyan","Cyan","color_menu",1)
	#copyright menu
	tde4.addMenuWidget(req,"about","About","menu_bar")
	tde4.addMenuButtonWidget(req,"copyright","Copyright","about")
	#widgets
	tde4.addOptionMenuWidget(req,"mode_menu","Mode of Operation","Scale Slider","Scale Factor")
	tde4.addScaleWidget(req,"scale_slider","Scale Slider","DOUBLE",1.0,100.0,1.0)
	tde4.addTextFieldWidget(req, "scale_factor", "Scale Factor", "0.5")
	tde4.setWidgetSensitiveFlag(req,"scale_factor",0)
	tde4.addScaleWidget(req,"alpha_slider","Alpha","DOUBLE",0.0,1.0,0.32)
	tde4.addButtonWidget(req,"create","Create",90,10)
	tde4.setWidgetAttachModes(req,"create","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
	tde4.setWidgetOffsets(req,"create",3,15,135,0)
	tde4.addButtonWidget(req,"Selectall","SelectAll",90,10,"create")
	tde4.addButtonWidget(req,"Deselect","DeselectAll",90,10,"Selectall")
	tde4.addButtonWidget(req,"Getcones","Cone on Point",90,10,"Deselect")
	tde4.addButtonWidget(req,"snap","Snap",90,10,"Getcones")
	tde4.addButtonWidget(req,"Deleteall","DeleteAll",90,10,"snap")
	#callback
	tde4.setWidgetCallbackFunction(req,"create","CreateModel")
	tde4.setWidgetCallbackFunction(req,"mode_menu","Sensitivity")
	tde4.setWidgetCallbackFunction(req,"scale_slider","Scaling")
	tde4.setWidgetCallbackFunction(req,"scale_factor","Scaling")
	tde4.setWidgetCallbackFunction(req,"Selectall","SelectAll")
	tde4.setWidgetCallbackFunction(req,"Deselect","DeSelectAll")
	tde4.setWidgetCallbackFunction(req,"Getcones","GetCones")
	tde4.setWidgetCallbackFunction(req,"Deleteall","DeleteCones")
	tde4.setWidgetCallbackFunction(req,"snap","Snaping")
	tde4.setWidgetCallbackFunction(req,"view_menu","Show")
	tde4.setWidgetCallbackFunction(req,"color_menu","Color")
	tde4.setWidgetCallbackFunction(req,"alpha_slider","Color")
	tde4.setWidgetCallbackFunction(req,"about","copyright")
	#textbox
	tde4.addSeparatorWidget(req,"Separate")
	tde4.addTextFieldWidget(req,"rotx","X","0.0")
	tde4.setWidgetAttachModes(req,"rotx","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
	tde4.setWidgetOffsets(req,"rotx",15,30,185,0)
	tde4.addTextFieldWidget(req,"roty","Y","0.0")
	tde4.setWidgetAttachModes(req,"roty","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
	tde4.setWidgetOffsets(req,"roty",35,50,185,0)
	tde4.addTextFieldWidget(req,"rotz","Z","0.0")
	tde4.setWidgetAttachModes(req,"rotz","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
	tde4.setWidgetOffsets(req,"rotz",55,70,185,0)	
	tde4.addButtonWidget(req,"rot","Rotate",70,10,"rotz")
	tde4.setWidgetCallbackFunction(req,"rot","Rotate")
	tde4.addTextFieldWidget(req,"posx","X","0.0")
	tde4.setWidgetAttachModes(req,"posx","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
	tde4.setWidgetOffsets(req,"posx",15,30,220,0)
	tde4.addTextFieldWidget(req,"posy","Y","0.0")
	tde4.setWidgetAttachModes(req,"posy","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
	tde4.setWidgetOffsets(req,"posy",35,50,220,0)
	tde4.addTextFieldWidget(req,"posz","Z","0.0")
	tde4.setWidgetAttachModes(req,"posz","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
	tde4.setWidgetOffsets(req,"posz",55,70,220,0)	
	tde4.addButtonWidget(req,"pos","Translate",70,10,"posz")
	tde4.setWidgetCallbackFunction(req,"pos","Translate")
	
	
	
tde4.postCustomRequesterAndContinue(req,window_title,610,250)

		
