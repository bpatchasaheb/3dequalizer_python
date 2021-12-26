# 3DE4.script.name: 3DE Animation Layers...
# 3DE4.script.version: v1.0
# 3DE4.script.gui: Lineup Controls::Edit
# 3DE4.script.gui: Orientation Controls::Edit
# 3DE4.script.gui.button: Lineup Controls::Anim Layers, align-bottom-left, 80,20
# 3DE4.script.gui.button: Orientation Controls::Anim Layers, align-bottom-left, 70,20
# 3DE4.script.comment: This tool is similiar to Maya Animation Layers.
# 3DE4.script.gui.config_menus: true

# Patcha Saheb(patchasaheb@gmail.com)
# October 07 2021(Montreal)

import os
import sys
import json
from vl_sdv import*
import tde4

PREFERENCES_FILE_NAME = "patcha_3de_animation_layers_preferences.json"
WINDOW_TITLE = "Patcha 3DE Animation Layers v1.0"
RENAME_LAYER_WINDOW_TITLE = "Rename Layer"
DELETE_LAYER_WINDOW_TITLE = "Delete Layers"
MUTE_LAYER_WINDOW_TITLE = "Mute/Unmute Layers"
MERGE_LAYER_WINDOW_TITLE = "Merge Layers"
CREATE_KEY_WINDOW_TITLE = "Create Key"
DELETE_KEY_WINDOW_TITLE = "Delete Key"
JUMP_KEY_WINDOW_TITLE = "Jump to Key"
WEIGHT_KEY_WINDOW_TITLE = "Weight Key"
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
NEW_ANIM_LAYER_NAME = "AnimLayer"
PREFERENCES_WIDGETS = ["pref_wdgt_key_red", "pref_wdgt_key_green", "pref_wdgt_key_blue",
                       "pref_wdgt_key_alpha", "pref_wdgt_show_timeline_keys",
                       "pref_wdgt_auto_key", "pref_wdgt_auto_view_all",
                       "pref_wdgt_collapsed_flag", "pref_wdgt_window_width",
                       "pref_wdgt_window_height"]


def get_cam_pers_id():  
    """ Get current camera persistent id

    Returns:
        int: camera persistent id
    """      
    cam = tde4.getCurrentCamera()
    return tde4.getCameraPersistentID(cam)


def get_pg_pers_id():
    """ Get current pgroup persistent id

    Returns:
        int: pgroup persistent id
    """    
    pg = tde4.getCurrentPGroup()
    return tde4.getPGroupPersistentID(pg)


def load_data():
    """ Get persistent string from stringDB

    Returns:
        str: a persistent string
    """    
    data_load = json.loads(tde4.getPersistentString(PERSISTENT_STRING_NAME))
    return data_load


def save_data(data_to_save):
    """ Save persistent string to stringDB

    Returns:
        str: a persistent string
    """     
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
    """ Snap Edit curves to Filtered curves """    
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
    """ Create keys on a given curve from data

    Args:
        curve (int): curve type object
        axis_data (dict): a dictionary to extract keys
    """    
    for frame in axis_data.keys():
        x = float(frame)
        y = float(axis_data[frame])
        key = tde4.createCurveKey(curve, [x,y])
        tde4.setCurveKeyMode(curve, key, "LINEAR")
        tde4.setCurveKeyFixedXFlag(curve, key, 1)


def create_curve_set(layer_name): 
    """ Create curves and keys by extracting from data by layer name

    Args:
        layer_name (str): a layer name to create a curve set
    """    
    cam_pers_id = get_cam_pers_id()
    pg_pers_id = get_pg_pers_id()    
    data = load_data()
    pref_data = read_preferences_file()
    pref_collapsed_flag = pref_data["collapsed_flag"]

    # Create curves, insert list widget items
    data_curve_ids = data[str(cam_pers_id)][str(pg_pers_id)]["layers"][layer_name]["curve_ids"]
    if not data_curve_ids:
        curve_ids = [tde4.createCurve() for i in range(7)]
    else:
        # Try to check curves existance except create new curves
        try:
            curve_ids = [data_curve_ids[i] for i in range(7)]
            keys = tde4.getCurveKeyList(curve_ids[0], 0)
        except:
            curve_ids = [tde4.createCurve() for i in range(7)]
    
    # Update layer curve ids data
    data[str(cam_pers_id)][str(pg_pers_id)]["layers"][layer_name]["curve_ids"] = curve_ids
    save_data(data)
    
    # Create curve items
    parent_item = tde4.insertListWidgetItem(req, "layers_list_wdgt", layer_name,
                                            0, "LIST_ITEM_NODE")
    tde4.setListWidgetItemCollapsedFlag(req, "layers_list_wdgt", parent_item,
                                        int(pref_collapsed_flag))

    for count, curve_id in enumerate(curve_ids):
        item_name = CURVE_NAMES[count]+" "*SPACE_MULTIPLIER+"-"+str(curve_id)
        child_item = tde4.insertListWidgetItem(req, "layers_list_wdgt",
                                               item_name, 1, "LIST_ITEM_ATOM",
                                               parent_item)
        tde4.setListWidgetItemColor(req, "layers_list_wdgt", child_item,
                                CURVE_COLORS[count][0], CURVE_COLORS[count][1],
                                CURVE_COLORS[count][2])
    #Create curve keys
    for count, axis in enumerate(AXES):
        axis_data = data[str(cam_pers_id)][str(pg_pers_id)]["layers"][layer_name][axis]
        extract_keys_from_data(curve_ids[count], axis_data)
    # handle weight curve
    weight_curve = curve_ids[-1]
    axis_data = data[str(cam_pers_id)][str(pg_pers_id)]["layers"][layer_name]["weight"]
    extract_keys_from_data(weight_curve, axis_data)

    # Set active layer while UI loading
    active_layer = str(data[str(cam_pers_id)][str(pg_pers_id)]["layers_status"]["active"])
    if active_layer:
        item = get_layer_index_by_name(active_layer)
        if item:
            tde4.setListWidgetItemColor(req, "layers_list_wdgt", item,
                ACTIVE_LAYER_COLOR[0],  ACTIVE_LAYER_COLOR[1],  ACTIVE_LAYER_COLOR[2])


