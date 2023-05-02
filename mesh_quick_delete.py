"""
Copyright (C) 2023 Gixo

# ***** BEGIN GPL LICENSE BLOCK *****
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

# ***** END GPL LICENSE BLOCK *****
"""

import bpy

from bpy.types import (
    AddonPreferences,
    Operator,
)

from bpy.props import (
    BoolProperty,
)


bl_info = {
    "name": "Quick Mesh Delete",
    "author": "Gixo <notgixo@proton.me>",
    "description": "Quickly delete mesh components based on select mesh mode instead of using deletion pop-up menu.",
    "blender": (3, 0, 0),
    "version": (1, 0, 0),
    "location": 'In Edit Mode > "X" or "Del" (Replaces default delete shortcut to "Shift" + "X" or "Shift" + "Del")',
    "warning": "",
    "support": "COMMUNITY",
    "category": "Mesh",
}


def _quick_delete(context):
    mode = context.mode
    if mode == "EDIT_MESH":
        # Delete selected component based on mesh select mode
        select_mode = context.tool_settings.mesh_select_mode[:]
        del_types = ["VERT", "EDGE", "FACE"]
        active_select_mode = select_mode.index(True)
        del_type = del_types[active_select_mode]

        bpy.ops.mesh.delete(type=del_type)


def _assign_shortcuts(shift):
    wm = bpy.context.window_manager
    mesh_keymaps = wm.keyconfigs.user.keymaps["Mesh"].keymap_items
    # Changes Blender's default shortcuts
    for keymap in mesh_keymaps:
        if keymap.name == "Delete":
            keymap.shift = 0 if shift else 1
    # Replace Blender's default delete with quick delete
    mesh_keymaps.new(
        "qmd.quick_delete",
        type="X",
        value="PRESS",
        shift=shift
    )
    mesh_keymaps.new(
        "qmd.quick_delete",
        type="DEL",
        value="PRESS",
        shift=shift
    )


def _revert_shortcuts():
    wm = bpy.context.window_manager
    mesh_keymaps = wm.keyconfigs.user.keymaps["Mesh"].keymap_items
    # Deletes created shortcut for quick delete
    for keymap in mesh_keymaps:
        if keymap.idname == "qmd.quick_delete":
            mesh_keymaps.remove(keymap)

    # Changes Blender's delete shortcut to its default state
    for keymap in mesh_keymaps:
        if keymap.name == "Delete":
            keymap.shift = 0


def _shortcut_update(self, context):
    pref = bpy.context.preferences.addons["mesh_quick_delete"].preferences
    shift = pref.shift_shortcut
    _assign_shortcuts(shift)


class QMD_OT_quick_delete(Operator):
    """Delete mesh components based on selection mode"""
    bl_label = "Quick Delete"
    bl_idname = "qmd.quick_delete"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        _quick_delete(context)

        return {"FINISHED"}


class QMDPreferences(AddonPreferences):
    """Add-on's preferences"""
    bl_idname = "mesh_quick_delete"

    shift_shortcut: BoolProperty(
        name='Use "Shift" + "X" for Quick Delete',
        default=True,
        update=_shortcut_update,
    )

    def draw(self, context):
        layout = self.layout
        # ----------------------------------
        box = layout.box()
        col = box.column()
        col.label(text="Shortcuts:")
        col.prop(self, "shift_shortcut")
        # ----------------------------------


# -----------------------------------------------------
# Registration
# ------------------------------------------------------
classes = (
    QMDPreferences,
    QMD_OT_quick_delete,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    _assign_shortcuts(True)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    _revert_shortcuts()
