import bpy

# Clear All Markers
class TEXTMARKER_OT_clear_all(bpy.types.Operator):
    bl_idname = "textmarker.clear_all"
    bl_label = ""
    bl_description = "Delete all Markers from list"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        txt = bpy.context.space_data.text
        text = bpy.data.texts
        list = txt.text_marker_list
        return len(list) > 0 and len(text) > 0

    def execute(self, context):
        txt = bpy.context.space_data.text
        list = txt.text_marker_list
        for i in range(len(list) - 1, -1, -1):
            list.remove(i)

        return {"FINISHED"}


# Menu Validation Clear All
class TEXTMARKER_MT_delete_all(bpy.types.Menu):
    bl_label = "Delete all Text Markers"
    bl_idname = "textmarker.delete_all"

    def draw(self, context):
        layout = self.layout

        layout.operator(
            "textmarker.clear_all", text="Click to Clear All", icon='ERROR')


# Call Validation Clear All Menu
def callclearallmenu(context):
    bpy.ops.wm.call_menu(name=TEXTMARKER_MT_delete_all.bl_idname)


class TEXTMARKER_OT_delete_all_menu(bpy.types.Operator):
    """Delete all Text Markers"""
    bl_idname = "call.deleteall_menu"
    bl_label = "Delete all Text Markers"

    @classmethod
    def poll(cls, context):
        txt = bpy.context.space_data.text
        text = bpy.data.texts
        list = txt.text_marker_list
        return len(list) > 0 and len(text) > 0

    def execute(self, context):
        callclearallmenu(context)
        return {'FINISHED'}


    