def get_curve_min_max_y_value(curve_list):
    """ Get minimum and maximum y values of given curves

    Args:
        curve_list (list): a list containing curve ids

    Returns:
        list: a list containing minimum and maximum values
    """    
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


def view_all():    
    curve_list = tde4.getCurveAreaWidgetCurveList(req, "curve_area_wdgt")
    frames = tde4.getCameraNoFrames(tde4.getCurrentCamera())   
    dmin = get_curve_min_max_y_value(curve_list)[0]
    dmax = get_curve_min_max_y_value(curve_list)[1]         
    if dmin != None and dmax != None:        
        if dmin == dmax:
            dmax = dmax * 2 
    else:
        dmin = -0.5
        dmax = 0.5
    if dmin == 0: dmin = -0.5
    if dmax == 0: dmax = 0.5
    tde4.setCurveAreaWidgetDimensions(req,"curve_area_wdgt",1.0,
                        frames,dmin-((dmax-dmin)*0.05),dmax+((dmax-dmin)*0.05))
    tde4.setCurveAreaWidgetFOV(req,"curve_area_wdgt",1.0-(frames*0.05),
                frames*1.05,dmin-((dmax-dmin)*0.10),dmax+((dmax-dmin)*0.10))


def view_all_btn_callback(req, widget, action):
    view_all()


def insert_pg_editcurve_data(layer_name, edit_curve, axis):
    """ Insert current pgroup transformation into data by layer name and axis

    Args:
        layer_name (str): a layer name to insert data
        edit_curve (str): edit curve name
        axis (str): an axis name
    """    
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
    """ Insert an empty layer into data

    Args:
        layer_name (str): a layer name
    """    
    cam_pers_id = get_cam_pers_id()
    pg_pers_id = get_pg_pers_id()      
    data = load_data()
    data[str(cam_pers_id)][str(pg_pers_id)]["layers"].update({layer_name: {"position_x": {}, 
                                                                "position_y": {},
                                                                "position_z": {},
                                                                "rotation_x": {},
                                                                "rotation_y": {},
                                                                "rotation_z": {},
                                                                "weight": {1:1},
                                                                "curve_ids": []}})
    data[str(cam_pers_id)][str(pg_pers_id)]["layers_order"].append(layer_name)
    save_data(data)


def convert_to_angles(r3d):
    """ Convert radians to degrees

    Args:
        r3d (list): a matrix3d object
    """    
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
    """ Check if pgroup animation is changed or not

    Returns:
        bool: True if animation is changed
    """    
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
    """ Insert inital data if not exists

    Args:
        for_cam (bool, optional): insert all data. Defaults to False.
        for_pg (bool, optional): insert pgroup data under cam. Defaults to False.
    """    
    cam_pers_id = get_cam_pers_id()
    pg_pers_id = get_pg_pers_id()      
    data = load_data()
    if for_cam == True:
        data.update({str(cam_pers_id): {str(pg_pers_id): {"layers": {},
                                                "bake": insert_pg_bake_data(),
                                                "frames_count": frames,
                                                "layers_order": [],
                                                "layers_status": {"active": None, "mute": []}}}})
    if for_pg == True:
        data[str(cam_pers_id)].update({str(pg_pers_id): {"layers": {},
                                                "bake": insert_pg_bake_data(),
                                                "frames_count": frames,
                                                "layers_order": [],
                                                "layers_status": {"active": None, "mute": []}}})       
    save_data(data)
    insert_empty_layer_data("BaseAnimation")
    insert_base_anim_data()


def get_layer_indices(selected=False):
    """ Get selected or all layer indices

    Args:
        selected (bool, optional): if True get only selected layers. Defaults to False.

    Returns:
        list: a list containing layer(parent item) indices
    """    
    layer_indices = []
    if selected == False:
        items = tde4.getListWidgetNoItems(req, "layers_list_wdgt")
        items = range(items)
    else:
        items = tde4.getListWidgetSelectedItems(req, "layers_list_wdgt")
    for item in items:
        if tde4.getListWidgetItemType(req, "layers_list_wdgt", item) == "LIST_ITEM_NODE":
            layer_indices.append(item)
    return layer_indices


def get_layer_names_from_ui(selected=False):
    """ Get selected or all layer names

    Args:
        selected (bool, optional): if True get only selected layers. Defaults to False.

    Returns:
        list: layer names list
    """    
    layer_names = []
    for item in get_layer_indices(selected):
        label = tde4.getListWidgetItemLabel(req, "layers_list_wdgt", item)
        layer_names.append(label)
    return layer_names


def get_layer_index_by_name(name):
    """ Get a layer(parent item) index by its name(label)

    Args:
        label (str): a layer name(parent item label) 

    Returns:
        int: layer index(parent item index)
    """    
    for item in get_layer_indices(False):
        if tde4.getListWidgetItemLabel(req, "layers_list_wdgt", item) == name:
            item = item
            break
        else:
            item = None            
    return item


