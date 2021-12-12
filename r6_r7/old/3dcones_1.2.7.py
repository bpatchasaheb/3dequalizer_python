# 3DE4.script.name: 3D Cones...
# 3DE4.script.version: v1.2.7
# 3DE4.script.gui.config_menus: true
# 3DE4.script.gui.button: Lineup Controls::3D Cones, align-bottom-left, 80, 20
# 3DE4.script.gui.button: Orientation Controls::3D Cones, align-bottom-left, 70, 20
# 3DE4.script.comment: Create 3D cones on selected 3D points.

# updated for python3/R7
# July 19 2021, Montreal
# Patcha Saheb(patchasaheb@gmail.com)


from vl_sdv import *
import os,sys
import math

WINDOW_TITLE = "Patcha 3D Cones v1.2.7"
CONE_NAME_PREFIX = "3D_Cone_"

def create_box_cone():
	pg = tde4.getCurrentPGroup()
	model = tde4.create3DModel(pg, 5)
	i0 = tde4.add3DModelVertex(pg, model, [0.0, 0.0, 0.0])
	i1 = tde4.add3DModelVertex(pg, model, [-0.361,1.798, -0.358])
	i2 = tde4.add3DModelVertex(pg, model, [-0.361,1.798, 0.358])
	i3 = tde4.add3DModelVertex(pg, model, [0.361, 1.798, -0.358])
	i4 = tde4.add3DModelVertex(pg, model, [0.361, 1.798, 0.358])
	tde4.add3DModelLine(pg, model, [i0,i1])
	tde4.add3DModelLine(pg, model, [i0,i2])
	tde4.add3DModelLine(pg, model, [i0,i3])
	tde4.add3DModelLine(pg, model, [i0,i4])
	tde4.add3DModelLine(pg, model, [i1,i2])
	tde4.add3DModelLine(pg, model, [i1,i3])
	tde4.add3DModelLine(pg, model, [i2,i4])
	tde4.add3DModelLine(pg, model, [i3,i4])
	tde4.add3DModelFace(pg, model, [i0,i3,i4,i0])
	tde4.add3DModelFace(pg, model, [i0,i1,i3,i0])
	tde4.add3DModelFace(pg, model, [i0,i2,i1,i0])
	tde4.add3DModelFace(pg, model, [i0,i4,i2,i0])
	tde4.add3DModelFace(pg, model, [i1,i2,i4,i3,i1])
	tde4.set3DModelSurveyFlag(pg, model, 0)
	tde4.set3DModelColor(pg, model, 1.0,0.0,0.0,1.0)
	return model

def create_round_cone():
	pg = tde4.getCurrentPGroup()
	model = tde4.create3DModel(pg, 17)
	i0 = tde4.add3DModelVertex(pg, model, [0.0, 1.803521, 0.5])
	i1 = tde4.add3DModelVertex(pg, model, [0.0, 0.0, 0.0])
	i2 = tde4.add3DModelVertex(pg, model, [0.191342, 1.803521, 0.46194])
	i3 = tde4.add3DModelVertex(pg, model, [0.353553, 1.803521, 0.353553])
	i4 = tde4.add3DModelVertex(pg, model, [0.46194, 1.803521, 0.191342])
	i5 = tde4.add3DModelVertex(pg, model, [0.5, 1.803521, 0.0])
	i6 = tde4.add3DModelVertex(pg, model, [0.46194, 1.803521, -0.191342])
	i7 = tde4.add3DModelVertex(pg, model, [0.353553, 1.803521, -0.353553])
	i8 = tde4.add3DModelVertex(pg, model, [0.191342, 1.803521, -0.46194])
	i9 = tde4.add3DModelVertex(pg, model, [0.0, 1.803521, -0.5])
	i10 = tde4.add3DModelVertex(pg, model, [-0.191342, 1.803521, -0.46194])
	i11 = tde4.add3DModelVertex(pg, model, [-0.353553, 1.803521, -0.353553])
	i12 = tde4.add3DModelVertex(pg, model, [-0.46194, 1.803521, -0.191342])
	i13 = tde4.add3DModelVertex(pg, model, [-0.5, 1.803521, 0.0])
	i14 = tde4.add3DModelVertex(pg, model, [-0.46194, 1.803521, 0.191342])
	i15 = tde4.add3DModelVertex(pg, model, [-0.353553, 1.803521, 0.353553])
	i16 = tde4.add3DModelVertex(pg, model, [-0.191342, 1.803521, 0.46194])
	tde4.add3DModelLine(pg, model, [i0, i1, i2])
	tde4.add3DModelLine(pg, model, [i3, i1, i4])
	tde4.add3DModelLine(pg, model, [i5, i1, i6])
	tde4.add3DModelLine(pg, model, [i7, i1, i8])
	tde4.add3DModelLine(pg, model, [i9, i1, i10])
	tde4.add3DModelLine(pg, model, [i11, i1, i12])
	tde4.add3DModelLine(pg, model, [i13, i1, i14])
	tde4.add3DModelLine(pg, model, [i15, i1, i16])
	tde4.add3DModelLine(pg, model, [i0, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12, i13, i14, i15, i16, i0])
	tde4.add3DModelFace(pg, model, [i0, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12, i13, i14, i15, i16])
	tde4.add3DModelFace(pg, model, [i0, i1, i2])
	tde4.add3DModelFace(pg, model, [i2, i1, i3])
	tde4.add3DModelFace(pg, model, [i3, i1, i4])
	tde4.add3DModelFace(pg, model, [i4, i1, i5])
	tde4.add3DModelFace(pg, model, [i5, i1, i6])
	tde4.add3DModelFace(pg, model, [i6, i1, i7])
	tde4.add3DModelFace(pg, model, [i7, i1, i8])
	tde4.add3DModelFace(pg, model, [i8, i1, i9])
	tde4.add3DModelFace(pg, model, [i9, i1, i10])
	tde4.add3DModelFace(pg, model, [i10, i1, i11])
	tde4.add3DModelFace(pg, model, [i11, i1, i12])
	tde4.add3DModelFace(pg, model, [i12, i1, i13])
	tde4.add3DModelFace(pg, model, [i13, i1, i14])
	tde4.add3DModelFace(pg, model, [i14, i1, i15])
	tde4.add3DModelFace(pg, model, [i15, i1, i16])
	tde4.add3DModelFace(pg, model, [i16, i1, i0])
	tde4.set3DModelSurveyFlag(pg, model, 0)
	tde4.set3DModelColor(pg, model, 1.0,0.0,0.0,1.0)
	return model		

