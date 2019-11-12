'''
Copyright (C) 2018 Samy Tichadou (tonton)
samytichadou@gmail.com

Created by Samy Tichadou (tonton)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
 "name": "Text Marker",
 "author": "Samy Tichadou (tonton), tin2tin",
 "version": (1, 2),
 "blender": (2, 80, 0),
 "location": "Text Editor",
 "description": "",
 "wiki_url": "https://github.com/samytichadou/TextMarker_blender_addon/wiki",
 "tracker_url": "https://github.com/samytichadou/TextMarker_blender_addon/issues/new",
 "category": "Development"}


import bpy


# IMPORT SPECIFICS
##################################
from .operators.add_marker_from_search import *
from .operators.clear_all_markers import *
from .operators.clear_missing import *
from .operators.jump_to_line import *
from .operators.marker_actions import *
from .operators.sort_list import *
from .operators.update_list import *

from .gui import *
from .marker_property_group import *
from .markers_ui_list import *

# register
##################################

classes = (TEXTMARKER_UL_ui_list,
            TEXTMARKER_PT_panel,
            TEXTMARKER_MT_actions,
            TEXTMARKER_OT_jump_to,
            TEXTMARKER_OT_sort,
            TEXTMARKER_OT_update,
            TEXTMARKER_OT_clear_missing,
            TEXTMARKER_OT_add_from_search,
            TEXTMARKER_OT_clear_all,
            TEXTMARKER_MT_delete_all,
            TEXTMARKER_OT_delete_all_menu,
            TEXTMARKER_OT_list
            )

def register():

    ### OPERATORS ###

    from bpy.utils import register_class
    for cls in classes :
        register_class(cls)

    ### PROPS ###

    bpy.types.Text.text_marker_list = bpy.props.CollectionProperty(type=TEXTMARKER_OT_list)
    bpy.types.Text.text_marker_index = bpy.props.IntProperty(update=jumpto)
    bpy.types.Text.text_marker_ignoreindent = bpy.props.BoolProperty(default=True, description="If False, indent will be ignored for Update")
    bpy.types.Text.text_marker_autojump = bpy.props.BoolProperty(default=True, description="Automatically jump to selected Marker")
    bpy.types.Text.text_marker_show_lines = bpy.props.BoolProperty(description="Show marker line number")
    bpy.types.Text.text_marker_searchterm = bpy.props.StringProperty(description="Search Terms for adding Markers")


def unregister():

    ### OPERATORS ###

    from bpy.utils import unregister_class
    for cls in reversed(classes) :
        unregister_class(cls)

    ### PROPS ###

    del bpy.types.Text.text_marker_list
    del bpy.types.Text.text_marker_index
    del bpy.types.Text.text_marker_ignoreindent
    del bpy.types.Text.text_marker_autojump
    del bpy.types.Text.text_marker_show_lines
    del bpy.types.Text.text_marker_searchterm