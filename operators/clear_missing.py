import bpy

# Clear Missing Lines
class TEXTMARKER_OT_clear_missing(bpy.types.Operator):
    bl_idname = "textmarker.clear_missing"
    bl_label = ""
    bl_description = "Delete missing Markers from list"
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
        idx = -1

        for p in list:
            idx = idx + 1
            if p.linemissing:
                list.remove(idx)

        return {"FINISHED"}