def create_cube():
	pg = tde4.getCurrentPGroup()
	model = tde4.create3DModel(pg, 8)
	i0 = tde4.add3DModelVertex(pg, model, [0.5, 1.0, 0.5])
	i1 = tde4.add3DModelVertex(pg, model, [-0.5, 1.0, 0.5])
	i2 = tde4.add3DModelVertex(pg, model, [-0.5, 1.0, -0.5])
	i3 = tde4.add3DModelVertex(pg, model, [0.5, 1.0, -0.5])
	i4 = tde4.add3DModelVertex(pg, model, [0.5, 0.0, 0.5])
	i5 = tde4.add3DModelVertex(pg, model, [-0.5, 0.0, 0.5])
	i6 = tde4.add3DModelVertex(pg, model, [-0.5, 0.0, -0.5])
	i7 = tde4.add3DModelVertex(pg, model, [0.5, 0.0, -0.5])
	tde4.add3DModelLine(pg, model, [i0, i1, i2, i3, i0, i4, i5, i1])
	tde4.add3DModelLine(pg, model, [2, 6, 5])
	tde4.add3DModelLine(pg, model, [3, 7, 4])
	tde4.add3DModelLine(pg, model, [6, 7])
	tde4.add3DModelFace(pg, model, [3, 2, 1, 0])
	tde4.add3DModelFace(pg, model, [4, 5, 6, 7])
	tde4.add3DModelFace(pg, model, [0, 4, 7, 3])
	tde4.add3DModelFace(pg, model, [2, 6, 5, 1])
	tde4.add3DModelFace(pg, model, [1, 5, 4, 0])
	tde4.add3DModelFace(pg, model, [3, 7, 6, 2])
	tde4.set3DModelSurveyFlag(pg, model, 0)
	tde4.set3DModelColor(pg, model, 1.0,0.0,0.0,1.0)
	return model

def create_locator():
	pg = tde4.getCurrentPGroup()
	model = tde4.create3DModel(pg, 8)
	tde4.add3DModelVertex(pg, model, [0.0, 0.0, 0.0])
	tde4.add3DModelVertex(pg, model, [1.0, 0.0, 0.0])
	tde4.add3DModelVertex(pg, model, [-1.0, 0.0, 0.0])
	tde4.add3DModelVertex(pg, model, [0.0, 1.0, 0.0])
	tde4.add3DModelVertex(pg, model, [0.0, -1.0, 0.0])
	tde4.add3DModelVertex(pg, model, [0.0, 0.0, 1.0])
	tde4.add3DModelVertex(pg, model, [0.0, 0.0, -1.0])
	for i in range(7):
		tde4.add3DModelLine(pg, model, [0, i])
	tde4.set3DModelSurveyFlag(pg, model, 0)
	tde4.set3DModelColor(pg, model, 1.0,0.0,0.0,1.0)
	return model

def get_all_model_list(filter_selected=False):
	models = []
	pg = tde4.getCurrentPGroup()
	model_list = tde4.get3DModelList(pg, 0)
	if filter_selected == True:
		model_list = tde4.get3DModelList(pg, 1)	
	if len(model_list) == 0:
		return
	for model in model_list:
		name = tde4.get3DModelName(pg, model)
		if CONE_NAME_PREFIX in name:
			models.append(model)
	return models

def create_models_clicked(req, widget, action):
	pg = tde4.getCurrentPGroup()
	cam = tde4.getCurrentCamera()
	frame = tde4.getCurrentFrame(cam)
	point_list = tde4.getPointList(pg, 1) or []
	if len(point_list) == 0:
		tde4.postQuestionRequester(WINDOW_TITLE, "Error, please select point(s) to create models.", "ok")
		return
	delete_models()
	for point in point_list:
		point_name = tde4.getPointName(pg, point)
		if tde4.isPointCalculated3D(pg, point):
			point_pos = tde4.getPointCalcPosition3D(pg, point)
			model = create_box_cone()
			tde4.set3DModelName(pg, model, CONE_NAME_PREFIX+str(point_name))
			tde4.set3DModelPosition3D(pg, model, point_pos)
			tde4.set3DModelSnappingPoint(pg, model, point)

def select_all_clicked(req, widget, action):
	pg = tde4.getCurrentPGroup()
	model_list = get_all_model_list() or []
	for model in model_list:
		tde4.set3DModelSelectionFlag(pg, model, 1)

def delete_models():
	pg = tde4.getCurrentPGroup()
	model_list = get_all_model_list() or []
	if model_list:
		for model in model_list:
			tde4.delete3DModel(pg, model)

def delete_extra_models_clicked(req, widget, action):
	pg = tde4.getCurrentPGroup()
	model_list = get_all_model_list() or []
	count = 0
	for model in model_list:
		snap_point = tde4.get3DModelSnappingPoint(pg, model)
		if not snap_point:
			tde4.delete3DModel(pg, model)
			count = count + 1
	if count > 0:
		tde4.postQuestionRequester(WINDOW_TITLE, "Number of 3DCone model(s) deleted: "+str(count), "ok")

def delete_all_models_clicked(req, widget, action):
	delete_models()

def prop_scale_rdo_toggle():
	prop_scale_enable = tde4.getWidgetValue(req, "prop_scale_rdo_box")
	scale_value = float(tde4.getWidgetValue(req, "scale_text_value"))
	if prop_scale_enable == 1:
		tde4.setWidgetSensitiveFlag(req, "scale_slider", 0)
		tde4.setWidgetSensitiveFlag(req, "scale_text_value", 0)
		tde4.setWidgetSensitiveFlag(req, "prop_scale_x_txt", 1)
		tde4.setWidgetSensitiveFlag(req, "prop_scale_y_txt", 1)
		tde4.setWidgetSensitiveFlag(req, "prop_scale_z_txt", 1)
		tde4.setWidgetSensitiveFlag(req, "scale_positive_btn", 1)
		tde4.setWidgetSensitiveFlag(req, "scale_negative_btn", 1)
		tde4.setWidgetSensitiveFlag(req, "scale_x_txt_value", 0)
		tde4.setWidgetSensitiveFlag(req, "scale_y_txt_value", 0)
		tde4.setWidgetSensitiveFlag(req, "scale_z_txt_value", 0)
	elif prop_scale_enable == 0:
		tde4.setWidgetSensitiveFlag(req, "scale_slider", 1)
		tde4.setWidgetSensitiveFlag(req, "scale_text_value", 1)
		tde4.setWidgetSensitiveFlag(req, "prop_scale_x_txt", 0)
		tde4.setWidgetSensitiveFlag(req, "prop_scale_y_txt", 0)
		tde4.setWidgetSensitiveFlag(req, "prop_scale_z_txt", 0)
		tde4.setWidgetSensitiveFlag(req, "scale_positive_btn", 0)
		tde4.setWidgetSensitiveFlag(req, "scale_negative_btn", 0)
		tde4.setWidgetSensitiveFlag(req, "scale_x_txt_value", 1)
		tde4.setWidgetSensitiveFlag(req, "scale_y_txt_value", 1)
		tde4.setWidgetSensitiveFlag(req, "scale_z_txt_value", 1)		
		if scale_value > 10.0:
			tde4.setWidgetSensitiveFlag(req, "scale_slider", 0)

