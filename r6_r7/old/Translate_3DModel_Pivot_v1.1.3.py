# 3DE4.script.name:	Translate 3DModel Pivot...
# 3DE4.script.version:	v1.1.3
# 3DE4.script.gui:	Orientation Controls::3D Models
# 3DE4.script.gui.button:	Orientation Controls::Model Pivot, align-bottom-left, 70, 20
# 3DE4.script.gui.button:	Lineup Controls::Model Pivot, align-bottom-left, 80, 20
#24-July-2015
#Patcha Saheb(patchasaheb@gmail.com)

from vl_sdv import*

pg = tde4.getCurrentPGroup()
cam = tde4.getCurrentCamera()
frame = tde4.getCurrentFrame(cam)
mlist = tde4.get3DModelList(pg,1)
window_title = "Patcha Translate 3DModel Pivot v1.1.3"

def update(req):
	pg = tde4.getCurrentPGroup()
	cam = tde4.getCurrentCamera()
	frame = tde4.getCurrentFrame(cam)
	mlist = tde4.get3DModelList(pg,1)
	pl = tde4.getPointList(pg,1)
	try:
		if len(mlist) > 0:
			model_name = tde4.get3DModelName(pg,mlist[0])
			tde4.setWidgetValue(req,"name",str(model_name))
		else:
			tde4.setWidgetValue(req,"name"," ")
	except:
		pass
	try:
		if len(pl) > 0:
			point_name = tde4.getPointName(pg,pl[0])
			tde4.setWidgetValue(req,"name",str(str(model_name) + " " + "&" + " " + str(point_name)))
	except:
		pass
		
#update names...
def Names(req,widget,action):
		pg = tde4.getCurrentPGroup()
		cam = tde4.getCurrentCamera()
		frame = tde4.getCurrentFrame(cam)
		mlist = tde4.get3DModelList(pg,1)
		if len(mlist) == 1:
			model = mlist[0]
			name = tde4.get3DModelName(pg,model)
			if widget == "parent_get":
				tde4.setWidgetValue(req,"parent",str(name))
				p_v = tde4.getWidgetValue(req,"parent")
				c_v = tde4.getWidgetValue(req,"child")
				if p_v == c_v:
					tde4.setWidgetValue(req,"parent"," ")
					tde4.postQuestionRequester(window_title,"Error, parent and child models are should not be same.","Ok")
			if widget == "child_get":
				tde4.setWidgetValue(req,"child",str(name))
				p_v = tde4.getWidgetValue(req,"parent")
				c_v = tde4.getWidgetValue(req,"child")				
				if p_v == c_v:
					tde4.setWidgetValue(req,"child"," ")
					tde4.postQuestionRequester(window_title,"Error, parent and child models are should not be same.","Ok")
		else:
			tde4.postQuestionRequester(window_title,"Error, Exactly one 3DModel must be selected or 3DModels should be under current PGroup","Ok")	