def set_layers_status():
    cam_pers_id = get_cam_pers_id()
    pg_pers_id = get_pg_pers_id()      
    data = load_data()
    # Set default layer color for all parent nodes first
    for parent_item in get_layer_indices(False):
        tde4.setListWidgetItemColor(req, "layers_list_wdgt", parent_item,
        DEFAULT_LAYER_COLOR[0], DEFAULT_LAYER_COLOR[1], DEFAULT_LAYER_COLOR[2])
    # Set active layer color
    active_layer = data[str(cam_pers_id)][str(pg_pers_id)]["layers_status"]["active"]
    if active_layer:
        item = get_layer_index_by_name(active_layer)
        tde4.setListWidgetItemColor(req, "layers_list_wdgt", item,
            ACTIVE_LAYER_COLOR[0], ACTIVE_LAYER_COLOR[1], ACTIVE_LAYER_COLOR[2])
    # Set mute layers color
    mute_layers = data[str(cam_pers_id)][str(pg_pers_id)]["layers_status"]["mute"]
    for mute_layer in mute_layers:
        item = get_layer_index_by_name(mute_layer)
        tde4.setListWidgetItemColor(req, "layers_list_wdgt", item,
                MUTE_LAYER_COLOR[0], MUTE_LAYER_COLOR[1], MUTE_LAYER_COLOR[2])        


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
                                            item_color[0], item_color[1],
                                            item_color[2], edit_status)
        # Update active layer status data 
        parent = item
        if tde4.getListWidgetItemType(req, "layers_list_wdgt", item) == "LIST_ITEM_ATOM":
            parent = tde4.getListWidgetItemParentIndex(req, "layers_list_wdgt", item)
        # Make sure it is not BaseAnimation layer
        layer_name = tde4.getListWidgetItemLabel(req, "layers_list_wdgt", parent)
        if not "BaseAnimation" in layer_name:
            # Make sure it is not a mute layer
            if not tde4.getListWidgetItemColor(req, "layers_list_wdgt", parent) == MUTE_LAYER_COLOR:
                data = load_data()
                data[str(cam_pers_id)][str(pg_pers_id)]["layers_status"]["active"] = layer_name
                save_data(data)
    # Set layers status
    set_layers_status()
    # Show timeline keys
    show_timeline_keys()
    # Auto view all
    if tde4.getWidgetValue(req, "main_wdgt_auto_view_all") == 1:
        view_all() 


def get_layer_increment_number(layer_type_name):
    """ Get the increment number of a layer type
    
    Args:
        label (str): layer type name(ex:AnimLayer or MergeLayer)    

    Returns:
        int: a number 
    """    
    nums = [0]
    item_labels = get_layer_names_from_ui(selected=False)
    for label in item_labels:
        if layer_type_name in label:
            label = label.replace(layer_type_name, "")
            if label.isdigit():
                nums.append(int(label))
    return max(nums)+1


def sort_layers_order():
    """
    Sort layers order in UI
    """    
    order = []
    parent_items = get_layer_indices(False)
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
    update_layers_order_data()
    # Set layers status         
    set_layers_status()


def update_layers_order_data():
    """
    Update layers order from UI to data
    """   
    cam_pers_id = get_cam_pers_id()
    pg_pers_id = get_pg_pers_id()    
    data = load_data()
    data[str(cam_pers_id)][str(pg_pers_id)]["layers_order"] = get_layer_names_from_ui(selected=False)
    save_data(data)
    
    
def update_layer_status_data():
    """
    Update layers status from UI to data
    """    
    cam_pers_id = get_cam_pers_id()
    pg_pers_id = get_pg_pers_id()    
    data = load_data()      
    active_layer = get_active_layer_name_from_ui()
    data[str(cam_pers_id)][str(pg_pers_id)]["layers_status"]["active"] = active_layer
    data[str(cam_pers_id)][str(pg_pers_id)]["layers_status"]["mute"] = get_mute_layer_names_from_ui()            
    save_data(data)     


def update_active_layer_data(old_name, new_name):
    """ Swap current layer name with new name and update data

    Args:
        old_name (str): current layer name
        new_name (str): new name 
    """    
    cam_pers_id = get_cam_pers_id()
    pg_pers_id = get_pg_pers_id()    
    data = load_data()
    data[str(cam_pers_id)][str(pg_pers_id)]["layers"][new_name] = (data[str(cam_pers_id)][str(pg_pers_id)]["layers"]).pop(old_name)
    data[str(cam_pers_id)][str(pg_pers_id)]["layers_status"]["active"] = str(new_name)
    save_data(data)


def create_empty_layer_callback(req, widget, action):
    layer_name = NEW_ANIM_LAYER_NAME + str(get_layer_increment_number(NEW_ANIM_LAYER_NAME))
    insert_empty_layer_data(layer_name)
    create_curve_set(layer_name)
    sort_layers_order()


def get_active_layer_name_from_ui():
    """ Get an active layer name

    Returns:
        str: an active layer name
    """    
    items = get_layer_indices(selected=False)
    for item in items:
        if tde4.getListWidgetItemColor(req, "layers_list_wdgt", item) == ACTIVE_LAYER_COLOR:
            return tde4.getListWidgetItemLabel(req, "layers_list_wdgt", item)
            break
        
        
def get_mute_layer_names_from_ui():
    """ Get mute layer names

    Returns:
        list: a list containing mute layer names
    """    
    mute_layers = []
    items = get_layer_indices(selected=False)
    for item in items:
        if tde4.getListWidgetItemColor(req, "layers_list_wdgt", item) == MUTE_LAYER_COLOR:
            layer_name = tde4.getListWidgetItemLabel(req, "layers_list_wdgt", item)
            mute_layers.append(layer_name)
    return mute_layers        