def get_model_rotation_scale(model):
	pg = tde4.getCurrentPGroup()
	matrices = []
	rot_scale_matrix = mat3d(tde4.get3DModelRotationScale3D(pg, model)).trans()
	scale_values_from_matrix = vec3d(rot_scale_matrix[0].norm2(), rot_scale_matrix[1].norm2(), rot_scale_matrix[2].norm2())
	scale_matrix = mat3d(scale_values_from_matrix[0],0.0,0.0,0.0,scale_values_from_matrix[1],0.0,0.0,0.0,scale_values_from_matrix[2])
	rotation_matrix = mat3d(rot_scale_matrix[0].unit(), rot_scale_matrix[1].unit(), rot_scale_matrix[2].unit()).trans()
	matrices.append(rotation_matrix)
	matrices.append(scale_matrix)
	return matrices

def set_model_scale(models, x, y, z):
	pg = tde4.getCurrentPGroup()
	cam = tde4.getCurrentCamera()
	frame = tde4.getCurrentFrame(cam)
	if models:
		for model in models:
			scale_matrix = get_model_rotation_scale(model)[1]
			rotation_matrix = get_model_rotation_scale(model)[0]
			scale_matrix = mat3d(float(x),0.0,0.0, 0.0,float(y),0.0, 0.0,0.0,float(z))
			final_matrix = rotation_matrix * scale_matrix
			tde4.set3DModelRotationScale3D(pg, model, final_matrix.list())				

def scale_clicked(req, widget, action):
	pg = tde4.getCurrentPGroup()
	cam = tde4.getCurrentCamera()
	frame = tde4.getCurrentFrame(cam)
	slider_value = tde4.getWidgetValue(req, "scale_slider")
	scale_value = float(tde4.getWidgetValue(req, "scale_text_value"))
	scale_x_value = float(tde4.getWidgetValue(req, "scale_x_txt_value"))
	scale_y_value = float(tde4.getWidgetValue(req, "scale_y_txt_value"))
	scale_z_value = float(tde4.getWidgetValue(req, "scale_z_txt_value"))
	prop_scale_rdo_box_value = tde4.getWidgetValue(req, "prop_scale_rdo_box")
	prop_scale_x = float(tde4.getWidgetValue(req, "prop_scale_x_txt"))
	prop_scale_y = float(tde4.getWidgetValue(req, "prop_scale_y_txt"))
	prop_scale_z = float(tde4.getWidgetValue(req, "prop_scale_z_txt"))

	models = get_all_model_list() or []
	if widget == "scale_slider":
		tde4.setWidgetValue(req, "scale_text_value", str(round(slider_value, 3)))

	if widget == "scale_text_value":
		if scale_value > 10.0:
			tde4.setWidgetSensitiveFlag(req, "scale_slider", 0)
		else:
			tde4.setWidgetSensitiveFlag(req, "scale_slider", 1)
			tde4.setWidgetValue(req, "scale_slider", str(scale_value))

	if widget == "scale_slider" or widget == "scale_text_value" or prop_scale_rdo_box_value == 0:		
		set_model_scale(models, scale_value, scale_value, scale_value)

	if widget == "scale_x_txt_value" or widget == "scale_y_txt_value" or widget == "scale_z_txt_value":
		set_model_scale(models, scale_x_value, scale_y_value, scale_z_value)

	if widget == "prop_scale_rdo_box":
		prop_scale_rdo_toggle()
		if prop_scale_rdo_box_value == 1:
			cam_pos = tde4.getPGroupPosition3D(pg, cam, frame)
			point_list = tde4.getPointList(pg, 0) or []
			for point in point_list:
				if tde4.isPointCalculated3D(pg, point):
					point_pos = tde4.getPointCalcPosition3D(pg, point)
					for model in models:
						model_pos = tde4.get3DModelPosition3D(pg, model, cam, frame)
						if point_pos == model_pos:
							distance = (vec3d(cam_pos) - vec3d(point_pos)).norm2()
							distance = float((1.5/100.0) * distance)
							set_model_scale([model], distance, distance, distance)

	if widget == "scale_positive_btn" or widget == "scale_negative_btn":
		for model in models:
			rot_scale_matrix = mat3d(tde4.get3DModelRotationScale3D(pg, model)).trans()
			scale_values_from_matrix = vec3d(rot_scale_matrix[0].norm2(), rot_scale_matrix[1].norm2(), rot_scale_matrix[2].norm2())			
			scale_value_x = scale_values_from_matrix[0]
			scale_value_y = scale_values_from_matrix[1]
			scale_value_z = scale_values_from_matrix[2]
			dx = (prop_scale_x / 100.0) * scale_value_x
			dy = (prop_scale_y / 100.0) * scale_value_y
			dz = (prop_scale_z / 100.0) * scale_value_z
			if widget == "scale_negative_btn":
				dx = -float(dx)
				dy = -float(dy)
				dz = -float(dz)
			dx = scale_value_x + dx
			dy = scale_value_y + dy
			dz = scale_value_z + dz
			set_model_scale([model], dx, dy, dz)

	if widget == "prop_scale_x_txt" or "prop_scale_y_txt" or "prop_scale_z_txt":
		load_save_gui_settings(req, "save")
	load_save_gui_settings(req, "save")

def rotation_clicked(req, widget, action):
	pg = tde4.getCurrentPGroup()
	rotate_x_value = float(tde4.getWidgetValue(req, "rot_x_txt_value"))
	rotate_y_value = float(tde4.getWidgetValue(req, "rot_y_txt_value"))
	rotate_z_value = float(tde4.getWidgetValue(req, "rot_z_txt_value"))	
	models = get_all_model_list() or []
	for model in models:
		rot_x = float(rotate_x_value) *  math.pi /180.0
		rot_y = float(rotate_y_value) *  math.pi /180.0
		rot_z = float(rotate_z_value) *  math.pi /180.0		
		rotation_matrix = mat3d(rot3d(rot_x, rot_y, rot_z, VL_APPLY_ZXY))
		m = mat3d(tde4.get3DModelRotationScale3D(pg, model))
		s0 = vec3d(m[0][0],m[1][0],m[2][0]).norm2()
		s1 = vec3d(m[0][1],m[1][1],m[2][1]).norm2()
		s2 = vec3d(m[0][2],m[1][2],m[2][2]).norm2()
		scale_matrix = mat3d(s0,0.0,0.0,0.0,s1,0.0,0.0,0.0,s2)				
		final_matrix = rotation_matrix * scale_matrix
		tde4.set3DModelRotationScale3D(pg, model, final_matrix.list())
	load_save_gui_settings(req, "save")

