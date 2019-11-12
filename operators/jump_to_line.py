import bpy

# Jump to Line
class TEXTMARKER_OT_jump_to(bpy.types.Operator):
    bl_idname = "textmarker.jump_to"
    bl_label = ""
    bl_description = "Jump to selected Text Marker"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        txt = bpy.context.space_data.text
        text = bpy.data.texts
        list = txt.text_marker_list
        idx = txt.text_marker_index
        return len(list) > 0 and len(text) > 0 and idx < len(list)

    def execute(self, context):
        txt = bpy.context.space_data.text
        idx = txt.text_marker_index
        items = txt.text_marker_list

        try:
            item = txt.text_marker_list[idx]
        except IndexError:
            pass
        else:
            bpy.ops.text.jump(line=item.linenumber)

        return {"FINISHED"}


# update jump to
def jumpto(self, context):
    txt = bpy.context.space_data.text
    if txt.text_marker_autojump:
        bpy.ops.textmarker.jump_to()