# 3DE4.script.name: 3DE Animation Layers...
# 3DE4.script.version: v1.0
# 3DE4.script.gui: Lineup Controls::Edit
# 3DE4.script.gui: Orientation Controls::Edit
# 3DE4.script.gui.button: Lineup Controls::Anim Layers, align-bottom-left, 80,20
# 3DE4.script.gui.button: Orientation Controls::Anim Layers, align-bottom-left, 70,20
# 3DE4.script.comment: This tool works as Maya Animation Layers.
# 3DE4.script.gui.config_menus: true

# Patcha Saheb(patchasaheb@gmail.com)
# October 07 2021(Montreal)

import os, sys
import json
from vl_sdv import*
import tde4

PREFERENCES_FILE_NAME = "patcha_3de_animation_layers_preferences.json"
WINDOW_TITLE = "Patcha 3DE Animation Layers v1.0"
RENAME_LAYER_WINDOW_TITLE = "Rename Layer"
DELETE_LAYER_WINDOW_TITLE = "Delete Layer"
CREATE_KEY_WINDOW_TITLE = "Create Key"
PREFERENCES_WINDOW_TITLE = "3DE Animation Layers Preferences"
PERSISTENT_STRING_NAME = "PATCHA-3DE-ANIMATION-LAYERS-DATA"
SPACE_MULTIPLIER = 10
CURVE_NAMES = ["Pos X", "Pos Y", "Pos Z", "Rot X", "Rot Y", "Rot Z", "Weight"]
CURVE_COLORS = [(0.812,0.277,0.257),(0.441,0.816,0.354),(0.422,0.408,0.820),
                (0.453,0.815,0.809),(0.855,0.272,0.816),(0.819,0.812,0.387),
                (0.583,0.584,0.144)] 
TIMELINE_KEY_COLOR = [0.0, 1.0, 1.0, 0.3]
EDIT_CURVES_LIST = ["TX_CURVE", "TY_CURVE", "TZ_CURVE",
                    "RX_CURVE", "RY_CURVE", "RZ_CURVE"]
AXES = ["position_x", "position_y", "position_z",
        "rotation_x", "rotation_y", "rotation_z"] 
DEFAULT_LAYER_COLOR = [1.0, 1.0, 0.95]
ACTIVE_LAYER_COLOR = [0.0, 1.0, 0.0]
MUTE_LAYER_COLOR = [1.0, 1.0, 0.0]
NEW_LAYER_NAME = "AnimLayer"
PREFERENCES_WIDGETS = ["pref_wdgt_key_red", "pref_wdgt_key_green", "pref_wdgt_key_blue",
                       "pref_wdgt_key_alpha", "pref_wdgt_show_timeline_keys",
                       "pref_wdgt_auto_key", "pref_wdgt_auto_view_all",
                       "pref_wdgt_collapsed_flag", "pref_wdgt_window_width",
                       "pref_wdgt_window_height"]







def get_cam_pers_id():
    cam = tde4.getCurrentCamera()
    return tde4.getCameraPersistentID(cam)


def get_pg_pers_id():
    pg = tde4.getCurrentPGroup()
    return tde4.getPGroupPersistentID(pg)


def load_data():
    data_load = json.loads(tde4.getPersistentString(PERSISTENT_STRING_NAME))
    return data_load


def save_data(data_to_save):
    data_save = json.dumps(data_to_save, sort_keys=True)
    tde4.addPersistentString(PERSISTENT_STRING_NAME, data_save)


def cursor_update(req):
    cam = tde4.getCurrentCamera()
    frame = tde4.getCurrentFrame(cam)
    tde4.setCurveAreaWidgetCursorPosition(req, "curve_area_wdgt", frame, 1)


def curve_area_callback(req, widget, action):
    if action==3 or action==2:
        f = tde4.getCurveAreaWidgetCursorPosition(req, "curve_area_wdgt")
        n = tde4.getCameraNoFrames(cam)
        if f < 1: f = 1
        if f > n: f = 1
        tde4.setCurrentFrame(cam, int(f))


def snap_edit_to_filtered_curves():
    pg = tde4.getCurrentPGroup()
    cam = tde4.getCurrentCamera()
    frame = tde4.getCurrentFrame(cam)
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


def extract_keys_from_data(curve, axis_data):
    for frame in axis_data.keys():
        x = float(frame)
        y = float(axis_data[frame])
        key = tde4.createCurveKey(curve, [x,y])
        tde4.setCurveKeyMode(curve, key, "LINEAR")
        tde4.setCurveKeyFixedXFlag(curve, key, 1)


def create_curve_set(layer_name): 
    cam_pers_id = get_cam_pers_id()
    pg_pers_id = get_pg_pers_id()    
    data = load_data()
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
    #Create curve keys
    for count, axis in enumerate(AXES):
        axis_data = data[str(cam_pers_id)][str(pg_pers_id)]["layers"][layer_name][axis]
        extract_keys_from_data(curve_ids[count], axis_data)
    # handle weight curve
    axis_data = data[str(cam_pers_id)][str(pg_pers_id)]["layers"][layer_name]["weight"]
    extract_keys_from_data(weight_curve, axis_data)

    # Set layer colors
    active_layer = str(data[str(cam_pers_id)][str(pg_pers_id)]["layers_status"]["active"])
    if active_layer:
        item = get_parent_item_by_label(active_layer)
        if item:
            tde4.setListWidgetItemColor(req, "layers_list_wdgt", item,
                ACTIVE_LAYER_COLOR[0],  ACTIVE_LAYER_COLOR[1],  ACTIVE_LAYER_COLOR[2])


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


def view_all_btn_callback(req, widget, action):
    view_all_helper()