def set_color_slider_value(r, g, b):
	tde4.setWidgetValue(req, "color_red_slider", str(r))
	tde4.setWidgetValue(req, "color_green_slider", str(g))
	tde4.setWidgetValue(req, "color_blue_slider", str(b))

def set_model_visibility(models, show_flag=False):
	pg = tde4.getCurrentPGroup()
	for model in models:
		tde4.set3DModelVisibleFlag(pg, model, show_flag)

def view_menu_clicked(req, widget, action):
	models = get_all_model_list() or []
	if widget == "show_all_models_menu_btn":
		set_model_visibility(models, True)
	if widget == "hide_all_models_menu_btn":
		set_model_visibility(models, False)
	if widget == "show_sel_models_menu_btn":
		models = get_all_model_list(True) or []
		if models:
			set_model_visibility(models, True)
	if widget == "hide_sel_models_menu_btn":
		models = get_all_model_list(True) or []
		if models:
			set_model_visibility(models, False)

def deselect_all_other_models():
	pg = tde4.getCurrentPGroup()
	model_list = tde4.get3DModelList(pg, 0)
	for model in model_list:
		tde4.set3DModelSelectionFlag(pg, model, 0)

def deselect_all_other_points():
	pg = tde4.getCurrentPGroup()
	point_list = tde4.getPointList(pg, 0) or []
	for point in point_list:
		tde4.setPointSelectionFlag(pg, point, 0)

def select_menu_clicked(req, widget, action):
	pg = tde4.getCurrentPGroup()
	cam = tde4.getCurrentCamera()
	frame = tde4.getCurrentFrame(cam)

	if widget == "select_model_on_point_menu_btn":
		point_list = tde4.getPointList(pg, 1) or []
	if widget == "select_points_menu_btn":
		point_list = tde4.getPointList(pg, 0) or []

	model_list = get_all_model_list() or []
	if widget == "select_all_models_menu_btn":
		deselect_all_other_models()		
		for model in model_list:
			tde4.set3DModelSelectionFlag(pg, model, 1)

	if widget == "select_model_on_point_menu_btn" or widget == "select_points_menu_btn":		
		if len(point_list) == 0:
			tde4.postQuestionRequester(WINDOW_TITLE, "Error, please select point(s).", "ok")
			return
		deselect_all_other_models()
		deselect_all_other_points()
		for point in point_list:
			if tde4.isPointCalculated3D(pg, point):
				point_pos = tde4.getPointCalcPosition3D(pg, point)
				for model in model_list:
					model_pos = tde4.get3DModelPosition3D(pg, model, cam, frame)
					if point_pos == model_pos:
						if widget == "select_model_on_point_menu_btn":						
							tde4.set3DModelSelectionFlag(pg, model, 1)
						if widget == "select_points_menu_btn":
							tde4.setPointSelectionFlag(pg, point, 1)

def color_menu_clicked(req, widget, action):
	pg = tde4.getCurrentPGroup()
	model_list = get_all_model_list() or []
	if widget == "red_menu_btn": color = [1.0, 0.0, 0.0]
	if widget == "green_menu_btn": color = [0.0, 1.0, 0.0]
	if widget == "blue_menu_btn": color = [0.0, 0.0, 1.0]
	if widget == "yellow_menu_btn": color = [1.0, 1.0, 0.0]
	if widget == "black_menu_btn": color = [0.0, 0.0, 0.0]
	if widget == "white_menu_btn": color = [1.0, 1.0, 1.0]
	if widget == "gray_menu_btn": color = [0.5, 0.5, 0.5]
	if widget == "purple_menu_btn": color = [1.0, 0.0, 1.0]
	if widget == "cyan_menu_btn": color = [0.22, 0.45, 0.65]
	set_color_slider_value(color[0], color[1], color[2])
	alpha = float(tde4.getWidgetValue(req, "color_alpha_slider")) 
	for model in model_list:
		tde4.set3DModelColor(pg, model, color[0], color[1], color[2], alpha )

def color_slider_clicked(req, widget, action):
	pg = tde4.getCurrentPGroup()
	model_list = get_all_model_list() or []	
	red = tde4.getWidgetValue(req, "color_red_slider")
	green = tde4.getWidgetValue(req, "color_green_slider")
	blue = tde4.getWidgetValue(req, "color_blue_slider")
	alpha = tde4.getWidgetValue(req, "color_alpha_slider")
	for model in model_list:
		tde4.set3DModelColor(pg, model, red, green, blue, alpha)
	load_save_gui_settings(req, "save")

def rendering_menu_clicked(req, widget, action):
	pg = tde4.getCurrentPGroup()
	show_lines_value = tde4.getWidgetValue(req, "show_lines_rdo_box")
	show_polygons_value = tde4.getWidgetValue(req, "show_polygons_rdo_box")
	if widget == "show_lines_rdo_box" or widget == "show_polygons_rdo_box":
		model_list = get_all_model_list() or []
		for model in model_list:
			render_flag = tde4.get3DModelRenderingFlags(pg, model)
			if widget == "show_lines_rdo_box":
				if show_lines_value == 1:
					tde4.set3DModelRenderingFlags(pg, model, render_flag[0], 1, render_flag[2])
				else:
					tde4.set3DModelRenderingFlags(pg, model, render_flag[0], 0, render_flag[2])
			if widget == "show_polygons_rdo_box":
				if show_polygons_value == 1:
					tde4.set3DModelRenderingFlags(pg, model, render_flag[0] , render_flag[1], 1)
				else:
					tde4.set3DModelRenderingFlags(pg, model, render_flag[0], render_flag[1], 0)
		load_save_gui_settings(req, "save")	