#match pivots function...
def Match_Pivot(req,widget,action):
	cam	= tde4.getCurrentCamera()
	pg	= tde4.getCurrentPGroup()
	frame = tde4.getCurrentFrame(cam)
	mlist = tde4.get3DModelList(pg,0)
	p_v = tde4.getWidgetValue(req,"parent")
	c_v = tde4.getWidgetValue(req,"child")	
	if c_v and p_v != " ":
		for model in mlist:
			name = tde4.get3DModelName(pg,model)
			if name == p_v:
				parent = model
		for model in mlist:
			name = tde4.get3DModelName(pg,model)
			if name == c_v:
				child = model
		#turn off parent & child models survey data...	
		tde4.set3DModelSurveyFlag(pg,parent,0)
		tde4.set3DModelSurveyFlag(pg,child,0)
		parent_pos = tde4.get3DModelPosition3D(pg,parent,cam,frame)
		parent_rot = tde4.get3DModelRotationScale3D(pg,parent)
		tde4.set3DModelPosition3D(pg,child,parent_pos)
		tde4.set3DModelRotationScale3D(pg,child,parent_rot)		
		parent_list = []
		child_list = []
		n = tde4.get3DModelNoVertices(pg,parent)
		mrot = tde4.get3DModelRotationScale3D(pg,parent)
		mpos= tde4.get3DModelPosition3D(pg,parent,cam,frame)
		for i in range(0,n):
			v = tde4.get3DModelVertex(pg,parent,i,cam,frame)
			vector = mat3d(mrot).invert()*(vec3d(0,0,0)-vec3d(mpos))
			v[0] = v[0]-vector[0]
			v[1] = v[1]-vector[1]
			v[2] = v[2]-vector[2]
			v = mat3d(mrot)*vec3d(v)
			parent_list.append(v)
			break
		n = tde4.get3DModelNoVertices(pg,child)
		mrot = tde4.get3DModelRotationScale3D(pg,child)
		mpos= tde4.get3DModelPosition3D(pg,child,cam,frame)
		for i in range(0,n):
			v = tde4.get3DModelVertex(pg,child,i,cam,frame)
			vector = mat3d(mrot).invert()*(vec3d(0,0,0)-vec3d(mpos))
			v[0] = v[0]-vector[0]
			v[1] = v[1]-vector[1]
			v[2] = v[2]-vector[2]
			v = mat3d(mrot)*vec3d(v)
			child_list.append(v)
			break
		newpos = vec3d(child_list[0]) - vec3d(parent_list[0])
		newpos = vec3d(mpos) - vec3d(newpos)
		tde4.set3DModelPosition3D(pg,child,newpos.list())
	else:
		tde4.postQuestionRequester(window_title,"Error, please select Parent & Child 3DModels","Ok")
#function for getting vector and baked vertices...		
def Vector(pg,model,cam,frame,p3d,vlist):
	mpos = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame))
	mrot = tde4.get3DModelRotationScale3D(pg,model)
	vector = mat3d(mrot).invert() * (vec3d(p3d) - vec3d(mpos))
	l = []
	for i in range(0,vlist):
		v = tde4.get3DModelVertex(pg,model,i,cam,frame)
		v[0] = v[0] - vector[0]
		v[1] = v[1] - vector[1]
		v[2] = v[2] - vector[2]
		l.append(v)
	return l	
	
#function for getting center pivot position...
def Center_Pivot(pg,model,cam,frame,vlist):
	mpos = tde4.get3DModelPosition3D(pg,model,cam,frame)
	mrot = tde4.get3DModelRotationScale3D(pg,model)
	n = tde4.get3DModelNoVertices(pg,model)
	x_list = []
	y_list = []
	z_list = []
	for i in range(0,n):
		vpos = tde4.get3DModelVertex(pg,model,i,cam,frame)
		x_list.append(vpos[0])
		y_list.append(vpos[1])
		z_list.append(vpos[2])
	x = sum(x_list) / len(x_list)
	y = sum(y_list) / len(y_list)
	z = sum(z_list) / len(z_list)
	#convert local to global...
	com_global = (mat3d(mrot)*vec3d(x,y,z)) + vec3d(mpos)
	return com_global
	
#delete pivot locator funciton...
def Delete(requester,widget,action):
	pg = tde4.getCurrentPGroup()
	cam = tde4.getCurrentCamera()
	frame = tde4.getCurrentFrame(cam)
	if widget == "delete":
		model_list = tde4.get3DModelList(pg,0)
		for item in model_list:
			name = tde4.get3DModelName(pg,item)
			if name.startswith("Pivot_Locator") == True:
				tde4.delete3DModel(pg,item)
				
#clear funciton...
def Clear(requester,widget,action):	
	if widget == "parent_clear":
		tde4.setWidgetValue(req,"parent"," ")
	if widget == "child_clear":
		tde4.setWidgetValue(req,"child"," ")	