def rename_layer_callback(req, widget, action):   
    layer_names = get_layer_names_from_ui(selected=True)
    if not len(layer_names) == 1:
        tde4.postQuestionRequester(RENAME_LAYER_WINDOW_TITLE,
                                   "Warning, Exactly one layer must be selected.", "Ok")
        return
    if "BaseAnimation" in layer_names:
        tde4.postQuestionRequester(RENAME_LAYER_WINDOW_TITLE,
                                   "Warning, BaseAnimation layer can not be renamed.", "Ok")
        return        
    rename_req = tde4.createCustomRequester()
    tde4.addTextFieldWidget(rename_req, "layer_rename_wdgt", "Name", "")
    tde4.setWidgetOffsets(rename_req,"layer_rename_wdgt",60,10,5,0)
    tde4.setWidgetAttachModes(rename_req,"layer_rename_wdgt","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_NONE")
    tde4.setWidgetSize(rename_req,"layer_rename_wdgt",80,20) 
    if tde4.postCustomRequester(rename_req, RENAME_LAYER_WINDOW_TITLE, 600, 100, "Ok", "Cancel") == 1:
        new_name = tde4.getWidgetValue(rename_req,"layer_rename_wdgt")
        if not new_name:
            return
        if new_name in get_layer_names_from_ui(False):
            tde4.postQuestionRequester(RENAME_LAYER_WINDOW_TITLE,
                                       "Warning, layer name already exists.", "Ok")
            return
        item = get_layer_index_by_name(layer_names[0])
        tde4.setListWidgetItemLabel(req, "layers_list_wdgt", item, new_name)
        # Update active layer data
        update_active_layer_data(layer_names[0], new_name)
        # Update layers order data
        update_layers_order_data()
        # Update layers status data
        update_layer_status_data()
        
        
def delete_layers(layer_names):
    """ Helper function to delete layers

    Args:
        layer_names (list): a list of layer names
    """    
    cam_pers_id = get_cam_pers_id()
    pg_pers_id = get_pg_pers_id()    
    data = load_data()
    for name in layer_names:
        item = get_layer_index_by_name(name)
        # BaseAnimation layer can not be deleted
        if name == "BaseAnimation":
            tde4.postQuestionRequester(DELETE_LAYER_WINDOW_TITLE,
                       "Warning, BaseAnimation layer can not be deleted.", "Ok")
            return
        tde4.removeListWidgetItem(req, "layers_list_wdgt", item)
        # Update layers data
        del data[str(cam_pers_id)][str(pg_pers_id)]["layers"][str(name)]
    # Update layer status data
    update_layer_status_data()
    # Update layers order data
    update_layers_order_data() 


def delete_layers_callback(req, widget, action):
    layer_names = get_layer_names_from_ui(True)
    if not layer_names:
        tde4.postQuestionRequester(DELETE_LAYER_WINDOW_TITLE,
                                   "Warning, No layer(s) are selected.", "Ok")
        return
    delete_layers(layer_names)
    
    
def mute_or_unmute_layers(mute_string):
    """ Mute or unmute selected layers

    Args:
        mute_string (str): string ("mute" or "unmute")
    """    
    cam_pers_id = get_cam_pers_id()
    pg_pers_id = get_pg_pers_id()    
    data = load_data()    
    layer_names = get_layer_names_from_ui(selected=True)
    if not layer_names:
        tde4.postQuestionRequester(MUTE_LAYER_WINDOW_TITLE,
                                   "Warning, No layer(s) are selected.", "Ok")
        return
    
    if "BaseAnimation" in layer_names:
        tde4.postQuestionRequester(MUTE_LAYER_WINDOW_TITLE,
                                "Warning, BaseAnimation layer can not be muted or unmuted..", "Ok")
        return        
    mute_layers = data[str(cam_pers_id)][str(pg_pers_id)]["layers_status"]["mute"]
    for layer_name in layer_names:
        if mute_string == "mute":
            if not layer_name in mute_layers:
                mute_layers.append(layer_name)
        if mute_string == "unmute":
            if layer_name in mute_layers:
                mute_layers.remove(layer_name)                
                
    save_data(data)
    # Set layers status
    set_layers_status()    
    # Update layers status data
    update_layer_status_data()  


def mute_or_unmute_layers_callback(req, widget, action):
    """
    Mute Layers or Unmute Layers menu button callback.
    """   
    if widget == "mute_layers_menu_btn": 
        mute_or_unmute_layers("mute")
    if widget == "unmute_layers_menu_btn": 
        mute_or_unmute_layers("unmute") 
        
        
def merge_layers_callback(req, widget, action):
    cam_pers_id = get_cam_pers_id()
    pg_pers_id = get_pg_pers_id()    
    data = load_data()      
    layer_names = get_layer_names_from_ui(selected=True)
    if not len(layer_names) >= 2:
        tde4.postQuestionRequester(MERGE_LAYER_WINDOW_TITLE,
                                   "Warning, at least two layers must be selected.", "Ok")
        return 
    for layer in layer_names:
        print (data[str(cam_pers_id)][str(pg_pers_id)]["layers"][layer])
        
    
    
    
                   


def collapse_or_expand_layers_callback(req, widget, action):
    for item in get_layer_indices(False):
        if widget == "collapse_all_menu_btn":
            tde4.setListWidgetItemCollapsedFlag(req, "layers_list_wdgt", item, 1)
        if widget == "expand_all_menu_btn":
            tde4.setListWidgetItemCollapsedFlag(req, "layers_list_wdgt", item, 0)
            
            
