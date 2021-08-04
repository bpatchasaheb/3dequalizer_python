# 3DE4.script.name:Nudge3D...
# 3DE4.script.version:	 v1.3
# 3DE4.script.gui.button:	Lineup Controls::Nudge3D, align-bottom-left, 80, 20
# 3DE4.script.gui.button:	Orientation Controls::Nudge3D, align-bottom-left, 70, 20
# 3DE4.script.gui:	Lineup Controls::Edit
# 3DE4.script.gui:	Orientation Controls::Edit
# 3DE4.script.comment:	Nudges translation, rotation and scale, of Cameras, Objects, 3D Models or Motion paths, in Local, Global, Screen space.
# Author : Patcha Saheb (patchasaheb@gmail.com) and Michael Karp (mckarp@aol.com)



from vl_sdv import *
import math


class Nudge():

	def main(self):
		self.GUI()

#update function...		
	def update(self,requester):
		self.req = requester
		s_type = tde4.getWidgetValue(self.req,"selected_menu")	
		pg =tde4.getCurrentPGroup()
		cam = tde4.getCurrentCamera()
		frame = tde4.getCurrentFrame(cam)
		offset = tde4.getCameraFrameOffset(cam)-1
		pl = tde4.getPointList(pg,1)
		r_space = tde4.getWidgetValue(self.req,"r_space")
		if s_type == 2:	
			tde4.setWidgetValue(self.req,"sel",str(tde4.getPGroupName(tde4.getCurrentPGroup())))
		if s_type == 3:
			l = []
			mlist = tde4.get3DModelList(pg,1)
			for model in mlist:
				name = tde4.get3DModelName(pg,model)
				l.append(name)
			tde4.setWidgetValue(self.req,"sel",str(l))

#increment sensitive funciton...
	def Increment_Sensitive(self,requester,widget,action):
		self.req = requester
		self.widget = widget
		self.action = action
		s_type = tde4.getWidgetValue(self.req,"selected_menu")
#getting widgets values...
		t_slider_v = tde4.getWidgetValue(self.req,"t_increment")
		t_factor_v = tde4.getWidgetValue(self.req,"t_increment_factor")
		r_slider_v = tde4.getWidgetValue(self.req,"r_increment")
		r_factor_v = tde4.getWidgetValue(self.req,"r_increment_factor")
		s_slider_v = tde4.getWidgetValue(self.req,"s_increment")
		s_factor_v = tde4.getWidgetValue(self.req,"s_increment_factor")
#translation increment sensitive...
		if self.widget == "t_increment":
			tde4.setWidgetValue(self.req,"t_increment_factor",str(t_slider_v))
		if self.widget == "t_increment_factor":
			if float(t_factor_v) > 0.1:
				tde4.setWidgetSensitiveFlag(self.req,"t_increment",0)
			else:
				tde4.setWidgetSensitiveFlag(self.req,"t_increment",1)
				tde4.setWidgetValue(self.req,"t_increment",str(t_factor_v))
#rotation increment sensitive...
		if self.widget == "r_increment":
			tde4.setWidgetValue(self.req,"r_increment_factor",str(r_slider_v))
		if self.widget == "r_increment_factor":
			if float(r_factor_v) > 0.1:
				tde4.setWidgetSensitiveFlag(self.req,"r_increment",0)
			else:
				tde4.setWidgetSensitiveFlag(self.req,"r_increment",1)
				tde4.setWidgetValue(self.req,"r_increment",str(r_factor_v))
#scale increment sensitive...
		if self.widget == "s_increment":
			tde4.setWidgetValue(self.req,"s_increment_factor",str(s_slider_v))
		if self.widget == "s_increment_factor":
			if float(s_factor_v) > 1.0:
				tde4.setWidgetSensitiveFlag(self.req,"s_increment",0)
			else:
				tde4.setWidgetSensitiveFlag(self.req,"s_increment",1)
				tde4.setWidgetValue(self.req,"s_increment",str(s_factor_v))
		if s_type == 4:
			tde4.setWidgetSensitiveFlag(self.req,"s_increment",0)
			if not float(tde4.getWidgetValue(self.req,"s_increment_factor")) <= 0.1:
				tde4.postQuestionRequester(self.window_title,"Error, maximum increment value is 0.1.","Ok")
				tde4.setWidgetValue(self.req,"s_increment_factor","0.1")

#pivot option menu edit...	
	def Pivot_Menu_Edit(self,requester,widget,action):
		self.req = requester
		self.widget = widget
		self.action = action
		s_type = tde4.getWidgetValue(self.req,"selected_menu")
		pg =tde4.getCurrentPGroup()
		cam = tde4.getCurrentCamera()
		frame = tde4.getCurrentFrame(cam)
		pl = tde4.getPointList(pg,1)
		name = tde4.getCameraName(cam)
		t_space = tde4.getWidgetValue(self.req,"t_space")
		r_space = tde4.getWidgetValue(self.req,"r_space")			
		if s_type == 1:
			tde4.modifyOptionMenuWidget(self.req,"t_space","Pivot Space","Global","Local/Screen")
			tde4.modifyOptionMenuWidget(self.req,"r_space","Pivot Space","Global","Local/Screen","Around 3DPoint - Global","Around 3DPoint - Local")	
			tde4.setWidgetValue(self.req,"sel",str(tde4.getCameraName(tde4.getCurrentCamera())))
			tde4.setWidgetValue(self.req,"look"," ")
			tde4.setWidgetSensitiveFlag(self.req,"move_3dmodels",0)
			if r_space == 1 or r_space == 2:
				tde4.setWidgetSensitiveFlag(self.req,"pick_pivot",0)
				tde4.setWidgetSensitiveFlag(self.req,"avg_3dpoint",0)
			else:
				tde4.setWidgetSensitiveFlag(self.req,"pick_pivot",1)
				tde4.setWidgetSensitiveFlag(self.req,"avg_3dpoint",1)				
		if s_type == 2:
			tde4.modifyOptionMenuWidget(self.req,"t_space","Pivot Space","Global","Local","Screen")
			tde4.modifyOptionMenuWidget(self.req,"r_space","Pivot Space","Global","Local","Screen","Around 3DPoint - Global","Around 3DPoint - Local")
			tde4.setWidgetValue(self.req,"sel",str(tde4.getPGroupName(tde4.getCurrentPGroup())))
			tde4.setWidgetSensitiveFlag(self.req,"move_3dmodels",0)	
			if t_space == 3 or r_space == 3:
				tde4.setWidgetValue(self.req,"look",str(tde4.getCameraName(tde4.getCurrentCamera())))	
			else:
				tde4.setWidgetValue(self.req,"look"," ")
			if r_space == 1 or r_space == 2 or r_space == 3:
				tde4.setWidgetSensitiveFlag(self.req,"pick_pivot",0)
				tde4.setWidgetSensitiveFlag(self.req,"avg_3dpoint",0)
			else:
				tde4.setWidgetSensitiveFlag(self.req,"pick_pivot",1)
				tde4.setWidgetSensitiveFlag(self.req,"avg_3dpoint",1)				
		if s_type == 3:
			tde4.setWidgetSensitiveFlag(self.req,"move_3dmodels",0)
			l = []
			mlist = tde4.get3DModelList(pg,1)
			for model in mlist:
				name = tde4.get3DModelName(pg,model)
				l.append(name)
			tde4.modifyOptionMenuWidget(self.req,"t_space","Pivot Space","Global","Local","Screen")
			tde4.modifyOptionMenuWidget(self.req,"r_space","Pivot Space","Global","Local","Screen","Around 3DPoint - Global","Around 3DPoint - Local")
			tde4.setWidgetValue(self.req,"sel",str(l))
			if t_space == 3 or r_space == 3:
				tde4.setWidgetValue(self.req,"look",str(tde4.getCameraName(tde4.getCurrentCamera())))
			else:
				tde4.setWidgetValue(self.req,"look"," ")
		if s_type == 3: 
				if r_space == 1 or r_space == 2 or r_space == 3:
					tde4.setWidgetSensitiveFlag(self.req,"pick_pivot",0)
					tde4.setWidgetSensitiveFlag(self.req,"avg_3dpoint",0)
				else:
					tde4.setWidgetSensitiveFlag(self.req,"pick_pivot",1)
					tde4.setWidgetSensitiveFlag(self.req,"avg_3dpoint",1)							
		if s_type == 4:
			tde4.setWidgetSensitiveFlag(self.req,"move_3dmodels",1)
			tde4.modifyOptionMenuWidget(self.req,"t_space","Pivot Space","Global")
			tde4.modifyOptionMenuWidget(self.req,"r_space","Pivot Space","Global","Local","Around 3DPoint - Global","Around 3DPoint - Local")
			tde4.setWidgetSensitiveFlag(self.req,"scale_around_pivot",1)
			tde4.setWidgetValue(self.req,"sel"," ")
			tde4.setWidgetValue(self.req,"look"," ")
		else:
			tde4.setWidgetSensitiveFlag(self.req,"scale_around_pivot",0)
			#tde4.setWidgetSensitiveFlag(self.req,"toggle",1)
		if s_type == 4:
			if r_space == 1 or r_space == 2:
				tde4.setWidgetSensitiveFlag(self.req,"pick_pivot",0)
				tde4.setWidgetSensitiveFlag(self.req,"avg_3dpoint",0)			
			else:
				tde4.setWidgetSensitiveFlag(self.req,"pick_pivot",1)
				tde4.setWidgetSensitiveFlag(self.req,"avg_3dpoint",1)
#disable/enable scale buttons...	
		if s_type == 1 or s_type == 2 or s_type == 4:
			tde4.setWidgetSensitiveFlag(self.req,"rot_x+",1)
			tde4.setWidgetSensitiveFlag(self.req,"rot_x-",1)
			tde4.setWidgetSensitiveFlag(self.req,"rot_y+",1)
			tde4.setWidgetSensitiveFlag(self.req,"rot_y-",1)
			tde4.setWidgetSensitiveFlag(self.req,"rot_z+",1)	
			tde4.setWidgetSensitiveFlag(self.req,"rot_z-",1)
			#tde4.setWidgetSensitiveFlag(self.req,"r_increment",1)
			#tde4.setWidgetSensitiveFlag(self.req,"r_increment_factor",1)
			tde4.setWidgetSensitiveFlag(self.req,"r_space",1)	
			tde4.setWidgetSensitiveFlag(self.req,"scale_x+",0)
			tde4.setWidgetSensitiveFlag(self.req,"scale_x-",0)
			tde4.setWidgetSensitiveFlag(self.req,"scale_y+",0)
			tde4.setWidgetSensitiveFlag(self.req,"scale_y-",0)
			tde4.setWidgetSensitiveFlag(self.req,"scale_z+",0)
			tde4.setWidgetSensitiveFlag(self.req,"scale_z-",0)
			tde4.setWidgetSensitiveFlag(self.req,"uniform_scale+",0)
			tde4.setWidgetSensitiveFlag(self.req,"uniform_scale-",0)
			tde4.setWidgetSensitiveFlag(self.req,"s_increment",0)
			tde4.setWidgetSensitiveFlag(self.req,"s_increment_factor",0)
		if s_type == 3:
			tde4.setWidgetSensitiveFlag(self.req,"rot_x+",1)
			tde4.setWidgetSensitiveFlag(self.req,"rot_x-",1)
			tde4.setWidgetSensitiveFlag(self.req,"rot_y+",1)
			tde4.setWidgetSensitiveFlag(self.req,"rot_y-",1)
			tde4.setWidgetSensitiveFlag(self.req,"rot_z+",1)	
			tde4.setWidgetSensitiveFlag(self.req,"rot_z-",1)
			#tde4.setWidgetSensitiveFlag(self.req,"r_increment",1)
			#tde4.setWidgetSensitiveFlag(self.req,"r_increment_factor",1)
			tde4.setWidgetSensitiveFlag(self.req,"r_space",1)	
			tde4.setWidgetSensitiveFlag(self.req,"scale_x+",1)
			tde4.setWidgetSensitiveFlag(self.req,"scale_x-",1)
			tde4.setWidgetSensitiveFlag(self.req,"scale_y+",1)
			tde4.setWidgetSensitiveFlag(self.req,"scale_y-",1)
			tde4.setWidgetSensitiveFlag(self.req,"scale_z+",1)
			tde4.setWidgetSensitiveFlag(self.req,"scale_z-",1)
			tde4.setWidgetSensitiveFlag(self.req,"uniform_scale+",1)
			tde4.setWidgetSensitiveFlag(self.req,"uniform_scale-",1)
			tde4.setWidgetSensitiveFlag(self.req,"s_increment",1)
			tde4.setWidgetSensitiveFlag(self.req,"s_increment_factor",1)
		if s_type == 1 or s_type == 2:										
			tde4.setWidgetSensitiveFlag(self.req,"rot_x+",1)
			tde4.setWidgetSensitiveFlag(self.req,"rot_x-",1)
			tde4.setWidgetSensitiveFlag(self.req,"rot_y+",1)
			tde4.setWidgetSensitiveFlag(self.req,"rot_y-",1)
			tde4.setWidgetSensitiveFlag(self.req,"rot_z+",1)	
			tde4.setWidgetSensitiveFlag(self.req,"rot_z-",1)
			#tde4.setWidgetSensitiveFlag(self.req,"r_increment",1)
			#tde4.setWidgetSensitiveFlag(self.req,"r_increment_factor",1)
			tde4.setWidgetSensitiveFlag(self.req,"r_space",1)										
			tde4.setWidgetSensitiveFlag(self.req,"scale_x+",0)
			tde4.setWidgetSensitiveFlag(self.req,"scale_x-",0)
			tde4.setWidgetSensitiveFlag(self.req,"scale_y+",0)
			tde4.setWidgetSensitiveFlag(self.req,"scale_y-",0)
			tde4.setWidgetSensitiveFlag(self.req,"scale_z+",0)
			tde4.setWidgetSensitiveFlag(self.req,"scale_z-",0)
			tde4.setWidgetSensitiveFlag(self.req,"uniform_scale+",0)
			tde4.setWidgetSensitiveFlag(self.req,"uniform_scale-",0)
			tde4.setWidgetSensitiveFlag(self.req,"scale_around_pivot",0)
			tde4.setWidgetSensitiveFlag(self.req,"s_increment",0)
			tde4.setWidgetSensitiveFlag(self.req,"s_increment_factor",0)
		if s_type == 4:
			tde4.setWidgetSensitiveFlag(self.req,"uniform_scale+",1)
			tde4.setWidgetSensitiveFlag(self.req,"uniform_scale-",1)
			tde4.setWidgetSensitiveFlag(self.req,"s_increment",0)
			tde4.setWidgetSensitiveFlag(self.req,"s_increment_factor",1)
			tde4.setWidgetValue(self.req,"s_increment_factor","0.1")
		else:
			tde4.setWidgetValue(self.req,"scale_around_pivot","0")
			"""if s_type == 1 or s_type == 2:
				tde4.setWidgetSensitiveFlag(self.req,"pick_frame_in",0)
				tde4.setWidgetSensitiveFlag(self.req,"pick_frame_out",0)
				tde4.setWidgetSensitiveFlag(self.req,"set_key",0)
				tde4.setWidgetValue(self.req,"toggle","0")
			if s_type == 3 or s_type == 4:
				tde4.setWidgetSensitiveFlag(self.req,"pick_frame_in",0)
				tde4.setWidgetSensitiveFlag(self.req,"pick_frame_out",0)
				tde4.setWidgetSensitiveFlag(self.req,"set_key",0)
				tde4.setWidgetSensitiveFlag(self.req,"toggle",0)			
				tde4.setWidgetValue(self.req,"toggle","0")"""	
		if s_type == 1:
			tde4.setWidgetSensitiveFlag(self.req,"focal_increment_factor",1)
			tde4.setWidgetSensitiveFlag(self.req,"focal_inc",1)
			tde4.setWidgetSensitiveFlag(self.req,"focal_dec",1)
			tde4.setWidgetSensitiveFlag(self.req,"match_frame",1)
		else:
			tde4.setWidgetSensitiveFlag(self.req,"focal_increment_factor",0)
			tde4.setWidgetSensitiveFlag(self.req,"focal_inc",0)
			tde4.setWidgetSensitiveFlag(self.req,"focal_dec",0)
			tde4.setWidgetSensitiveFlag(self.req,"match_frame",0)													