#snap 3DModel to vertex function...		
def Snap_Vertex(req,widget,action):
	pg = tde4.getCurrentPGroup()
	cam = tde4.getCurrentCamera()
	frame = tde4.getCurrentFrame(cam)
	mlist = tde4.get3DModelList(pg,0)
	p_v = tde4.getWidgetValue(req,"parent")
	c_v = tde4.getWidgetValue(req,"child")
	l = []
	for model in mlist:
		name = tde4.get3DModelName(pg,model)
		if name == p_v:
			l.append(model)
	for model in mlist:
		name = tde4.get3DModelName(pg,model)
		if name == c_v:
			child_model = model
			l.append(model)
	if len(l) == 2:
		parent = l[0]
		child = l[1]
		#turn off child model survey data...
		tde4.set3DModelSurveyFlag(pg,child,0)
		parent_pos = vec3d(tde4.get3DModelPosition3D(pg,parent,cam,frame))
		parent_mrot = mat3d(tde4.get3DModelRotationScale3D(pg,parent))
		child_pos = vec3d(tde4.get3DModelPosition3D(pg,child,cam,frame)) 
		parent_v_list = tde4.get3DModelNoVertices(pg,parent)
		#create a list with vector lengths...
		length_list = []
		tde4.postProgressRequesterAndContinue(window_title, "Calculating nearest vertex...Step 1/2", parent_v_list,"Ok")
		for v in range(0,parent_v_list):
			v_pos = vec3d(tde4.get3DModelVertex(pg,parent,v,cam,frame))
			#convert vertex position from local to global...
			v_pos = (mat3d(parent_mrot) * vec3d(v_pos)) + vec3d(parent_pos)
			vector = vec3d(child_pos) - vec3d(v_pos)
			length = vector.norm2()
			length_list.append(length)
			if v%1000 == 0:
				tde4.updateProgressRequester(v,"Calculating nearest vertex...Step 1/2")
		tde4.unpostProgressRequester()
		#lower length...
		lower_value = min(length_list)
		tde4.postProgressRequesterAndContinue(window_title, "Calculating nearest vertex...Step 2/2", parent_v_list,"Ok")
		for v in range(0,parent_v_list):
			v_pos = vec3d(tde4.get3DModelVertex(pg,parent,v,cam,frame))
			#convert vertex position from local to global...
			v_pos = (mat3d(parent_mrot) * vec3d(v_pos)) + vec3d(parent_pos)
			vector = vec3d(child_pos) - vec3d(v_pos)
			length = vector.norm2()
			if v%1000 == 0:
				tde4.updateProgressRequester(v,"Calculating nearest vertex...Step 2/2")
			if length == lower_value:
				v_pos = tde4.get3DModelVertex(pg,parent,v,cam,frame)
				#convert vertex position from local to global...
				v_pos = (mat3d(parent_mrot) * vec3d(v_pos)) + vec3d(parent_pos)
				tde4.set3DModelPosition3D(pg,child,v_pos.list())
		tde4.unpostProgressRequester()					
	else:
		tde4.postQuestionRequester(window_title,"Error, please select Parent & Child 3DModels","Ok")

