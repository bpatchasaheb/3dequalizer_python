# 3DE4.script.name: 3DE Animation Layers...
# 3DE4.script.version: v1.0
# 3DE4.script.gui: Lineup Controls::Edit
# 3DE4.script.gui: Orientation Controls::Edit
# 3DE4.script.gui.button: Lineup Controls::Anim Layers, align-bottom-left, 80,20
# 3DE4.script.gui.button: Orientation Controls::Anim Layers, align-bottom-left, 70,20
# 3DE4.script.comment:  This tool works as Maya Animation Layers.
# 3DE4.script.gui.config_menus: true

# Patcha Saheb(patchasaheb@gmail.com)
# October 07 2021(Montreal)

import json
from vl_sdv import*

WINDOW_TITLE = "Patcha 3DE Animation Layers v1.0"
PERSISTENT_STRING_NAME = "PATCHA_3DE_ANIMATION_LAYERS_DATA"
SPACE_MULTIPLIER = 10
CURVE_NAMES = ["Pos X", "Pos Y", "Pos Z", "Rot X", "Rot Y", "Rot Z", "Weight"]
CURVE_COLORS = [(0.812,0.277,0.257),(0.441,0.816,0.354),(0.422,0.408,0.820),
                (0.453,0.815,0.809),(0.855,0.272,0.816),(0.819,0.812,0.387),
                (0.583,0.584,0.144)] 
EDIT_CURVES_LIST = ["TX_CURVE", "TY_CURVE", "TZ_CURVE",
                    "RX_CURVE", "RY_CURVE", "RZ_CURVE"]
AXES = ["position_x", "position_y", "position_z",
        "rotation_x", "rotation_y", "rotation_z"]                

pg = tde4.getCurrentPGroup()
cam = tde4.getCurrentCamera()
frames = tde4.getCameraNoFrames(cam)

cam_pers_id = tde4.getCameraPersistentID(cam)
pg_pers_id = tde4.getPGroupPersistentID(pg)

def snap_edit_to_filtered_curves():
    pg_type = tde4.getPGroupType(pg)
    for frame in range(1, frames+1):
        pos = tde4.getPGroupPosition3D(pg, cam, frame)
        rot = tde4.getPGroupRotation3D(pg, cam, frame)
        scale = tde4.getPGroupScale3D(pg)
        if pg_type == "OBJECT":
            rot, pos = tde4.convertObjectPGroupTransformationWorldTo3DE(cam, 
                                                      frame, rot, pos, scale, 1)
        tde4.setPGroupPosition3D(pg, cam, frame, pos)
        tde4.setPGroupRotation3D(pg, cam, frame, rot)
    tde4.setPGroupScale3D(pg, scale)
    postfilter_mode  = tde4.getPGroupPostfilterMode(pg)
    tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
    tde4.filterPGroup(pg, cam)
    tde4.setPGroupPostfilterMode(pg, postfilter_mode)

def create_curve_set(cam_pers_id, pg_pers_id, layer_name): 
    # Create curves, insert list widget items
    pos_x_curve = tde4.createCurve()
    pos_y_curve = tde4.createCurve()
    pos_z_curve = tde4.createCurve()
    rot_x_curve = tde4.createCurve()
    rot_y_curve = tde4.createCurve()
    rot_z_curve = tde4.createCurve()    
    weight_curve = tde4.createCurve()
    curve_ids = [pos_x_curve, pos_y_curve, pos_z_curve,
                 rot_x_curve, rot_y_curve, rot_z_curve, weight_curve]     
    parent_item = tde4.insertListWidgetItem(req, "layers_list_wdgt", layer_name,
                                            0, "LIST_ITEM_NODE")
    tde4.setListWidgetItemCollapsedFlag(req, "layers_list_wdgt", parent_item, 0)
    for count, curve_id in enumerate(curve_ids):
        item_name = CURVE_NAMES[count]+" "*SPACE_MULTIPLIER+"-"+str(curve_id)
        child_item = tde4.insertListWidgetItem(req, "layers_list_wdgt",
                                   item_name, 1, "LIST_ITEM_ATOM", parent_item)
        tde4.setListWidgetItemColor(req, "layers_list_wdgt", child_item,
                                CURVE_COLORS[count][0], CURVE_COLORS[count][1],
                                CURVE_COLORS[count][2])
    # Create curve keys
    data = load_data()
    for count, axis in enumerate(AXES):
        axis_data = data[str(cam_pers_id)][str(pg_pers_id)]["layers"][layer_name][axis]
        extract_keys_from_data(curve_ids[count], axis_data)
    # handle weight curve
    axis_data = data[str(cam_pers_id)][str(pg_pers_id)]["layers"][layer_name]["weight"]
    extract_keys_from_data(weight_curve, axis_data)