#pick pivot point function...	
	def Pick_Pivot(self,requester,widget,action):
		self.req = requester
		self.widget = widget
		self.action = action
		pg =tde4.getCurrentPGroup()
		cam = tde4.getCurrentCamera()
		frame = tde4.getCurrentFrame(cam)
		pl = tde4.getPointList(pg,1)
		if len(pl) == 1:
			name = tde4.getPointName(pg,pl[0])
			tde4.setWidgetValue(self.req,"pivot_3dpoint",str(name))
		else:
			tde4.postQuestionRequester(self.window_title,"Error, exactly one 3dpoint must be selected.","Ok")

#scale around 3dpoint toggle widget function...
	def Scale_Toggle(self,requester,widget,action):	
		self.req = requester
		self.widget = widget
		self.action = action
		v = tde4.getWidgetValue(self.req,"scale_around_pivot")
		if v == 1:
			tde4.setWidgetSensitiveFlag(self.req,"pick_pivot",1)
			tde4.setWidgetSensitiveFlag(self.req,"avg_3dpoint",1)
		else:
			tde4.setWidgetSensitiveFlag(self.req,"pick_pivot",0)
			tde4.setWidgetSensitiveFlag(self.req,"avg_3dpoint",0)

#average 3dpoint function...	
	def Average_3dpoint(self,requester,widget,action):
		self.req = requester
		self.widget = widget
		self.action = action
		pg =tde4.getCurrentPGroup()
		cam = tde4.getCurrentCamera()
		frame = tde4.getCurrentFrame(cam)
		pl = tde4.getPointList(pg,1)
		pg_type = tde4.getPGroupType(pg)
		if len(pl) >= 2 :	
			x_list = []
			y_list = []
			z_list = []
			for point in pl:
				p3d = tde4.getPointCalcPosition3D(pg,point)
				x_list.append(p3d[0])
				y_list.append(p3d[1])
				z_list.append(p3d[2])
			x = sum(x_list) / len(x_list)
			y = sum(y_list) / len(y_list)
			z = sum(z_list) / len(z_list)
			p3d = [x,y,z]
			p = tde4.createPoint(pg)
			tde4.setPointName(pg,p,"Avg_3dpoint_01")
			tde4.setPointSurveyMode(pg,p,"SURVEY_EXACT")
			tde4.setPointSurveyPosition3D(pg,p,p3d)
		else:
			tde4.postQuestionRequester(self.window_title,"Error, atleast two points must be selected.","Ok")

#enable frame range widget function...
	def Frame_Range(self,requester,widget,action):
		self.req = requester
		self.widget = widget
		self.action = action
		toggle_value = tde4.getWidgetValue(self.req,"toggle")
		if toggle_value == 1:
			tde4.setWidgetSensitiveFlag(self.req,"pick_frame_in",1)
			tde4.setWidgetSensitiveFlag(self.req,"pick_frame_out",1)
			tde4.setWidgetSensitiveFlag(self.req,"set_key",1)
		if toggle_value == 0:
			tde4.setWidgetValue(self.req,"set_key_frame"," ")
			tde4.setWidgetSensitiveFlag(self.req,"pick_frame_in",0)
			tde4.setWidgetSensitiveFlag(self.req,"pick_frame_out",0)
			tde4.setWidgetSensitiveFlag(self.req,"set_key",0)			

#set key frame function...	
	def Set_Keyframe(self,requester,widget,action):
		self.req = requester
		self.widget = widget
		self.action = action
		pg = tde4.getCurrentPGroup()
		pgl = tde4.getPGroupList()
		cam = tde4.getCurrentCamera()
		frame = tde4.getCurrentFrame(cam)
		offset = tde4.getCameraFrameOffset(cam)-1		
		if widget == "set_key":
			tde4.setWidgetValue(self.req,"set_key_frame",str(frame+offset))
		if widget == "pick_frame_in":
			tde4.setWidgetValue(self.req,"frame_in",str(frame+offset))
		if widget == "pick_frame_out":
			tde4.setWidgetValue(self.req,"frame_out",str(frame+offset))			

#bake buffer curves fuction...
	def Bake_Buffer_Curves(self):
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
				tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
		if pg_type == "OBJECT":
			for i in range(1,frames+1):
				tde4.setCurrentFrame(cam,i)
				frame = tde4.getCurrentFrame(cam)
				obj_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
				obj_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
				scale = tde4.getPGroupScale3D(pg)
				focal = tde4.getCameraFocalLength(cam,frame)
				new_values = tde4.convertObjectPGroupTransformationWorldTo3DE(cam, frame, obj_rot.list(), obj_pos.list(), 1.0, 0)
				tde4.setPGroupPosition3D(pg,cam,frame,new_values[1])
				tde4.setPGroupRotation3D(pg,cam,frame,new_values[0])
				tde4.setPGroupScale3D(pg,scale)
				tde4.setCameraFocalLength(cam,frame,focal)
				tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
		#only change from public, returns to parked frame
		tde4.setCurrentFrame(cam,currentFrame)	

#focal length nudge function...	
	def Focal_Nudge(self,requester,widget,action):
		self.req = requester
		self.widget = widget
		self.action = action
		match_toggle = tde4.getWidgetValue(self.req,"match_frame")
		focal_factor = tde4.getWidgetValue(self.req,"focal_increment_factor")
		pg = tde4.getCurrentPGroup()
		pgl = tde4.getPGroupList()
		cam = tde4.getCurrentCamera()
		frame = tde4.getCurrentFrame(cam)
		pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
		rot  = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
		if focal_factor != None:
			if widget == "focal_inc" or widget == "focal_dec":
				if widget == "focal_dec": focal_factor = -float(focal_factor)
				tde4.setCameraFocalLengthMode(cam,"FOCAL_DYNAMIC")
				focal_curve = tde4.getCameraZoomCurve(cam)
				y = tde4.evaluateCurve(focal_curve,frame)
				new_focal = float(y) + (float(focal_factor)/10.0)
				key = tde4.createCurveKey(focal_curve,[frame,new_focal])
				tde4.setCurveKeyMode(focal_curve,key,"LINEAR")
				tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
				tde4.filterPGroup(pg,cam)
				if match_toggle == 1:
					lineup_only = 1
				else:
					lineup_only = 0
				tde4.calcMatchFrame(pg,cam,frame,lineup_only)
				if lineup_only == 0:
					tde4.setPGroupPosition3D(pg,cam,frame,pos.list())
					tde4.setPGroupRotation3D(pg,cam,frame,rot.list())
					tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
					tde4.filterPGroup(pg,cam)
		else:
			tde4.postQuestionRequester(self.window_title,"Error, please enter proper focal length nudge value.","Ok")

#main callback...			
	def Nudge_Callback(self,requester,widget,action):
		self.req = requester
		self.widget = widget
		self.action = action
		pg = tde4.getCurrentPGroup()
		pgl = tde4.getPGroupList()
		pg_type = tde4.getPGroupType(pg)
		cam = tde4.getCurrentCamera()
		frame = tde4.getCurrentFrame(cam)
		frames = tde4.getCameraNoFrames(cam)
		offset = tde4.getCameraFrameOffset(cam)-1
		mlist = tde4.get3DModelList(pg,1)
		pl = tde4.getPointList(pg,1)
		s_type = tde4.getWidgetValue(self.req,"selected_menu")
		p_space = tde4.getWidgetValue(self.req,"t_space")
		r_space = tde4.getWidgetValue(self.req,"r_space")
		power = tde4.getWidgetValue(self.req,"t_increment_factor")
		r_power = tde4.getWidgetValue(self.req,"r_increment_factor")
		s_power = tde4.getWidgetValue(self.req,"s_increment_factor")
		#toggle_value = tde4.getWidgetValue(self.req,"toggle")
		#if camera type selected...
		if s_type == 1:
			if pg_type == "CAMERA":
				if pg != None:
					#self.Bake_Buffer_Curves()
					if p_space == 1:
						if widget == "pos_x+" or widget == "pos_x-" or widget == "pos_y+" or widget == "pos_y-" or widget == "pos_z+" or widget == "pos_z-":
							cam_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
							cam_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
#camera global translation nudge...
							if widget == "pos_x+" or widget == "pos_x-":
								if widget == "pos_x-": power = -float(power)
								pos_x = float(cam_pos[0]) + float(power)
								tde4.setPGroupPosition3D(pg,cam,frame,[pos_x,cam_pos[1],cam_pos[2]])
							if widget == "pos_y+" or widget == "pos_y-":
								if widget == "pos_y-": power = -float(power)
								pos_y = float(cam_pos[1]) + float(power)
								tde4.setPGroupPosition3D(pg,cam,frame,[cam_pos[0],pos_y,cam_pos[2]])
							if widget == "pos_z+" or widget == "pos_z-":
								if widget == "pos_z-": power = -float(power)
								pos_z = float(cam_pos[2]) + float(power)
								tde4.setPGroupPosition3D(pg,cam,frame,[cam_pos[0],cam_pos[1],pos_z])
							tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
							tde4.filterPGroup(pg,cam)
#camera global rotation nudge...
					if r_space == 1:
						if widget == "rot_x+" or widget == "rot_x-" or widget == "rot_y+" or widget == "rot_y-" or widget == "rot_z+" or widget == "rot_z-":
							cam_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
							cam_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))					
							x_axis = vec3d(1,0,0)
							y_axis = vec3d(0,1,0)
							z_axis = vec3d(0,0,1)
							if widget == "rot_x+" or widget == "rot_x-":
								if widget == "rot_x-": r_power = -float(r_power)
								r = mat3d(rot3d(x_axis,math.radians(float(r_power))))
								rot = cam_rot * r
								tde4.setPGroupRotation3D(pg,cam,frame,rot.list())
							if widget == "rot_y+" or widget == "rot_y-":
								if widget == "rot_y-": r_power = -float(r_power)
								r = mat3d(rot3d(y_axis,math.radians(float(r_power))))
								rot = cam_rot * r
								tde4.setPGroupRotation3D(pg,cam,frame,rot.list())
							if widget == "rot_z+" or widget == "rot_z-":
								if widget == "rot_z-": r_power = -float(r_power)
								r = mat3d(rot3d(z_axis,math.radians(float(r_power))))
								rot = cam_rot * r
								tde4.setPGroupRotation3D(pg,cam,frame,rot.list())
							tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
							tde4.filterPGroup(pg,cam)							
#camera local translation buttons nudge...
					if p_space == 2:
						if widget == "pos_x+" or widget == "pos_x-" or widget == "pos_y+" or widget == "pos_y-" or widget == "pos_z+" or widget == "pos_z-":
							cam_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
							cam_rot = tde4.getPGroupRotation3D(pg,cam,frame)
							cam_rot = mat3d(cam_rot).trans()	
							x_axis = vec3d(cam_rot[0]).unit()
							y_axis = vec3d(cam_rot[1]).unit()
							z_axis = vec3d(cam_rot[2]).unit()			
							if widget == "pos_x+":
								v1 = x_axis * float(power)
								cam_pos = v1 + cam_pos
								tde4.setPGroupPosition3D(pg,cam,frame,cam_pos.list())
							if widget == "pos_x-":
								v1 = x_axis * float(power)
								cam_pos = cam_pos - v1
								tde4.setPGroupPosition3D(pg,cam,frame,cam_pos.list())
							if widget == "pos_y+":
								v1 = y_axis * float(power)
								cam_pos = v1 + cam_pos
								tde4.setPGroupPosition3D(pg,cam,frame,cam_pos.list())
							if widget == "pos_y-":
								v1 = y_axis * float(power)
								cam_pos = cam_pos - v1
								tde4.setPGroupPosition3D(pg,cam,frame,cam_pos.list())
							if widget == "pos_z+":
								v1 = z_axis * float(power)
								cam_pos = v1 + cam_pos
								tde4.setPGroupPosition3D(pg,cam,frame,cam_pos.list())
							if widget == "pos_z-":
								v1 = z_axis * float(power)
								cam_pos = cam_pos - v1
								tde4.setPGroupPosition3D(pg,cam,frame,cam_pos.list())
							tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
							tde4.filterPGroup(pg,cam)							
#camera local rotation nudge...
					if r_space == 2:
						if widget == "rot_x+" or widget == "rot_x-" or widget == "rot_y+" or widget == "rot_y-" or widget == "rot_z+" or widget == "rot_z-":
							pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
							rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
							x_axis = rot * vec3d(1,0,0)
							y_axis = rot * vec3d(0,1,0)
							z_axis = rot * vec3d(0,0,1)
							if widget == "rot_x+" or widget == "rot_x-":
								if widget == "rot_x-": r_power = -float(r_power)
								r = mat3d(rot3d(x_axis,math.radians(float(r_power))))
								rot1 = rot * r
								tde4.setPGroupRotation3D(pg,cam,frame,rot1.list())
							if widget == "rot_y+" or widget == "rot_y-":
								if widget == "rot_y-": r_power = -float(r_power)
								r = mat3d(rot3d(y_axis,math.radians(float(r_power))))
								rot1 = rot * r
								tde4.setPGroupRotation3D(pg,cam,frame,rot1.list())
							if widget == "rot_z+" or widget == "rot_z-":
								if widget == "rot_z-": r_power = -float(r_power)
								r = mat3d(rot3d(z_axis,math.radians(float(r_power))))
								rot1 = rot * r
								tde4.setPGroupRotation3D(pg,cam,frame,rot1.list())
							tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
							tde4.filterPGroup(pg,cam)

