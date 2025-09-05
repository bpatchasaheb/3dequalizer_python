# 3DE4.script.name: 3DE Animation Layers...
# 3DE4.script.version: v1.1
# 3DE4.script.gui: Lineup Controls::Edit
# 3DE4.script.gui: Orientation Controls::Edit
# 3DE4.script.gui.button: Lineup Controls::Anim Layers, align-bottom-left, 80,20
# 3DE4.script.gui.button: Orientation Controls::Anim Layers, align-bottom-left, 70,20
# 3DE4.script.comment: This tool is similiar to Maya Animation Layers.
# 3DE4.script.gui.config_menus: true

# Patcha Saheb(patchasaheb@gmail.com)
# September 5 2025(Montreal)

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








# Main GUI
frames = tde4.getCameraNoFrames(tde4.getCurrentCamera())

req = tde4.createCustomRequester()

tde4.addListWidget(req,"layers_list_wdgt","",1)
tde4.setWidgetOffsets(req,"layers_list_wdgt",0,5,28,68)
tde4.setWidgetAttachModes(req,"layers_list_wdgt","ATTACH_NONE","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_WINDOW")
tde4.setWidgetSize(req,"layers_list_wdgt",290,150)
tde4.addCurveAreaWidget(req,"curve_area_wdgt","")
tde4.setWidgetOffsets(req,"curve_area_wdgt",5,5,25,40)
tde4.setWidgetAttachModes(req,"curve_area_wdgt","ATTACH_WINDOW","ATTACH_WIDGET","ATTACH_WINDOW","ATTACH_WINDOW")
tde4.setWidgetSize(req,"curve_area_wdgt",150,150)
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
tde4.addButtonWidget(req,"view_all_btn","View All")
tde4.setWidgetOffsets(req,"view_all_btn",0,300,10,0)
tde4.setWidgetAttachModes(req,"view_all_btn","ATTACH_NONE","ATTACH_WINDOW","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"view_all_btn",80,20)
tde4.addToggleWidget(req,"main_wdgt_auto_key","Auto Key",1)
tde4.setWidgetOffsets(req,"main_wdgt_auto_key",84,0,9,0)
tde4.setWidgetAttachModes(req,"main_wdgt_auto_key","ATTACH_WIDGET","ATTACH_NONE","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"main_wdgt_auto_key",20,20)
tde4.addScaleWidget(req,"tween_slider_wdgt","Tween","DOUBLE",-1.0,1.0,0.0)
tde4.setWidgetOffsets(req,"tween_slider_wdgt",52,5,10,0)
tde4.setWidgetAttachModes(req,"tween_slider_wdgt","ATTACH_WIDGET","ATTACH_WINDOW","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"tween_slider_wdgt",200,20)
tde4.addButtonWidget(req,"jump_to_prev_key_btn","|<")
tde4.setWidgetOffsets(req,"jump_to_prev_key_btn",10,167,8,0)
tde4.setWidgetAttachModes(req,"jump_to_prev_key_btn","ATTACH_WIDGET","ATTACH_NONE","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"jump_to_prev_key_btn",33,19)
tde4.addButtonWidget(req,"jump_to_next_key_btn",">|")
tde4.setWidgetOffsets(req,"jump_to_next_key_btn",10,167,8,0)
tde4.setWidgetAttachModes(req,"jump_to_next_key_btn","ATTACH_WIDGET","ATTACH_NONE","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"jump_to_next_key_btn",33,19)
tde4.addButtonWidget(req,"jump_to_pb_start_btn","[<<")
tde4.setWidgetOffsets(req,"jump_to_pb_start_btn",13,167,8,0)
tde4.setWidgetAttachModes(req,"jump_to_pb_start_btn","ATTACH_WIDGET","ATTACH_NONE","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"jump_to_pb_start_btn",40,19)
tde4.addButtonWidget(req,"jump_to_pb_end_btn",">>]")
tde4.setWidgetOffsets(req,"jump_to_pb_end_btn",10,167,8,0)
tde4.setWidgetAttachModes(req,"jump_to_pb_end_btn","ATTACH_WIDGET","ATTACH_NONE","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"jump_to_pb_end_btn",40,19)
tde4.addButtonWidget(req,"create_key_btn","Create Key")
tde4.setWidgetOffsets(req,"create_key_btn",10,0,10,0)
tde4.setWidgetAttachModes(req,"create_key_btn","ATTACH_WINDOW","ATTACH_NONE","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"create_key_btn",120,20)
tde4.addButtonWidget(req,"update_viewport_btn","Update Viewport")
tde4.setWidgetOffsets(req,"update_viewport_btn",10,0,10,0)
tde4.setWidgetAttachModes(req,"update_viewport_btn","ATTACH_WIDGET","ATTACH_NONE","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"update_viewport_btn",150,20)
tde4.addButtonWidget(req,"delete_key_btn","Delete Key")
tde4.setWidgetOffsets(req,"delete_key_btn",10,0,10,0)
tde4.setWidgetAttachModes(req,"delete_key_btn","ATTACH_WIDGET","ATTACH_NONE","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"delete_key_btn",120,20)
tde4.addTextFieldWidget(req,"pg_name_text_wdgt","","")
tde4.setWidgetOffsets(req,"pg_name_text_wdgt",5,5,3,0)
tde4.setWidgetAttachModes(req,"pg_name_text_wdgt","ATTACH_WIDGET","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"pg_name_text_wdgt",200,20)
tde4.setWidgetSensitiveFlag(req,"pg_name_text_wdgt",0)
tde4.setWidgetLinks(req,"layers_list_wdgt","","","","")
tde4.setWidgetLinks(req,"curve_area_wdgt","","layers_list_wdgt","","")
tde4.setWidgetLinks(req,"menu_bar","","","","")
tde4.setWidgetLinks(req,"view_all_btn","","","curve_area_wdgt","")
tde4.setWidgetLinks(req,"main_wdgt_auto_key","jump_to_pb_end_btn","","tween_slider_wdgt","")
tde4.setWidgetLinks(req,"tween_slider_wdgt","curve_area_wdgt","","layers_list_wdgt","")
tde4.setWidgetLinks(req,"jump_to_prev_key_btn","jump_to_pb_start_btn","","tween_slider_wdgt","")
tde4.setWidgetLinks(req,"jump_to_next_key_btn","jump_to_prev_key_btn","","tween_slider_wdgt","")
tde4.setWidgetLinks(req,"jump_to_pb_start_btn","curve_area_wdgt","","tween_slider_wdgt","")
tde4.setWidgetLinks(req,"jump_to_pb_end_btn","jump_to_next_key_btn","","tween_slider_wdgt","")
tde4.setWidgetLinks(req,"create_key_btn","","","curve_area_wdgt","")
tde4.setWidgetLinks(req,"update_viewport_btn","create_key_btn","","curve_area_wdgt","")
tde4.setWidgetLinks(req,"delete_key_btn","update_viewport_btn","","curve_area_wdgt","")
tde4.setWidgetLinks(req,"pg_name_text_wdgt","menu_bar","","","")


cam = tde4.getCurrentCamera()
frame_offset = tde4.getCameraFrameOffset(cam)
tde4.setCurveAreaWidgetXOffset(req, "curve_area_wdgt", frame_offset-1)

# Preferences GUI



tde4.postCustomRequesterAndContinue(req, WINDOW_TITLE, 1000, 800)