def extract_keys_from_data(curve, axis_data):
    for frame in axis_data.keys():
        x = float(frame)
        y = float(axis_data[frame])
        key = tde4.createCurveKey(curve, [x,y])
        tde4.setCurveKeyMode(curve, key, "LINEAR")
        tde4.setCurveKeyFixedXFlag(curve, key, 1)


def layer_item_clicked(req, widget, action):
    sel_items = tde4.getListWidgetSelectedItems(req, "layers_list_wdgt") or []
    if len(sel_items) > 0:
        tde4.detachCurveAreaWidgetAllCurves(req, "curve_area_wdgt")        
        for item in sel_items:
            item_label = tde4.getListWidgetItemLabel(req, "layers_list_wdgt", item)
            item_color = tde4.getListWidgetItemColor(req, "layers_list_wdgt", item)
            if tde4.getListWidgetItemType(req, "layers_list_wdgt", item) == "LIST_ITEM_ATOM":
                curve = item_label.split("-")[1]
                tde4.attachCurveAreaWidgetCurve(req, "curve_area_wdgt", curve,
                                    item_color[0],item_color[1],item_color[2],1)



def get_curve_min_max_y_value(curve_list):
    min_max_values = [None, None]    
    key_data = []
    for curve in curve_list:
        key_list = tde4.getCurveKeyList(curve, 0)
        if len(key_list) > 0:
            for key in key_list:
                pos2d = tde4.getCurveKeyPosition(curve, key)
                key_data.append(pos2d[1])
    if len(key_data) >= 1:
        min_max_values = [round(min(key_data), 4), round(max(key_data), 4)]
    return min_max_values


def view_all_helper():
    curve_list = tde4.getCurveAreaWidgetCurveList(req, "curve_area_wdgt")
    for curve in curve_list:
        frames = tde4.getCameraNoFrames(tde4.getCurrentCamera())   
        dmin = get_curve_min_max_y_value(curve_list)[0]
        dmax = get_curve_min_max_y_value(curve_list)[1]         
        if dmin and dmax:        
            if dmin == dmax:
                dmax = dmax * 2 
        else:
            dmin = -0.5
            dmax = 0.5 
        tde4.setCurveAreaWidgetDimensions(req,"curve_area_wdgt",1.0,
                         frames,dmin-((dmax-dmin)*0.05),dmax+((dmax-dmin)*0.05))
        tde4.setCurveAreaWidgetFOV(req,"curve_area_wdgt",1.0-(frames*0.05),
                    frames*1.05,dmin-((dmax-dmin)*0.10),dmax+((dmax-dmin)*0.10))


def view_all_btn_clicked(req, widget, action):
    view_all_helper()


req = tde4.createCustomRequester()