def get_curves_by_layer_name(layer_name):
    """ Get all curves of a layer

    Args:
        layer_name (str): a layer name to obatain the curves

    Returns:
        list: returns layer curve ids
    """    
    curve_ids = []
    parent_item = get_layer_index_by_name(layer_name)
    for item in range(parent_item+1, parent_item+8):
        label = tde4.getListWidgetItemLabel(req, "layers_list_wdgt", item)
        curve_id = label.split("-")[1]
        curve_ids.append(curve_id)
    return curve_ids


def show_timeline_keys():
    """
    Show or hide timeline keys
    """    
    pref_data = read_preferences_file()
    if tde4.getWidgetValue(req, "main_wdgt_show_timeline_keys") == 1:
        cam_pers_id = get_cam_pers_id()
        pg_pers_id = get_pg_pers_id()
        data = load_data()
        active_layer = get_active_layer_name_from_ui()
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
    show_timeline_keys()


def get_curve_key_at_frame(curve, frame):
    """ Check existance of a curve key

    Args:
        curve (int): curve type object
        frame (int): a frame to check the key

    Returns:
        (int): curve key id if exists
    """    
    status = None
    key_list = tde4.getCurveKeyList(curve, 0)
    for key in key_list:
        pos2d = tde4.getCurveKeyPosition(curve, key)
        if frame == pos2d[0]:
            status = key
            break
    return status

    
def create_or_delete_key(weight_curve=False, create=True, delete=False):
    """ Helper function to create or delete keys

    Args:
        weight_curve (bool): respect weight curve or not. Defaults to False.
        create (bool): create key on active layer. Defaults to True.
        delete (booll): delete key on active layer. Defaults to False.
    """    
    cam = tde4.getCurrentCamera()
    frame = tde4.getCurrentFrame(cam)
    cam_pers_id = get_cam_pers_id()
    pg_pers_id = get_pg_pers_id()    
    data = load_data()
    active_layer = get_active_layer_name_from_ui()
    if not active_layer:
        tde4.postQuestionRequester(CREATE_KEY_WINDOW_TITLE,
                                   "Warning, No active layer found to create key.", "Ok")
        return
    curves = get_curves_by_layer_name(active_layer)
    if weight_curve == False:
        curves.pop()  # Remove weight curve 
    else:
        curves = [curves.pop()]  # Extract weight curve
    for count, curve in enumerate(curves):
        if create == True:
            y_value = tde4.evaluateCurve(curve, frame)
            key = tde4.createCurveKey(curve,[frame, y_value])
            tde4.setCurveKeyMode(curve, key, "LINEAR")
            tde4.setCurveKeyFixedXFlag(curve, key, 1)
            if weight_curve == False:
                # Update layer axes data
                data[str(cam_pers_id)][str(pg_pers_id)]["layers"][str(active_layer)][AXES[count]][str(frame)] = y_value
            else:
                # Update layer weight data
                data[str(cam_pers_id)][str(pg_pers_id)]["layers"][str(active_layer)]["weight"][str(frame)] = y_value
        if delete == True:
            key = get_curve_key_at_frame(curve, frame)            
            if not key:
                tde4.postQuestionRequester(DELETE_KEY_WINDOW_TITLE,
                      "Warning, No key found to delete at current frame.", "Ok")
                return
            tde4.deleteCurveKey(curve, key)
            if weight_curve == False:
                # Update layer axes data
                del data[str(cam_pers_id)][str(pg_pers_id)]["layers"][str(active_layer)][AXES[count]][str(frame)]
            else:
                # Update layer weight data
                del data[str(cam_pers_id)][str(pg_pers_id)]["layers"][str(active_layer)]["weight"][str(frame)]         
    save_data(data)
    # Show timeline keys
    show_timeline_keys()


def create_key_callback(req, widget, action):
    create_or_delete_key(weight_curve=False, create=True, delete=False)


def delete_key_callback(req, widget, action):
    create_or_delete_key(weight_curve=False, create=False, delete=True)


def weight_curve_key_callback(req, widget, action):
    if widget == "weight_key_btn":
        create_or_delete_key(weight_curve=True, create=True, delete=False)
    if widget == "weight_key_delete_btn":
        create_or_delete_key(weight_curve=True, create=False, delete=True)


def get_auto_key_status():
    """get auto key from main UI

    Returns:
        int: auto key status(1 or 0)
    """    
    return int(tde4.getWidgetValue(req, "main_wdgt_auto_key"))
       

def weight_slider_callback(req, widget, action):
    cam = tde4.getCurrentCamera()
    frame = tde4.getCurrentFrame(cam)
    cam_pers_id = get_cam_pers_id()
    pg_pers_id = get_pg_pers_id()    
    data = load_data()
    active_layer = get_active_layer_name_from_ui()
    value = tde4.getWidgetValue(req, "weight_slider_wdgt")
    if active_layer:
        # Respect auto key
        if get_auto_key_status() == 1:
            create_or_delete_key(weight_curve=True, create=True, delete=False)
        # Set curve key y value
        weight_curve = get_curves_by_layer_name(active_layer)[-1]
        key_list = tde4.getCurveKeyList(weight_curve, 0)
        for key in key_list:
            pos2d = tde4.getCurveKeyPosition(weight_curve, key)
            if frame == pos2d[0]:
                tde4.setCurveKeyPosition(weight_curve, key, [frame, float(value)])
                # Update layer weight data
                data[str(cam_pers_id)][str(pg_pers_id)]["layers"][active_layer]["weight"][str(frame)] = value
                save_data(data)
                break 
        if action == 2:
            tde4.setWidgetValue(req, "weight_slider_wdgt", str(1))
            
            
