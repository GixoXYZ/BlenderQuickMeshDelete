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

from bpy.types import (
    Operator,
)


import bpy
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


def _quick_delete():
    mode = bpy.context.mode
    if mode == "EDIT_MESH":
        select_mode = bpy.context.tool_settings.mesh_select_mode[:]
        del_types = ["VERT", "EDGE", "FACE"]
        active_select_mode = select_mode.index(True)
        del_type = del_types[active_select_mode]

        bpy.ops.mesh.delete(type=del_type)


def _assign_shortcuts():
    wm = bpy.context.window_manager
    items = wm.keyconfigs.user.keymaps["Mesh"].keymap_items
    # Changes Blender's default shortcuts
    for item in items:
        if item.name == "Delete":
            item.shift = 1

    # Replace Blender's default delete with quick delete
    mesh_keymaps = wm.keyconfigs.user.keymaps["Mesh"].keymap_items
    mesh_keymaps.new("qmd.quick_delete", type='X', value='PRESS')


def _revert_shortcuts():
    wm = bpy.context.window_manager
    items = wm.keyconfigs.user.keymaps["Mesh"].keymap_items
    # Changes Blender's delete shortcut to its default state
    for item in items:
        if item.name == "Delete":
            item.shift = 0

    # Deletes created shortcut for quick delete
    mesh_keymaps = wm.keyconfigs.user.keymaps["Mesh"].keymap_items
    qmd_keymap = wm.keyconfigs.user.keymaps["Mesh"].keymap_items["qmd.quick_delete"]
    mesh_keymaps.remove(qmd_keymap)


class QMD_OT_quick_delete(Operator):
    """Delete mesh components based on selection mode"""
    bl_label = "Quick Delete"
    bl_idname = "qmd.quick_delete"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        _quick_delete()

        return {"FINISHED"}


# -----------------------------------------------------
# Registration
# ------------------------------------------------------
classes = (
    QMD_OT_quick_delete,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    _assign_shortcuts()


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    _revert_shortcuts()