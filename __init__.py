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
 "author": "Samy Tichadou (tonton)",
 "version": (1, 1),
 "blender": (2, 80, 0),
 "location": "Text Editor",
 "description": "",
 "wiki_url": "https://github.com/samytichadou/TextMarker-blender-addon/wiki",
 "tracker_url": "https://github.com/samytichadou/TextMarker-blender-addon/issues/new",
 "category": "Development"}


import bpy


# IMPORT SPECIFICS
##################################



# register
##################################

classes = (
            )

def register():

    ### OPERATORS ###

    from bpy.utils import register_class
    for cls in classes :
        register_class(cls)

    ### PROPS ###

    bpy.types.Text.text_marker_list : bpy.props.CollectionProperty(type=TextMarkerList)
    bpy.types.Text.text_marker_index : bpy.props.IntProperty(update=jumpto)
    bpy.types.Text.text_marker_ignoreindent : bpy.props.BoolProperty(default=True, description="If False, indent will be ignored for Update")
    bpy.types.Text.text_marker_autojump : bpy.props.BoolProperty(default=True, description="Automatically jump to selected Marker")
    bpy.types.Text.text_marker_searchterm : bpy.props.StringProperty(description="Search Terms for adding Markers")


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
    del bpy.types.Text.text_marker_searchterm