#parent constraint function..		
def Parent_Constraint(req,widget,action):
	pg = tde4.getCurrentPGroup()
	cam = tde4.getCurrentCamera()
	frame = tde4.getCurrentFrame(cam)
	mlist = tde4.get3DModelList(pg,0)
	p_v = tde4.getWidgetValue(req,"parent")
	c_v = tde4.getWidgetValue(req,"child")
	l = []
	if c_v and p_v != " ":	
		for model in mlist:
			name = tde4.get3DModelName(pg,model)
			if name == p_v:
				l.append(model)
		for model in mlist:
			name = tde4.get3DModelName(pg,model)
			if name == c_v:
				child_model = model
				l.append(model)

		parent = l[0]
		child = l[1]
		#turn off child model survey data...
		tde4.set3DModelSurveyFlag(pg,child,0)
		#get both models pos & rot values...
		parent_pos = vec3d(tde4.get3DModelPosition3D(pg,parent,cam,frame))
		parent_mrot = mat3d(tde4.get3DModelRotationScale3D(pg,parent))
		child_pos = vec3d(tde4.get3DModelPosition3D(pg,child,cam,frame))					
		child_mrot = mat3d(tde4.get3DModelRotationScale3D(pg,child))
		#set parent model pos & rot values to child model...
		tde4.set3DModelPosition3D(pg,child,parent_pos.list())
		tde4.set3DModelRotationScale3D(pg,child,parent_mrot.list())
	else:
		tde4.postQuestionRequester(window_title,"Error, please select Parent & Child 3DModels","Ok")	
#main...		
def Move_Pivot(requester,widget,action):
	pg = tde4.getCurrentPGroup()
	cam = tde4.getCurrentCamera()
	frame = tde4.getCurrentFrame(cam)
	pl = tde4.getPointList(pg,1)
	mlist = tde4.get3DModelList(pg,1)
	if len(mlist) == 1:
		model = mlist[0]
		tde4.set3DModelSurveyFlag(pg,model,0)
#origin...
		if widget == "origin":
			p3d = vec3d(0,0,0)
			vlist = tde4.get3DModelNoVertices(pg,model)
			tde4.postProgressRequesterAndContinue(window_title, "Calculating...", vlist,"Ok")			
			v = Vector(pg,model,cam,frame,p3d,vlist)
			for i in range(0,vlist):
				tde4.set3DModelVertex(pg,model,i,v[i])
				if i % 1000 == 0:
					tde4.updateProgressRequester(i,"Calculating...")				
			tde4.set3DModelPosition3D(pg,model,p3d.list())
			tde4.unpostProgressRequester()			
#point...
		if widget == "point":
			if len(pl) == 1 and len(mlist) == 1:
				p3d = tde4.getPointCalcPosition3D(pg,pl[0])	
				vlist = tde4.get3DModelNoVertices(pg,model)
				tde4.postProgressRequesterAndContinue(window_title, "Calculating...", vlist,"Ok")				
				v = Vector(pg,model,cam,frame,p3d,vlist)
				for i in range(0,vlist):
					tde4.set3DModelVertex(pg,model,i,v[i])
					if i % 1000 == 0:
						tde4.updateProgressRequester(i,"Calculating...")						
				tde4.set3DModelPosition3D(pg,model,p3d)
				tde4.unpostProgressRequester()								
			else:
				tde4.postQuestionRequester(window_title,"Error, exactly one 3DModel and one Point must be selected","Ok")		
#locator...
		if widget == "locator":
			vlist = tde4.get3DModelNoVertices(pg,model)
			cp = Center_Pivot(pg,model,cam,frame,vlist)
			model_list = tde4.get3DModelList(pg,0)
			l = []
			for item in model_list:
				name = tde4.get3DModelName(pg,item)
				if name.startswith("Pivot_Locator") == True:
					l.append(item)
					break
			if len(l) > 0:
				p3d = vec3d(tde4.get3DModelPosition3D(pg,l[0],cam,frame))
				vlist = tde4.get3DModelNoVertices(pg,model)
				tde4.postProgressRequesterAndContinue(window_title, "Calculating...", vlist,"Ok")				
				v = Vector(pg,model,cam,frame,p3d,vlist)
				for i in range(0,vlist):
					tde4.set3DModelVertex(pg,model,i,v[i])
					if i % 1000 == 0:
						tde4.updateProgressRequester(i,"Calculating...")					
				tde4.set3DModelPosition3D(pg,model,p3d.list())
				tde4.unpostProgressRequester()				
			else:
				tde4.postQuestionRequester(window_title,"Error, first please create 'Pivot Locator'.","Ok")					