#rotate camera around 3dpoint(changes camera pivot to selected 3dpoint)...
					if r_space == 3 or r_space == 4:
						if widget == "rot_x+" or widget == "rot_x-" or widget == "rot_y+" or widget == "rot_y-" or widget == "rot_z+" or widget == "rot_z-":
							pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
							rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))						
							x_axis = rot * vec3d(1,0,0)
							y_axis = rot * vec3d(0,1,0)
							z_axis = rot * vec3d(0,0,1)
							if widget == "rot_x+" or widget == "rot_x-":
								if widget == "rot_x-": r_power = -float(r_power)
								rx = float(r_power) * math.pi / 180.0
								ry = 0
								rz = 0
								axis = vec3d(1,0,0)
							if widget == "rot_y+" or widget == "rot_y-":
								if widget == "rot_y-": r_power = -float(r_power)
								rx = 0
								ry = float(r_power) * math.pi / 180.0
								rz = 0
								axis = vec3d(0,1,0)	
							if widget == "rot_z+" or widget == "rot_z-":
								if widget == "rot_z-": r_power = -float(r_power)
								rx = 0
								ry = 0
								rz = float(r_power) * math.pi / 180.0
								axis = vec3d(0,0,1)	
							point_name = tde4.getWidgetValue(self.req,"pivot_3dpoint")
							f = tde4.findPointByName(pg,point_name)
							if f != None:
								pivot = tde4.getPointCalcPosition3D(pg,f)									
								cam_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
								cam_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
								if r_space == 3 :
									p3d = rot3d(rx,ry,rz,VL_APPLY_ZXY) * (cam_pos - pivot) + pivot
									tde4.setPGroupPosition3D(pg,cam,frame,p3d.list())
									r = mat3d(rot3d(axis,math.radians(float(r_power))))
									rot = r * cam_rot
									tde4.setPGroupRotation3D(pg,cam,frame,rot.list())
									tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
									tde4.filterPGroup(pg,cam)
								if r_space == 4:
									# We interpret this as a rotation in local coordinates.
									delta_rot_local = mat3d(rot3d(rx,ry,rz,VL_APPLY_ZXY))
									# Now the task is to express this matrix in *global* coordinates.
									# In order to transform a rotation matrix like this one
									# to another coordinate system, we have do apply the transformation
									# from the left and the inverse one from the right, like a "sandwich".
									# The camera rotation is precisely the link between local and global coordinates.
									# So let's do the sandwich technique; apply transform from left and
									# inverse transform from the right:
									delta_rot_global = cam_rot * delta_rot_local * (cam_rot).trans()
									# you determine the point's position in global space.
									# So, we have constructed a rotation in LOCAL space (delta_rot_local)
									# transferred it to global space (delta_rot_global). Now I think
									# delta_rot_global and your pivot are compatible, as they are both defined
									# in global coordinates.
									# Now apply this to the camera. Position:
									p3d = delta_rot_global * (cam_pos - pivot) + pivot
									tde4.setPGroupPosition3D(pg,cam,frame,p3d.list())
									# Rotation. Use the old rotation and apply our new global delta rotation.
									cam_rot_new = delta_rot_global * cam_rot
									tde4.setPGroupRotation3D(pg,cam,frame,cam_rot_new.list())
									tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
									tde4.filterPGroup(pg,cam)
							else:
								tde4.postQuestionRequester(self.window_title,"Error, please pick pivot 3dpoint.","Ok")
			else:
				tde4.postQuestionRequester(self.window_title,"Camera PGroup must be selected","OK")			
######################################################################################
#if object PGroup type selected...
		if s_type == 2:
			if pg_type == "OBJECT":
				if pg!= None:
					#self.Bake_Buffer_Curves()
					if p_space == 2:
						if widget == "pos_x+" or widget == "pos_x-" or widget == "pos_y+" or widget == "pos_y-" or widget == "pos_z+" or widget == "pos_z-":
							obj_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
							obj_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
							newvalues = tde4.convertObjectPGroupTransformationWorldTo3DE(cam, frame, obj_rot.list(), obj_pos.list(), 1.0, 0)
							pos = newvalues[1]
							rot = newvalues[0]
#object pgroup local translation nudge...
							if widget == "pos_x+" or widget == "pos_x-":
								if widget == "pos_x-": power = -float(power)
								pos_x = float(pos[0]) + float(power)
								tde4.setPGroupPosition3D(pg,cam,frame,[pos_x,pos[1],pos[2]])
							if widget == "pos_y+" or widget == "pos_y-":
								if widget == "pos_y-": power = -float(power)
								pos_y = float(pos[1]) + float(power)
								tde4.setPGroupPosition3D(pg,cam,frame,[pos[0],pos_y,pos[2]])
							if self.widget == "pos_z+" or widget == "pos_z-":
								if widget == "pos_z-": power = -float(power)
								pos_z = float(pos[2]) + float(power)
								tde4.setPGroupPosition3D(pg,cam,frame,[pos[0],pos[1],pos_z])
							tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
							tde4.filterPGroup(pg,cam)
#object local rotation nudge...
					if r_space == 2:
						if widget == "rot_x+" or widget == "rot_x-" or widget == "rot_y+" or widget == "rot_y-" or widget == "rot_z+" or widget == "rot_z-":
							obj_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
							obj_pos = tde4.getPGroupPosition3D(pg,cam,frame)
							if r_space == 2:
								xaxis = obj_rot * vec3d(1,0,0)
								yaxis = obj_rot * vec3d(0,1,0)
								zaxis = obj_rot * vec3d(0,0,1)
							if widget == "rot_x+" or widget == "rot_x-":
								if widget == "rot_x-": r_power = -float((r_power))
								r = mat3d(rot3d(xaxis,math.radians(float(r_power))))
								m1 = r * obj_rot
								newvalues = tde4.convertObjectPGroupTransformationWorldTo3DE(cam,frame,m1.list(),obj_pos,1.0,0)
								pos = newvalues[1]
								rot = newvalues[0]
								tde4.setPGroupPosition3D(pg,cam,frame,pos)
								tde4.setPGroupRotation3D(pg,cam,frame,rot)
							if widget == "rot_y+" or widget == "rot_y-":
								if widget == "rot_y-": r_power = -float((r_power)) 
								r = mat3d(rot3d(yaxis,math.radians(float(r_power))))
								m1 = r * obj_rot
								newvalues = tde4.convertObjectPGroupTransformationWorldTo3DE(cam,frame,m1.list(),obj_pos,1.0,0)
								pos = newvalues[1]
								rot = newvalues[0]
								tde4.setPGroupPosition3D(pg,cam,frame,pos)
								tde4.setPGroupRotation3D(pg,cam,frame,rot)
							if widget == "rot_z+" or widget == "rot_z-":
								if widget == "rot_z-": r_power = -float((r_power))
								r = mat3d(rot3d(zaxis,math.radians(float(r_power))))
								m1 = r * obj_rot
								newvalues = tde4.convertObjectPGroupTransformationWorldTo3DE(cam,frame,m1.list(),obj_pos,1.0,0)
								pos = newvalues[1]
								rot = newvalues[0]
								tde4.setPGroupPosition3D(pg,cam,frame,pos)
								tde4.setPGroupRotation3D(pg,cam,frame,rot)
							tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
							tde4.filterPGroup(pg,cam)
#object pgroup global translation nudge...
					if p_space == 1:
						if widget == "pos_x+" or widget == "pos_x-" or widget == "pos_y+" or widget == "pos_y-" or widget == "pos_z+" or widget == "pos_z-":
							obj_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
							obj_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
							if widget == "pos_x+" or widget == "pos_x-":
								if widget == "pos_x-": power = -float(power)
								xaxis = obj_pos[0] + float(power)
								pos = vec3d(xaxis,obj_pos[1],obj_pos[2])
								newvalues = tde4.convertObjectPGroupTransformationWorldTo3DE(cam,frame,obj_rot.list(),pos.list(),1.0,0)
								tde4.setPGroupPosition3D(pg,cam,frame,newvalues[1])
							if widget == "pos_y+" or widget == "pos_y-":
								if widget == "pos_y-": power = -float(power)
								yaxis = obj_pos[1] + float(power)
								pos = vec3d(obj_pos[0],yaxis,obj_pos[2])
								newvalues = tde4.convertObjectPGroupTransformationWorldTo3DE(cam,frame,obj_rot.list(),pos.list(),1.0,0)
								tde4.setPGroupPosition3D(pg,cam,frame,newvalues[1])
							if widget == "pos_z+" or widget == "pos_z-":
								if widget == "pos_z-": power = -float(power)
								zaxis = obj_pos[2] + float(power)
								pos = vec3d(obj_pos[0],obj_pos[1],zaxis)
								newvalues = tde4.convertObjectPGroupTransformationWorldTo3DE(cam,frame,obj_rot.list(),pos.list(),1.0,0)
								tde4.setPGroupPosition3D(pg,cam,frame,newvalues[1])
							tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
							tde4.filterPGroup(pg,cam)
#object pgroup global rotation nudge...
					if r_space == 1:
						if widget == "rot_x+" or widget == "rot_x-" or widget == "rot_y+" or widget == "rot_y-" or widget == "rot_z+" or widget == "rot_z-":
							obj_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
							obj_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
							if widget == "rot_x+" or widget == "rot_x-":
								if widget == "rot_x-": r_power = -float(r_power)
								r = mat3d(rot3d(vec(1,0,0),math.radians(float(r_power))))
								m = r * obj_rot
								n = tde4.convertObjectPGroupTransformationWorldTo3DE(cam,frame,m.list(),obj_pos.list(),1.0,0)
								tde4.setPGroupPosition3D(pg,cam,frame,n[1])
								tde4.setPGroupRotation3D(pg,cam,frame,n[0])
							if widget == "rot_y+" or widget == "rot_y-":
								if widget == "rot_y-": r_power = -float(r_power)
								r = mat3d(rot3d(vec(0,1,0),math.radians(float(r_power))))
								m = r * obj_rot
								n = tde4.convertObjectPGroupTransformationWorldTo3DE(cam,frame,m.list(),obj_pos.list(),1.0,0)
								tde4.setPGroupPosition3D(pg,cam,frame,n[1])
								tde4.setPGroupRotation3D(pg,cam,frame,n[0])
							if widget == "rot_z+" or widget == "rot_z-":
								if widget == "rot_z-": r_power = -float(r_power)
								r = mat3d(rot3d(vec(0,0,1),math.radians(float(r_power))))
								m = r * obj_rot
								n = tde4.convertObjectPGroupTransformationWorldTo3DE(cam,frame,m.list(),obj_pos.list(),1.0,0)
								tde4.setPGroupPosition3D(pg,cam,frame,n[1])
								tde4.setPGroupRotation3D(pg,cam,frame,n[0])
							tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
							tde4.filterPGroup(pg,cam)
#object pgroup screen translation nudge...
					if p_space == 3:
						if widget == "pos_x+" or widget == "pos_x-" or widget == "pos_y+" or widget == "pos_y-" or widget == "pos_z+" or widget == "pos_z-":											
							cam	= tde4.getCurrentCamera()
							pg	= tde4.getCurrentPGroup()
							frame = tde4.getCurrentFrame(cam)
							pgl = tde4.getPGroupList(0)
							for campg in pgl:
								if tde4.getPGroupType(campg) == "CAMERA":
									break
							cam_pos = vec3d(tde4.getPGroupPosition3D(campg,cam,frame))
							cam_rot = mat3d(tde4.getPGroupRotation3D(campg,cam,frame))
							obj_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
							obj_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
							cam_rot = mat3d(cam_rot).trans()	
							d = vec3d(obj_pos) - vec3d(cam_pos)
							x_axis = vec3d(cam_rot[0]).unit()
							y_axis = vec3d(cam_rot[1]).unit()
							z_axis = vec3d(cam_rot[2]).unit()
							if widget == "pos_x+" or widget == "pos_x-" or widget == "pos_y+" or widget == "pos_y-" or widget == "pos_z+" or widget == "pos_z-":
								if float(power) <= 0.1:
									if widget == "pos_x+" or widget == "pos_x-":
										if widget == "pos_x-": power = -float(power)
										x_axis = x_axis * float(power)
										x_axis = x_axis + cam_pos + d
										f = tde4.convertObjectPGroupTransformationWorldTo3DE(cam, frame, obj_rot.list(), x_axis.list(), 1.0, 0)
										tde4.setPGroupPosition3D(pg,cam,frame,f[1])
									if widget == "pos_y+" or widget == "pos_y-":
										if widget == "pos_y-": power = -float(power)
										y_axis = y_axis * float(power)
										y_axis = y_axis + cam_pos + d
										f = tde4.convertObjectPGroupTransformationWorldTo3DE(cam, frame, obj_rot.list(), y_axis.list(), 1.0, 0)
										tde4.setPGroupPosition3D(pg,cam,frame,f[1])
									#aim math for screen Z...							
									if widget == "pos_z+" or widget == "pos_z-":
										if widget == "pos_z-": power = -float(power)
										p1	= cam_pos+((obj_pos-cam_pos)*(1.0+float(power)))
										f = tde4.convertObjectPGroupTransformationWorldTo3DE(cam, frame, obj_rot.list(), p1.list(), 1.0, 0)
										tde4.setPGroupPosition3D(pg,cam,frame,f[1])
									tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
									tde4.filterPGroup(pg,cam)
								else:
									tde4.postQuestionRequester(self.window_title,"Error, screen translation nudge maximum value is 0.1","Ok")
									tde4.setWidgetValue(self.req,"t_increment_factor","0.05")
									tde4.setWidgetValue(self.req,"t_increment","0.05")
									tde4.setWidgetSensitiveFlag(self.req,"t_increment",1)