def insert_pg_editcurve_data(layer_name, edit_curve, axis):
    pg = tde4.getCurrentPGroup()
    cam = tde4.getCurrentCamera()
    cam_pers_id = get_cam_pers_id()
    pg_pers_id = get_pg_pers_id()    
    data = load_data()
    curve = tde4.getPGroupEditCurveGlobalSpace(pg, cam, edit_curve)
    key_list = tde4.getCurveKeyList(curve, 0)
    for key in key_list:
        pos2d = tde4.getCurveKeyPosition(curve, key)
        data[str(cam_pers_id)][str(pg_pers_id)]["layers"][layer_name][axis].update(
                                                         {int(pos2d[0]): pos2d[1]})
    save_data(data)  


def insert_base_anim_data():
    for count, edit_curve in enumerate(EDIT_CURVES_LIST):
        insert_pg_editcurve_data("BaseAnimation", EDIT_CURVES_LIST[count], AXES[count])


def insert_empty_layer_data(layer_name):
    cam_pers_id = get_cam_pers_id()
    pg_pers_id = get_pg_pers_id()      
    data = load_data()
    data[str(cam_pers_id)][str(pg_pers_id)]["layers"].update({layer_name: {"position_x": {}, 
                                                                "position_y": {},
                                                                "position_z": {},
                                                                "rotation_x": {},
                                                                "rotation_y": {},
                                                                "rotation_z": {},
                                                                "weight": {1:1}}})
    data[str(cam_pers_id)][str(pg_pers_id)]["layers_order"].append(layer_name)
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


def insert_pg_bake_data():
    pg = tde4.getCurrentPGroup()
    cam = tde4.getCurrentCamera()
    frames = tde4.getCameraNoFrames(cam)
    bake_data = {"position": {}, "rotation": {}}
    for frame in range(1, frames+1):
        pos_3d = tde4.getPGroupPosition3D(pg, cam, frame)
        pos_3d = [round(pos_3d[0], 4), round(pos_3d[1], 4), round(pos_3d[1], 4)]
        rot_3d = tde4.getPGroupRotation3D(pg, cam, frame)
        rot_3d = convert_to_angles(rot_3d)
        bake_data["position"][frame] = pos_3d
        bake_data["rotation"][frame] = rot_3d
    return bake_data
    

def is_pg_animation_changed():
    pg = tde4.getCurrentPGroup()
    cam = tde4.getCurrentCamera()
    cam_pers_id = get_cam_pers_id()
    pg_pers_id = get_pg_pers_id()      
    data = load_data()
    status = False
    pos_3d_data = data[str(cam_pers_id)][str(pg_pers_id)]["bake"]["position"]
    rot_3d_data = data[str(cam_pers_id)][str(pg_pers_id)]["bake"]["rotation"]
    for frame in pos_3d_data.keys():
        pos_3d = tde4.getPGroupPosition3D(pg, cam, int(frame))
        pos_3d = [round(pos_3d[0], 4), round(pos_3d[1], 4), round(pos_3d[1], 4)]
        rot_3d = tde4.getPGroupRotation3D(pg, cam, int(frame))
        rot_3d = convert_to_angles(rot_3d)
        if (not pos_3d_data[str(frame)] == pos_3d) or (not rot_3d_data[str(frame)] == rot_3d):
            status = True
            break
    return status


def insert_inital_data(for_cam=False, for_pg=False):
    cam_pers_id = get_cam_pers_id()
    pg_pers_id = get_pg_pers_id()      
    data = load_data()
    if for_cam == True:
        data.update({str(cam_pers_id): {str(pg_pers_id): {"layers": {},
                                                "bake": insert_pg_bake_data(),
                                                "frames_count": frames,
                                                "layers_order": [],
                                                "layers_status": {"active": None, "muted": []}}}})
    if for_pg == True:
        data[str(cam_pers_id)].update({str(pg_pers_id): {"layers": {},
                                                "bake": insert_pg_bake_data(),
                                                "frames_count": frames,
                                                "layers_order": [],
                                                "layers_status": {"active": None, "muted": []}}})       
    save_data(data)
    insert_empty_layer_data("BaseAnimation")
    insert_base_anim_data()


def get_parent_items(selected=False):
    parent_nodes = []
    if selected == False:
        items = tde4.getListWidgetNoItems(req, "layers_list_wdgt")
        items = range(items)
    else:
        items = tde4.getListWidgetSelectedItems(req, "layers_list_wdgt")
    for item in items:
        if tde4.getListWidgetItemType(req, "layers_list_wdgt", item) == "LIST_ITEM_NODE":
            parent_nodes.append(item)
    return parent_nodes


def get_parent_item_labels(selected=False):
    item_labels = []
    for item in get_parent_items(selected):
        label = tde4.getListWidgetItemLabel(req, "layers_list_wdgt", item)
        item_labels.append(label)
    return item_labels


def get_parent_item_by_label(label):
    for item in get_parent_items(False):
        if tde4.getListWidgetItemLabel(req, "layers_list_wdgt", item) == label:
            item = item
            break
        else:
            item = None            
    return item


def set_layer_colors():
    cam_pers_id = get_cam_pers_id()
    pg_pers_id = get_pg_pers_id()      
    data = load_data()
    # Set default layer color for all parent nodes first
    for parent_item in get_parent_items(False):
        tde4.setListWidgetItemColor(req, "layers_list_wdgt", parent_item,
        DEFAULT_LAYER_COLOR[0], DEFAULT_LAYER_COLOR[1], DEFAULT_LAYER_COLOR[2])
    # Set active layer color
    active_layer = data[str(cam_pers_id)][str(pg_pers_id)]["layers_status"]["active"]
    if active_layer:
        item = get_parent_item_by_label(active_layer)
        tde4.setListWidgetItemColor(req, "layers_list_wdgt", item,
            ACTIVE_LAYER_COLOR[0], ACTIVE_LAYER_COLOR[1], ACTIVE_LAYER_COLOR[2])
    # Set muted layers color
    # TODO


