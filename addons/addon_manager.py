bl_info = {
    "name": "Add-on Manager",
    "author": "gogo",
    "version": (0, 0, 1),
    "blender": (2, 82, 0),
    "description": "Add-on to manage Add-ons.",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "https://github.com/3str6/addon_manager",
    "category": "Development"
}

import bpy
from bpy.types import (
    Panel,
)
from bpy.props import (
    FloatProperty,
    BoolProperty,
    EnumProperty,
    PointerProperty,
)
from rna_prop_ui import PropertyPanel
import os


class WorkSpaceButtonsPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"


class ADDON_PT_addon_manager(WorkSpaceButtonsPanel, Panel):
    bl_label = "Add-on Manager"
    bl_options = {'DEFAULT_CLOSED'}
    bl_idname = "ADDON_PT_addon_manager"

    def draw(self, context):
        layout = self.layout
        propGrp = context.scene.myaddon
        layout.row().prop(propGrp, "ePathTab", expand=True)
        layout.prop(propGrp, property="bEnabledOnly", text="Enabled Add-ons Only")

        # align just to pack more tightly
        col = layout.box().column(align=True)
        prefs = context.preferences

        import addon_utils
        addon_map = {mod.__name__: mod for mod in addon_utils.modules()}

        addon_path = ""

        if propGrp.ePathTab == 'USER':
            addon_path = bpy.utils.script_path_user() + "\\addons"
        elif propGrp.ePathTab == 'PREF':
            if bpy.utils.script_path_pref() is not None:
                ddon_path = bpy.utils.script_path_pref() + "\\addons"
        else:
            addon_path = bpy.utils.script_paths(user_pref=False, use_user=False)[1] + "\\addons"
       
        if os.path.exists(addon_path):
            for addon, addon_path in bpy.path.module_names(addon_path):
                module_name = addon
                module = addon_map.get(module_name)
                if (module is None):
                    continue
                
                is_enabled = module_name in (ad.module for ad in prefs.addons)
                if propGrp.bEnabledOnly:
                    if is_enabled is False:
                        continue

                info = addon_utils.module_bl_info(module)
                row = col.row()
                row.alignment = 'LEFT'
                row.operator(
                    "preferences.addon_disable" if is_enabled else "preferences.addon_enable",
                    icon='CHECKBOX_HLT' if is_enabled else 'CHECKBOX_DEHLT',
                    text="%s: %s" % (info["category"], info["name"]),
                    emboss=False,
                ).module = module_name
            

class ADDON_PT_custom_props(bpy.types.PropertyGroup):
    bl_parent_id = "WORKSPACE_PT_main"

    bEnabledOnly: BoolProperty(
        name="ShowEnabledOnly",
        description="Show Enabled Add-ons only",
        default=False,
    )
    ePathTab: EnumProperty(
        name="Add-on Path",
        description="test tab",
        items=(
            ('USER', 'User', 'User Tab'),
            ('PREF', 'Prefs', 'Custom Tab'),
            ('LOCAL', 'Local', 'Local Tab'),
        ),
    )


classes = (
    ADDON_PT_addon_manager,
    ADDON_PT_custom_props
)


def register():
    for i in classes:
        bpy.utils.register_class(i)
    
    bpy.types.Scene.myaddon = PointerProperty(type=ADDON_PT_custom_props)


def unregister():
    del bpy.types.Scene.myaddon
    for i in classes:
        bpy.utils.unregister_class(i)


if __name__ == "__main__":
    register()