def tween_slider_callback(req, widget, action):
    cam = tde4.getCurrentCamera()
    frame = tde4.getCurrentFrame(cam)
    cam_pers_id = get_cam_pers_id()
    pg_pers_id = get_pg_pers_id()    
    data = load_data()
    active_layer = get_active_layer_name_from_ui()
    tween_value = tde4.getWidgetValue(req, "tween_slider_wdgt")
    if active_layer: 
        curves = get_curves_by_layer_name(active_layer)
        curves.pop()  # Remove weight curve
        for curve in curves:
            # Get previous and next key frames
            prev_key_frame = jump_key("previous")
            next_key_frame = jump_key("next")
            if prev_key_frame and next_key_frame:                
                # Get previous and next key ids
                prev_key = get_curve_key_at_frame(curve, prev_key_frame)
                prev_key_y_value = tde4.getCurveKeyPosition(curve, prev_key)[1]
                next_key = get_curve_key_at_frame(curve, next_key_frame)
                next_key_y_value = tde4.getCurveKeyPosition(curve, next_key)[1]                
                # Create a temp key 
                y_value = tde4.evaluateCurve(curve, frame)
                key = tde4.createCurveKey(curve, [frame, y_value])
                tde4.setCurveKeyMode(curve, key, "LINEAR")
                tde4.setCurveKeyFixedXFlag(curve, key, 1)                
                # Math from Maya tweenMachine
                bias = (tween_value + 1.0) / 2.0
                new_y_value = prev_key_y_value + ((next_key_y_value - prev_key_y_value) * bias)                
                tde4.setCurveKeyPosition(curve, key, [frame, new_y_value])                
                # Call create key helper function to update layer keys data
                create_or_delete_key(weight_curve=False, create=True, delete=False)             
    if action == 2:
        tde4.setWidgetValue(req, "tween_slider_wdgt", str(0))
        


def jump_key(frame_string):
    """ Helper function for jump to keys

    Args:
        frame_string (str): accepts strings "previous" or "next"
    """ 
    return_frame = None 
    cam = tde4.getCurrentCamera()
    frame = tde4.getCurrentFrame(cam)
    cam_pers_id = get_cam_pers_id()
    pg_pers_id = get_pg_pers_id()    
    data = load_data()
    active_layer = get_active_layer_name_from_ui()
    if not active_layer:
        tde4.postQuestionRequester(JUMP_KEY_WINDOW_TITLE,
                                   "Warning, No active layer found.", "Ok")
        return
    curve = get_curves_by_layer_name(active_layer)[0]
    # Extract key frames and sort
    key_frames = data[str(cam_pers_id)][str(pg_pers_id)]["layers"][active_layer][AXES[0]].keys()
    key_frames = [int(key) for key in key_frames]
    key_frames.sort()
    # Find next or previous key frame
    if frame_string == "previous":
        key_frames.reverse()
    for key_frame in key_frames:        
        if frame_string == "next":
            if key_frame > frame:
                return_frame = key_frame
                break
        if frame_string == "previous":
            if key_frame < frame:
                return_frame = key_frame
                break
    return return_frame     


def jump_key_callback(req, widget, action):
    cam = tde4.getCurrentCamera()
    playback_start, playback_end = tde4.getCameraPlaybackRange(cam)
    frames = tde4.getCameraNoFrames(cam)
    cam = tde4.getCurrentCamera()
    if widget == "jump_to_next_key_btn": frame = jump_key("next")
    if widget == "jump_to_prev_key_btn": frame = jump_key("previous")
    if widget == "jump_to_pb_start_btn": frame = playback_start
    if widget == "jump_to_pb_end_btn": frame = playback_end
    if widget == "jump_to_start_btn": frame = 1
    if widget == "jump_to_end_btn": frame = frames      
    if frame:
        tde4.setCurrentFrame(cam, frame)
        cursor_update(req)


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

    # Set layers status
    set_layers_status()

    # Show timeline keys
    show_timeline_keys()


def pg_option_menu_callback(req, widget, action):
    pg_option_menu_helper()


def edit_preferences_helper():
    pref_data = read_preferences_file()
    for key in pref_data.keys():
        value = pref_data[key]        
        tde4.setWidgetValue(pref_req, ("pref_wdgt_" + str(key)), str(value))  


def edit_preferences_callback(req, widget, action):
    edit_preferences_helper()
    tde4.postCustomRequesterAndContinue(pref_req, PREFERENCES_WINDOW_TITLE, 500, 400)


def create_inital_preferences_data():
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


def reset_preferences_callback(req, widget, action):
    pref_data = read_preferences_file()
    pref_data.update(create_inital_preferences_data())
    write_preferences_file(pref_data)
    edit_preferences_helper()
    load_preferences_main_ui()


def save_preferences():
    pref_data = read_preferences_file()
    for widget in PREFERENCES_WIDGETS:
        value = tde4.getWidgetValue(pref_req, widget)
        key = widget.replace("pref_wdgt_", "")
        pref_data[key] = value
    write_preferences_file(pref_data)


def load_preferences_main_ui():
    pref_data = read_preferences_file()
    for widget in PREFERENCES_WIDGETS:
        key = widget.replace("pref_wdgt_", "")
        value = pref_data[key]
        try:
            tde4.setWidgetValue(req, ("main_wdgt_"+str(key)), str(value))
        except:
            pass

    show_timeline_keys()
    view_all()
        

def preferences_widgets_callback(req, widget, action):
    save_preferences()
    load_preferences_main_ui()


# Main GUI
frames = tde4.getCameraNoFrames(tde4.getCurrentCamera())