def layer_item_callback(req, widget, action):
    cam_pers_id = get_cam_pers_id()
    pg_pers_id = get_pg_pers_id()      
    sel_items = tde4.getListWidgetSelectedItems(req, "layers_list_wdgt") or []
    # Detach all curves
    tde4.detachCurveAreaWidgetAllCurves(req, "curve_area_wdgt")        
    # Attach Curves
    for item in sel_items:
        item_label = tde4.getListWidgetItemLabel(req, "layers_list_wdgt", item)
        item_color = tde4.getListWidgetItemColor(req, "layers_list_wdgt", item)
        if tde4.getListWidgetItemType(req, "layers_list_wdgt", item) == "LIST_ITEM_ATOM":
            # Disable BaseAnimation curves
            parent_item = tde4.getListWidgetItemParentIndex(req, "layers_list_wdgt", item)
            parent_label = tde4.getListWidgetItemLabel(req, "layers_list_wdgt", parent_item)
            if parent_label == "BaseAnimation":
                edit_status = 0
            else:
                edit_status = 1
            curve = item_label.split("-")[1]
            tde4.attachCurveAreaWidgetCurve(req, "curve_area_wdgt", curve,
                                item_color[0],item_color[1],item_color[2], edit_status)
        # update active layer status data 
        parent = item
        if tde4.getListWidgetItemType(req, "layers_list_wdgt", item) == "LIST_ITEM_ATOM":
            parent = tde4.getListWidgetItemParentIndex(req, "layers_list_wdgt", item)
        # Make sure it is not BaseAnimation layer
        label = tde4.getListWidgetItemLabel(req, "layers_list_wdgt", parent)
        if not "BaseAnimation" in label:
            # Make sure it is not muted layer
            if not tde4.getListWidgetItemColor(req, "layers_list_wdgt", parent) == MUTE_LAYER_COLOR:
                data = load_data()
                data[str(cam_pers_id)][str(pg_pers_id)]["layers_status"]["active"] = label
                save_data(data)
    # Set layer colors
    set_layer_colors()
    # Show timeline keys
    show_timeline_keys_helper()
    # Auto view all
    if tde4.getWidgetValue(req, "main_wdgt_auto_view_all") == 1:
        view_all_helper() 


def get_animlayer_increment_number():
    nums = [0]
    item_labels = get_parent_item_labels(False)
    for label in item_labels:
        if NEW_LAYER_NAME in label:
            label = label.replace(NEW_LAYER_NAME, "")
            if label.isdigit():
                nums.append(int(label))
    return max(nums)+1


def sort_layers_order():
    order = []
    parent_items = get_parent_items(False)
    for parent_item in parent_items:
        parent_label = tde4.getListWidgetItemLabel(req, "layers_list_wdgt",
                                                                    parent_item)
        parent_collapse_flag = tde4.getListWidgetItemCollapsedFlag(req,
                                                "layers_list_wdgt", parent_item)
        d = {parent_label: []}
        for child_item in range(parent_item+1, parent_item+8):
            child_label = tde4.getListWidgetItemLabel(req, "layers_list_wdgt",
                                                                     child_item)
            child_color = tde4.getListWidgetItemColor(req, "layers_list_wdgt",
                                                                     child_item)
            d[parent_label].append((parent_collapse_flag, child_label, child_color))
        order.append(d)
    # Insert last element as first element
    order.insert(0, order.pop(-1))
    # Remove all items
    tde4.removeAllListWidgetItems(req, "layers_list_wdgt")
    # Create new items from stored data
    for i in order:
        for parent_label in i.keys():
            parent = tde4.insertListWidgetItem(req, "layers_list_wdgt",
                                              parent_label, 0, "LIST_ITEM_NODE")
            for item in i[parent_label]:
                parent_collapse_flag = item[0]
                child_label = item[1]
                child_color = item[2]
                tde4.setListWidgetItemCollapsedFlag(req, "layers_list_wdgt", parent,
                                                           parent_collapse_flag)
                child = tde4.insertListWidgetItem(req, "layers_list_wdgt",
                                       child_label, 0, "LIST_ITEM_ATOM", parent)
                tde4.setListWidgetItemColor(req, "layers_list_wdgt", child, 
                                 child_color[0], child_color[1], child_color[2])
    # update layers order data
    update_layers_order_data(get_parent_item_labels(False))
    # Set layer colors(active, muted)               
    set_layer_colors()


def update_layers_order_data(order_list):
    cam_pers_id = get_cam_pers_id()
    pg_pers_id = get_pg_pers_id()    
    data = load_data()
    data[str(cam_pers_id)][str(pg_pers_id)]["layers_order"] = order_list
    save_data(data) 


def update_active_layer_data(old_name, new_name):
    cam_pers_id = get_cam_pers_id()
    pg_pers_id = get_pg_pers_id()    
    data = load_data()
    data[str(cam_pers_id)][str(pg_pers_id)]["layers"][new_name] = (data[str(cam_pers_id)][str(pg_pers_id)]["layers"]).pop(old_name)
    data[str(cam_pers_id)][str(pg_pers_id)]["layers_status"]["active"] = str(new_name)
    save_data(data)


def create_empty_layer_callback(req, widget, action):
    layer_name = NEW_LAYER_NAME + str(get_animlayer_increment_number())
    insert_empty_layer_data(layer_name)
    create_curve_set(layer_name)
    sort_layers_order()