#object pgroup screen rotation nudge...
					if r_space == 3:
						if widget == "rot_x+" or widget == "rot_x-" or widget == "rot_y+" or widget == "rot_y-" or widget == "rot_z+" or widget == "rot_z-":
							pgl = tde4.getPGroupList(0)
							for campg in pgl:
								if tde4.getPGroupType(campg) == "CAMERA":
									break
							cam_pos = vec3d(tde4.getPGroupPosition3D(campg,cam,frame))
							cam_rot = mat3d(tde4.getPGroupRotation3D(campg,cam,frame))
							obj_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
							obj_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
							x_axis = cam_rot * vec3d(1,0,0)
							y_axis = cam_rot * vec3d(0,1,0)
							z_axis = cam_rot * vec3d(0,0,1)
							if widget == "rot_x+" or widget == "rot_x-":
								if widget == "rot_x-": r_power = -float((r_power))						
								r1 = mat3d(rot3d(x_axis,math.radians(float(r_power))))
								r = r1 * mat3d(obj_rot)
								f = tde4.convertObjectPGroupTransformationWorldTo3DE(cam, frame, r.list(), obj_pos.list(), 1.0, 0)
								tde4.setPGroupPosition3D(pg,cam,frame,f[1])
								tde4.setPGroupRotation3D(pg,cam,frame,f[0])							
							if widget == "rot_y+" or widget == "rot_y-":
								if widget == "rot_y-": r_power = -float((r_power))						
								r1 = mat3d(rot3d(y_axis,math.radians(float(r_power))))
								r = r1 * mat3d(obj_rot)
								f = tde4.convertObjectPGroupTransformationWorldTo3DE(cam, frame, r.list(), obj_pos.list(), 1.0, 0)
								tde4.setPGroupPosition3D(pg,cam,frame,f[1])
								tde4.setPGroupRotation3D(pg,cam,frame,f[0])							
							if widget == "rot_z+" or widget == "rot_z-":
								if widget == "rot_z-": r_power = -float((r_power))						
								r1 = mat3d(rot3d(z_axis,math.radians(float(r_power))))
								r = r1 * mat3d(obj_rot)
								f = tde4.convertObjectPGroupTransformationWorldTo3DE(cam, frame, r.list(), obj_pos.list(), 1.0, 0)
								tde4.setPGroupPosition3D(pg,cam,frame,f[1])
								tde4.setPGroupRotation3D(pg,cam,frame,f[0])	
							tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")						
							tde4.filterPGroup(pg,cam)

#rotate objectPGroup around 3dpoint(changes objectPGroup pivot to selected 3dpoint)...
					if r_space == 4 or r_space == 5:
						if widget == "rot_x+" or widget == "rot_x-" or widget == "rot_y+" or widget == "rot_y-" or widget == "rot_z+" or widget == "rot_z-":
							pivot = tde4.getWidgetValue(self.req,"pivot_3dpoint")
							f = tde4.findPointByName(pg,pivot)
							if f != None:
								p3d = tde4.getPointCalcPosition3D(pg,f)
								pivot_local = vec3d(p3d[0],p3d[1],p3d[2])
								# Find camera point group
								for i_pg in tde4.getPGroupList():
									if tde4.getPGroupType(i_pg) == "CAMERA":
										id_cpg = i_pg
										break
								# We pick the first object point group. Please modify according to your requirements.
								#for i_pg in tde4.getPGroupList():
								#if tde4.getPGroupType(i_pg) == "OBJECT":
								id_opg = tde4.getCurrentPGroup()
								#break
								# Current camera
								id_cam = tde4.getCurrentCamera()
								# Current rotation and position of the object point group.
								pos_opg_global = vec3d(tde4.getPGroupPosition3D(id_opg,id_cam,frame))
								rot_opg_global = mat3d(tde4.getPGroupRotation3D(id_opg,id_cam,frame))
								pivot_global = (mat3d(rot_opg_global)*vec3d(pivot_local)) + vec3d(pos_opg_global)

								# Feel free to try out some of the following three segments.
								# 1. This will just do nothing.
								#	rot_opg_new_global = rot_opg_global
								#	pos_opg_new_global = pos_opg_global

								# 2. This will translate the entire point group to the left by fifty units.
								#	rot_opg_new_global = rot_opg_global
								#	pos_opg_new_global = vl.igl3d(vl.mat3d(1),vl.vec3d(-50,0,0)) * pos_opg_global
									
								# 3. This one rotates the entire point group and its path
								# around the given pivot in global coords by the given global matrix.
								if widget == "rot_x+" or widget == "rot_x-":
									if widget == "rot_x-": r_power = -float((r_power))
									delta_rot_global = rot3d(vec3d(1,0,0),math.radians(float(r_power))).mat()
								if widget == "rot_y+" or widget == "rot_y-":
									if widget == "rot_y-": r_power = -float((r_power))
									delta_rot_global = rot3d(vec3d(0,1,0),math.radians(float(r_power))).mat()
								if widget == "rot_z+" or widget == "rot_z-":
									if widget == "rot_z-": r_power = -float((r_power))
									delta_rot_global = rot3d(vec3d(0,0,1),math.radians(float(r_power))).mat()
								if r_space == 4:
									delta_rot_global = delta_rot_global
								if r_space == 5:
									delta_rot_global = rot_opg_global * delta_rot_global * rot_opg_global.trans()
								rot_opg_new_global = delta_rot_global * rot_opg_global
								pos_opg_new_global = igl3d(mat3d(1),pivot_global) * igl3d(delta_rot_global) * igl3d(mat3d(1),-pivot_global) * pos_opg_global
								# The base transform from the camera point group.
								# We need rot_pos_base because unfortunately our set-functions
								# are not the exact counterpart to the get-functions. It's well-defined, but unpleasent.
								rot_cpg = mat3d(tde4.getPGroupRotation3D(id_cpg,id_cam,frame))
								pos_cpg = vec3d(tde4.getPGroupPosition3D(id_cpg,id_cam,frame))
								rot_pos_base = igl3d(rot_cpg,pos_cpg)
								# Now we can build rotation and position of the object point group.
								rot_pos_opg_new = igl3d(rot_opg_new_global,pos_opg_new_global).invert() * rot_pos_base
								tde4.setPGroupRotation3D(id_opg,id_cam,frame,rot_pos_opg_new.m.list())
								tde4.setPGroupPosition3D(id_opg,id_cam,frame,rot_pos_opg_new.v.list())
								tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
								tde4.filterPGroup(id_opg,id_cam)
							else:
								tde4.postQuestionRequester(self.window_title,"Error, please pick pivot 3dpoint.","Ok")
			else:
				tde4.postQuestionRequester(self.window_title,"Object PGroup must be selected","OK")	
##########################################################################################
#if 3D Model type selected under camera group... 	
		if s_type == 3:
			if len(mlist) > 0:
				for model in mlist:
					tde4.set3DModelSurveyFlag(pg,model,0)
					if tde4.getPGroupType(pg) == "CAMERA":
						power = tde4.getWidgetValue(self.req,"t_increment_factor")
						r_power = tde4.getWidgetValue(self.req,"r_increment_factor")						
						if p_space == 1:
							if widget == "pos_x+" or widget == "pos_x-" or widget == "pos_y+" or widget == "pos_y-" or widget == "pos_z+" or widget == "pos_z-":
								pos = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame))
#3D model global translation nudge...
								if widget == "pos_x+" or widget == "pos_x-":
									if widget == "pos_x-": power = -float(power)
									pos_x = float(pos[0]) + float(power)
									tde4.set3DModelPosition3D(pg,model,[pos_x,pos[1],pos[2]])
								if widget == "pos_y+" or widget == "pos_y-":
									if widget == "pos_y-": power = -float(power)
									pos_y = float(pos[1]) + float(power)
									tde4.set3DModelPosition3D(pg,model,[pos[0],pos_y,pos[2]])	
								if widget == "pos_z+" or widget == "pos_z-":
									if widget == "pos_z-": power = -float(power)
									pos_z = float(pos[2]) + float(power)
									tde4.set3DModelPosition3D(pg,model,[pos[0],pos[1],pos_z])			
#3D model global rotation nudge...
						if r_space == 1:
							if widget == "rot_x+" or widget == "rot_x-" or widget == "rot_y+" or widget == "rot_y-" or widget == "rot_z+" or widget == "rot_z-":
								rot = mat3d(tde4.get3DModelRotationScale3D(pg,model))
								if widget == "rot_x+" or widget == "rot_x-":
									if widget == "rot_x-": r_power = -float(r_power)
									r = mat3d(rot3d(vec(1,0,0),math.radians(float(r_power))))
									rot = r * rot
									tde4.set3DModelRotationScale3D(pg,model,rot.list())							
								if widget == "rot_y+" or widget == "rot_y-":
									if widget == "rot_y-": r_power = -float(r_power)
									r = mat3d(rot3d(vec(0,1,0),math.radians(float(r_power))))
									rot = r * rot
									tde4.set3DModelRotationScale3D(pg,model,rot.list())								
								if widget == "rot_z+" or widget == "rot_z-":
									if widget == "rot_z-": r_power = -float(r_power)
									r = mat3d(rot3d(vec(0,0,1),math.radians(float(r_power))))
									rot = r * rot
									tde4.set3DModelRotationScale3D(pg,model,rot.list())								
#3D model local translation buttons nudge...
						if p_space == 2:
							if widget == "pos_x+" or widget == "pos_x-" or widget == "pos_y+" or widget == "pos_y-" or widget == "pos_z+" or widget == "pos_z-":
								pos = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame))
								rot = mat3d(tde4.get3DModelRotationScale3D(pg,model))
								rot1 = mat3d(rot).trans()
								x_axis = vec3d(rot1[0]).unit()
								y_axis = vec3d(rot1[1]).unit()
								z_axis = vec3d(rot1[2]).unit()
								if widget == "pos_x+":
									v = x_axis * float(power)
									pos = vec3d(v) + vec3d(pos)
									tde4.set3DModelPosition3D(pg,model,pos.list())
								if widget == "pos_x-":
									v = x_axis * float(power)
									pos = vec3d(pos) - vec3d(v) 
									tde4.set3DModelPosition3D(pg,model,pos.list())
								if widget == "pos_y+":
									v = y_axis * float(power)
									pos = vec3d(v) + vec3d(pos)
									tde4.set3DModelPosition3D(pg,model,pos.list())
								if widget == "pos_y-":
									v = y_axis * float(power)
									pos = vec3d(pos) - vec3d(v)
									tde4.set3DModelPosition3D(pg,model,pos.list()) 
								if widget == "pos_z+":
									v = z_axis * float(power)
									pos = vec3d(v) + vec3d(pos)
									tde4.set3DModelPosition3D(pg,model,pos.list())
								if widget == "pos_z-":
									v = z_axis * float(power)
									pos = vec3d(pos) - vec3d(v) 
									tde4.set3DModelPosition3D(pg,model,pos.list())
#3D model local rotation nudge...
						if r_space == 2:
							if widget == "rot_x+" or widget == "rot_x-" or widget == "rot_y+" or widget == "rot_y-" or widget == "rot_z+" or widget == "rot_z-":
								rot = mat3d(tde4.get3DModelRotationScale3D(pg,model))
								if widget == "rot_x+" or widget == "rot_x-":
									if widget == "rot_x-": r_power = -float(r_power)
									r = mat3d(rot3d(vec(1,0,0),math.radians(float(r_power))))
									rot = rot * r
									tde4.set3DModelRotationScale3D(pg,model,rot.list())							
								if widget == "rot_y+" or widget == "rot_y-":
									if widget == "rot_y-": r_power = -float(r_power)
									r = mat3d(rot3d(vec(0,1,0),math.radians(float(r_power))))
									rot = rot * r
									tde4.set3DModelRotationScale3D(pg,model,rot.list())								
								if widget == "rot_z+" or widget == "rot_z-":
									if widget == "rot_z-": r_power = -float(r_power)
									r = mat3d(rot3d(vec(0,0,1),math.radians(float(r_power))))
									rot = rot * r
									tde4.set3DModelRotationScale3D(pg,model,rot.list())								
#3D model screen translate nudge...		
						if p_space == 3:
							if widget == "pos_x+" or widget == "pos_x-" or widget == "pos_y+" or widget == "pos_y-" or widget == "pos_z+" or widget == "pos_z-":
								cam_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
								cam_rot = tde4.getPGroupRotation3D(pg,cam,frame)
								cam_rot = mat3d(cam_rot).trans()	
								m_pos = tde4.get3DModelPosition3D(pg,mlist[0],cam,frame)
								d = vec3d(m_pos) - vec3d(cam_pos)
								x_axis = vec3d(cam_rot[0]).unit()
								y_axis = vec3d(cam_rot[1]).unit()
								z_axis = vec3d(cam_rot[2]).unit()
								if widget == "pos_x+" or widget == "pos_x-" or widget == "pos_y+" or widget == "pos_y-" or widget == "pos_z+" or widget == "pos_z-":
									if widget == "pos_x+" or widget == "pos_x-":
										if widget == "pos_x-": power = -float(power)
										x_axis = x_axis * float(power)
										x_axis = x_axis + cam_pos + d
										tde4.set3DModelPosition3D(pg,mlist[0],x_axis.list())
									if widget == "pos_y+" or widget == "pos_y-":
										if widget == "pos_y-": power = -float(power)
										y_axis = y_axis * float(power)
										y_axis = y_axis + cam_pos + d
										tde4.set3DModelPosition3D(pg,mlist[0],y_axis.list())
									m = mat3d(tde4.get3DModelRotationScale3D(pg,model)).trans()
									s = vec3d(m[0].norm2(),m[1].norm2(),m[2].norm2())
									r3d = mat3d(m[0].unit(),m[1].unit(),m[2].unit()).trans()
									#aim math for screen Z mode...							
									if widget == "pos_z+" or widget == "pos_z-":
										if float(power) <= 0.1:
											if widget == "pos_z-": power = -float(power)
											l	= r3d*vec3d(0.0,0.0,1.0)
											p0 = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame))
											p1	= cam_pos+((p0-cam_pos)) * (1.0+float(power))
											tde4.set3DModelPosition3D(pg,model,p1.list())
										else:
											tde4.postQuestionRequester(self.window_title,"Error, Z-Axis screen translation nudge maximum value is 0.1","Ok")
											tde4.setWidgetValue(self.req,"t_increment_factor","0.05")
											tde4.setWidgetValue(self.req,"t_increment","0.05")
											tde4.setWidgetSensitiveFlag(self.req,"t_increment",1)								
#3D model screen rotation nudge...	
						if r_space == 3:
							if widget == "rot_x+" or widget == "rot_x-" or widget == "rot_y+" or widget == "rot_y-" or widget == "rot_z+" or widget == "rot_z-":
								pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
								rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
								x_axis = rot * vec3d(1,0,0)
								y_axis = rot * vec3d(0,1,0)
								z_axis = rot * vec3d(0,0,1)
								m = mat3d(tde4.get3DModelRotationScale3D(pg,mlist[0])).trans()
								s = vec3d(m[0].norm2(),m[1].norm2(),m[2].norm2())
								s = mat3d(s[0],0.0,0.0,0.0,s[1],0.0,0.0,0.0,s[2])
								r = mat3d(m[0].unit(),m[1].unit(),m[2].unit()).trans()
								if widget == "rot_x+" or widget == "rot_x-":
									if widget == "rot_x-": r_power = -float(r_power)
									r1 = mat3d(rot3d(x_axis,math.radians(float(r_power))))
									r = r1 * r
									r = r *s
									tde4.set3DModelRotationScale3D(pg,mlist[0],r.list())
								if widget == "rot_y+" or widget == "rot_y-":
									if widget == "rot_y-": r_power = -float(r_power)
									r1 = mat3d(rot3d(y_axis,math.radians(float(r_power))))
									r = r1 * r
									r = r *s
									tde4.set3DModelRotationScale3D(pg,mlist[0],r.list())
								if widget == "rot_z+" or widget == "rot_z-":
									if widget == "rot_z-": r_power = -float(r_power)
									r1 = mat3d(rot3d(z_axis,math.radians(float(r_power))))
									r = r1 * r
									r = r *s
									tde4.set3DModelRotationScale3D(pg,mlist[0],r.list())
