# 3DE4.script.name: Pose Saver/Loader
# 3DE4.script.version: v2.4
# 3DE4.script.gui.config_menus: true		
# 3DE4.script.gui:Main Window::3DE4
# 3DE4.script.comment: Import/Export 3D rot/pos channels from/to a .pose file.
# 28 Nov 2016(Mumbai)
# Updated April 2018(Montreal)
# Updated August 2021(Montreal)
# Patcha Saheb (patchasaheb@gmail.com)

from vl_sdv import *
import math

WINDOW_TITLE = "Patcha Pose Saver/Loader v2.4"

def enable_disable_widgets(value):
	tde4.setWidgetSensitiveFlag(req, "browse_btn_text", 1-value)
	tde4.setWidgetSensitiveFlag(req, "import_pose_btn", 1-value)
	tde4.setWidgetSensitiveFlag(req, "export_pose_btn", 1-value)
	tde4.setWidgetSensitiveFlag(req, "copy_pose_btn", value)
	tde4.setWidgetSensitiveFlag(req, "paste_pose_btn", value)

def disk_operation_rdo_btn_clicked(req, widget, action):
	if tde4.getWidgetValue(req, "disk_rdo_btn") == 1:
		tde4.setWidgetValue(req, "clipboard_rdo_btn", str(0))
		enable_disable_widgets(0)
	else:
		tde4.setWidgetValue(req, "clipboard_rdo_btn", str(1))
		enable_disable_widgets(1)		

def clipboard_operation_rdo_btn_clicked(req, widget, action):
	if tde4.getWidgetValue(req, "clipboard_rdo_btn") == 1:
		tde4.setWidgetValue(req, "disk_rdo_btn", str(0))
		enable_disable_widgets(1)
	else:
		tde4.setWidgetValue(req, "disk_rdo_btn", str(1))
		enable_disable_widgets(0)		

def frame_update(req):
	pg	= tde4.getCurrentPGroup()
	cam     = tde4.getCurrentCamera()
	frame   = tde4.getCurrentFrame(cam)
	offset = tde4.getCameraFrameOffset(cam)-1
	frame = frame + offset
	tde4.setWidgetValue(req,"import_start_txt",str(frame))
	tde4.setWidgetValue(req,"import_end_text",str(frame))