def get_active_layer():
    cam_pers_id = get_cam_pers_id()
    pg_pers_id = get_pg_pers_id()    
    data = load_data()
    return data[str(cam_pers_id)][str(pg_pers_id)]["layers_status"]["active"]  


def rename_layer_callback(req, widget, action):    
    active_layer = get_active_layer()
    if not active_layer:
        tde4.postQuestionRequester(RENAME_LAYER_WINDOW_TITLE,
                              "Warning, No active layer found to rename.", "Ok")
        return
    rename_req = tde4.createCustomRequester()
    tde4.addTextFieldWidget(rename_req, "layer_rename_wdgt", "Name", str(active_layer))
    tde4.setWidgetOffsets(rename_req,"layer_rename_wdgt",60,10,5,0)
    tde4.setWidgetAttachModes(rename_req,"layer_rename_wdgt","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_NONE")
    tde4.setWidgetSize(rename_req,"layer_rename_wdgt",80,20) 
    if tde4.postCustomRequester(rename_req, RENAME_LAYER_WINDOW_TITLE, 600, 100, "Ok", "Cancel") == 1:
        new_name = tde4.getWidgetValue(rename_req,"layer_rename_wdgt")
        if not new_name:
            return
        if new_name in get_parent_item_labels(False):
            tde4.postQuestionRequester(RENAME_LAYER_WINDOW_TITLE,
                                       "Warning, name already exists.", "Ok")
            return
        item = get_parent_item_by_label(active_layer)
        tde4.setListWidgetItemLabel(req, "layers_list_wdgt", item, new_name)
        # Update active layer data
        update_active_layer_data(active_layer, new_name)
        # Update layers order data
        update_layers_order_data(get_parent_item_labels(False)) 


def delete_layers_callback(req, widget, action):
    cam_pers_id = get_cam_pers_id()
    pg_pers_id = get_pg_pers_id()    
    data = load_data()
    sel_labels = get_parent_item_labels(True)
    if not sel_labels:
        tde4.postQuestionRequester(DELETE_LAYER_WINDOW_TITLE,
                                   "Warning, No layers are selected.", "Ok")
        return
    for label in sel_labels:
        item = get_parent_item_by_label(label)
        # BaseAnimation layer can not be deletedSs
        if label == "BaseAnimation":
            tde4.postQuestionRequester(DELETE_LAYER_WINDOW_TITLE,
                       "Warning, BaseAnimation layer can not be deleted.", "Ok")
            return
        tde4.removeListWidgetItem(req, "layers_list_wdgt", item)
        # Update layers data
        del data[str(cam_pers_id)][str(pg_pers_id)]["layers"][str(label)]
        # Update active layer data to None
        data[str(cam_pers_id)][str(pg_pers_id)]["layers_status"]["active"] = None
    # Update layers order
    data[str(cam_pers_id)][str(pg_pers_id)]["layers_order"] = get_parent_item_labels(False)
    save_data(data)


def collapse_or_expand_layers_callback(req, widget, action):
    for item in get_parent_items(False):
        if widget == "collapse_all_menu_btn":
            tde4.setListWidgetItemCollapsedFlag(req, "layers_list_wdgt", item, 1)
        if widget == "expand_all_menu_btn":
            tde4.setListWidgetItemCollapsedFlag(req, "layers_list_wdgt", item, 0)


def get_curves_by_layer_name(layer_name):
    curve_ids = []
    parent_item = get_parent_item_by_label(layer_name)
    for item in range(parent_item+1, parent_item+7):
        label = tde4.getListWidgetItemLabel(req, "layers_list_wdgt", item)
        curve_id = label.split("-")[1]
        curve_ids.append(curve_id)
    return curve_ids


def show_timeline_keys_helper():
    pref_data = read_preferences_file()
    if tde4.getWidgetValue(req, "main_wdgt_show_timeline_keys") == 1:
        cam_pers_id = get_cam_pers_id()
        pg_pers_id = get_pg_pers_id()
        data = load_data()
        active_layer = get_active_layer()
        if not active_layer:
            tde4.deleteAllFrameSliderMarks()
            return
        axis = data[str(cam_pers_id)][str(pg_pers_id)]["layers"][active_layer][AXES[0]] 
        tde4.deleteAllFrameSliderMarks()
        for frame in axis.keys():   
            tde4.addFrameSliderMark(int(frame), int(frame), pref_data["key_red"], 
                                                            pref_data["key_green"],
                                                            pref_data["key_blue"], 
                                                            pref_data["key_alpha"])
    else:
        tde4.deleteAllFrameSliderMarks()


def show_timeline_keys_callback(req, widget, action):
    show_timeline_keys_helper()


def create_key_helper():
    cam = tde4.getCurrentCamera()
    frame   = tde4.getCurrentFrame(cam)
    cam_pers_id = get_cam_pers_id()
    pg_pers_id = get_pg_pers_id()    
    data = load_data()
    active_layer = get_active_layer()
    if not active_layer:
        tde4.postQuestionRequester(CREATE_KEY_WINDOW_TITLE,
                                       "Warning, No active layer found.", "Ok")
        return
    curves = get_curves_by_layer_name(active_layer)
    for count, curve in enumerate(curves):
        y_value = tde4.evaluateCurve(curve, frame)
        key = tde4.createCurveKey(curve,[frame, y_value])
        tde4.setCurveKeyMode(curve, key, "LINEAR")
        tde4.setCurveKeyFixedXFlag(curve, key, 1)
        # Update layers data
        data[str(cam_pers_id)][str(pg_pers_id)]["layers"][str(active_layer)][AXES[count]][str(frame)] = y_value
    save_data(data)
    # Show timeline keys
    show_timeline_keys_helper()


def create_key_callback(req, widget, action):
    create_key_helper()