#center...
		if widget == "center":
			vlist = tde4.get3DModelNoVertices(pg,model)
			tde4.postProgressRequesterAndContinue(window_title, "Calculating...", vlist,"Ok")			
			p3d = Center_Pivot(pg,model,cam,frame,vlist)	
			v = Vector(pg,model,cam,frame,p3d,vlist)			
			for i in range(0,vlist):
				tde4.set3DModelVertex(pg,model,i,v[i])
				if i % 1000 == 0:
					tde4.updateProgressRequester(i,"Calculating...")				
			tde4.set3DModelPosition3D(pg,model,p3d.list())	
			tde4.unpostProgressRequester()							
#camera...
		if widget == "camera":
			if tde4.getPGroupType(pg) == "CAMERA":
				p3d = tde4.getPGroupPosition3D(pg,cam,frame)
				vlist = tde4.get3DModelNoVertices(pg,model)
				tde4.postProgressRequesterAndContinue(window_title, "Calculating...", vlist,"Ok")				
				v = Vector(pg,model,cam,frame,p3d,vlist)
				for i in range(0,vlist):
					tde4.set3DModelVertex(pg,model,i,v[i])
					if i % 1000 == 0:
						tde4.updateProgressRequester(i,"Calculating...")						
				tde4.set3DModelPosition3D(pg,model,p3d)	
				tde4.unpostProgressRequester()								
			else:
				tde4.postQuestionRequester(window_title,"Error, 3DModel should be under camera PGroup.","Ok")	
#pivot locator...
		if widget == "pivot_loc":
			model_list = tde4.get3DModelList(pg,0)
			for item in model_list:
				name = tde4.get3DModelName(pg,item)
				if name.startswith("Pivot_Locator") == True:
					tde4.delete3DModel(pg,item)	
			m = tde4.create3DModel(pg, 7)
			tde4.set3DModelName(pg, m, "Pivot_Locator")
			tde4.add3DModelVertex(pg, m, [0.0, 0.0, 0.0])
			tde4.add3DModelVertex(pg, m, [10.0, 0.0, 0.0])
			tde4.add3DModelVertex(pg, m, [-10.0, 0.0, 0.0])
			tde4.add3DModelVertex(pg, m, [0.0, 10.0, 0.0])
			tde4.add3DModelVertex(pg, m, [0.0, -10.0, 0.0])
			tde4.add3DModelVertex(pg, m, [0.0, 0.0, 10.0])
			tde4.add3DModelVertex(pg, m, [0.0, 0.0, -10.0])
			tde4.postProgressRequesterAndContinue(window_title, "Calculating...", 7,"Ok")			
			for i in range(7):
				tde4.add3DModelLine(pg, m, [0, i])
				if i % 1000 == 0:
					tde4.updateProgressRequester(i,"Calculating...")					
			tde4.set3DModelColor(pg,m,1.0,0.0,0.0,1.0)
			tde4.set3DModelSurveyFlag(pg, m, 0)
			vlist = tde4.get3DModelNoVertices(pg,model)
			cp = Center_Pivot(pg,model,cam,frame,vlist)			
			tde4.set3DModelPosition3D(pg, m, [cp[0],cp[1],cp[2]])
			tde4.unpostProgressRequester()				
