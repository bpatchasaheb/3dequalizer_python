# 3DE4.script.name:Copy FOV to camera...
# 3DE4.script.version:		v1.0.1
# 3DE4.script.comment:	Copies FOV values from one camera/proxy, to another
# 3DE4.script.gui:	Lineup Controls::Edit
# 3DE4.script.gui:	Orientation Controls::Edit
# 3DE4.script.gui:	Manual Tracking Controls::Edit
# 3DE4.script.hide: false
# 3DE4.script.startup: false
#Patcha Saheb/Michael Karp


class Copy_FOV():

	def main(self):
		self.GUI()
		
	def Copy_Callback(self,requester,widget,action):
		self.req = requester
		self.widget = widget
		self.action = action
		pg = tde4.getCurrentPGroup()
		cam = tde4.getCurrentCamera()
		frame = tde4.getCurrentFrame(cam)
		cam_list = []
		n = tde4.getCameraList(0)
		for cam in n:
			name = tde4.getCameraName(cam)
			cam_list.append(name)
		s_cam = tde4.getWidgetValue(self.req,"sourceCam")
		s_proxy = tde4.getWidgetValue(self.req,"sourceProxy")
		t_cam = tde4.getWidgetValue(self.req,"targetCam")
		t_proxy = tde4.getWidgetValue(self.req,"targetProxy")
		if widget == "copy":
			s_proxy_fov = tde4.setCameraProxyFootage(n[s_cam-1],s_proxy-1)
			s_fov = tde4.getCameraFOV(n[s_cam-1])
			tde4.setCameraProxyFootage(n[t_cam-1],t_proxy-1)
			tde4.setCameraFOV(n[t_cam-1],s_fov[0],s_fov[1],s_fov[2],s_fov[3])
			s_fov = str(str(s_fov[0]) + " " + str(s_fov[1]) + " " + str(s_fov[2]) + " " + str(s_fov[3]))
			t_fov = tde4.getCameraFOV(n[t_cam-1])
			tde4.setWidgetValue(self.req,"sourceFOV",str(s_fov))
			t_fov = str(str(t_fov[0]) + " " + str(t_fov[1]) + " " + str(t_fov[2]) + " " + str(t_fov[3]))
			tde4.setWidgetValue(self.req,"targetFOV",t_fov)
		if widget == "refresh":
			tde4.modifyOptionMenuWidget(self.req,"sourceCam","Source Camera",*cam_list)
			tde4.modifyOptionMenuWidget(self.req,"targetCam","Target Camera",*cam_list)
		if widget == "close":
			tde4.unpostCustomRequester(self.req)

	def GUI(self):
		self.req = tde4.createCustomRequester()
		self.copyTitle="Copy FOV to camera v1.0.1"
#camera list...
		pg = tde4.getCurrentPGroup()
		cam = tde4.getCurrentCamera()
		frame = tde4.getCurrentFrame(cam)
		cam_list = []
		n = tde4.getCameraList(0)
		for cam in n:
			name = tde4.getCameraName(cam)
			cam_list.append(name)
#source widgets...
		tde4.addOptionMenuWidget(self.req,"sourceCam","Source Camera",*cam_list)
		tde4.addOptionMenuWidget(self.req,"sourceProxy","Source Proxy","Main","Alternate #1","Alternate #2","Alternate #3")
		tde4.addTextFieldWidget(self.req, "sourceFOV", "Source FOV", " ")
		tde4.addSeparatorWidget(self.req,"sep1")
#target widgets...
		tde4.addOptionMenuWidget(self.req,"targetCam","Target Camera",*cam_list)
		tde4.addOptionMenuWidget(self.req,"targetProxy","Target Proxy","Main","Alternate #1","Alternate #2","Alternate #3")
		tde4.addTextFieldWidget(self.req, "targetFOV", "Target FOV", " ")
#disable widgets...
		tde4.setWidgetSensitiveFlag(self.req,"sourceFOV",0)
		tde4.setWidgetSensitiveFlag(self.req,"targetFOV",0)
#copy button widget...
		tde4.addButtonWidget(self.req,"copy","Copy FOV",90,10)	
		tde4.setWidgetAttachModes(self.req,"copy","ATTACH_POSITION", "ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"copy",46,62,185,0)
#refresh button widget...
		tde4.addButtonWidget(self.req,"refresh","Refresh",90,10)	
		tde4.setWidgetAttachModes(self.req,"refresh","ATTACH_POSITION", "ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"refresh",64,80,185,0)
#close button widget...
		tde4.addButtonWidget(self.req,"close","Close",90,10)	
		tde4.setWidgetAttachModes(self.req,"close","ATTACH_POSITION", "ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"close",82,97,185,0)
#callback...
		tde4.setWidgetCallbackFunction(self.req,"copy","copy.Copy_Callback")
		tde4.setWidgetCallbackFunction(self.req,"refresh","copy.Copy_Callback")
		tde4.setWidgetCallbackFunction(self.req,"close","copy.Copy_Callback")		
		tde4.postCustomRequesterAndContinue(self.req,self.copyTitle,550,220)
		
copy = Copy_FOV()
copy.main()