req = tde4.createCustomRequester()
tde4.addMenuBarWidget(req,"menubar")
tde4.setWidgetOffsets(req,"menubar",0,0,0,0)
tde4.setWidgetAttachModes(req,"menubar","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"menubar",200,20)
tde4.addMenuWidget(req,"undo_menu","Undo","menubar",0)
tde4.setWidgetOffsets(req,"undo_menu",0,0,0,0)
tde4.setWidgetAttachModes(req,"undo_menu","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"undo_menu",80,20)
tde4.addMenuButtonWidget(req,"undo_menu_btn","Undo last import","undo_menu")
tde4.setWidgetOffsets(req,"undo_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"undo_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"undo_menu_btn",80,20)
tde4.addMenuWidget(req,"pose_file_menu","Pose file","menubar",0)
tde4.setWidgetOffsets(req,"pose_file_menu",0,0,0,0)
tde4.setWidgetAttachModes(req,"pose_file_menu","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"pose_file_menu",80,20)
tde4.addMenuButtonWidget(req,"show_pose_file_menu_btn","Show pose file","pose_file_menu")
tde4.setWidgetOffsets(req,"show_pose_file_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"show_pose_file_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"show_pose_file_menu_btn",80,20)
tde4.addFileWidget(req,"browse_btn_text","Browse...","*","")
tde4.setWidgetOffsets(req,"browse_btn_text",20,98,10,0)
tde4.setWidgetAttachModes(req,"browse_btn_text","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"browse_btn_text",200,20)
tde4.addToggleWidget(req,"disk_rdo_btn","Disk operation",1)
tde4.setWidgetOffsets(req,"disk_rdo_btn",200,0,15,0)
tde4.setWidgetAttachModes(req,"disk_rdo_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"disk_rdo_btn",20,20)
tde4.addToggleWidget(req,"clipboard_rdo_btn","Clipboard operation",0)
tde4.setWidgetOffsets(req,"clipboard_rdo_btn",450,0,15,0)
tde4.setWidgetAttachModes(req,"clipboard_rdo_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"clipboard_rdo_btn",20,20)
tde4.addOptionMenuWidget(req,"type_option_menu","Type","Camera/REF Camera","ObjectPGroup","3D Model")
tde4.setWidgetOffsets(req,"type_option_menu",15,95,15,0)
tde4.setWidgetAttachModes(req,"type_option_menu","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"type_option_menu",150,20)
tde4.addTextFieldWidget(req,"import_start_txt","Import start frame","0")
tde4.setWidgetOffsets(req,"import_start_txt",30,45,15,0)
tde4.setWidgetAttachModes(req,"import_start_txt","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"import_start_txt",200,20)
tde4.addTextFieldWidget(req,"import_end_text","Import end frame","0")
tde4.setWidgetOffsets(req,"import_end_text",80,95,15,0)
tde4.setWidgetAttachModes(req,"import_end_text","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"import_end_text",200,20)
tde4.addButtonWidget(req,"import_pose_btn","Import pose")
tde4.setWidgetOffsets(req,"import_pose_btn",2,24,20,0)
tde4.setWidgetAttachModes(req,"import_pose_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"import_pose_btn",80,20)
tde4.addButtonWidget(req,"export_pose_btn","Export pose")
tde4.setWidgetOffsets(req,"export_pose_btn",28,49,20,0)
tde4.setWidgetAttachModes(req,"export_pose_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"export_pose_btn",80,20)
tde4.addButtonWidget(req,"copy_pose_btn","Copy pose")
tde4.setWidgetOffsets(req,"copy_pose_btn",53,73,20,0)
tde4.setWidgetAttachModes(req,"copy_pose_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"copy_pose_btn",80,20)
tde4.setWidgetSensitiveFlag(req,"copy_pose_btn",0)
tde4.addButtonWidget(req,"paste_pose_btn","Paste pose")
tde4.setWidgetOffsets(req,"paste_pose_btn",77,97,20,0)
tde4.setWidgetAttachModes(req,"paste_pose_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"paste_pose_btn",80,20)
tde4.setWidgetSensitiveFlag(req,"paste_pose_btn",0)
tde4.setWidgetLinks(req,"menubar","","","","")
tde4.setWidgetLinks(req,"browse_btn_text","","","menubar","")
tde4.setWidgetLinks(req,"disk_rdo_btn","","","browse_btn_text","")
tde4.setWidgetLinks(req,"clipboard_rdo_btn","","","browse_btn_text","")
tde4.setWidgetLinks(req,"type_option_menu","","","disk_rdo_btn","")
tde4.setWidgetLinks(req,"import_start_txt","","","type_option_menu","")
tde4.setWidgetLinks(req,"import_end_text","","","type_option_menu","")
tde4.setWidgetLinks(req,"import_pose_btn","","","import_start_txt","")
tde4.setWidgetLinks(req,"export_pose_btn","","","import_start_txt","")
tde4.setWidgetLinks(req,"copy_pose_btn","","","import_start_txt","")
tde4.setWidgetLinks(req,"paste_pose_btn","","","import_start_txt","")

# Callbacks
tde4.setWidgetCallbackFunction(req, "disk_rdo_btn", "disk_operation_rdo_btn_clicked")
tde4.setWidgetCallbackFunction(req, "clipboard_rdo_btn", "clipboard_operation_rdo_btn_clicked")

tde4.postCustomRequesterAndContinue(req,WINDOW_TITLE,500,205,"frame_update")