#3D model rotation around a point nudge...									
						if r_space == 4 or r_space == 5:
							if widget == "rot_x+" or widget == "rot_x-" or widget == "rot_y+" or widget == "rot_y-" or widget == "rot_z+" or widget == "rot_z-":
								mpos = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame))							
								if widget == "rot_x+" or widget == "rot_x-":
									if widget == "rot_x-": r_power = -float(r_power)
									rx = float(r_power) * math.pi / 180.0
									ry = 0.0
									rz = 0.0
								if widget == "rot_y+" or widget == "rot_y-":
									if widget == "rot_y-": r_power = -float(r_power)
									rx = 0.0
									ry = float(r_power) * math.pi / 180.0
									rz = 0.0
								if widget == "rot_z+" or widget == "rot_z-":
									if widget == "rot_z-": r_power = -float(r_power)
									rx = 0.0
									ry = 0.0
									rz = float(r_power) * math.pi / 180.0
								point_name = tde4.getWidgetValue(self.req,"pivot_3dpoint")
								f = tde4.findPointByName(pg,point_name)
								if f != None:
									pivot = tde4.getPointCalcPosition3D(pg,f)
									mpos = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame))
									m = mat3d(tde4.get3DModelRotationScale3D(pg,model)).trans()
									s = vec3d(m[0].norm2(),m[1].norm2(),m[2].norm2())
									s = mat3d(s[0],0.0,0.0,0.0,s[1],0.0,0.0,0.0,s[2])
									rotation_matrix = mat3d(m[0].unit(),m[1].unit(),m[2].unit()).trans()										
									if r_space == 4:
										delta_rot_global = rot3d(rx,ry,rz,VL_APPLY_ZXY)
									if r_space == 5:
										delta_rot_local = rot3d(rx,ry,rz,VL_APPLY_ZXY)
										delta_rot_global = rotation_matrix * mat3d(delta_rot_local) * rotation_matrix.trans()
									p3d = delta_rot_global * (mpos - pivot) + pivot
									tde4.set3DModelPosition3D(pg,model,p3d.list())
									mrot = mat3d(tde4.get3DModelRotationScale3D(pg,model))
									rot = mat3d(delta_rot_global) * mrot
									tde4.set3DModelRotationScale3D(pg,model,rot.list())									
								else:
									tde4.postQuestionRequester(self.window_title,"Error, please pick pivot 3dpoint.","Ok")
#if 3D Model type selected under object group... 	
					if tde4.getPGroupType(pg) == "OBJECT":
#3D model global translation nudge...
						if p_space == 1:
							if widget == "pos_x+" or widget == "pos_x-" or widget == "pos_y+" or widget == "pos_y-" or widget == "pos_z+" or widget == "pos_z-":
								rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
								xaxis = rot.invert()*vec3d(1,0,0)
								yaxis = rot.invert()*vec3d(0,1,0)
								zaxis = rot.invert()*vec3d(0,0,1)
								if widget == "pos_x+" or widget == "pos_x-":
									if widget == "pos_x-": power = -float(power)
									xaxis = xaxis*float(power)
									xaxis = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame)) + vec3d(xaxis)
									tde4.set3DModelPosition3D(pg,model,[xaxis[0],xaxis[1],xaxis[2]])
								if widget == "pos_y+" or widget == "pos_y-":
									if widget == "pos_y-": power = -float(power)
									yaxis = yaxis*float(power)
									yaxis = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame)) + vec3d(yaxis)
									tde4.set3DModelPosition3D(pg,model,[yaxis[0],yaxis[1],yaxis[2]])
								if widget == "pos_z+" or widget == "pos_z-":
									if widget == "pos_z-": power = -float(power)
									zaxis = zaxis*float(power)
									zaxis = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame)) + vec3d(zaxis)
									tde4.set3DModelPosition3D(pg,model,[zaxis[0],zaxis[1],zaxis[2]])
#3D model local translation nudge...
						if p_space == 2:
							if widget == "pos_x+" or widget == "pos_x-" or widget == "pos_y+" or widget == "pos_y-" or widget == "pos_z+" or widget == "pos_z-":
								pos = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame))
								rot = mat3d(tde4.get3DModelRotationScale3D(pg,model))
								rot1 = mat3d(rot).trans()
								x_axis = vec3d(rot1[0]).unit()
								y_axis = vec3d(rot1[1]).unit()
								z_axis = vec3d(rot1[2]).unit()
								if widget == "pos_x+" or widget == "pos_x-":
									if widget == "pos_x-": power = -float(power)
									v = x_axis * float(power)
									pos = vec3d(v) + vec3d(pos)
									tde4.set3DModelPosition3D(pg,model,pos.list())
								if widget == "pos_y+" or widget == "pos_y-":
									if widget == "pos_y-": power = -float(power)
									v = y_axis * float(power)
									pos = vec3d(v) + vec3d(pos)
									tde4.set3DModelPosition3D(pg,model,pos.list())
								if widget == "pos_z+" or widget == "pos_z-":
									if widget == "pos_z-": power = -float(power)
									v = z_axis * float(power)
									pos = vec3d(v) + vec3d(pos)
									tde4.set3DModelPosition3D(pg,model,pos.list())
#3D model global rotation nudge...
						if r_space == 1:
							if widget == "rot_x+" or widget == "rot_x-" or widget == "rot_y+" or widget == "rot_y-" or widget == "rot_z+" or widget == "rot_z-":
								rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
								xaxis = (rot.invert()*vec3d(1,0,0))
								yaxis = (rot.invert()*vec3d(0,1,0))
								zaxis = (rot.invert()*vec3d(0,0,1))
								if widget == "rot_x+" or widget == "rot_x-":
									if widget == "rot_x-": r_power = -float(r_power)
									r = mat3d(rot3d(xaxis,math.radians(float(r_power))))
									f = r * mat3d(tde4.get3DModelRotationScale3D(pg,model))
									tde4.set3DModelRotationScale3D(pg,model,f.list())
								if widget == "rot_y+" or widget == "rot_y-":
									if widget == "rot_y-": r_power = -float(r_power)
									r = mat3d(rot3d(yaxis,math.radians(float(r_power))))
									f = r * mat3d(tde4.get3DModelRotationScale3D(pg,model))
									tde4.set3DModelRotationScale3D(pg,model,f.list())
								if widget == "rot_z+" or widget == "rot_z-":
									if widget == "rot_z-": r_power = -float(r_power)
									r = mat3d(rot3d(zaxis,math.radians(float(r_power))))
									f = r * mat3d(tde4.get3DModelRotationScale3D(pg,model))
									tde4.set3DModelRotationScale3D(pg,model,f.list())
#3D model local rotation nudge...
						if r_space == 2:
							if widget == "rot_x+" or widget == "rot_x-" or widget == "rot_y+" or widget == "rot_y-" or widget == "rot_z+" or widget == "rot_z-":
								rot = mat3d(tde4.get3DModelRotationScale3D(pg,model))
								if widget == "rot_x+" or widget == "rot_x-":
									if widget == "rot_x-": r_power = -float(r_power)
									r = mat3d(rot3d(vec(1,0,0),math.radians(float(r_power))))
									rot = rot *r
									tde4.set3DModelRotationScale3D(pg,model,rot.list())							
								if widget == "rot_y+" or widget == "rot_y-":
									if widget == "rot_y-": r_power = -float(r_power)
									r = mat3d(rot3d(vec(0,1,0),math.radians(float(r_power))))
									rot = rot *r
									tde4.set3DModelRotationScale3D(pg,model,rot.list())	
								if widget == "rot_z+" or widget == "rot_z-":
									if widget == "rot_z-": r_power = -float(r_power)
									r = mat3d(rot3d(vec(0,0,1),math.radians(float(r_power))))
									rot = rot *r
									tde4.set3DModelRotationScale3D(pg,model,rot.list())	
#3D model screen translate nudge...	
						if p_space == 3:
							if widget == "pos_x+" or widget == "pos_x-" or widget == "pos_y+" or widget == "pos_y-" or widget == "pos_z+" or widget == "pos_z-":
								cam	= tde4.getCurrentCamera()
								pg	= tde4.getCurrentPGroup()
								frame = tde4.getCurrentFrame(cam)
								pgl = tde4.getPGroupList(0)
								for campg in pgl:
									if tde4.getPGroupType(campg) == "CAMERA":
										break
								mpos = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame))
								cam_pos = vec3d(tde4.getPGroupPosition3D(campg,cam,frame))
								cam_rot = mat3d(tde4.getPGroupRotation3D(campg,cam,frame))
								obj_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
								obj_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
								#convert 3DModel local to global...
								mpos = (mat3d(obj_rot)*vec3d(mpos)) + vec3d(obj_pos)
								vector = vec3d(mpos) - vec3d(obj_pos)
								cam_rot = mat3d(cam_rot).trans()	
								d = vec3d(obj_pos) - vec3d(cam_pos)
								x_axis = vec3d(cam_rot[0]).unit()
								y_axis = vec3d(cam_rot[1]).unit()
								z_axis = vec3d(cam_rot[2]).unit()
								if widget == "pos_x+" or widget == "pos_x-":
									if widget == "pos_x-": power = -float(power)
									x_axis = x_axis * float(power)
									x_axis = x_axis + cam_pos + d
									x_axis = vec3d(x_axis) + vec3d(vector)
									#convert 3DModel global to local...
									mpos = mat3d(obj_rot).invert() * (vec3d(x_axis)-vec3d(obj_pos))
									tde4.set3DModelPosition3D(pg,model,mpos.list())
								if widget == "pos_y+" or widget == "pos_y-":
									if widget == "pos_y-": power = -float(power)
									y_axis = y_axis * float(power)
									y_axis = y_axis + cam_pos + d
									y_axis = vec3d(y_axis) + vec3d(vector)
									#convert 3DModel global to local...
									mpos = mat3d(obj_rot).invert() * (vec3d(y_axis)-vec3d(obj_pos))
									tde4.set3DModelPosition3D(pg,model,mpos.list())
								#aim math for screen Z...
								if widget == "pos_z+" or widget == "pos_z-":							
									if float(power) <= 0.1: 
										if widget == "pos_z-": power = -float(power)
										pg = tde4.getCurrentPGroup()
										cam = tde4.getCurrentCamera()
										frame = tde4.getCurrentFrame(cam)
										pgl	= tde4.getPGroupList(0)
										for campg in pgl:
											pgt	= tde4.getPGroupType(campg)
											if pgt=="CAMERA": break
										cam_pos = vec3d(tde4.getPGroupPosition3D(campg,cam,frame))
										cam_rot = mat3d(tde4.getPGroupRotation3D(campg,cam,frame))
										obj_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
										obj_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
										p3d = obj_rot.trans()*(cam_pos-obj_pos)
										p0 = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame))
										p1 = p3d+((p0-p3d)*(1.0+float(power)))
										tde4.set3DModelPosition3D(pg,model,[p1[0],p1[1],p1[2]])
									else:
										tde4.postQuestionRequester(self.window_title,"Error, screen translation nudge maximum value is 0.1","Ok")
										tde4.setWidgetValue(self.req,"t_increment_factor","0.05")
										tde4.setWidgetValue(self.req,"t_increment","0.05")
										tde4.setWidgetSensitiveFlag(self.req,"t_increment",1)
#3D model screen rotation nudge...	
						if r_space == 3:
							if widget == "rot_x+" or widget == "rot_x-" or widget == "rot_y+" or widget == "rot_y-" or widget == "rot_z+" or widget == "rot_z-":
								pgl = tde4.getPGroupList(0)
								for campg in pgl:
									if tde4.getPGroupType(campg) == "CAMERA":
										break
								mpos = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame))
								cam_pos = vec3d(tde4.getPGroupPosition3D(campg,cam,frame))
								cam_rot = mat3d(tde4.getPGroupRotation3D(campg,cam,frame))
								obj_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
								obj_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))	
								#convert 3DModel local to global...
								mpos = (mat3d(obj_rot)*vec3d(mpos)) + vec3d(obj_pos)	
								mrot = mat3d(tde4.get3DModelRotationScale3D(pg,model))
								mrot = mat3d(obj_rot) * mat3d(mrot)
								#extract 3DModel rot and scale matrices...
								m = mat3d(mrot).trans()
								s        = vec3d(m[0].norm2(),m[1].norm2(),m[2].norm2())
								scale_matrix = mat3d(s[0],0.0,0.0,0.0,s[1],0.0,0.0,0.0,s[2])
								r = mat3d(m[0].unit(),m[1].unit(),m[2].unit()).trans()
								x_axis = cam_rot * vec3d(1,0,0)
								y_axis = cam_rot * vec3d(0,1,0)
								z_axis = cam_rot * vec3d(0,0,1)
								if widget == "rot_x+" or widget == "rot_x-":
									if widget == "rot_x-": r_power = -float((r_power))						
									r1 = mat3d(rot3d(x_axis,math.radians(float(r_power))))
									r = r1 * r
									r = r*scale_matrix
									#convert global rotations to local...
									f = mat3d(obj_rot).invert()*mat3d(r)
									tde4.set3DModelRotationScale3D(pg,model,f.list())
								if widget == "rot_y+" or widget == "rot_y-":
									if widget == "rot_y-": r_power = -float((r_power))						
									r1 = mat3d(rot3d(y_axis,math.radians(float(r_power))))
									r = r1 * r
									r = r*scale_matrix
									#convert global rotations to local...
									f = mat3d(obj_rot).invert()*mat3d(r)
									tde4.set3DModelRotationScale3D(pg,model,f.list())
								if widget == "rot_z+" or widget == "rot_z-":
									if widget == "rot_z-": r_power = -float((r_power))						
									r1 = mat3d(rot3d(z_axis,math.radians(float(r_power))))
									r = r1 * r
									r = r*scale_matrix
									#convert global rotations to local...
									f = mat3d(obj_rot).invert()*mat3d(r)
									tde4.set3DModelRotationScale3D(pg,model,f.list())