tde4.addListWidget(req,"layers_list_wdgt","",1)
tde4.setWidgetOffsets(req,"layers_list_wdgt",0,5,5,90)
tde4.setWidgetAttachModes(req,"layers_list_wdgt","ATTACH_NONE","ATTACH_WINDOW","ATTACH_WIDGET","ATTACH_WINDOW")
tde4.setWidgetSize(req,"layers_list_wdgt",280,150)
tde4.addCurveAreaWidget(req,"curve_area_wdgt","")
tde4.setWidgetOffsets(req,"curve_area_wdgt",5,5,25,30)
tde4.setWidgetAttachModes(req,"curve_area_wdgt","ATTACH_WINDOW","ATTACH_WIDGET","ATTACH_WINDOW","ATTACH_WINDOW")
tde4.setWidgetSize(req,"curve_area_wdgt",150,150)
tde4.addTextFieldWidget(req,"pgroup_name_wdgt","","")
tde4.setWidgetOffsets(req,"pgroup_name_wdgt",5,5,25,0)
tde4.setWidgetAttachModes(req,"pgroup_name_wdgt","ATTACH_WIDGET","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"pgroup_name_wdgt",200,20)
tde4.setWidgetSensitiveFlag(req,"pgroup_name_wdgt",0)
tde4.addMenuBarWidget(req,"w006")
tde4.setWidgetOffsets(req,"w006",0,0,0,0)
tde4.setWidgetAttachModes(req,"w006","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"w006",300,20)
tde4.addMenuWidget(req,"layers_menu_wdgt","Layers","w006",0)
tde4.setWidgetOffsets(req,"layers_menu_wdgt",0,0,0,0)
tde4.setWidgetAttachModes(req,"layers_menu_wdgt","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"layers_menu_wdgt",80,20)
tde4.addMenuButtonWidget(req,"create_empty_layer_menu_btn","Create Empty Layer","layers_menu_wdgt")
tde4.setWidgetOffsets(req,"create_empty_layer_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"create_empty_layer_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"create_empty_layer_menu_btn",80,20)
tde4.addMenuButtonWidget(req,"rename_layer_menu_btn","Rename Layer","layers_menu_wdgt")
tde4.setWidgetOffsets(req,"rename_layer_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"rename_layer_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"rename_layer_menu_btn",80,20)
tde4.addMenuSeparatorWidget(req,"w015","layers_menu_wdgt")
tde4.setWidgetOffsets(req,"w015",0,0,0,0)
tde4.setWidgetAttachModes(req,"w015","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"w015",80,20)
tde4.addMenuButtonWidget(req,"del_layers_menu_btn","Delete Layers","layers_menu_wdgt")
tde4.setWidgetOffsets(req,"del_layers_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"del_layers_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"del_layers_menu_btn",80,20)
tde4.addMenuButtonWidget(req,"del_empty_layers_menu_btn","Delete Empty Layers","layers_menu_wdgt")
tde4.setWidgetOffsets(req,"del_empty_layers_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"del_empty_layers_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"del_empty_layers_menu_btn",80,20)
tde4.addMenuSeparatorWidget(req,"w018","layers_menu_wdgt")
tde4.setWidgetOffsets(req,"w018",0,0,0,0)
tde4.setWidgetAttachModes(req,"w018","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"w018",80,20)
tde4.addMenuButtonWidget(req,"mute_layers_menu_btn","Mute Layers","layers_menu_wdgt")
tde4.setWidgetOffsets(req,"mute_layers_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"mute_layers_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"mute_layers_menu_btn",80,20)
tde4.addMenuButtonWidget(req,"unmute_layers_menu_btn","Unmute Layers","layers_menu_wdgt")
tde4.setWidgetOffsets(req,"unmute_layers_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"unmute_layers_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"unmute_layers_menu_btn",80,20)
tde4.addMenuSeparatorWidget(req,"w021","layers_menu_wdgt")
tde4.setWidgetOffsets(req,"w021",0,0,0,0)
tde4.setWidgetAttachModes(req,"w021","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"w021",80,20)
tde4.addMenuButtonWidget(req,"merge_layers_menu_btn","Merge Layers","layers_menu_wdgt")
tde4.setWidgetOffsets(req,"merge_layers_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"merge_layers_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"merge_layers_menu_btn",80,20)
tde4.addMenuSeparatorWidget(req,"w045","layers_menu_wdgt")
tde4.setWidgetOffsets(req,"w045",0,0,0,0)
tde4.setWidgetAttachModes(req,"w045","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"w045",80,20)
tde4.addMenuButtonWidget(req,"make_layers_empty_menu_btn","Make Layers Empty","layers_menu_wdgt")
tde4.setWidgetOffsets(req,"make_layers_empty_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"make_layers_empty_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"make_layers_empty_menu_btn",80,20)
tde4.addMenuWidget(req,"keys_menu","Keys","w006",0)
tde4.setWidgetOffsets(req,"keys_menu",0,0,0,0)
tde4.setWidgetAttachModes(req,"keys_menu","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"keys_menu",80,20)
tde4.addMenuButtonWidget(req,"create_key_menu_btn","Create Key","keys_menu")
tde4.setWidgetOffsets(req,"create_key_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"create_key_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"create_key_menu_btn",80,20)
tde4.addMenuButtonWidget(req,"delete_key_menu_btn","Delete Key","keys_menu")
tde4.setWidgetOffsets(req,"delete_key_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"delete_key_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"delete_key_menu_btn",80,20)
tde4.addMenuSeparatorWidget(req,"w056","keys_menu")
tde4.setWidgetOffsets(req,"w056",0,0,0,0)
tde4.setWidgetAttachModes(req,"w056","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"w056",80,20)
tde4.addMenuButtonWidget(req,"jump_prev_key_menu_btn","Jump to Previous Key","keys_menu")
tde4.setWidgetOffsets(req,"jump_prev_key_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"jump_prev_key_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"jump_prev_key_menu_btn",80,20)
tde4.addMenuButtonWidget(req,"jump_next_key_menu_btn","Jump to Next Key","keys_menu")
tde4.setWidgetOffsets(req,"jump_next_key_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"jump_next_key_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"jump_next_key_menu_btn",80,20)
tde4.addMenuSeparatorWidget(req,"w060","keys_menu")
tde4.setWidgetOffsets(req,"w060",0,0,0,0)
tde4.setWidgetAttachModes(req,"w060","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"w060",80,20)
tde4.addMenuButtonWidget(req,"create_zero_key_menu_btn","Create Zero Key","keys_menu")
tde4.setWidgetOffsets(req,"create_zero_key_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"create_zero_key_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"create_zero_key_menu_btn",80,20)
tde4.addMenuSeparatorWidget(req,"w071","keys_menu")
tde4.setWidgetOffsets(req,"w071",0,0,0,0)
tde4.setWidgetAttachModes(req,"w071","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"w071",80,20)
tde4.addMenuToggleWidget(req,"show_timeline_keys_menu_btn","Show Timeline Keys","keys_menu",1)
tde4.setWidgetOffsets(req,"show_timeline_keys_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"show_timeline_keys_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"show_timeline_keys_menu_btn",80,20)
tde4.addMenuWidget(req,"objpg_menu","ObjectPG","w006",0)
tde4.setWidgetOffsets(req,"objpg_menu",0,0,0,0)
tde4.setWidgetAttachModes(req,"objpg_menu","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"objpg_menu",80,20)
tde4.addMenuToggleWidget(req,"update_objpg_menu_btn","Update ObjectPG along with Camera","objpg_menu",1)
tde4.setWidgetOffsets(req,"update_objpg_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"update_objpg_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"update_objpg_menu_btn",80,20)
tde4.addToggleWidget(req,"auto_view_all_toggle_btn","Auto View All",0)
tde4.setWidgetOffsets(req,"auto_view_all_toggle_btn",0,10,5,0)
tde4.setWidgetAttachModes(req,"auto_view_all_toggle_btn","ATTACH_NONE","ATTACH_WIDGET","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"auto_view_all_toggle_btn",20,20)
tde4.addButtonWidget(req,"view_all_btn","View All")
tde4.setWidgetOffsets(req,"view_all_btn",0,300,5,0)
tde4.setWidgetAttachModes(req,"view_all_btn","ATTACH_NONE","ATTACH_WINDOW","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"view_all_btn",80,20)
tde4.addButtonWidget(req,"create_key_btn","Create Key")
tde4.setWidgetOffsets(req,"create_key_btn",0,10,7,0)
tde4.setWidgetAttachModes(req,"create_key_btn","ATTACH_NONE","ATTACH_WIDGET","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"create_key_btn",120,20)
tde4.addButtonWidget(req,"update_viewport_btn","Update Viewport")
tde4.setWidgetOffsets(req,"update_viewport_btn",0,7,7,0)
tde4.setWidgetAttachModes(req,"update_viewport_btn","ATTACH_NONE","ATTACH_WINDOW","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"update_viewport_btn",145,20)
tde4.addScaleWidget(req,"weight_slider_wdgt","Weight","DOUBLE",0.0,1.0,1.0)
tde4.setWidgetOffsets(req,"weight_slider_wdgt",54,60,36,0)
tde4.setWidgetAttachModes(req,"weight_slider_wdgt","ATTACH_WIDGET","ATTACH_WINDOW","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"weight_slider_wdgt",200,20)
tde4.addButtonWidget(req,"weight_key_btn","K")
tde4.setWidgetOffsets(req,"weight_key_btn",5,35,36,0)
tde4.setWidgetAttachModes(req,"weight_key_btn","ATTACH_WIDGET","ATTACH_WINDOW","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"weight_key_btn",30,20)
tde4.addButtonWidget(req,"weight_key_delete_btn","D")
tde4.setWidgetOffsets(req,"weight_key_delete_btn",32,5,36,0)
tde4.setWidgetAttachModes(req,"weight_key_delete_btn","ATTACH_WIDGET","ATTACH_WINDOW","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"weight_key_delete_btn",30,20)
tde4.addScaleWidget(req,"tween_slider_wdgt","Tween","DOUBLE",-1.0,1.0,0.0)
tde4.setWidgetOffsets(req,"tween_slider_wdgt",52,35,64,0)
tde4.setWidgetAttachModes(req,"tween_slider_wdgt","ATTACH_WIDGET","ATTACH_WINDOW","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"tween_slider_wdgt",200,20)
tde4.addButtonWidget(req,"tween_reset_btn","R")
tde4.setWidgetOffsets(req,"tween_reset_btn",7,5,64,0)
tde4.setWidgetAttachModes(req,"tween_reset_btn","ATTACH_WIDGET","ATTACH_WINDOW","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"tween_reset_btn",30,20)
tde4.setWidgetLinks(req,"layers_list_wdgt","","","pgroup_name_wdgt","")
tde4.setWidgetLinks(req,"curve_area_wdgt","","layers_list_wdgt","","")
tde4.setWidgetLinks(req,"pgroup_name_wdgt","curve_area_wdgt","","w006","")
tde4.setWidgetLinks(req,"w006","","","","")
tde4.setWidgetLinks(req,"auto_view_all_toggle_btn","","view_all_btn","curve_area_wdgt","")
tde4.setWidgetLinks(req,"view_all_btn","","","curve_area_wdgt","")
tde4.setWidgetLinks(req,"create_key_btn","","update_viewport_btn","layers_list_wdgt","")
tde4.setWidgetLinks(req,"update_viewport_btn","","","layers_list_wdgt","")
tde4.setWidgetLinks(req,"weight_slider_wdgt","curve_area_wdgt","","layers_list_wdgt","")
tde4.setWidgetLinks(req,"weight_key_btn","weight_slider_wdgt","","layers_list_wdgt","")
tde4.setWidgetLinks(req,"weight_key_delete_btn","weight_slider_wdgt","","layers_list_wdgt","")
tde4.setWidgetLinks(req,"tween_slider_wdgt","curve_area_wdgt","","layers_list_wdgt","")
tde4.setWidgetLinks(req,"tween_reset_btn","tween_slider_wdgt","","layers_list_wdgt","weight_key_delete_btn")


def load_data():
    data_load = json.loads(tde4.getPersistentString(PERSISTENT_STRING_NAME))
    return data_load


def save_data(data_to_save):
    data_save = json.dumps(data_to_save, sort_keys=True)
    tde4.addPersistentString(PERSISTENT_STRING_NAME, data_save)


def insert_pg_editcurve_data(cam_pers_id, pg_pers_id, layer_name, edit_curve, axis):
    data = load_data()
    curve = tde4.getPGroupEditCurveGlobalSpace(pg, cam, edit_curve)
    key_list = tde4.getCurveKeyList(curve, 0)
    for key in key_list:
        pos2d = tde4.getCurveKeyPosition(curve, key)
        data[str(cam_pers_id)][str(pg_pers_id)]["layers"][layer_name][axis].update(
                                                         {int(pos2d[0]): pos2d[1]})
    save_data(data)  


def insert_base_anim_data(cam_pers_id, pg_pers_id):
    data = load_data()
    for count, edit_curve in enumerate(EDIT_CURVES_LIST):
        insert_pg_editcurve_data(cam_pers_id, pg_pers_id, "BaseAnimation",
                                           EDIT_CURVES_LIST[count], AXES[count])


def insert_empty_layer_data(cam_pers_id, pg_pers_id, layer_name):
    data = load_data()
    data[str(cam_pers_id)][str(pg_pers_id)]["layers"].update({layer_name: {"position_x": {}, 
                                                                "position_y": {},
                                                                "position_z": {},
                                                                "rotation_x": {},
                                                                "rotation_y": {},
                                                                "rotation_z": {},
                                                                "weight": {1:1}}})
    save_data(data)

def convert_to_angles(r3d):
    rot	= rot3d(mat3d(r3d)).angles(VL_APPLY_ZXY)
    rx	= (rot[0]*180.0)/3.141592654
    ry	= (rot[1]*180.0)/3.141592654
    rz	= (rot[2]*180.0)/3.141592654
    rx = round(rx, 4)
    ry = round(ry, 4)
    rz = round(rz, 4)
    return[rx,ry,rz]

def insert_pg_bake_data(pg):
    bake_data = {"position": {}, "rotation": {}}
    for frame in range(1, frames+1):
        pos_3d = tde4.getPGroupPosition3D(pg, cam,frame)
        rot_3d = tde4.getPGroupRotation3D(pg,cam,frame)
        rot_3d = convert_to_angles(rot_3d)
        bake_data["position"][frame] = pos_3d
        bake_data["rotation"][frame] = rot_3d
    return bake_data
    

def is_pg_animation_changed(cam_pers_id, pg_pers_id, pg):
    status = False
    data = load_data()
    pos_3d_data = data[str(cam_pers_id)][str(pg_pers_id)]["bake"]["position"]
    rot_3d_data = data[str(cam_pers_id)][str(pg_pers_id)]["bake"]["rotation"]
    for frame in pos_3d_data.keys():
        pos_3d = tde4.getPGroupPosition3D(pg, cam, int(frame))
        rot_3d = tde4.getPGroupRotation3D(pg, cam, int(frame))
        rot_3d = convert_to_angles(rot_3d)
        if (not pos_3d_data[str(frame)] == pos_3d) or (not rot_3d_data[str(frame)] == rot_3d):
            status = True
            break
    return status


def insert_inital_data(cam_pers_id, pg_pers_id, for_cam=False, for_pg=False):
    data = load_data()
    if for_cam == True:
        data.update({str(cam_pers_id): {str(pg_pers_id): {"layers": {},
                                                "bake": insert_pg_bake_data(pg),
                                                "frames_count": frames,
                                                "layers_order": ["BaseAnimation"]}}})
    if for_pg == True:
        data[str(cam_pers_id)].update({str(pg_pers_id): {"layers": {},
                                                "bake": insert_pg_bake_data(pg),
                                                "frames_count": frames,
                                                "layers_order": ["BaseAnimation"]}})       
    save_data(data)
    insert_empty_layer_data(str(cam_pers_id), str(pg_pers_id), "BaseAnimation")
    insert_base_anim_data(cam_pers_id, pg_pers_id)


# Bake post filtered buffer curves
snap_edit_to_filtered_curves()

# Handle persistent string
if tde4.getPersistentString(PERSISTENT_STRING_NAME) == None:
    data = {}
    save_data(data)
    insert_inital_data(cam_pers_id, pg_pers_id, True, False)
else:
    # If cam_pers_id does not exist
    data = load_data()
    if not str(cam_pers_id) in data.keys():
        insert_inital_data(cam_pers_id, pg_pers_id, True, False)

    # If pg_pers_id does not exist
    data = load_data()
    if not str(pg_pers_id) in data[str(cam_pers_id)].keys():
        insert_inital_data(cam_pers_id, pg_pers_id, False, True)

# Create curve set
# Check frames count and bake data before creating curves
data = load_data()
is_frame_count_changed = False
if not int(data[str(cam_pers_id)][str(pg_pers_id)]["frames_count"]) == frames:
    is_frame_count_changed = True

if is_frame_count_changed == False and is_pg_animation_changed(cam_pers_id, pg_pers_id, pg) == False:
    layers_order = data[str(cam_pers_id)][str(pg_pers_id)]["layers_order"]
    for layer_name in layers_order:
        create_curve_set(cam_pers_id, pg_pers_id, layer_name)
else:
    insert_inital_data(cam_pers_id, pg_pers_id, True, False)
    create_curve_set(cam_pers_id, pg_pers_id, "BaseAnimation")


#Callbacks
tde4.setWidgetCallbackFunction(req, "layers_list_wdgt", "layer_item_clicked")
tde4.setWidgetCallbackFunction(req, "view_all_btn", "view_all_btn_clicked")


tde4.postCustomRequesterAndContinue(req,WINDOW_TITLE,1000,700)