def model_shape_menu_clicked(req, widget, action):
	pg = tde4.getCurrentPGroup()
	cam = tde4.getCurrentCamera()
	frame = tde4.getCurrentFrame(cam)
	model_list = get_all_model_list() or []
	for model in model_list:
		name = tde4.get3DModelName(pg, model)
		color = tde4.get3DModelColor(pg, model)
		render_flag = tde4.get3DModelRenderingFlags(pg, model)
		per_vertex_flag = tde4.get3DModelPerVertexColorsFlag(pg, model)
		pos = tde4.get3DModelPosition3D(pg, model, cam, frame)
		rot_scale_matrix = tde4.get3DModelRotationScale3D(pg, model)
		visibility = tde4.get3DModelVisibleFlag(pg, model)
		snap_point = tde4.get3DModelSnappingPoint(pg, model)
		tde4.delete3DModel(pg, model)
		if widget == "box_cone_menu_btn":
			new_model = create_box_cone()
		if widget == "round_cone_menu_btn":
			new_model = create_round_cone()
		if widget == "cube_menu_btn":
			new_model = create_cube()
		if widget == "locator_menu_btn":
			new_model = create_locator()
		tde4.set3DModelName(pg, new_model, name)
		tde4.set3DModelColor(pg, new_model, color[0], color[1], color[2], color[3])
		tde4.set3DModelRenderingFlags(pg, new_model, render_flag[0], render_flag[1], render_flag[2])
		tde4.set3DModelPerVertexColorsFlag(pg, new_model, per_vertex_flag)
		tde4.set3DModelPosition3D(pg, new_model, pos)
		tde4.set3DModelRotationScale3D(pg, new_model, rot_scale_matrix)
		tde4.set3DModelVisibleFlag(pg, new_model, visibility)
		tde4.set3DModelSnappingPoint(pg, new_model, snap_point)

def close_btn_clicked(req, widget, action):
	tde4.unpostCustomRequester(req)

load_save_widgets = [("show_lines_rdo_box",1), ("show_polygons_rdo_box",1), 
                     ("scale_slider",1.0), ("scale_text_value",1.0), ("prop_scale_rdo_box",0),
                     ("prop_scale_x_txt",10), ("prop_scale_y_txt",10), ("prop_scale_z_txt",10),
                     ("color_red_slider",1.0), ("color_green_slider",0.0), ("color_blue_slider",0.0), ("color_alpha_slider",1.0),
                     ("scale_x_txt_value",1.0), ("scale_y_txt_value",1.0), ("scale_z_txt_value",1.0),
                     ("rot_x_txt_value",0.0), ("rot_y_txt_value",0.0), ("rot_z_txt_value",0.0)]

def load_save_gui_settings(req, operation):
	pg	= tde4.getCurrentPGroup()
	cam	= tde4.getCurrentCamera()
	tag	= "PATCHA-3D-CONES-GUI-SETTINGS-%d-%d"%(tde4.getCameraPersistentID(cam),tde4.getPGroupPersistentID(pg))	
	string = ""
	if operation == "save":
		for i in range(len(load_save_widgets)):
			value = tde4.getWidgetValue(req, load_save_widgets[i][0])
			string = string + " " + str(value)
		tde4.addPersistentString(tag, string)

	if operation == "load":
		string	= tde4.getPersistentString(tag)
		if string!=None:
			string = string.split()
			for i in range(len(string)):
				tde4.setWidgetValue(req, load_save_widgets[i][0], string[i])
			prop_scale_rdo_toggle()
	return

def reset_ui_settings_clicked(req, widget, action):
	for i in range(len(load_save_widgets)):
		tde4.setWidgetValue(req, load_save_widgets[i][0], str(load_save_widgets[i][1]))
	prop_scale_rdo_toggle()
	load_save_gui_settings(req, "save")