#3D model rotation around a point nudge...									
						if r_space == 4 or r_space == 5:
							if widget == "rot_x+" or widget == "rot_x-" or widget == "rot_y+" or widget == "rot_y-" or widget == "rot_z+" or widget == "rot_z-":
								mpos = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame))	
								if widget == "rot_x+" or widget == "rot_x-":
									if widget == "rot_x-": r_power = -float(r_power)
									rx = float(r_power) * math.pi / 180.0
									ry = 0.0
									rz = 0.0
								if widget == "rot_y+" or widget == "rot_y-":
									if widget == "rot_y-": r_power = -float(r_power)
									rx = 0.0
									ry = float(r_power) * math.pi / 180.0
									rz = 0.0
								if widget == "rot_z+" or widget == "rot_z-":
									if widget == "rot_z-": r_power = -float(r_power)
									rx = 0.0
									ry = 0.0
									rz = float(r_power) * math.pi / 180.0
								point_name = tde4.getWidgetValue(self.req,"pivot_3dpoint")
								f = tde4.findPointByName(pg,point_name)
								if f != None:
									pivot = tde4.getPointCalcPosition3D(pg,f)
									pivot = (mat3d(tde4.getPGroupRotation3D(pg,cam,frame)) * vec3d(pivot)) + vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
									mpos = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame))
									mpos = (mat3d(tde4.getPGroupRotation3D(pg,cam,frame)) * mpos) + vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
									m = mat3d(tde4.get3DModelRotationScale3D(pg,model)).trans()
									s = vec3d(m[0].norm2(),m[1].norm2(),m[2].norm2())
									s = mat3d(s[0],0.0,0.0,0.0,s[1],0.0,0.0,0.0,s[2])
									rotation_matrix = mat3d(m[0].unit(),m[1].unit(),m[2].unit()).trans()										
									if r_space == 4:
										delta_rot_global = rot3d(rx,ry,rz,VL_APPLY_ZXY)
									if r_space == 5:
										delta_rot_local = rot3d(rx,ry,rz,VL_APPLY_ZXY)
										delta_rot_global = rotation_matrix * mat3d(delta_rot_local) * rotation_matrix.trans()
									p3d = delta_rot_global * (mpos - pivot) + pivot
									new_values = mat3d(tde4.getPGroupRotation3D(pg,cam,frame)).invert() * (p3d - vec3d(tde4.getPGroupPosition3D(pg,cam,frame)))
									tde4.set3DModelPosition3D(pg,model,new_values.list())
									mrot = mat3d(tde4.get3DModelRotationScale3D(pg,model))
									rot = mat3d(delta_rot_global) * mrot
									tde4.set3DModelRotationScale3D(pg,model,rot.list())									
								else:
									tde4.postQuestionRequester(self.window_title,"Error, please pick pivot 3dpoint.","Ok")
#3d model scale...
					m = mat3d(tde4.get3DModelRotationScale3D(pg,model)).trans()
					s        = vec3d(m[0].norm2(),m[1].norm2(),m[2].norm2())
					r_matrix        = mat3d(m[0].unit(),m[1].unit(),m[2].unit()).trans()
					if widget == "scale_x+" or widget == "scale_x-":
						if widget == "scale_x-": s_power = -float(s_power)
						s_matrix = mat3d(s[0]+float(s_power),0.0,0.0,0.0,s[1],0.0,0.0,0.0,s[2])
						m = r_matrix * s_matrix
						tde4.set3DModelRotationScale3D(pg,model,m.list())
					if widget == "scale_y+" or widget == "scale_y-":
						if widget == "scale_y-": s_power = -float(s_power)
						s_matrix = mat3d(s[0],0.0,0.0,0.0,s[1]+float(s_power),0.0,0.0,0.0,s[2])
						m = r_matrix * s_matrix
						tde4.set3DModelRotationScale3D(pg,model,m.list())
					if widget == "scale_z+" or widget == "scale_z-":
						if widget == "scale_z-": s_power = -float(s_power)
						s_matrix = mat3d(s[0],0.0,0.0,0.0,s[1],0.0,0.0,0.0,s[2]+float(s_power))
						m = r_matrix * s_matrix
						tde4.set3DModelRotationScale3D(pg,model,m.list())
					if widget == "uniform_scale+":
						s_matrix = mat3d(s[0]+float(s_power),0.0,0.0,0.0,s[1]+float(s_power),0.0,0.0,0.0,s[2]+float(s_power))
						m = r_matrix * s_matrix
						tde4.set3DModelRotationScale3D(pg,model,m.list())
					if widget == "uniform_scale-":
						if float(s_power) >= s[0]-0.1 or float(s_power) >= s[1]-0.1 or float(s_power) >= s[2]-0.1:
							s_power = float((s[0]+s[1]+s[2])/3)/10.0
							tde4.setWidgetValue(self.req,"s_increment",str(s_power))
							tde4.setWidgetValue(self.req,"s_increment_factor",str(s_power))
						if s[0] <= 0.2 or s[1] <= 0.2 or s[2] <= 0.2:
							tde4.setWidgetValue(self.req,"s_increment","0.001")
							tde4.setWidgetValue(self.req,"s_increment_factor","0.001")
							s_power = tde4.getWidgetValue(self.req,"s_increment_factor")
						s_matrix = mat3d(s[0]-float(s_power),0.0,0.0,0.0,s[1]-float(s_power),0.0,0.0,0.0,s[2]-float(s_power))
						m = r_matrix * s_matrix
						tde4.set3DModelRotationScale3D(pg,model,m.list())
			else:
				tde4.postQuestionRequester(self.window_title,"atleast one 3DModel must be selected or 3DModels should be under current PGroup.","OK")