#freeze transformations...
		if widget == "freeze":
			mpos = tde4.get3DModelPosition3D(pg,model,cam,frame)
			mrot = tde4.get3DModelRotationScale3D(pg,model)		
			m = 	mat3d(tde4.get3DModelRotationScale3D(pg,model)).trans()	
			s  =  vec3d(m[0].norm2(),m[1].norm2(),m[2].norm2())
			r  = mat3d(m[0].unit(),m[1].unit(),m[2].unit()).trans()
			p3d = vec3d(0,0,0)
			vlist = tde4.get3DModelNoVertices(pg,model)
			tde4.postProgressRequesterAndContinue(window_title, "Calculating...",vlist,"Ok")				
			vector = mat3d(mrot).invert() * (vec3d(p3d) - vec3d(mpos))
			for i in range(0,vlist):
				v = tde4.get3DModelVertex(pg,model,i,cam,frame)
				v[0] = v[0] - vector[0]
				v[1] = v[1] - vector[1]
				v[2] = v[2] - vector[2]	
				v = mat3d(mrot) * vec3d(v)
				tde4.set3DModelVertex(pg,model,i,v.list())
				if i % 1000 == 0:
					tde4.updateProgressRequester(i,"Calculating...")					
			tde4.set3DModelPosition3D(pg,model,[0,0,0])	
			scale_matrix = mat3d(1.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,1.0)
			rot_matrix = mat3d(1.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,1.0)
			f = rot_matrix * scale_matrix
			tde4.set3DModelRotationScale3D(pg,model,f.list())
			tde4.set3DModelSurveyFlag(pg,model,1)
			tde4.unpostProgressRequester()				
#reload 3DModels...
		if widget == "reload":
			mlist = tde4.get3DModelList(pg,1)
			if len(mlist) == 1:
				parent = mlist[0]
				path = tde4.get3DModelFilepath(pg,parent)
				tde4.set3DModelSurveyFlag(pg,parent,0)
				parent_pos = tde4.get3DModelPosition3D(pg,parent,cam,frame)
				parent_rot = tde4.get3DModelRotationScale3D(pg,parent)
				parent_name = tde4.get3DModelName(pg,parent)
				parent_list = []
				n = tde4.get3DModelNoVertices(pg,parent)
				mrot = tde4.get3DModelRotationScale3D(pg,parent)
				mpos= tde4.get3DModelPosition3D(pg,parent,cam,frame)
				tde4.postProgressRequesterAndContinue(window_title, "Calculating...Step1/2",n,"Ok")
				for i in range(0,n):
					v = tde4.get3DModelVertex(pg,parent,i,cam,frame)
					vector = mat3d(mrot).invert()*(vec3d(0,0,0)-vec3d(mpos))
					v[0] = v[0]-vector[0]
					v[1] = v[1]-vector[1]
					v[2] = v[2]-vector[2]
					v = mat3d(mrot)*vec3d(v)
					parent_list.append(v)
					if i % 1000 == 0:
						tde4.updateProgressRequester(i,"Calculating...Step1/2")
				tde4.unpostProgressRequester()
				#create dummy model and overwrite parent 3DModel data...
				model = tde4.create3DModel(pg, 2)
				tde4.set3DModelName(pg, model, "patcha_temp")
				tde4.add3DModelVertex(pg, model, [0.0, 0.0, 0.0])
				tde4.add3DModelVertex(pg, model, [0.0, 5.0, 0.0])
				tde4.add3DModelLine(pg, model, [0, 1])
				mlist = tde4.get3DModelList(pg,0)
				for m in mlist:
					name = tde4.get3DModelName(pg,m)
					if name == "patcha_temp":
						child = m
				tde4.importOBJ3DModel(pg,child,path)
				#set child 3DModels's vertices positions to parent 3DModels's vertices
				n = tde4.get3DModelNoVertices(pg,child)
				if len(parent_list) == n:
					for i in range(0,n):
						tde4.set3DModelVertex(pg,child,i,parent_list[i].list())
					#change child 3DModel's pivot to parent 3DModel's pivot...
					p3d = parent_pos
					vlist = tde4.get3DModelNoVertices(pg,child)
					tde4.postProgressRequesterAndContinue(window_title, "Calculating...2/2", vlist,"Ok")				
					v = Vector(pg,child,cam,frame,p3d,vlist)
					for i in range(0,vlist):
						tde4.set3DModelVertex(pg,child,i,v[i])
						if i % 1000 == 0:
							tde4.updateProgressRequester(i,"Calculating...2/2")						
					tde4.set3DModelPosition3D(pg,child,p3d)
					tde4.unpostProgressRequester()
					#delete parent 3DModel and renmae child 3DModel...
					tde4.delete3DModel(pg,parent)
					tde4.set3DModelName(pg,child,str(parent_name))
				else:
					tde4.delete3DModel(pg,child)
					tde4.postQuestionRequester(window_title,"Error, imported 3DModel must be identical to selected 3DModel.","Ok")
	else:
		tde4.postQuestionRequester(window_title,"Error, Exactly one 3DModel must be selected or 3DModels should be under current PGroup","Ok")	

