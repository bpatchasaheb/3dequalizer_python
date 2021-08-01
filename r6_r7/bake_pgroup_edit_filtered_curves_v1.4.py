# 3DE4.script.name: Bake PGroup edit/filtered curves
# 3DE4.script.version: v1.4
# 3DE4.script.gui:Curve Editor::Edit
# 3DE4.script.comment: Bakes translation and rotation keyframes, so that any postfilter smoothing, etc. is baked from the filtered curves to the edit curves. May then need euler flipping filter applied.

# Patcha Saheb(patchasaheb@gmail.com)
# August 01 2021, Montreal

WINDOW_TITLE = "Bake PGroup edit/filtered curves v1.4"

def snap_filtered_to_edit_btn_clicked(req, widget, action):
	pg = tde4.getCurrentPGroup()
	cam = tde4.getCurrentCamera()
	tde4.copyPGroupEditCurvesToFilteredCurves(pg, cam)

def snap_edit_to_filtered_btn_clicked(req, widget, action):
	pg = tde4.getCurrentPGroup()
	cam = tde4.getCurrentCamera()
	frames = tde4.getCameraNoFrames(cam)
	pg_type = tde4.getPGroupType(pg)
	for frame in range(1, frames+1):
		pos = tde4.getPGroupPosition3D(pg, cam, frame)
		rot = tde4.getPGroupRotation3D(pg, cam, frame)
		scale = tde4.getPGroupScale3D(pg)
		if pg_type == "OBJECT":
			rot, pos = tde4.convertObjectPGroupTransformationWorldTo3DE(cam, frame, rot, pos, scale, 1)
		tde4.setPGroupPosition3D(pg, cam, frame, pos)
		tde4.setPGroupRotation3D(pg, cam, frame, rot)
		tde4.setPGroupScale3D(pg, scale)
	postfilter_mode  = tde4.getPGroupPostfilterMode(pg)
	tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
	tde4.filterPGroup(pg, cam)
	tde4.setPGroupPostfilterMode(pg, postfilter_mode)

# GUI
req = tde4.createCustomRequester()
tde4.addLabelWidget(req,"edit_curves_label","Edit curves:   Actual curves with visible keys","ALIGN_LABEL_CENTER")
tde4.setWidgetOffsets(req,"edit_curves_label",5,95,10,0)
tde4.setWidgetAttachModes(req,"edit_curves_label","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"edit_curves_label",200,20)
tde4.addLabelWidget(req,"filtered_curves_label","Filtered curves:   Smooth curves with no visible keys","ALIGN_LABEL_CENTER")
tde4.setWidgetOffsets(req,"filtered_curves_label",7,95,10,0)
tde4.setWidgetAttachModes(req,"filtered_curves_label","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"filtered_curves_label",200,20)
tde4.addButtonWidget(req,"snap_edit_to_filtered_btn","Snap Edit curves to Filtered curves")
tde4.setWidgetOffsets(req,"snap_edit_to_filtered_btn",15,85,20,0)
tde4.setWidgetAttachModes(req,"snap_edit_to_filtered_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"snap_edit_to_filtered_btn",80,20)
tde4.addButtonWidget(req,"snap_filtered_to_edit_btn","Snap Filtered curves to Edit curves")
tde4.setWidgetOffsets(req,"snap_filtered_to_edit_btn",15,85,20,0)
tde4.setWidgetAttachModes(req,"snap_filtered_to_edit_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"snap_filtered_to_edit_btn",80,20)
tde4.setWidgetLinks(req,"edit_curves_label","","","","")
tde4.setWidgetLinks(req,"filtered_curves_label","","","edit_curves_label","")
tde4.setWidgetLinks(req,"snap_edit_to_filtered_btn","","","filtered_curves_label","")
tde4.setWidgetLinks(req,"snap_filtered_to_edit_btn","","","snap_edit_to_filtered_btn","")

# Callbacks
tde4.setWidgetCallbackFunction(req, "snap_filtered_to_edit_btn", "snap_filtered_to_edit_btn_clicked")
tde4.setWidgetCallbackFunction(req, "snap_edit_to_filtered_btn", "snap_edit_to_filtered_btn_clicked")

tde4.postCustomRequesterAndContinue(req,WINDOW_TITLE,400,155)