#if scene selected...
		if s_type == 4:
			if pg != None:
				pgl = tde4.getPGroupList()
				for pg in pgl:
					pg_type = tde4.getPGroupType(pg)
					if pg_type == "CAMERA":
						break
				pl = tde4.getPointList(pg)
				toggle_models = tde4.getWidgetValue(self.req,"move_3dmodels")
				if len(pl) > 0:
					self.Bake_Buffer_Curves()
					#scene global translation nudge...
					if p_space == 1:
						if widget == "pos_x+" or widget == "pos_x-" or widget == "pos_y+" or widget == "pos_y-" or widget == "pos_z+" or widget == "pos_z-":
							if widget == "pos_x+" or widget == "pos_x-":
								if widget == "pos_x-": power = -float(power)
								for frame in range(1,frames+1):
									cam_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
									cam_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))							
									pos_x = float(cam_pos[0]) + float(power)
									tde4.setPGroupPosition3D(pg,cam,frame,[pos_x,cam_pos[1],cam_pos[2]])
								for point in pl:
									survey_mode = tde4.getPointSurveyMode(pg,point)
									if tde4.isPointCalculated3D(pg,point):
										if survey_mode == "SURVEY_FREE" or survey_mode == "SURVEY_APPROX":								
											p3d = vec3d(tde4.getPointCalcPosition3D(pg,point))
											p3d = p3d + vec3d(float(power),0,0)
											tde4.setPointCalcPosition3D(pg,point,p3d.list())											
										if survey_mode == "SURVEY_EXACT" or survey_mode == "SURVEY_LINEUP":
											p3d = vec3d(tde4.getPointSurveyPosition3D(pg,point))
											p3d = p3d + vec3d(float(power),0,0)
											tde4.setPointSurveyPosition3D(pg,point,p3d.list())
								if toggle_models == 1:
									mlist = tde4.get3DModelList(pg,1)
									for model in mlist:
										tde4.set3DModelSurveyFlag(pg,model,0)
										mpos = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame))
										mpos = mpos + vec3d(float(power),0,0)
										tde4.set3DModelPosition3D(pg,model,mpos.list())	
							if widget == "pos_y+" or widget == "pos_y-":
								if widget == "pos_y-": power = -float(power)
								for frame in range(1,frames+1):
									cam_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
									cam_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))							
									pos_y = float(cam_pos[1]) + float(power)
									tde4.setPGroupPosition3D(pg,cam,frame,[cam_pos[0],pos_y,cam_pos[2]])
								for point in pl:
									survey_mode = tde4.getPointSurveyMode(pg,point)
									if tde4.isPointCalculated3D(pg,point):	
										if survey_mode == "SURVEY_FREE" or survey_mode == "SURVEY_APPROX":								
											p3d = vec3d(tde4.getPointCalcPosition3D(pg,point))										
											p3d = p3d + vec3d(0,float(power),0)
											tde4.setPointCalcPosition3D(pg,point,p3d.list())
										if survey_mode == "SURVEY_EXACT" or survey_mode == "SURVEY_LINEUP":
											p3d = vec3d(tde4.getPointSurveyPosition3D(pg,point))
											p3d = p3d + vec3d(0,float(power),0)											
											tde4.setPointSurveyPosition3D(pg,point,p3d.list())
								if toggle_models == 1:
									mlist = tde4.get3DModelList(pg,1)
									for model in mlist:
										tde4.set3DModelSurveyFlag(pg,model,0)
										mpos = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame))
										mpos = mpos + vec3d(0,float(power),0)
										tde4.set3DModelPosition3D(pg,model,mpos.list())																
							if widget == "pos_z+" or widget == "pos_z-":
								if widget == "pos_z-": power = -float(power)
								for frame in range(1,frames+1):
									cam_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
									cam_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))							
									pos_z = float(cam_pos[2]) + float(power)
									tde4.setPGroupPosition3D(pg,cam,frame,[cam_pos[0],cam_pos[1],pos_z])
								for point in pl:
									survey_mode = tde4.getPointSurveyMode(pg,point)
									if tde4.isPointCalculated3D(pg,point):
										if survey_mode == "SURVEY_FREE" or survey_mode == "SURVEY_APPROX":								
											p3d = vec3d(tde4.getPointCalcPosition3D(pg,point))										
											p3d = p3d + vec3d(0,0,float(power))
											tde4.setPointCalcPosition3D(pg,point,p3d.list())
										if survey_mode == "SURVEY_EXACT" or survey_mode == "SURVEY_LINEUP":
											p3d = vec3d(tde4.getPointSurveyPosition3D(pg,point))
											p3d = p3d + vec3d(0,0,float(power))											
											tde4.setPointSurveyPosition3D(pg,point,p3d.list())
								if toggle_models == 1:
									mlist = tde4.get3DModelList(pg,1)
									for model in mlist:
										tde4.set3DModelSurveyFlag(pg,model,0)
										mpos = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame))
										mpos = mpos + vec3d(0,0,float(power))
										tde4.set3DModelPosition3D(pg,model,mpos.list())											
							#tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")						
							tde4.filterPGroup(pg,cam)
							cam = tde4.getCurrentCamera()
							pgl = tde4.getPGroupList()
							for pgroup in pgl:
								pg_type = tde4.getPGroupType(pgroup)
								if pg_type == "OBJECT":
									tde4.setPGroupScale3D(pgroup,tde4.getPGroupScale3D(pgroup))												
					#scene global or local or around 3dpoint rotation nudge...
					if r_space == 1 or r_space == 2 or r_space == 3 or r_space == 4:
						if widget == "rot_x+" or widget == "rot_x-" or widget == "rot_y+" or widget == "rot_y-" or widget == "rot_z+" or widget == "rot_z-":
							toggle_models = tde4.getWidgetValue(self.req,"move_3dmodels")
							if widget == "rot_x+" or widget == "rot_x-":
								if widget == "rot_x-": r_power = -float(r_power)
								null = 0
								if r_space == 1 or r_space == 2:
									pivot = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
								if r_space == 3 or r_space == 4:
									point_name = tde4.getWidgetValue(self.req,"pivot_3dpoint")
									f = tde4.findPointByName(pg,point_name)
									if f != None:
										pivot = tde4.getPointCalcPosition3D(pg,f)									
									else:
										null = 1
										#tde4.postQuestionRequester(self.window_title,"Error, please pick pivot 3dpoint.","Ok")
								if r_space == 1 or r_space == 2 or r_space == 3 or r_space == 4:
									if null != 1:
										cam_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
										rx = float(r_power) * math.pi / 180.0
										ry = 0
										rz = 0
										if r_space == 1 or r_space == 3:
											delta_rot_global = rot3d(rx,ry,rz,VL_APPLY_ZXY)
										if r_space == 2 or r_space == 4:
											delta_rot_local = mat3d(rot3d(rx,ry,rz,VL_APPLY_ZXY))
											delta_rot_global = cam_rot * delta_rot_local * (cam_rot).trans()										
										for frame in range(1,frames+1):
											cam_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
											cam_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
											p3d = delta_rot_global * (cam_pos - pivot) + pivot
											tde4.setPGroupPosition3D(pg,cam,frame,p3d.list())
											x_axis = vec3d(1,0,0)
											r = mat3d(rot3d(x_axis,math.radians(float(r_power))))
											if r_space == 1 or r_space == 3:
												rot = r * cam_rot
											if r_space == 2 or r_space == 4:
												rot = mat3d(delta_rot_global) * cam_rot
											tde4.setPGroupRotation3D(pg,cam,frame,rot.list())
										for point in pl:
											survey_mode = tde4.getPointSurveyMode(pg,point)
											if tde4.isPointCalculated3D(pg,point):
												if survey_mode == "SURVEY_FREE" or survey_mode == "SURVEY_APPROX":								
													p3d = vec3d(tde4.getPointCalcPosition3D(pg,point))																			
													p3d = delta_rot_global * (p3d - pivot) + pivot
													tde4.setPointCalcPosition3D(pg,point,p3d.list())
											if survey_mode == "SURVEY_EXACT" or survey_mode == "SURVEY_LINEUP":
												p3d = vec3d(tde4.getPointSurveyPosition3D(pg,point))
												p3d = delta_rot_global * (p3d - pivot) + pivot											
												tde4.setPointSurveyPosition3D(pg,point,p3d.list())
										if toggle_models == 1:
											mlist = tde4.get3DModelList(pg,1)
											for model in mlist:
												tde4.set3DModelSurveyFlag(pg,model,0)
												mpos = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame))
												m = mat3d(tde4.get3DModelRotationScale3D(pg,model)).trans()
												s = vec3d(m[0].norm2(),m[1].norm2(),m[2].norm2())
												s = mat3d(s[0],0.0,0.0,0.0,s[1],0.0,0.0,0.0,s[2])
												rotation_matrix = mat3d(m[0].unit(),m[1].unit(),m[2].unit()).trans()
												p3d = delta_rot_global * (mpos - pivot) + pivot
												tde4.set3DModelPosition3D(pg,model,p3d.list())
												mrot = mat3d(tde4.get3DModelRotationScale3D(pg,model))
												rot = mat3d(delta_rot_global) * rotation_matrix
												rot = rot * s
												tde4.set3DModelRotationScale3D(pg,model,rot.list())
										tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
										tde4.filterPGroup(pg,cam)		
									else:
										tde4.postQuestionRequester(self.window_title,"Error, please pick pivot 3dpoint.","Ok")
							if widget == "rot_y+" or widget == "rot_y-":
								if widget == "rot_y-": r_power = -float(r_power)
								null = 0
								if r_space == 1 or r_space == 2:
									pivot = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
								if r_space == 3 or r_space == 4:
									point_name = tde4.getWidgetValue(self.req,"pivot_3dpoint")
									f = tde4.findPointByName(pg,point_name)
									if f != None:
										pivot = tde4.getPointCalcPosition3D(pg,f)									
									else:
										null = 1
								if r_space == 1 or r_space == 2 or r_space == 3 or r_space == 4:
									if null != 1:	
										cam_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
										rx = 0
										ry = float(r_power) * math.pi / 180.0
										rz = 0
										if r_space == 1 or r_space == 3:
											delta_rot_global = rot3d(rx,ry,rz,VL_APPLY_ZXY)
										if r_space == 2 or r_space == 4:
											delta_rot_local = mat3d(rot3d(rx,ry,rz,VL_APPLY_ZXY))
											delta_rot_global = cam_rot * delta_rot_local * (cam_rot).trans()																
										for frame in range(1,frames+1):
											cam_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
											cam_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
											p3d = delta_rot_global * (cam_pos - pivot) + pivot
											tde4.setPGroupPosition3D(pg,cam,frame,p3d.list())
											y_axis = vec3d(0,1,0)
											r = mat3d(rot3d(y_axis,math.radians(float(r_power))))
											if r_space == 1 or r_space == 3:
												rot = r * cam_rot
											if r_space == 2 or r_space == 4:
												rot = mat3d(delta_rot_global) * cam_rot
											tde4.setPGroupRotation3D(pg,cam,frame,rot.list())
										for point in pl:
											survey_mode = tde4.getPointSurveyMode(pg,point)
											if tde4.isPointCalculated3D(pg,point):
												if survey_mode == "SURVEY_FREE" or survey_mode == "SURVEY_APPROX":								
													p3d = vec3d(tde4.getPointCalcPosition3D(pg,point))																			
													p3d = delta_rot_global * (p3d - pivot) + pivot
													tde4.setPointCalcPosition3D(pg,point,p3d.list())
											if survey_mode == "SURVEY_EXACT" or survey_mode == "SURVEY_LINEUP":
												p3d = vec3d(tde4.getPointSurveyPosition3D(pg,point))
												p3d = delta_rot_global * (p3d - pivot) + pivot											
												tde4.setPointSurveyPosition3D(pg,point,p3d.list())
										if toggle_models == 1:
											mlist = tde4.get3DModelList(pg,1)
											for model in mlist:
												tde4.set3DModelSurveyFlag(pg,model,0)
												mpos = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame))
												m = mat3d(tde4.get3DModelRotationScale3D(pg,model)).trans()
												s = vec3d(m[0].norm2(),m[1].norm2(),m[2].norm2())
												s = mat3d(s[0],0.0,0.0,0.0,s[1],0.0,0.0,0.0,s[2])
												rotation_matrix = mat3d(m[0].unit(),m[1].unit(),m[2].unit()).trans()
												p3d = delta_rot_global * (mpos - pivot) + pivot
												tde4.set3DModelPosition3D(pg,model,p3d.list())
												mrot = mat3d(tde4.get3DModelRotationScale3D(pg,model))
												rot = mat3d(delta_rot_global) * rotation_matrix
												rot = rot * s
												tde4.set3DModelRotationScale3D(pg,model,rot.list())
										tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
										tde4.filterPGroup(pg,cam)
									else:
										tde4.postQuestionRequester(self.window_title,"Error, please pick pivot 3dpoint.","Ok")												
							if widget == "rot_z+" or widget == "rot_z-":
								if widget == "rot_z-": r_power = -float(r_power)
								null = 0
								if r_space == 1 or r_space == 2:
									pivot = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
								if r_space == 3 or r_space == 4:
									point_name = tde4.getWidgetValue(self.req,"pivot_3dpoint")
									f = tde4.findPointByName(pg,point_name)
									if f != None:
										pivot = tde4.getPointCalcPosition3D(pg,f)									
									else:
										null = 1
								if r_space == 1 or r_space == 2 or r_space == 3 or r_space == 4:
									if null != 1:
										cam_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
										rx = 0
										ry = 0
										rz = float(r_power) * math.pi / 180.0
										if r_space == 1 or r_space == 3:
											delta_rot_global = rot3d(rx,ry,rz,VL_APPLY_ZXY)
										if r_space == 2 or r_space == 4:
											delta_rot_local = mat3d(rot3d(rx,ry,rz,VL_APPLY_ZXY))
											delta_rot_global = cam_rot * delta_rot_local * (cam_rot).trans()										
										for frame in range(1,frames+1):
											cam_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
											cam_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
											p3d = delta_rot_global * (cam_pos - pivot) + pivot
											tde4.setPGroupPosition3D(pg,cam,frame,p3d.list())									
											z_axis = vec3d(0,0,1)
											r = mat3d(rot3d(z_axis,math.radians(float(r_power))))
											if r_space == 1 or r_space == 3:
												rot = r * cam_rot
											if r_space == 2 or r_space == 4:
												rot = mat3d(delta_rot_global) * cam_rot
											tde4.setPGroupRotation3D(pg,cam,frame,rot.list())
										for point in pl:
											survey_mode = tde4.getPointSurveyMode(pg,point)
											if tde4.isPointCalculated3D(pg,point):
												if survey_mode == "SURVEY_FREE" or survey_mode == "SURVEY_APPROX":								
													p3d = vec3d(tde4.getPointCalcPosition3D(pg,point))																			
													p3d = delta_rot_global * (p3d - pivot) + pivot
													tde4.setPointCalcPosition3D(pg,point,p3d.list())
											if survey_mode == "SURVEY_EXACT" or survey_mode == "SURVEY_LINEUP":
												p3d = vec3d(tde4.getPointSurveyPosition3D(pg,point))
												p3d = delta_rot_global * (p3d - pivot) + pivot											
												tde4.setPointSurveyPosition3D(pg,point,p3d.list())
										if toggle_models == 1:
											mlist = tde4.get3DModelList(pg,1)
											for model in mlist:
												tde4.set3DModelSurveyFlag(pg,model,0)
												mpos = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame))
												m = mat3d(tde4.get3DModelRotationScale3D(pg,model)).trans()
												s = vec3d(m[0].norm2(),m[1].norm2(),m[2].norm2())
												s = mat3d(s[0],0.0,0.0,0.0,s[1],0.0,0.0,0.0,s[2])
												rotation_matrix = mat3d(m[0].unit(),m[1].unit(),m[2].unit()).trans()
												p3d = delta_rot_global * (mpos - pivot) + pivot
												tde4.set3DModelPosition3D(pg,model,p3d.list())
												mrot = mat3d(tde4.get3DModelRotationScale3D(pg,model))
												rot = mat3d(delta_rot_global) * rotation_matrix
												rot = rot * s
												tde4.set3DModelRotationScale3D(pg,model,rot.list())
									else:
										tde4.postQuestionRequester(self.window_title,"Error, please pick pivot 3dpoint.","Ok")
							#tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")												
							tde4.filterPGroup(pg,cam)
							cam = tde4.getCurrentCamera()
							pgl = tde4.getPGroupList()
							for pgroup in pgl:
								pg_type = tde4.getPGroupType(pgroup)
								if pg_type == "OBJECT":
									tde4.setPGroupScale3D(pgroup,tde4.getPGroupScale3D(pgroup))	
					#scene scale around pivot or around camera...
					if self.widget == "uniform_scale+" or self.widget == "uniform_scale-":
						null = 0	
						v = tde4.getWidgetValue(self.req,"scale_around_pivot")
						if v == 0:					
							pivot = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
						else:
							point_name = tde4.getWidgetValue(self.req,"pivot_3dpoint")
							f = tde4.findPointByName(pg,point_name)
							if f != None:
								pivot = tde4.getPointCalcPosition3D(pg,f)									
							else:
								null = 1	
						if v == 0 or v== 1:
							if null != 1:							
								if self.widget == "uniform_scale+" or self.widget == "uniform_scale-":
									if self.widget == "uniform_scale-": s_power = -float(s_power)
									sx = 1.0 + float(s_power)
									sy = 1.0 + float(s_power)
									sz = 1.0 + float(s_power)
									for i in range(1,frames+1):
										cam_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,i))
										p3d = (mat3d(sx,0,0,0,sy,0,0,0,sz) * (cam_pos - pivot)) + pivot
										tde4.setPGroupPosition3D(pg,cam,i,p3d.list())
									#tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
									tde4.filterPGroup(pg,cam)
									cam = tde4.getCurrentCamera()
									pgl = tde4.getPGroupList()
									for pgroup in pgl:
										pg_type = tde4.getPGroupType(pgroup)
										if pg_type == "OBJECT":
											#tde4.filterPGroup(pgroup,cam)
											tde4.setPGroupScale3D(pgroup,tde4.getPGroupScale3D(pgroup))							
									for point in pl:
										survey_mode = tde4.getPointSurveyMode(pg,point)
										if tde4.isPointCalculated3D(pg,point):
											if survey_mode == "SURVEY_FREE" or survey_mode == "SURVEY_APPROX":								
												p3d = vec3d(tde4.getPointCalcPosition3D(pg,point))																	
												sx = 1.0 + float(s_power)
												sy = 1.0 + float(s_power)
												sz = 1.0 + float(s_power)
												p3d = (mat3d(sx,0,0,0,sy,0,0,0,sz) * (p3d - pivot)) + pivot
												tde4.setPointCalcPosition3D(pg,point,p3d.list())
											if survey_mode == "SURVEY_EXACT" or survey_mode == "SURVEY_LINEUP":
												p3d = vec3d(tde4.getPointSurveyPosition3D(pg,point))
												sx = 1.0 + float(s_power)
												sy = 1.0 + float(s_power)
												sz = 1.0 + float(s_power)
												p3d = (mat3d(sx,0,0,0,sy,0,0,0,sz) * (p3d - pivot)) + pivot
												tde4.setPointSurveyPosition3D(pg,point,p3d.list())
									if toggle_models == 1:
										mlist = tde4.get3DModelList(pg,1)
										for model in mlist:	
											tde4.set3DModelSurveyFlag(pg,model,0)
											m = mat3d(tde4.get3DModelRotationScale3D(pg,model)).trans()
											s = vec3d(m[0].norm2(),m[1].norm2(),m[2].norm2())
											#print (1+float(s_power)) * s[0]
											s = mat3d((1+float(s_power))*s[0],0.0,0.0,0.0,(1+float(s_power))*s[1],0.0,0.0,0.0,(1+float(s_power))*s[2])
											rotation_matrix = mat3d(m[0].unit(),m[1].unit(),m[2].unit()).trans()
											mpos = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame))
											sx = 1.0 + float(s_power)
											sy = 1.0 + float(s_power)
											sz = 1.0 + float(s_power)	
											p3d = (mat3d(sx,0,0,0,sy,0,0,0,sz) * (mpos - pivot)) + pivot
											tde4.set3DModelPosition3D(pg,model,p3d.list())
											f = rotation_matrix * s
											tde4.set3DModelRotationScale3D(pg,model,f.list())
							else:
								tde4.postQuestionRequester(self.window_title,"Error, please pick pivot 3dpoint.","Ok")										
				else:
					tde4.postQuestionRequester(self.window_title,"there are no points.","OK")			
				
##################################################################################################

#build GUI....
	def GUI(self):
		self.window_title = "Patcha Nudge3D Tool v1.3"
		self.req = tde4.createCustomRequester()
#type widget...
		tde4.addOptionMenuWidget(self.req,"selected_menu","Selected Type","Camera","Object PGroup","3D Model","Scene")