def Model_Pivot_Help(req,widget,action):
	model_pivot_help_req = tde4.createCustomRequester()
	tde4.addTextAreaWidget(model_pivot_help_req,"textarea","",0,0)
	tde4.setWidgetAttachModes(model_pivot_help_req,"textarea","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_WINDOW")
	tde4.setWidgetOffsets(model_pivot_help_req,"textarea",2,2,2,2)	
	tde4.addTextAreaWidget(model_pivot_help_req,"textarea","",0,0)
	tde4.setWidgetAttachModes(model_pivot_help_req,"textarea","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_WINDOW")
	tde4.setWidgetOffsets(model_pivot_help_req,"textarea",2,2,2,2)
	tde4.appendTextAreaWidgetString(model_pivot_help_req,"textarea","Add Help text here.\n\n")








	tde4.postCustomRequesterAndContinue(model_pivot_help_req,"Help",800,520)



				
#GUI...
#try:
#req	= _pivot_requester
#except (ValueError,NameError,TypeError):
req	= tde4.createCustomRequester()
#_pivot_requester	= req
#add model name text field widget...
tde4.addTextFieldWidget(req,"name","Selected Model & Point"," ")
tde4.setWidgetAttachModes(req,"name","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"name",27,98,10,0)	
#set widget sensitive flag...
tde4.setWidgetSensitiveFlag(req,"name",0)
#move pivot to origin...
tde4.addButtonWidget(req,"origin","Move pivot to Origin",70,10)
tde4.setWidgetAttachModes(req,"origin","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"origin",4,32,40,0)		
#move pivot to point...
tde4.addButtonWidget(req,"point","Move pivot to Point",70,10)
tde4.setWidgetAttachModes(req,"point","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"point",35,65,40,0)		
#move pivot to locator...
tde4.addButtonWidget(req,"locator","Move pivot to Locator",70,10)
tde4.setWidgetAttachModes(req,"locator","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"locator",68,96,40,0)	
#move pivot to center...
tde4.addButtonWidget(req,"center","Move pivot to Center",70,10)
tde4.setWidgetAttachModes(req,"center","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"center",4,32,70,0)	
#move pivot to camera...
tde4.addButtonWidget(req,"camera","Move pivot to Camera",70,10)
tde4.setWidgetAttachModes(req,"camera","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"camera",35,65,70,0)	
#freeze transformations...
tde4.addButtonWidget(req,"freeze","Freeze Transformations",70,10)
tde4.setWidgetAttachModes(req,"freeze","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"freeze",68,96,70,0)
#pivot locator widget...
tde4.addButtonWidget(req,"pivot_loc","Create Pivot Locator",70,10)
tde4.setWidgetAttachModes(req,"pivot_loc","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"pivot_loc",4,32,100,0)
#reload widget...
tde4.addButtonWidget(req,"reload","Reload Model",70,10)
tde4.setWidgetAttachModes(req,"reload","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"reload",35,65,100,0)
#delete pivot locator button widget...
tde4.addButtonWidget(req,"delete","Delete Pivot Locator",70,10)
tde4.setWidgetAttachModes(req,"delete","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"delete",68,96,100,0)	
#sep2 widget...
tde4.addSeparatorWidget(req,"sep1")
tde4.setWidgetAttachModes(req,"sep1","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"sep1",2,98,120,0)
#parent model name widget...
tde4.addTextFieldWidget(req,"parent","Parent Model"," ")
tde4.setWidgetAttachModes(req,"parent","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"parent",20,75,140,0)
tde4.setWidgetSensitiveFlag(req,"parent",0)
#parent model get widget...
tde4.addButtonWidget(req,"parent_get","Get",70,10)
tde4.setWidgetAttachModes(req,"parent_get","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"parent_get",77,87,140,0)
#parent model clear widget...
tde4.addButtonWidget(req,"parent_clear","Clear",70,10)
tde4.setWidgetAttachModes(req,"parent_clear","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"parent_clear",89,98,140,0)
#child model name widget...
tde4.addTextFieldWidget(req,"child","Child Model"," ")
tde4.setWidgetAttachModes(req,"child","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"child",20,75,170,0)
tde4.setWidgetSensitiveFlag(req,"child",0)
#child model get widget...
tde4.addButtonWidget(req,"child_get","Get",70,10)
tde4.setWidgetAttachModes(req,"child_get","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"child_get",77,87,170,0)
#child model clear widget...
tde4.addButtonWidget(req,"child_clear","Clear",70,10)
tde4.setWidgetAttachModes(req,"child_clear","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"child_clear",89,98,170,0)
#match pivots button widget...
tde4.addButtonWidget(req,"match_pivots","Match 3DModels Transform, maintain pivots",70,10)
tde4.setWidgetAttachModes(req,"match_pivots","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"match_pivots",15,85,200,0)
#parent constraint button widget...
tde4.addButtonWidget(req,"parent_constraint","Snap child 3DModel to parent 3DModel",70,10)
tde4.setWidgetAttachModes(req,"parent_constraint","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"parent_constraint",15,85,230,0)	
#Snap 3DModel to vertex button widget...
tde4.addButtonWidget(req,"snap_vertex","Snap child 3DModel to parent 3DModel's nearest vertex",70,10)
tde4.setWidgetAttachModes(req,"snap_vertex","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"snap_vertex",15,85,260,0)
#add help widget...
tde4.addButtonWidget(req,"model_pivot_help","Help",70,10)
tde4.setWidgetAttachModes(req,"model_pivot_help","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_WINDOW")
tde4.setWidgetOffsets(req,"model_pivot_help",87,97,215,25)
#widget callbacks...
tde4.setWidgetCallbackFunction(req,"origin","Move_Pivot")	
tde4.setWidgetCallbackFunction(req,"point","Move_Pivot")	
tde4.setWidgetCallbackFunction(req,"locator","Move_Pivot")
tde4.setWidgetCallbackFunction(req,"center","Move_Pivot")	
tde4.setWidgetCallbackFunction(req,"camera","Move_Pivot")	
tde4.setWidgetCallbackFunction(req,"freeze","Move_Pivot")	
tde4.setWidgetCallbackFunction(req,"pivot_loc","Move_Pivot")
tde4.setWidgetCallbackFunction(req,"reload","Move_Pivot")
tde4.setWidgetCallbackFunction(req,"delete","Delete")
tde4.setWidgetCallbackFunction(req,"parent_get","Names")
tde4.setWidgetCallbackFunction(req,"child_get","Names")	
tde4.setWidgetCallbackFunction(req,"parent_clear","Clear")
tde4.setWidgetCallbackFunction(req,"child_clear","Clear")	
tde4.setWidgetCallbackFunction(req,"match_pivots","Match_Pivot")
tde4.setWidgetCallbackFunction(req,"snap_vertex","Snap_Vertex")	
tde4.setWidgetCallbackFunction(req,"parent_constraint","Parent_Constraint")	
tde4.setWidgetCallbackFunction(req,"model_pivot_help","Model_Pivot_Help")
tde4.postCustomRequesterAndContinue(req,window_title,590,290,"update")