def pg_option_menu_helper():   
    count = tde4.getWidgetValue(req, "pg_option_menu_wdgt")
    pg_list = tde4.getPGroupList(0)
    tde4.setCurrentPGroup(pg_list[count-1])
    [tde4.setPGroupSelectionFlag(i,0) for i in pg_list]

    pg = tde4.getCurrentPGroup()
    cam = tde4.getCurrentCamera()
    frames = tde4.getCameraNoFrames(cam) 
    tde4.setPGroupSelectionFlag(pg, 1)

    cam_pers_id = get_cam_pers_id()
    pg_pers_id = get_pg_pers_id() 

    tde4.removeAllListWidgetItems(req, "layers_list_wdgt")
    tde4.detachCurveAreaWidgetAllCurves(req, "curve_area_wdgt")

    # Bake post filtered buffer curves
    snap_edit_to_filtered_curves()

    # Handle persistent string
    if tde4.getPersistentString(PERSISTENT_STRING_NAME) == None:
        data = {}
        save_data(data)
        insert_inital_data(True, False)
    else:
        # If cam_pers_id does not exist
        data = load_data()
        if not str(cam_pers_id) in data.keys():
            insert_inital_data(True, False)

        # If pg_pers_id does not exist
        data = load_data()
        if not str(pg_pers_id) in data[str(cam_pers_id)].keys():
            insert_inital_data(False, True)    

    # Create curve set
    # Check frames count and bake data before creating curves
    data = load_data()
    is_frame_count_changed = False
    if not int(data[str(cam_pers_id)][str(pg_pers_id)]["frames_count"]) == frames:
        is_frame_count_changed = True

    if is_frame_count_changed == False and is_pg_animation_changed() == False:
        layers_order = data[str(cam_pers_id)][str(pg_pers_id)]["layers_order"]
        for layer_name in layers_order:
            create_curve_set(layer_name)
    else:
        insert_inital_data(True, False)
        create_curve_set("BaseAnimation")

    # Set layer colors
    set_layer_colors()

    # Show timeline keys
    show_timeline_keys_helper()


def pg_option_menu_callback(req, widget, action):
    pg_option_menu_helper()


def edit_preferences_callback(req, widget, action):
    pref_data = read_preferences_file()
    for key in pref_data.keys():
        value = pref_data[key]        
        tde4.setWidgetValue(pref_req, ("pref_wdgt_" + str(key)), str(value))  
    tde4.postCustomRequesterAndContinue(pref_req, PREFERENCES_WINDOW_TITLE, 500, 400)


def create_inital_data():
    return {"key_red": 0.216, "key_green": 0.624, "key_blue": 0.588,
            "key_alpha": 0.75, "show_timeline_keys": 1, "auto_key": 1,
            "auto_view_all": 1, "collapsed_flag": 1,
            "window_width": 1000, "window_height": 700}


def read_preferences_file():
    with open(json_file_path, "r") as f:
        return json.load(f)


def write_preferences_file(data):
    with open(json_file_path, "w") as f:
        json.dump(data, f, indent=2, sort_keys=True)


def save_preferences():
    data = read_preferences_file()
    for widget in PREFERENCES_WIDGETS:
        value = tde4.getWidgetValue(pref_req, widget)
        key = widget.replace("pref_wdgt_", "")
        data[key] = value
    write_preferences_file(data)


def load_preferences():
    data = read_preferences_file()
    for widget in PREFERENCES_WIDGETS:
        key = widget.replace("pref_wdgt_", "")
        value = data[key]
        try:
            tde4.setWidgetValue(req, ("main_wdgt_"+str(key)), str(value))
        except:
            pass

    show_timeline_keys_helper()
    view_all_helper()

        

def preferences_widgets_callback(req, widget, action):
    save_preferences()
    load_preferences()



# Main GUI
frames = tde4.getCameraNoFrames(tde4.getCurrentCamera())