#sep1 widget...
		tde4.addSeparatorWidget(self.req,"sep1")
		tde4.setWidgetAttachModes(self.req,"sep1","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"sep1",2,98,25,0)	
#translation menubar widget...
		tde4.addMenuBarWidget(self.req,"t_menu_bar")
		tde4.setWidgetAttachModes(self.req,"t_menu_bar","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"t_menu_bar",0,100,45,0)
		tde4.addMenuWidget(self.req,"t_nudge","Translation Nudge","t_menu_bar",0)
#translation button widgets...
		tde4.addButtonWidget(self.req,"pos_x+","Pos +X",70,10)
		tde4.setWidgetAttachModes(self.req,"pos_x+","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"pos_x+",10,30,70,0)		
		tde4.addButtonWidget(self.req,"pos_y+","Pos +Y",70,10)
		tde4.setWidgetAttachModes(self.req,"pos_y+","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"pos_y+",40,60,70,0)			
		tde4.addButtonWidget(self.req,"pos_z+","Pos +Z",70,10)
		tde4.setWidgetAttachModes(self.req,"pos_z+","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"pos_z+",70,90,70,0)			
		tde4.addButtonWidget(self.req,"pos_x-","Pos -X",70,10)
		tde4.setWidgetAttachModes(self.req,"pos_x-","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"pos_x-",10,30,100,0)		
		tde4.addButtonWidget(self.req,"pos_y-","Pos -Y",70,10)
		tde4.setWidgetAttachModes(self.req,"pos_y-","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"pos_y-",40,60,100,0)			
		tde4.addButtonWidget(self.req,"pos_z-","Pos -Z",70,10)
		tde4.setWidgetAttachModes(self.req,"pos_z-","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"pos_z-",70,90,100,0)	
#translation pivot widgets...
		tde4.addOptionMenuWidget(self.req,"t_space","Pivot Space","Global","Local/Screen")
		tde4.addScaleWidget(self.req,"t_increment"," ","DOUBLE",0.001,0.1,0.05)
		tde4.setWidgetAttachModes(self.req,"t_increment","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"t_increment",5,75,153,0)	
		tde4.addTextFieldWidget(self.req,"t_increment_factor"," ","0.05")
		tde4.setWidgetAttachModes(self.req,"t_increment_factor","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"t_increment_factor",78,98,153,0)
#rotation menubar widget...
		tde4.addMenuBarWidget(self.req,"r_menu_bar")
		tde4.setWidgetAttachModes(self.req,"r_menu_bar","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"r_menu_bar",0,100,180,0)
		tde4.addMenuWidget(self.req,"r_nudge","Rotation Nudge","r_menu_bar",0)		
#rotation button widgets...
		tde4.addButtonWidget(self.req,"rot_x+","Rot +X",70,10)
		tde4.setWidgetAttachModes(self.req,"rot_x+","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"rot_x+",10,30,205,0)
		tde4.addButtonWidget(self.req,"rot_y+","Rot +Y",70,10)
		tde4.setWidgetAttachModes(self.req,"rot_y+","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"rot_y+",40,60,205,0)		
		tde4.addButtonWidget(self.req,"rot_z+","Rot +Z",70,10)
		tde4.setWidgetAttachModes(self.req,"rot_z+","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"rot_z+",70,90,205,0)		
		tde4.addButtonWidget(self.req,"rot_x-","Rot -X",70,10)
		tde4.setWidgetAttachModes(self.req,"rot_x-","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"rot_x-",10,30,235,0)		
		tde4.addButtonWidget(self.req,"rot_y-","Rot -Y",70,10)
		tde4.setWidgetAttachModes(self.req,"rot_y-","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"rot_y-",40,60,235,0)			
		tde4.addButtonWidget(self.req,"rot_z-","Rot -Z",70,10)
		tde4.setWidgetAttachModes(self.req,"rot_z-","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"rot_z-",70,90,235,0)	
#rotation pivot widgets...
		tde4.addOptionMenuWidget(self.req,"r_space","Pivot Space","Global","Local/Screen","Around 3DPoint - Global","Around 3DPoint - Local")
		tde4.addScaleWidget(self.req,"r_increment"," ","DOUBLE",0.001,0.1,0.05)
		tde4.setWidgetAttachModes(self.req,"r_increment","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"r_increment",5,75,288,0)
		tde4.addTextFieldWidget(self.req,"r_increment_factor"," ","0.05")
		tde4.setWidgetAttachModes(self.req,"r_increment_factor","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"r_increment_factor",78,98,288,0)
#scale menubar widget...
		tde4.addMenuBarWidget(self.req,"s_menu_bar")
		tde4.setWidgetAttachModes(self.req,"s_menu_bar","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"s_menu_bar",0,100,315,0)
		tde4.addMenuWidget(self.req,"s_nudge","Scale Nudge","s_menu_bar",0)	
#scale button widgets...
		tde4.addButtonWidget(self.req,"scale_x+","Scale +X",70,10)
		tde4.setWidgetAttachModes(self.req,"scale_x+","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"scale_x+",10,30,340,0)
		tde4.setWidgetSensitiveFlag(self.req,"scale_x+",0)		
		tde4.addButtonWidget(self.req,"scale_y+","Scale +Y",70,10)
		tde4.setWidgetAttachModes(self.req,"scale_y+","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"scale_y+",40,60,340,0)	
		tde4.setWidgetSensitiveFlag(self.req,"scale_y+",0)			
		tde4.addButtonWidget(self.req,"scale_z+","Scale +Z",70,10)
		tde4.setWidgetAttachModes(self.req,"scale_z+","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"scale_z+",70,90,340,0)
		tde4.setWidgetSensitiveFlag(self.req,"scale_z+",0)				
		tde4.addButtonWidget(self.req,"scale_x-","Scale -X",70,10)
		tde4.setWidgetAttachModes(self.req,"scale_x-","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"scale_x-",10,30,370,0)	
		tde4.setWidgetSensitiveFlag(self.req,"scale_x-",0)		
		tde4.addButtonWidget(self.req,"scale_y-","Scale -Y",70,10)
		tde4.setWidgetAttachModes(self.req,"scale_y-","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"scale_y-",40,60,370,0)
		tde4.setWidgetSensitiveFlag(self.req,"scale_y-",0)				
		tde4.addButtonWidget(self.req,"scale_z-","Scale -Z",70,10)
		tde4.setWidgetAttachModes(self.req,"scale_z-","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"scale_z-",70,90,370,0)
		tde4.setWidgetSensitiveFlag(self.req,"scale_z-",0)

		tde4.addButtonWidget(self.req,"uniform_scale-","Uniform Scale -",70,10)
		tde4.setWidgetAttachModes(self.req,"uniform_scale-","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"uniform_scale-",8,33,395,0)
		tde4.setWidgetSensitiveFlag(self.req,"uniform_scale-",0)

		tde4.addButtonWidget(self.req,"uniform_scale+","Uniform Scale +",70,10)
		tde4.setWidgetAttachModes(self.req,"uniform_scale+","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"uniform_scale+",38,63,395,0)	
		tde4.setWidgetSensitiveFlag(self.req,"uniform_scale+",0)

		tde4.addToggleWidget(self.req,"scale_around_pivot","Around 3dpoint")
		tde4.setWidgetAttachModes(self.req,"scale_around_pivot","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"scale_around_pivot",93,98,395,0)
		tde4.setWidgetSensitiveFlag(self.req,"scale_around_pivot",0)		

		tde4.addScaleWidget(self.req,"s_increment"," ","DOUBLE",0.001,1.0,0.5)
		tde4.setWidgetAttachModes(self.req,"s_increment","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"s_increment",5,75,423,0)
		tde4.setWidgetSensitiveFlag(self.req,"s_increment",0)
		tde4.addTextFieldWidget(self.req,"s_increment_factor"," ","0.5")
		tde4.setWidgetAttachModes(self.req,"s_increment_factor","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"s_increment_factor",78,98,423,0)
		tde4.setWidgetSensitiveFlag(self.req,"s_increment_factor",0)
#sep2 widget...
		tde4.addSeparatorWidget(self.req,"sep2")
		tde4.setWidgetAttachModes(self.req,"sep2","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"sep2",2,98,440,0)		
#look through camera text field widget...
		tde4.addTextFieldWidget(self.req,"look","look thru camera"," ")
		tde4.setWidgetAttachModes(self.req,"look","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"look",37,98,457,0)
		tde4.setWidgetSensitiveFlag(self.req,"look",0)
#selected text field widget...
		tde4.addTextFieldWidget(self.req,"sel","effected"," ")
		tde4.setWidgetAttachModes(self.req,"sel","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"sel",20,98,487,0)
		tde4.setWidgetValue(self.req,"sel",str(tde4.getCameraName(tde4.getCurrentCamera())))
		tde4.setWidgetSensitiveFlag(self.req,"sel",0)
#pivot on 3dpoint...
		tde4.addTextFieldWidget(self.req,"pivot_3dpoint","Pivot on 3DPoints"," ")
		tde4.setWidgetAttachModes(self.req,"pivot_3dpoint","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"pivot_3dpoint",38,98,517,0)
		tde4.setWidgetSensitiveFlag(self.req,"pivot_3dpoint",0)
#pick pivot point button...
		tde4.addButtonWidget(self.req,"pick_pivot","Pick Pivot 3dpoint",70,10)
		tde4.setWidgetAttachModes(self.req,"pick_pivot","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"pick_pivot",5,45,545,0)	
#average 3dpoint button...
		tde4.addButtonWidget(self.req,"avg_3dpoint","Create average 3dpoint",70,10)
		tde4.setWidgetAttachModes(self.req,"avg_3dpoint","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"avg_3dpoint",50,95,545,0)
#add sep3 widget...
		tde4.addSeparatorWidget(self.req,"sep3")
		tde4.setWidgetAttachModes(self.req,"sep3","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"sep3",2,98,562,0)
		"""#frame in widget...
				tde4.addTextFieldWidget(self.req,"frame_in","Frame in")
				tde4.setWidgetAttachModes(self.req,"frame_in","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
				tde4.setWidgetOffsets(self.req,"frame_in",20,45,580,0)	
				tde4.setWidgetSensitiveFlag(self.req,"frame_in",0)			
		#frame out widget...
				tde4.addTextFieldWidget(self.req,"frame_out","Frame out")
				tde4.setWidgetAttachModes(self.req,"frame_out","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
				tde4.setWidgetOffsets(self.req,"frame_out",70,97,580,0)
				tde4.setWidgetSensitiveFlag(self.req,"frame_out",0)
		#pick frame in button widget...
				tde4.addButtonWidget(self.req,"pick_frame_in","Pick frame in",70,10)
				tde4.setWidgetAttachModes(self.req,"pick_frame_in","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
				tde4.setWidgetOffsets(self.req,"pick_frame_in",5,43,610,0)
				tde4.setWidgetSensitiveFlag(self.req,"pick_frame_in",0)		
		#pick frame out button widget...
				tde4.addButtonWidget(self.req,"pick_frame_out","Pick frame out",70,10)
				tde4.setWidgetAttachModes(self.req,"pick_frame_out","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
				tde4.setWidgetOffsets(self.req,"pick_frame_out",60,98,610,0)
				tde4.setWidgetSensitiveFlag(self.req,"pick_frame_out",0)
		#enable frame range widget...
				tde4.addToggleWidget(self.req,"toggle","enable frame range")
				tde4.setWidgetAttachModes(self.req,"toggle","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
				tde4.setWidgetOffsets(self.req,"toggle",38,43,640,0)
		#set key button widget...
				tde4.addButtonWidget(self.req,"set_key","set Pivot frame",70,10)
				tde4.setWidgetAttachModes(self.req,"set_key","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
				tde4.setWidgetOffsets(self.req,"set_key",46,73,640,0)
				tde4.setWidgetSensitiveFlag(self.req,"set_key",0)
		#set key text field widget...
				tde4.addTextFieldWidget(self.req,"set_key_frame"," ")
				tde4.setWidgetAttachModes(self.req,"set_key_frame","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
				tde4.setWidgetOffsets(self.req,"set_key_frame",77,98,640,0)	
				tde4.setWidgetSensitiveFlag(self.req,"set_key_frame",0)
		#add sep4 widget...
				tde4.addSeparatorWidget(self.req,"sep4")
				tde4.setWidgetAttachModes(self.req,"sep4","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
				tde4.setWidgetOffsets(self.req,"sep4",2,98,657,0)"""
#focal length nudge menubar widget...
		tde4.addMenuBarWidget(self.req,"focal_menu_bar")
		tde4.setWidgetAttachModes(self.req,"focal_menu_bar","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"focal_menu_bar",0,100,578,0)
		tde4.addMenuWidget(self.req,"focal_nudge","Focal Length Nudge","focal_menu_bar",0)
#focal length increment factor widget...
		tde4.addTextFieldWidget(self.req,"focal_increment_factor"," ","0.1")
		tde4.setWidgetAttachModes(self.req,"focal_increment_factor","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"focal_increment_factor",5,20,608,0)
#focal length inc/dec button widgets...
		tde4.addButtonWidget(self.req,"focal_dec","-")
		tde4.setWidgetAttachModes(self.req,"focal_dec","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"focal_dec",23,38,608,0)
		tde4.addButtonWidget(self.req,"focal_inc","+")
		tde4.setWidgetAttachModes(self.req,"focal_inc","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"focal_inc",41,56,608,0)
#calc match frame button...
		tde4.addToggleWidget(self.req,"match_frame","Calc Match Frame",1)
		tde4.setWidgetAttachModes(self.req,"match_frame","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"match_frame",90,95,608,0)	
#add sep5 widget...
		tde4.addSeparatorWidget(self.req,"sep5")
		tde4.setWidgetAttachModes(self.req,"sep5","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"sep5",2,98,628,0)
#add move 3dmodels along with scene widget...
		tde4.addToggleWidget(self.req,"move_3dmodels","Move selected 3DModels along with Scene",0)
		tde4.setWidgetAttachModes(self.req,"move_3dmodels","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"move_3dmodels",80,85,648,0)
		tde4.setWidgetSensitiveFlag(self.req,"move_3dmodels",0)
#widget callbacks...
		tde4.setWidgetCallbackFunction(self.req,"pos_x+","do.Nudge_Callback")				
		tde4.setWidgetCallbackFunction(self.req,"pos_x-","do.Nudge_Callback")			
		tde4.setWidgetCallbackFunction(self.req,"pos_y+","do.Nudge_Callback")			
		tde4.setWidgetCallbackFunction(self.req,"pos_y-","do.Nudge_Callback")			
		tde4.setWidgetCallbackFunction(self.req,"pos_z+","do.Nudge_Callback")			
		tde4.setWidgetCallbackFunction(self.req,"pos_z-","do.Nudge_Callback")	
		tde4.setWidgetCallbackFunction(self.req,"rot_x+","do.Nudge_Callback")	
		tde4.setWidgetCallbackFunction(self.req,"rot_x-","do.Nudge_Callback")	
		tde4.setWidgetCallbackFunction(self.req,"rot_y+","do.Nudge_Callback")	
		tde4.setWidgetCallbackFunction(self.req,"rot_y-","do.Nudge_Callback")	
		tde4.setWidgetCallbackFunction(self.req,"rot_z+","do.Nudge_Callback")	
		tde4.setWidgetCallbackFunction(self.req,"rot_z-","do.Nudge_Callback")	
		tde4.setWidgetCallbackFunction(self.req,"scale_x+","do.Nudge_Callback")	
		tde4.setWidgetCallbackFunction(self.req,"scale_x-","do.Nudge_Callback")			
		tde4.setWidgetCallbackFunction(self.req,"scale_y+","do.Nudge_Callback")	
		tde4.setWidgetCallbackFunction(self.req,"scale_y-","do.Nudge_Callback")			
		tde4.setWidgetCallbackFunction(self.req,"scale_z+","do.Nudge_Callback")	
		tde4.setWidgetCallbackFunction(self.req,"scale_z-","do.Nudge_Callback")			
		tde4.setWidgetCallbackFunction(self.req,"uniform_scale+","do.Nudge_Callback")		
		tde4.setWidgetCallbackFunction(self.req,"uniform_scale-","do.Nudge_Callback")	
#increment widgets callbacks...
		tde4.setWidgetCallbackFunction(self.req,"t_increment","do.Increment_Sensitive")
		tde4.setWidgetCallbackFunction(self.req,"t_increment_factor","do.Increment_Sensitive")
		tde4.setWidgetCallbackFunction(self.req,"r_increment","do.Increment_Sensitive")	
		tde4.setWidgetCallbackFunction(self.req,"r_increment_factor","do.Increment_Sensitive")
		tde4.setWidgetCallbackFunction(self.req,"s_increment","do.Increment_Sensitive")	
		tde4.setWidgetCallbackFunction(self.req,"s_increment_factor","do.Increment_Sensitive")	
#pivot menu callback...
		tde4.setWidgetCallbackFunction(self.req,"selected_menu","do.Pivot_Menu_Edit")
		tde4.setWidgetCallbackFunction(self.req,"t_space","do.Pivot_Menu_Edit")
		tde4.setWidgetCallbackFunction(self.req,"r_space","do.Pivot_Menu_Edit")	
#pick pivot point callback...
		tde4.setWidgetCallbackFunction(self.req,"pick_pivot","do.Pick_Pivot")
#average 3dpoint callback...
		tde4.setWidgetCallbackFunction(self.req,"avg_3dpoint","do.Average_3dpoint")	
#frame range callback...		
		#tde4.setWidgetCallbackFunction(self.req,"toggle","do.Frame_Range")	
#set key frame callback...
		#tde4.setWidgetCallbackFunction(self.req,"set_key","do.Set_Keyframe")
#pick frame in callback...
		#tde4.setWidgetCallbackFunction(self.req,"pick_frame_in","do.Set_Keyframe")
#pick frame out callback...
		#tde4.setWidgetCallbackFunction(self.req,"pick_frame_out","do.Set_Keyframe")
#scale around 3dpoint toggle widget callback...
		tde4.setWidgetCallbackFunction(self.req,"scale_around_pivot","do.Scale_Toggle")
#focal nudget callback...
		tde4.setWidgetCallbackFunction(self.req,"focal_inc","do.Focal_Nudge")
		tde4.setWidgetCallbackFunction(self.req,"focal_dec","do.Focal_Nudge")
		tde4.postCustomRequesterAndContinue(self.req,self.window_title,380,678,"do.update")
		
do = Nudge()
do.main()
		