# GUI
req = tde4.createCustomRequester()
tde4.addMenuBarWidget(req,"menu_bar")
tde4.setWidgetOffsets(req,"menu_bar",0,0,0,0)
tde4.setWidgetAttachModes(req,"menu_bar","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"menu_bar",200,20)
tde4.addMenuWidget(req,"view_menu","View","menu_bar",1)
tde4.setWidgetOffsets(req,"view_menu",0,0,0,0)
tde4.setWidgetAttachModes(req,"view_menu","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"view_menu",80,20)
tde4.addMenuButtonWidget(req,"show_all_models_menu_btn","Show all models","view_menu")
tde4.setWidgetOffsets(req,"show_all_models_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"show_all_models_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"show_all_models_menu_btn",80,20)
tde4.addMenuButtonWidget(req,"hide_all_models_menu_btn","Hide all models","view_menu")
tde4.setWidgetOffsets(req,"hide_all_models_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"hide_all_models_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"hide_all_models_menu_btn",80,20)
tde4.addMenuButtonWidget(req,"show_sel_models_menu_btn","Show selected models","view_menu")
tde4.setWidgetOffsets(req,"show_sel_models_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"show_sel_models_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"show_sel_models_menu_btn",80,20)
tde4.addMenuButtonWidget(req,"hide_sel_models_menu_btn","Hide selected models","view_menu")
tde4.setWidgetOffsets(req,"hide_sel_models_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"hide_sel_models_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"hide_sel_models_menu_btn",80,20)
tde4.addMenuWidget(req,"select_menu","Select","menu_bar",0)
tde4.setWidgetOffsets(req,"select_menu",0,0,0,0)
tde4.setWidgetAttachModes(req,"select_menu","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"select_menu",80,20)
tde4.addMenuButtonWidget(req,"select_all_models_menu_btn","Select all models","select_menu")
tde4.setWidgetOffsets(req,"select_all_models_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"select_all_models_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"select_all_models_menu_btn",80,20)
tde4.addMenuButtonWidget(req,"select_model_on_point_menu_btn","Select model(s) on point(s)","select_menu")
tde4.setWidgetOffsets(req,"select_model_on_point_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"select_model_on_point_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"select_model_on_point_menu_btn",80,20)
tde4.addMenuButtonWidget(req,"select_points_menu_btn","Select points","select_menu")
tde4.setWidgetOffsets(req,"select_points_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"select_points_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"select_points_menu_btn",80,20)
tde4.addMenuWidget(req,"color_menu","Color","menu_bar",1)
tde4.setWidgetOffsets(req,"color_menu",0,0,0,0)
tde4.setWidgetAttachModes(req,"color_menu","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"color_menu",80,20)
tde4.setWidgetBGColor(req,"color_menu",0.000000,0.000000,0.000000)
tde4.addMenuButtonWidget(req,"red_menu_btn","Red","color_menu")
tde4.setWidgetOffsets(req,"red_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"red_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"red_menu_btn",80,20)
tde4.setWidgetFGColor(req,"red_menu_btn",1.000000,0.000000,0.000000)
tde4.addMenuButtonWidget(req,"green_menu_btn","Green","color_menu")
tde4.setWidgetOffsets(req,"green_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"green_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"green_menu_btn",80,20)
tde4.setWidgetFGColor(req,"green_menu_btn",0.000000,1.000000,0.000000)
tde4.addMenuButtonWidget(req,"blue_menu_btn","Blue","color_menu")
tde4.setWidgetOffsets(req,"blue_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"blue_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"blue_menu_btn",80,20)
tde4.setWidgetFGColor(req,"blue_menu_btn",0.000000,0.000000,1.000000)
tde4.addMenuButtonWidget(req,"yellow_menu_btn","Yellow","color_menu")
tde4.setWidgetOffsets(req,"yellow_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"yellow_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"yellow_menu_btn",80,20)
tde4.setWidgetFGColor(req,"yellow_menu_btn",1.000000,1.000000,0.000000)
tde4.addMenuButtonWidget(req,"black_menu_btn","Black","color_menu")
tde4.setWidgetOffsets(req,"black_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"black_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"black_menu_btn",80,20)
tde4.setWidgetFGColor(req,"black_menu_btn",0.000000,0.000000,0.000000)
tde4.addMenuButtonWidget(req,"white_menu_btn","White","color_menu")
tde4.setWidgetOffsets(req,"white_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"white_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"white_menu_btn",80,20)
tde4.setWidgetFGColor(req,"white_menu_btn",1.000000,1.000000,1.000000)
tde4.addMenuButtonWidget(req,"gray_menu_btn","Gray","color_menu")
tde4.setWidgetOffsets(req,"gray_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"gray_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"gray_menu_btn",80,20)
tde4.setWidgetFGColor(req,"gray_menu_btn",0.500000,0.500000,0.500000)
tde4.addMenuButtonWidget(req,"purple_menu_btn","Purple","color_menu")
tde4.setWidgetOffsets(req,"purple_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"purple_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"purple_menu_btn",80,20)
tde4.setWidgetFGColor(req,"purple_menu_btn",1.000000,0.000000,1.000000)
tde4.addMenuButtonWidget(req,"cyan_menu_btn","Cyan","color_menu")
tde4.setWidgetOffsets(req,"cyan_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"cyan_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"cyan_menu_btn",80,20)
tde4.setWidgetFGColor(req,"cyan_menu_btn",0.220000,0.450000,0.650000)
tde4.addMenuWidget(req,"rendering_menu","Rendering","menu_bar",0)
tde4.setWidgetOffsets(req,"rendering_menu",0,0,0,0)
tde4.setWidgetAttachModes(req,"rendering_menu","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"rendering_menu",80,20)
tde4.addMenuToggleWidget(req,"show_lines_rdo_box","Show lines","rendering_menu",1)
tde4.setWidgetOffsets(req,"show_lines_rdo_box",0,0,0,0)
tde4.setWidgetAttachModes(req,"show_lines_rdo_box","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"show_lines_rdo_box",80,20)
tde4.addMenuToggleWidget(req,"show_polygons_rdo_box","Show polygons","rendering_menu",1)
tde4.setWidgetOffsets(req,"show_polygons_rdo_box",0,0,0,0)
tde4.setWidgetAttachModes(req,"show_polygons_rdo_box","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"show_polygons_rdo_box",80,20)
tde4.addMenuWidget(req,"model_shape_menu","Model shape","menu_bar",1)
tde4.setWidgetOffsets(req,"model_shape_menu",0,0,0,0)
tde4.setWidgetAttachModes(req,"model_shape_menu","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"model_shape_menu",80,20)
tde4.addMenuButtonWidget(req,"box_cone_menu_btn","Box cone","model_shape_menu")
tde4.setWidgetOffsets(req,"box_cone_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"box_cone_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"box_cone_menu_btn",80,20)
tde4.addMenuButtonWidget(req,"round_cone_menu_btn","Round cone","model_shape_menu")
tde4.setWidgetOffsets(req,"round_cone_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"round_cone_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"round_cone_menu_btn",80,20)
tde4.addMenuButtonWidget(req,"cube_menu_btn","Cube","model_shape_menu")
tde4.setWidgetOffsets(req,"cube_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"cube_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"cube_menu_btn",80,20)
tde4.addMenuButtonWidget(req,"locator_menu_btn","Locator","model_shape_menu")
tde4.setWidgetOffsets(req,"locator_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"locator_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"locator_menu_btn",80,20)
tde4.addMenuWidget(req,"reset_menu","Reset","menu_bar",0)
tde4.setWidgetOffsets(req,"reset_menu",0,0,0,0)
tde4.setWidgetAttachModes(req,"reset_menu","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"reset_menu",80,20)
tde4.addMenuButtonWidget(req,"reset_ui_menu_btn","Reset UI settings","reset_menu")
tde4.setWidgetOffsets(req,"reset_ui_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"reset_ui_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"reset_ui_menu_btn",80,20)
tde4.addScaleWidget(req,"scale_slider","Uniform scale","DOUBLE",0.001,10.0,1.0)
tde4.setWidgetOffsets(req,"scale_slider",17,83,35,0)
tde4.setWidgetAttachModes(req,"scale_slider","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"scale_slider",200,20)
tde4.addTextFieldWidget(req,"scale_text_value","","1.0")
tde4.setWidgetOffsets(req,"scale_text_value",85,98,35,0)
tde4.setWidgetAttachModes(req,"scale_text_value","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"scale_text_value",200,20)
tde4.addToggleWidget(req,"prop_scale_rdo_box","Set proportional scale",0)
tde4.setWidgetOffsets(req,"prop_scale_rdo_box",165,50,10,0)
tde4.setWidgetAttachModes(req,"prop_scale_rdo_box","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"prop_scale_rdo_box",20,20)
tde4.addLabelWidget(req,"scale_in_percentage_label","Scale in %","ALIGN_LABEL_LEFT")
tde4.setWidgetOffsets(req,"scale_in_percentage_label",30,42,10,0)
tde4.setWidgetAttachModes(req,"scale_in_percentage_label","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"scale_in_percentage_label",200,20)
tde4.addTextFieldWidget(req,"prop_scale_x_txt","X","10")
tde4.setWidgetOffsets(req,"prop_scale_x_txt",45,53,10,0)
tde4.setWidgetAttachModes(req,"prop_scale_x_txt","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"prop_scale_x_txt",200,20)
tde4.setWidgetSensitiveFlag(req,"prop_scale_x_txt",0)
tde4.addTextFieldWidget(req,"prop_scale_y_txt","Y","10")
tde4.setWidgetOffsets(req,"prop_scale_y_txt",57,65,10,0)
tde4.setWidgetAttachModes(req,"prop_scale_y_txt","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"prop_scale_y_txt",200,20)
tde4.setWidgetSensitiveFlag(req,"prop_scale_y_txt",0)
tde4.addTextFieldWidget(req,"prop_scale_z_txt","Z","10")
tde4.setWidgetOffsets(req,"prop_scale_z_txt",69,77,10,0)
tde4.setWidgetAttachModes(req,"prop_scale_z_txt","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"prop_scale_z_txt",200,20)
tde4.setWidgetSensitiveFlag(req,"prop_scale_z_txt",0)
tde4.addButtonWidget(req,"scale_negative_btn","-")
tde4.setWidgetOffsets(req,"scale_negative_btn",80,88,10,0)
tde4.setWidgetAttachModes(req,"scale_negative_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"scale_negative_btn",80,20)
tde4.setWidgetSensitiveFlag(req,"scale_negative_btn",0)
tde4.addButtonWidget(req,"scale_positive_btn","+")
tde4.setWidgetOffsets(req,"scale_positive_btn",91,99,10,0)
tde4.setWidgetAttachModes(req,"scale_positive_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"scale_positive_btn",80,20)
tde4.setWidgetSensitiveFlag(req,"scale_positive_btn",0)
tde4.addSeparatorWidget(req,"sep1")
tde4.setWidgetOffsets(req,"sep1",5,5,0,0)
tde4.setWidgetAttachModes(req,"sep1","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"sep1",200,20)
tde4.addScaleWidget(req,"color_red_slider","R","DOUBLE",0.0,1.0,1.0)
tde4.setWidgetOffsets(req,"color_red_slider",3,32,20,0)
tde4.setWidgetAttachModes(req,"color_red_slider","ATTACH_POSITION","ATTACH_POSITION","ATTACH_OPPOSITE_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"color_red_slider",200,20)
tde4.addScaleWidget(req,"color_green_slider","G","DOUBLE",0.0,1.0,0.0)
tde4.setWidgetOffsets(req,"color_green_slider",36,65,20,0)
tde4.setWidgetAttachModes(req,"color_green_slider","ATTACH_POSITION","ATTACH_POSITION","ATTACH_OPPOSITE_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"color_green_slider",200,20)
tde4.addScaleWidget(req,"color_blue_slider","B","DOUBLE",0.0,1.0,0.0)
tde4.setWidgetOffsets(req,"color_blue_slider",69,99,20,0)
tde4.setWidgetAttachModes(req,"color_blue_slider","ATTACH_POSITION","ATTACH_POSITION","ATTACH_OPPOSITE_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"color_blue_slider",200,20)
tde4.addScaleWidget(req,"color_alpha_slider","Alpha","DOUBLE",0.0,1.0,1.0)
tde4.setWidgetOffsets(req,"color_alpha_slider",55,10,10,0)
tde4.setWidgetAttachModes(req,"color_alpha_slider","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"color_alpha_slider",200,20)
tde4.addSeparatorWidget(req,"sep2")
tde4.setWidgetOffsets(req,"sep2",5,5,0,0)
tde4.setWidgetAttachModes(req,"sep2","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"sep2",200,20)
tde4.addTextFieldWidget(req,"scale_x_txt_value","X","1.0")
tde4.setWidgetOffsets(req,"scale_x_txt_value",18,33,20,0)
tde4.setWidgetAttachModes(req,"scale_x_txt_value","ATTACH_POSITION","ATTACH_POSITION","ATTACH_OPPOSITE_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"scale_x_txt_value",100,20)
tde4.addTextFieldWidget(req,"scale_y_txt_value","Y","1.0")
tde4.setWidgetOffsets(req,"scale_y_txt_value",38,53,20,0)
tde4.setWidgetAttachModes(req,"scale_y_txt_value","ATTACH_POSITION","ATTACH_POSITION","ATTACH_OPPOSITE_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"scale_y_txt_value",100,20)
tde4.addTextFieldWidget(req,"scale_z_txt_value","Z","1.0")
tde4.setWidgetOffsets(req,"scale_z_txt_value",58,73,20,0)
tde4.setWidgetAttachModes(req,"scale_z_txt_value","ATTACH_POSITION","ATTACH_POSITION","ATTACH_OPPOSITE_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"scale_z_txt_value",100,20)
tde4.addLabelWidget(req,"scale_label","Scale","ALIGN_LABEL_RIGHT")
tde4.setWidgetOffsets(req,"scale_label",73,82,20,0)
tde4.setWidgetAttachModes(req,"scale_label","ATTACH_POSITION","ATTACH_POSITION","ATTACH_OPPOSITE_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"scale_label",50,20)
tde4.addTextFieldWidget(req,"rot_x_txt_value","X","0.0")
tde4.setWidgetOffsets(req,"rot_x_txt_value",18,33,10,0)
tde4.setWidgetAttachModes(req,"rot_x_txt_value","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"rot_x_txt_value",100,20)
tde4.addTextFieldWidget(req,"rot_y_txt_value","Y","0.0")
tde4.setWidgetOffsets(req,"rot_y_txt_value",38,53,10,0)
tde4.setWidgetAttachModes(req,"rot_y_txt_value","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"rot_y_txt_value",100,20)
tde4.addLabelWidget(req,"rotate_label","Rotate","ALIGN_LABEL_RIGHT")
tde4.setWidgetOffsets(req,"rotate_label",73,83,10,0)
tde4.setWidgetAttachModes(req,"rotate_label","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"rotate_label",50,20)
tde4.addTextFieldWidget(req,"rot_z_txt_value","Z","0.0")
tde4.setWidgetOffsets(req,"rot_z_txt_value",58,73,10,0)
tde4.setWidgetAttachModes(req,"rot_z_txt_value","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"rot_z_txt_value",100,20)
tde4.addSeparatorWidget(req,"sep3")
tde4.setWidgetOffsets(req,"sep3",5,5,0,0)
tde4.setWidgetAttachModes(req,"sep3","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"sep3",200,20)
tde4.addButtonWidget(req,"create_btn","Create models")
tde4.setWidgetOffsets(req,"create_btn",3,23,22,0)
tde4.setWidgetAttachModes(req,"create_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"create_btn",200,20)
tde4.addButtonWidget(req,"delete_extra_models_btn","Delete extra models")
tde4.setWidgetOffsets(req,"delete_extra_models_btn",27,52,22,0)
tde4.setWidgetAttachModes(req,"delete_extra_models_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"delete_extra_models_btn",200,20)
tde4.addButtonWidget(req,"delete_all_btn","Delete all models")
tde4.setWidgetOffsets(req,"delete_all_btn",56,80,22,0)
tde4.setWidgetAttachModes(req,"delete_all_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"delete_all_btn",200,20)
tde4.addButtonWidget(req,"close_btn","Close")
tde4.setWidgetOffsets(req,"close_btn",84,97,22,0)
tde4.setWidgetAttachModes(req,"close_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"close_btn",200,20)
tde4.setWidgetLinks(req,"menu_bar","","","","")
tde4.setWidgetLinks(req,"scale_slider","","","","")
tde4.setWidgetLinks(req,"scale_text_value","","","","")
tde4.setWidgetLinks(req,"prop_scale_rdo_box","","","scale_slider","")
tde4.setWidgetLinks(req,"scale_in_percentage_label","","","scale_slider","")
tde4.setWidgetLinks(req,"prop_scale_x_txt","","","scale_slider","")
tde4.setWidgetLinks(req,"prop_scale_y_txt","","","scale_slider","")
tde4.setWidgetLinks(req,"prop_scale_z_txt","","","scale_slider","")
tde4.setWidgetLinks(req,"scale_negative_btn","","","scale_slider","")
tde4.setWidgetLinks(req,"scale_positive_btn","","","scale_slider","")
tde4.setWidgetLinks(req,"sep1","","","scale_negative_btn","")
tde4.setWidgetLinks(req,"color_red_slider","","","sep1","")
tde4.setWidgetLinks(req,"color_green_slider","","","sep1","")
tde4.setWidgetLinks(req,"color_blue_slider","","","sep1","")
tde4.setWidgetLinks(req,"color_alpha_slider","","","color_green_slider","")
tde4.setWidgetLinks(req,"sep2","","","color_alpha_slider","")
tde4.setWidgetLinks(req,"scale_x_txt_value","","","sep2","")
tde4.setWidgetLinks(req,"scale_y_txt_value","","","sep2","")
tde4.setWidgetLinks(req,"scale_z_txt_value","","","sep2","")
tde4.setWidgetLinks(req,"scale_label","","","sep2","")
tde4.setWidgetLinks(req,"rot_x_txt_value","","","scale_x_txt_value","")
tde4.setWidgetLinks(req,"rot_y_txt_value","","","scale_y_txt_value","")
tde4.setWidgetLinks(req,"rotate_label","","color_alpha_slider","scale_z_txt_value","")
tde4.setWidgetLinks(req,"rot_z_txt_value","","","scale_z_txt_value","")
tde4.setWidgetLinks(req,"sep3","","","rot_y_txt_value","")
tde4.setWidgetLinks(req,"create_btn","","","rot_y_txt_value","")
tde4.setWidgetLinks(req,"delete_extra_models_btn","","","rot_y_txt_value","")
tde4.setWidgetLinks(req,"delete_all_btn","","","rot_y_txt_value","")
tde4.setWidgetLinks(req,"close_btn","","","rot_y_txt_value","")

load_save_gui_settings(req, "load")
load_save_gui_settings(req, "save")

# Callbacks
tde4.setWidgetCallbackFunction(req, "scale_slider", "scale_clicked")
tde4.setWidgetCallbackFunction(req, "scale_text_value", "scale_clicked")
tde4.setWidgetCallbackFunction(req, "prop_scale_rdo_box", "scale_clicked")
tde4.setWidgetCallbackFunction(req, "prop_scale_x_txt", "scale_clicked")
tde4.setWidgetCallbackFunction(req, "prop_scale_y_txt", "scale_clicked")
tde4.setWidgetCallbackFunction(req, "prop_scale_z_txt", "scale_clicked")
tde4.setWidgetCallbackFunction(req, "scale_positive_btn", "scale_clicked")
tde4.setWidgetCallbackFunction(req, "scale_negative_btn", "scale_clicked")
tde4.setWidgetCallbackFunction(req, "scale_x_txt_value", "scale_clicked")
tde4.setWidgetCallbackFunction(req, "scale_y_txt_value", "scale_clicked")
tde4.setWidgetCallbackFunction(req, "scale_z_txt_value", "scale_clicked")

tde4.setWidgetCallbackFunction(req, "rot_x_txt_value", "rotation_clicked")
tde4.setWidgetCallbackFunction(req, "rot_y_txt_value", "rotation_clicked")
tde4.setWidgetCallbackFunction(req, "rot_z_txt_value", "rotation_clicked")

tde4.setWidgetCallbackFunction(req, "show_all_models_menu_btn", "view_menu_clicked")
tde4.setWidgetCallbackFunction(req, "hide_all_models_menu_btn", "view_menu_clicked")
tde4.setWidgetCallbackFunction(req, "show_sel_models_menu_btn", "view_menu_clicked")
tde4.setWidgetCallbackFunction(req, "hide_sel_models_menu_btn", "view_menu_clicked")

tde4.setWidgetCallbackFunction(req, "select_all_models_menu_btn", "select_menu_clicked")
tde4.setWidgetCallbackFunction(req, "select_model_on_point_menu_btn", "select_menu_clicked")
tde4.setWidgetCallbackFunction(req, "select_points_menu_btn", "select_menu_clicked")

tde4.setWidgetCallbackFunction(req, "color_menu", "color_menu_clicked")
tde4.setWidgetCallbackFunction(req, "color_red_slider", "color_slider_clicked")
tde4.setWidgetCallbackFunction(req, "color_green_slider", "color_slider_clicked")
tde4.setWidgetCallbackFunction(req, "color_blue_slider", "color_slider_clicked")
tde4.setWidgetCallbackFunction(req, "color_alpha_slider", "color_slider_clicked")

tde4.setWidgetCallbackFunction(req, "show_lines_rdo_box", "rendering_menu_clicked")
tde4.setWidgetCallbackFunction(req, "show_polygons_rdo_box", "rendering_menu_clicked")

tde4.setWidgetCallbackFunction(req, "model_shape_menu", "model_shape_menu_clicked")

tde4.setWidgetCallbackFunction(req, "reset_ui_menu_btn", "reset_ui_settings_clicked")

tde4.setWidgetCallbackFunction(req, "create_btn", "create_models_clicked")
tde4.setWidgetCallbackFunction(req, "delete_extra_models_btn", "delete_extra_models_clicked")
tde4.setWidgetCallbackFunction(req, "delete_all_btn", "delete_all_models_clicked")

tde4.setWidgetCallbackFunction(req, "close_btn", "close_btn_clicked")

tde4.postCustomRequesterAndContinue(req, WINDOW_TITLE, 640, 277)