req = tde4.createCustomRequester()
tde4.addListWidget(req,"layers_list_wdgt","",1)
tde4.setWidgetOffsets(req,"layers_list_wdgt",0,5,50,90)
tde4.setWidgetAttachModes(req,"layers_list_wdgt","ATTACH_NONE","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_WINDOW")
tde4.setWidgetSize(req,"layers_list_wdgt",280,150)
tde4.addCurveAreaWidget(req,"curve_area_wdgt","")
tde4.setWidgetOffsets(req,"curve_area_wdgt",5,5,25,30)
tde4.setWidgetAttachModes(req,"curve_area_wdgt","ATTACH_WINDOW","ATTACH_WIDGET","ATTACH_WINDOW","ATTACH_WINDOW")
tde4.setWidgetSize(req,"curve_area_wdgt",150,150)
tde4.addOptionMenuWidget(req,"pg_option_menu_wdgt","","temp")
tde4.setWidgetOffsets(req,"pg_option_menu_wdgt",5,5,25,0)
tde4.setWidgetAttachModes(req,"pg_option_menu_wdgt","ATTACH_WIDGET","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"pg_option_menu_wdgt",150,20)
tde4.addMenuBarWidget(req,"menu_bar")
tde4.setWidgetOffsets(req,"menu_bar",0,0,0,0)
tde4.setWidgetAttachModes(req,"menu_bar","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"menu_bar",300,20)
tde4.addMenuWidget(req,"layers_menu_wdgt","Layers","menu_bar",0)
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
tde4.addMenuButtonWidget(req,"collapse_all_menu_btn","Collapse All Layers","layers_menu_wdgt")
tde4.setWidgetOffsets(req,"collapse_all_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"collapse_all_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"collapse_all_menu_btn",80,20)
tde4.addMenuButtonWidget(req,"expand_all_menu_btn","Expand All Layers","layers_menu_wdgt")
tde4.setWidgetOffsets(req,"expand_all_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"expand_all_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"expand_all_menu_btn",80,20)
tde4.addMenuWidget(req,"keys_menu","Keys","menu_bar",0)
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
tde4.addMenuToggleWidget(req,"main_wdgt_show_timeline_keys","Show Timeline Keys","keys_menu",1)
tde4.setWidgetOffsets(req,"main_wdgt_show_timeline_keys",0,0,0,0)
tde4.setWidgetAttachModes(req,"main_wdgt_show_timeline_keys","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"main_wdgt_show_timeline_keys",80,20)
tde4.addMenuToggleWidget(req,"main_wdgt_auto_key","Auto Key","keys_menu",1)
tde4.setWidgetOffsets(req,"main_wdgt_auto_key",0,0,0,0)
tde4.setWidgetAttachModes(req,"main_wdgt_auto_key","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"main_wdgt_auto_key",80,20)
tde4.addMenuWidget(req,"objpg_menu","ObjectPG","menu_bar",0)
tde4.setWidgetOffsets(req,"objpg_menu",0,0,0,0)
tde4.setWidgetAttachModes(req,"objpg_menu","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"objpg_menu",80,20)
tde4.addMenuToggleWidget(req,"update_objpg_menu_btn","Update ObjectPG along with Camera","objpg_menu",1)
tde4.setWidgetOffsets(req,"update_objpg_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"update_objpg_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"update_objpg_menu_btn",80,20)
tde4.addMenuWidget(req,"pref_menu","Preferences","menu_bar",0)
tde4.setWidgetOffsets(req,"pref_menu",0,0,0,0)
tde4.setWidgetAttachModes(req,"pref_menu","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"pref_menu",80,20)
tde4.addMenuButtonWidget(req,"edit_pref_menu_btn","Edit Preferences...","pref_menu")
tde4.setWidgetOffsets(req,"edit_pref_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"edit_pref_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"edit_pref_menu_btn",80,20)
tde4.addToggleWidget(req,"main_wdgt_auto_view_all","Auto View All",1)
tde4.setWidgetOffsets(req,"main_wdgt_auto_view_all",0,10,5,0)
tde4.setWidgetAttachModes(req,"main_wdgt_auto_view_all","ATTACH_NONE","ATTACH_WIDGET","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"main_wdgt_auto_view_all",20,20)
tde4.addButtonWidget(req,"view_all_btn","View All")
tde4.setWidgetOffsets(req,"view_all_btn",0,300,5,0)
tde4.setWidgetAttachModes(req,"view_all_btn","ATTACH_NONE","ATTACH_WINDOW","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"view_all_btn",80,20)
tde4.addButtonWidget(req,"update_viewport_btn","Update Viewport")
tde4.setWidgetOffsets(req,"update_viewport_btn",0,160,7,0)
tde4.setWidgetAttachModes(req,"update_viewport_btn","ATTACH_NONE","ATTACH_WINDOW","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"update_viewport_btn",125,20)
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
tde4.addButtonWidget(req,"w083","|<<")
tde4.setWidgetOffsets(req,"w083",11,167,7,0)
tde4.setWidgetAttachModes(req,"w083","ATTACH_WIDGET","ATTACH_NONE","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"w083",33,20)
tde4.addButtonWidget(req,"w084","<")
tde4.setWidgetOffsets(req,"w084",8,167,7,0)
tde4.setWidgetAttachModes(req,"w084","ATTACH_WIDGET","ATTACH_NONE","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"w084",27,20)
tde4.addButtonWidget(req,"w085",">")
tde4.setWidgetOffsets(req,"w085",8,167,7,0)
tde4.setWidgetAttachModes(req,"w085","ATTACH_WIDGET","ATTACH_NONE","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"w085",27,20)
tde4.addButtonWidget(req,"w086",">>|")
tde4.setWidgetOffsets(req,"w086",8,167,7,0)
tde4.setWidgetAttachModes(req,"w086","ATTACH_WIDGET","ATTACH_NONE","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"w086",33,20)
tde4.setWidgetLinks(req,"layers_list_wdgt","","","","")
tde4.setWidgetLinks(req,"curve_area_wdgt","","layers_list_wdgt","","")
tde4.setWidgetLinks(req,"pg_option_menu_wdgt","curve_area_wdgt","","","")
tde4.setWidgetLinks(req,"menu_bar","","","","")
tde4.setWidgetLinks(req,"main_wdgt_auto_view_all","","view_all_btn","curve_area_wdgt","")
tde4.setWidgetLinks(req,"view_all_btn","","","curve_area_wdgt","")
tde4.setWidgetLinks(req,"update_viewport_btn","","","layers_list_wdgt","")
tde4.setWidgetLinks(req,"weight_slider_wdgt","curve_area_wdgt","","layers_list_wdgt","")
tde4.setWidgetLinks(req,"weight_key_btn","weight_slider_wdgt","","layers_list_wdgt","")
tde4.setWidgetLinks(req,"weight_key_delete_btn","weight_slider_wdgt","","layers_list_wdgt","")
tde4.setWidgetLinks(req,"tween_slider_wdgt","curve_area_wdgt","","layers_list_wdgt","")
tde4.setWidgetLinks(req,"tween_reset_btn","tween_slider_wdgt","","layers_list_wdgt","weight_key_delete_btn")
tde4.setWidgetLinks(req,"w083","update_viewport_btn","","layers_list_wdgt","")
tde4.setWidgetLinks(req,"w084","w083","","layers_list_wdgt","")
tde4.setWidgetLinks(req,"w085","w084","","layers_list_wdgt","")
tde4.setWidgetLinks(req,"w086","w085","","layers_list_wdgt","")

cam = tde4.getCurrentCamera()
frame_offset = tde4.getCameraFrameOffset(cam)
tde4.setCurveAreaWidgetXOffset(req, "curve_area_wdgt", frame_offset-1)

# Preferences GUI
pref_req = tde4.createCustomRequester()
tde4.addLabelWidget(pref_req,"pref_wdgt_timeline_keys_color_label","Timeline Keys Color","ALIGN_LABEL_CENTER")
tde4.setWidgetOffsets(pref_req,"pref_wdgt_timeline_keys_color_label",20,80,10,0)
tde4.setWidgetAttachModes(pref_req,"pref_wdgt_timeline_keys_color_label","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(pref_req,"pref_wdgt_timeline_keys_color_label",200,20)
tde4.addScaleWidget(pref_req,"pref_wdgt_key_red","Red","DOUBLE",0.0,1.0,0.216)
tde4.setWidgetOffsets(pref_req,"pref_wdgt_key_red",15,95,10,0)
tde4.setWidgetAttachModes(pref_req,"pref_wdgt_key_red","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(pref_req,"pref_wdgt_key_red",200,20)
tde4.addScaleWidget(pref_req,"pref_wdgt_key_green","Green","DOUBLE",0.0,1.0,0.624)
tde4.setWidgetOffsets(pref_req,"pref_wdgt_key_green",15,95,15,0)
tde4.setWidgetAttachModes(pref_req,"pref_wdgt_key_green","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(pref_req,"pref_wdgt_key_green",200,20)
tde4.addScaleWidget(pref_req,"pref_wdgt_key_blue","Blue","DOUBLE",0.0,1.0,0.588)
tde4.setWidgetOffsets(pref_req,"pref_wdgt_key_blue",15,95,15,0)
tde4.setWidgetAttachModes(pref_req,"pref_wdgt_key_blue","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(pref_req,"pref_wdgt_key_blue",200,20)
tde4.addScaleWidget(pref_req,"pref_wdgt_key_alpha","Alpha","DOUBLE",0.0,1.0,0.75)
tde4.setWidgetOffsets(pref_req,"pref_wdgt_key_alpha",15,95,15,0)
tde4.setWidgetAttachModes(pref_req,"pref_wdgt_key_alpha","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(pref_req,"pref_wdgt_key_alpha",200,20)
tde4.addToggleWidget(pref_req,"pref_wdgt_show_timeline_keys","Show Timeline Keys",1)
tde4.setWidgetOffsets(pref_req,"pref_wdgt_show_timeline_keys",200,0,15,0)
tde4.setWidgetAttachModes(pref_req,"pref_wdgt_show_timeline_keys","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(pref_req,"pref_wdgt_show_timeline_keys",20,20)
tde4.addToggleWidget(pref_req,"pref_wdgt_auto_key","Auto Key",1)
tde4.setWidgetOffsets(pref_req,"pref_wdgt_auto_key",406,90,15,0)
tde4.setWidgetAttachModes(pref_req,"pref_wdgt_auto_key","ATTACH_NONE","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(pref_req,"pref_wdgt_auto_key",20,20)
tde4.addToggleWidget(pref_req,"pref_wdgt_auto_view_all","Auto View All",1)
tde4.setWidgetOffsets(pref_req,"pref_wdgt_auto_view_all",200,0,5,0)
tde4.setWidgetAttachModes(pref_req,"pref_wdgt_auto_view_all","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(pref_req,"pref_wdgt_auto_view_all",20,20)
tde4.addToggleWidget(pref_req,"pref_wdgt_collapsed_flag","New Layer Collapsed Flag",1)
tde4.setWidgetOffsets(pref_req,"pref_wdgt_collapsed_flag",410,90,5,0)
tde4.setWidgetAttachModes(pref_req,"pref_wdgt_collapsed_flag","ATTACH_NONE","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(pref_req,"pref_wdgt_collapsed_flag",20,20)
tde4.addSeparatorWidget(pref_req,"w010")
tde4.setWidgetOffsets(pref_req,"w010",1,99,5,0)
tde4.setWidgetAttachModes(pref_req,"w010","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(pref_req,"w010",200,20)
tde4.addSeparatorWidget(pref_req,"w018")
tde4.setWidgetOffsets(pref_req,"w018",1,99,90,0)
tde4.setWidgetAttachModes(pref_req,"w018","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(pref_req,"w018",200,20)
tde4.addLabelWidget(pref_req,"pref_window_dim_label_wdgt","Window Dimensions","ALIGN_LABEL_CENTER")
tde4.setWidgetOffsets(pref_req,"pref_window_dim_label_wdgt",20,80,5,0)
tde4.setWidgetAttachModes(pref_req,"pref_window_dim_label_wdgt","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(pref_req,"pref_window_dim_label_wdgt",180,20)
tde4.addTextFieldWidget(pref_req,"pref_wdgt_window_width","Width px","1000")
tde4.setWidgetOffsets(pref_req,"pref_wdgt_window_width",17,45,15,0)
tde4.setWidgetAttachModes(pref_req,"pref_wdgt_window_width","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(pref_req,"pref_wdgt_window_width",200,20)
tde4.addTextFieldWidget(pref_req,"pref_wdgt_window_height","Height px","700")
tde4.setWidgetOffsets(pref_req,"pref_wdgt_window_height",103,95,15,0)
tde4.setWidgetAttachModes(pref_req,"pref_wdgt_window_height","ATTACH_WIDGET","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(pref_req,"pref_wdgt_window_height",200,20)
tde4.addSeparatorWidget(pref_req,"w022")
tde4.setWidgetOffsets(pref_req,"w022",1,99,5,0)
tde4.setWidgetAttachModes(pref_req,"w022","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(pref_req,"w022",200,20)
tde4.addButtonWidget(pref_req,"pref_wdgt_reset_btn","Reset Preferences")
tde4.setWidgetOffsets(pref_req,"pref_wdgt_reset_btn",30,70,5,0)
tde4.setWidgetAttachModes(pref_req,"pref_wdgt_reset_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(pref_req,"pref_wdgt_reset_btn",80,20)
tde4.setWidgetLinks(pref_req,"pref_wdgt_timeline_keys_color_label","","","","")
tde4.setWidgetLinks(pref_req,"pref_wdgt_key_red","","","pref_wdgt_timeline_keys_color_label","")
tde4.setWidgetLinks(pref_req,"pref_wdgt_key_green","","","pref_wdgt_key_red","")
tde4.setWidgetLinks(pref_req,"pref_wdgt_key_blue","","","pref_wdgt_key_green","")
tde4.setWidgetLinks(pref_req,"pref_wdgt_key_alpha","","","pref_wdgt_key_blue","")
tde4.setWidgetLinks(pref_req,"pref_wdgt_show_timeline_keys","","","pref_wdgt_key_alpha","")
tde4.setWidgetLinks(pref_req,"pref_wdgt_auto_key","pref_wdgt_show_timeline_keys","","pref_wdgt_key_alpha","")
tde4.setWidgetLinks(pref_req,"pref_wdgt_auto_view_all","","","w010","")
tde4.setWidgetLinks(pref_req,"pref_wdgt_collapsed_flag","pref_wdgt_show_timeline_keys","","w010","")
tde4.setWidgetLinks(pref_req,"w010","","","pref_wdgt_show_timeline_keys","")
tde4.setWidgetLinks(pref_req,"w018","","","pref_wdgt_key_alpha","")
tde4.setWidgetLinks(pref_req,"pref_window_dim_label_wdgt","","","w018","")
tde4.setWidgetLinks(pref_req,"pref_wdgt_window_width","","","pref_window_dim_label_wdgt","")
tde4.setWidgetLinks(pref_req,"pref_wdgt_window_height","pref_wdgt_window_width","","pref_window_dim_label_wdgt","")
tde4.setWidgetLinks(pref_req,"w022","","","pref_wdgt_window_width","")
tde4.setWidgetLinks(pref_req,"pref_wdgt_reset_btn","","","w022","")


# Main requester callbacks
tde4.setWidgetCallbackFunction(req,"curve_area_wdgt", "curve_area_callback")
tde4.setWidgetCallbackFunction(req, "layers_list_wdgt", "layer_item_callback")
tde4.setWidgetCallbackFunction(req, "pg_option_menu_wdgt", "pg_option_menu_callback")
tde4.setWidgetCallbackFunction(req, "view_all_btn", "view_all_btn_callback")
tde4.setWidgetCallbackFunction(req, "create_empty_layer_menu_btn", "create_empty_layer_callback")
tde4.setWidgetCallbackFunction(req, "rename_layer_menu_btn", "rename_layer_callback")
tde4.setWidgetCallbackFunction(req, "del_layers_menu_btn", "delete_layers_callback")
tde4.setWidgetCallbackFunction(req, "collapse_all_menu_btn", "collapse_or_expand_layers_callback")
tde4.setWidgetCallbackFunction(req, "expand_all_menu_btn", "collapse_or_expand_layers_callback")
tde4.setWidgetCallbackFunction(req, "create_key_menu_btn", "create_key_callback")
tde4.setWidgetCallbackFunction(req, "main_wdgt_show_timeline_keys", "show_timeline_keys_callback")

tde4.setWidgetCallbackFunction(req, "edit_pref_menu_btn", "edit_preferences_callback")

# Preferences requester callbacks
for w in PREFERENCES_WIDGETS:
    tde4.setWidgetCallbackFunction(pref_req, str(w), "preferences_widgets_callback")




if frames > 0:
    if ("linux" in sys.platform) or ("darwin" in sys.platform):
        HOME = os.environ["HOME"]
        if not ".3dequalizer" in os.listdir(HOME):
            os.mkdir(HOME+"/.3dequalizer")
    else:
        if "win" in sys.platform:
            HOME = os.environ["APPDATA"]
            if not ".3dequalizer" in os.listdir(HOME):
                os.mkdir(HOME+"\\.3dequalizer")
    tde_path = HOME+"/.3dequalizer/"
    json_file_path = tde_path+PREFERENCES_FILE_NAME
    if not PREFERENCES_FILE_NAME in os.listdir(tde_path):
        with open(json_file_path, "w") as f:
            inital_data = create_inital_data()
            json.dump(inital_data, f, indent=2, sort_keys=True) 

    # Show pgroup names in option menu
    pg_name = tde4.getPGroupName(tde4.getCurrentPGroup())
    cam_name = tde4.getCameraName(tde4.getCurrentCamera())
    pg_names = [tde4.getPGroupName(i)+" | "+cam_name for i in tde4.getPGroupList(0)]
    stringlist = ",".join(['"%s"'%member for member in pg_names])
    eval('tde4.modifyOptionMenuWidget(req, "pg_option_menu_wdgt", " ", %s)'%stringlist)
    pg_option_menu_helper()    
    tde4.postCustomRequesterAndContinue(req, WINDOW_TITLE, 1000, 700, "cursor_update")
    tde4.setCurveAreaWidgetDimensions(req, "curve_area_wdgt", 1.0, frames, -0.2, 1.0)
    tde4.setCurveAreaWidgetFOV(req, "curve_area_wdgt", 1.0, frames, -0.2, 1.0)

    load_preferences()

else:
    tde4.postQuestionRequester(WINDOW_TITLE, "Warning, Frames are not found.", "Ok")