req = tde4.createCustomRequester()
tde4.addListWidget(req,"layers_list_wdgt","",1)
tde4.setWidgetOffsets(req,"layers_list_wdgt",0,5,5,115)
tde4.setWidgetAttachModes(req,"layers_list_wdgt","ATTACH_NONE","ATTACH_WINDOW","ATTACH_WIDGET","ATTACH_WINDOW")
tde4.setWidgetSize(req,"layers_list_wdgt",290,150)
tde4.addCurveAreaWidget(req,"curve_area_wdgt","")
tde4.setWidgetOffsets(req,"curve_area_wdgt",5,5,25,30)
tde4.setWidgetAttachModes(req,"curve_area_wdgt","ATTACH_WINDOW","ATTACH_WIDGET","ATTACH_WINDOW","ATTACH_WINDOW")
tde4.setWidgetSize(req,"curve_area_wdgt",150,150)
tde4.addOptionMenuWidget(req,"pg_option_menu_wdgt","","temp")
tde4.setWidgetOffsets(req,"pg_option_menu_wdgt",5,5,3,0)
tde4.setWidgetAttachModes(req,"pg_option_menu_wdgt","ATTACH_WIDGET","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"pg_option_menu_wdgt",150,20)
tde4.addMenuBarWidget(req,"menu_bar")
tde4.setWidgetOffsets(req,"menu_bar",0,300,0,0)
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
tde4.addMenuWidget(req,"objpg_menu","ObjectPG","menu_bar",0)
tde4.setWidgetOffsets(req,"objpg_menu",0,0,0,0)
tde4.setWidgetAttachModes(req,"objpg_menu","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"objpg_menu",80,20)
tde4.addMenuToggleWidget(req,"objpg_update_menu_btn","Always consistent with camera","objpg_menu",1)
tde4.setWidgetOffsets(req,"objpg_update_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"objpg_update_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"objpg_update_menu_btn",80,20)
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
tde4.addButtonWidget(req,"create_key_btn","Key")
tde4.setWidgetOffsets(req,"create_key_btn",5,0,7,0)
tde4.setWidgetAttachModes(req,"create_key_btn","ATTACH_WIDGET","ATTACH_NONE","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"create_key_btn",50,20)
tde4.addButtonWidget(req,"update_viewport_btn","Update Viewport")
tde4.setWidgetOffsets(req,"update_viewport_btn",13,0,7,0)
tde4.setWidgetAttachModes(req,"update_viewport_btn","ATTACH_WIDGET","ATTACH_NONE","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"update_viewport_btn",130,20)
tde4.addToggleWidget(req,"main_wdgt_auto_key","Auto Key",1)
tde4.setWidgetOffsets(req,"main_wdgt_auto_key",80,0,7,0)
tde4.setWidgetAttachModes(req,"main_wdgt_auto_key","ATTACH_WIDGET","ATTACH_NONE","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"main_wdgt_auto_key",20,20)
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
tde4.setWidgetOffsets(req,"tween_slider_wdgt",52,5,64,0)
tde4.setWidgetAttachModes(req,"tween_slider_wdgt","ATTACH_WIDGET","ATTACH_WINDOW","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"tween_slider_wdgt",200,20)
tde4.addButtonWidget(req,"jump_to_start_btn","|<<")
tde4.setWidgetOffsets(req,"jump_to_start_btn",13,167,8,0)
tde4.setWidgetAttachModes(req,"jump_to_start_btn","ATTACH_WIDGET","ATTACH_NONE","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"jump_to_start_btn",40,19)
tde4.addButtonWidget(req,"jump_to_prev_key_btn","<")
tde4.setWidgetOffsets(req,"jump_to_prev_key_btn",10,167,8,0)
tde4.setWidgetAttachModes(req,"jump_to_prev_key_btn","ATTACH_WIDGET","ATTACH_NONE","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"jump_to_prev_key_btn",33,19)
tde4.addButtonWidget(req,"jump_to_next_key_btn",">")
tde4.setWidgetOffsets(req,"jump_to_next_key_btn",10,167,8,0)
tde4.setWidgetAttachModes(req,"jump_to_next_key_btn","ATTACH_WIDGET","ATTACH_NONE","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"jump_to_next_key_btn",33,19)
tde4.addButtonWidget(req,"jump_to_end_btn",">>|")
tde4.setWidgetOffsets(req,"jump_to_end_btn",10,11,8,0)
tde4.setWidgetAttachModes(req,"jump_to_end_btn","ATTACH_WIDGET","ATTACH_WINDOW","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"jump_to_end_btn",40,19)
tde4.addButtonWidget(req,"jump_to_pb_start_btn","[<<")
tde4.setWidgetOffsets(req,"jump_to_pb_start_btn",10,167,8,0)
tde4.setWidgetAttachModes(req,"jump_to_pb_start_btn","ATTACH_WIDGET","ATTACH_NONE","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"jump_to_pb_start_btn",40,19)
tde4.addButtonWidget(req,"jump_to_pb_end_btn",">>]")
tde4.setWidgetOffsets(req,"jump_to_pb_end_btn",10,167,8,0)
tde4.setWidgetAttachModes(req,"jump_to_pb_end_btn","ATTACH_WIDGET","ATTACH_NONE","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"jump_to_pb_end_btn",40,19)
tde4.setWidgetLinks(req,"layers_list_wdgt","","","pg_option_menu_wdgt","")
tde4.setWidgetLinks(req,"curve_area_wdgt","","layers_list_wdgt","","")
tde4.setWidgetLinks(req,"pg_option_menu_wdgt","curve_area_wdgt","","","")
tde4.setWidgetLinks(req,"menu_bar","","","","")
tde4.setWidgetLinks(req,"main_wdgt_auto_view_all","","view_all_btn","curve_area_wdgt","")
tde4.setWidgetLinks(req,"view_all_btn","","","curve_area_wdgt","")
tde4.setWidgetLinks(req,"create_key_btn","curve_area_wdgt","","layers_list_wdgt","")
tde4.setWidgetLinks(req,"update_viewport_btn","create_key_btn","","layers_list_wdgt","")
tde4.setWidgetLinks(req,"main_wdgt_auto_key","update_viewport_btn","","layers_list_wdgt","")
tde4.setWidgetLinks(req,"weight_slider_wdgt","curve_area_wdgt","","layers_list_wdgt","")
tde4.setWidgetLinks(req,"weight_key_btn","weight_slider_wdgt","","layers_list_wdgt","")
tde4.setWidgetLinks(req,"weight_key_delete_btn","weight_slider_wdgt","","layers_list_wdgt","")
tde4.setWidgetLinks(req,"tween_slider_wdgt","curve_area_wdgt","","layers_list_wdgt","")
tde4.setWidgetLinks(req,"jump_to_start_btn","curve_area_wdgt","","tween_slider_wdgt","")
tde4.setWidgetLinks(req,"jump_to_prev_key_btn","jump_to_pb_start_btn","","tween_slider_wdgt","")
tde4.setWidgetLinks(req,"jump_to_next_key_btn","jump_to_prev_key_btn","","tween_slider_wdgt","")
tde4.setWidgetLinks(req,"jump_to_end_btn","jump_to_pb_end_btn","","tween_slider_wdgt","")
tde4.setWidgetLinks(req,"jump_to_pb_start_btn","jump_to_start_btn","","tween_slider_wdgt","")
tde4.setWidgetLinks(req,"jump_to_pb_end_btn","jump_to_next_key_btn","","tween_slider_wdgt","")


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
tde4.addToggleWidget(pref_req,"pref_wdgt_collapsed_flag","Layer Collapsed Flag",1)
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
tde4.setWidgetCallbackFunction(req, "mute_layers_menu_btn", "mute_or_unmute_layers_callback")
tde4.setWidgetCallbackFunction(req, "unmute_layers_menu_btn", "mute_or_unmute_layers_callback")
tde4.setWidgetCallbackFunction(req, "merge_layers_menu_btn", "merge_layers_callback")
tde4.setWidgetCallbackFunction(req, "collapse_all_menu_btn", "collapse_or_expand_layers_callback")
tde4.setWidgetCallbackFunction(req, "expand_all_menu_btn", "collapse_or_expand_layers_callback")
tde4.setWidgetCallbackFunction(req, "create_key_menu_btn", "create_key_callback")
tde4.setWidgetCallbackFunction(req, "create_key_btn", "create_key_callback")
tde4.setWidgetCallbackFunction(req, "delete_key_menu_btn", "delete_key_callback")
tde4.setWidgetCallbackFunction(req, "main_wdgt_show_timeline_keys", "show_timeline_keys_callback")
tde4.setWidgetCallbackFunction(req, "weight_key_btn", "weight_curve_key_callback")
tde4.setWidgetCallbackFunction(req, "weight_key_delete_btn", "weight_curve_key_callback")
tde4.setWidgetCallbackFunction(req, "weight_slider_wdgt", "weight_slider_callback")
tde4.setWidgetCallbackFunction(req, "tween_slider_wdgt", "tween_slider_callback")
tde4.setWidgetCallbackFunction(req, "jump_to_next_key_btn", "jump_key_callback")
tde4.setWidgetCallbackFunction(req, "jump_to_prev_key_btn", "jump_key_callback")
tde4.setWidgetCallbackFunction(req, "jump_to_pb_start_btn", "jump_key_callback")
tde4.setWidgetCallbackFunction(req, "jump_to_pb_end_btn", "jump_key_callback")
tde4.setWidgetCallbackFunction(req, "jump_to_start_btn", "jump_key_callback")
tde4.setWidgetCallbackFunction(req, "jump_to_end_btn", "jump_key_callback")

tde4.setWidgetCallbackFunction(req, "edit_pref_menu_btn", "edit_preferences_callback")

# Preferences requester callbacks
for w in PREFERENCES_WIDGETS:
    tde4.setWidgetCallbackFunction(pref_req, str(w), "preferences_widgets_callback")
tde4.setWidgetCallbackFunction(pref_req, "pref_wdgt_reset_btn", "reset_preferences_callback")
    




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
            inital_data = create_inital_preferences_data()
            json.dump(inital_data, f, indent=2, sort_keys=True) 

    # Show pgroup names in option menu
    pg_name = tde4.getPGroupName(tde4.getCurrentPGroup())
    cam_name = tde4.getCameraName(tde4.getCurrentCamera())
    pg_names = [tde4.getPGroupName(i)+" | "+cam_name for i in tde4.getPGroupList(0)]
    stringlist = ",".join(['"%s"'%member for member in pg_names])
    eval('tde4.modifyOptionMenuWidget(req, "pg_option_menu_wdgt", " ", %s)'%stringlist)
    pg_option_menu_helper()
    pref_data = read_preferences_file()
    width, height = int(pref_data["window_width"]), int(pref_data["window_height"])    
    tde4.postCustomRequesterAndContinue(req, WINDOW_TITLE, width, height, "cursor_update")
    tde4.setCurveAreaWidgetDimensions(req, "curve_area_wdgt", 1.0, frames, -0.2, 1.0)
    tde4.setCurveAreaWidgetFOV(req, "curve_area_wdgt", 1.0, frames, -0.2, 1.0)

    load_preferences_main_ui()

else:
    tde4.postQuestionRequester(WINDOW_TITLE, "Warning, Frames are not found.", "Ok")
