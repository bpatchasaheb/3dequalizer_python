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

pg = tde4.getCurrentPGroup()
pg_persistent_id = tde4.getPGroupPersistentID(pg)
cam = tde4.getCurrentCamera()

def create_curve_set(layer_name): 
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
    return curve_ids


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
        if len(key_list) > 1:
            for key in key_list:
                pos2d = tde4.getCurveKeyPosition(curve, key)
                key_data.append(pos2d[1])
    if len(key_data) >= 1:
        min_max_values = [min(key_data), max(key_data)]




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
tde4.setWidgetOffsets(req,"layers_list_wdgt",0,5,5,60)
tde4.setWidgetAttachModes(req,"layers_list_wdgt","ATTACH_NONE","ATTACH_WINDOW","ATTACH_WIDGET","ATTACH_WINDOW")
tde4.setWidgetSize(req,"layers_list_wdgt",280,150)
tde4.addCurveAreaWidget(req,"curve_area_wdgt","")
tde4.setWidgetOffsets(req,"curve_area_wdgt",5,5,25,30)
tde4.setWidgetAttachModes(req,"curve_area_wdgt","ATTACH_WINDOW","ATTACH_WIDGET","ATTACH_WINDOW","ATTACH_WINDOW")
tde4.setWidgetSize(req,"curve_area_wdgt",150,150)
tde4.addTextFieldWidget(req,"pgroup_name_wdgt","PGroup","")
tde4.setWidgetOffsets(req,"pgroup_name_wdgt",65,5,25,0)
tde4.setWidgetAttachModes(req,"pgroup_name_wdgt","ATTACH_WIDGET","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"pgroup_name_wdgt",200,20)
tde4.setWidgetSensitiveFlag(req,"pgroup_name_wdgt",0)
tde4.addMenuBarWidget(req,"w006")
tde4.setWidgetOffsets(req,"w006",0,0,0,0)
tde4.setWidgetAttachModes(req,"w006","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"w006",300,20)
tde4.addMenuWidget(req,"edit_menu_wdgt","Edit","w006",0)
tde4.setWidgetOffsets(req,"edit_menu_wdgt",0,0,0,0)
tde4.setWidgetAttachModes(req,"edit_menu_wdgt","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"edit_menu_wdgt",80,20)
tde4.addMenuButtonWidget(req,"del_cvs_menu_btn","Delete CVs","edit_menu_wdgt")
tde4.setWidgetOffsets(req,"del_cvs_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"del_cvs_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"del_cvs_menu_btn",80,20)
tde4.addMenuSeparatorWidget(req,"w024","edit_menu_wdgt")
tde4.setWidgetOffsets(req,"w024",0,0,0,0)
tde4.setWidgetAttachModes(req,"w024","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"w024",80,20)
tde4.addMenuWidget(req,"set_cvs_to_menu_wdgt","Set CVs To","edit_menu_wdgt",0)
tde4.setWidgetOffsets(req,"set_cvs_to_menu_wdgt",0,0,0,0)
tde4.setWidgetAttachModes(req,"set_cvs_to_menu_wdgt","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"set_cvs_to_menu_wdgt",80,20)
tde4.addMenuButtonWidget(req,"keys_linear_menu_btn","Linear","set_cvs_to_menu_wdgt")
tde4.setWidgetOffsets(req,"keys_linear_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"keys_linear_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"keys_linear_menu_btn",80,20)
tde4.addMenuButtonWidget(req,"keys_smooth_menu_btn","Smooth","set_cvs_to_menu_wdgt")
tde4.setWidgetOffsets(req,"keys_smooth_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"keys_smooth_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"keys_smooth_menu_btn",80,20)
tde4.addMenuButtonWidget(req,"keys_broken_menu_btn","Broken","set_cvs_to_menu_wdgt")
tde4.setWidgetOffsets(req,"keys_broken_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"keys_broken_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"keys_broken_menu_btn",80,20)
tde4.addMenuButtonWidget(req,"flatten_tangent_menu_btn","Flatten Tangents","edit_menu_wdgt")
tde4.setWidgetOffsets(req,"flatten_tangent_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"flatten_tangent_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"flatten_tangent_menu_btn",80,20)
tde4.addMenuButtonWidget(req,"fix_cvs_vert_menu_btn","Fix CVs Vertically","edit_menu_wdgt")
tde4.setWidgetOffsets(req,"fix_cvs_vert_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"fix_cvs_vert_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"fix_cvs_vert_menu_btn",80,20)
tde4.addMenuButtonWidget(req,"unfix_cvs_vert_menu_btn","Unfix CVs Vertically","edit_menu_wdgt")
tde4.setWidgetOffsets(req,"unfix_cvs_vert_menu_btn",0,0,0,0)
tde4.setWidgetAttachModes(req,"unfix_cvs_vert_menu_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"unfix_cvs_vert_menu_btn",80,20)
tde4.addMenuSeparatorWidget(req,"w035","edit_menu_wdgt")
tde4.setWidgetOffsets(req,"w035",0,0,0,0)
tde4.setWidgetAttachModes(req,"w035","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"w035",80,20)
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
tde4.setWidgetOffsets(req,"weight_slider_wdgt",54,30,35,0)
tde4.setWidgetAttachModes(req,"weight_slider_wdgt","ATTACH_WIDGET","ATTACH_WINDOW","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"weight_slider_wdgt",200,20)
tde4.addButtonWidget(req,"weight_key_btn","K")
tde4.setWidgetOffsets(req,"weight_key_btn",5,5,35,0)
tde4.setWidgetAttachModes(req,"weight_key_btn","ATTACH_WIDGET","ATTACH_WINDOW","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"weight_key_btn",30,20)
tde4.setWidgetLinks(req,"layers_list_wdgt","","","pgroup_name_wdgt","")
tde4.setWidgetLinks(req,"curve_area_wdgt","","layers_list_wdgt","","")
tde4.setWidgetLinks(req,"pgroup_name_wdgt","curve_area_wdgt","","w006","")
tde4.setWidgetLinks(req,"w006","","","","")
tde4.setWidgetLinks(req,"view_all_btn","","","curve_area_wdgt","")
tde4.setWidgetLinks(req,"create_key_btn","","update_viewport_btn","layers_list_wdgt","")
tde4.setWidgetLinks(req,"update_viewport_btn","","","layers_list_wdgt","")
tde4.setWidgetLinks(req,"weight_slider_wdgt","curve_area_wdgt","","layers_list_wdgt","")
tde4.setWidgetLinks(req,"weight_key_btn","weight_slider_wdgt","","layers_list_wdgt","")

create_curve_set("masterLayer")
create_curve_set("animLayer1")

if tde4.getPersistentString(PERSISTENT_STRING_NAME) == None:
    data = { 1 : {"layer_name" : "masterLayer",
                      "layer_index" : 0,
                      "position_x" : {},
                      "position_y" : {},
                      "position_z" : {},
                      "rotation_x" : {},
                      "rotation_y" : {},
                      "rotation_z" : {},
                      "weight" : {},
                     }
            }
    data = json.dumps(data, indent=2, sort_keys=True)
    tde4.addPersistentString(PERSISTENT_STRING_NAME, data)


    # create curve set

    # write_curve_keys

    #



#Callbacks
tde4.setWidgetCallbackFunction(req, "layers_list_wdgt", "layer_item_clicked")
tde4.setWidgetCallbackFunction(req, "view_all_btn", "view_all_btn_clicked")


tde4.postCustomRequesterAndContinue(req,WINDOW_TITLE,1000,700)

