import bpy

# Sort list by linenumber
class TEXTMARKER_OT_sort(bpy.types.Operator):
    bl_idname = "textmarker.sort"
    bl_label = ""
    bl_description = "Sort Text Markers by Line Number"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        txt = bpy.context.space_data.text
        text = bpy.data.texts
        list = txt.text_marker_list
        return len(list) > 0 and len(text) > 0

    def execute(self, context):
        txt = bpy.context.space_data.text
        list = txt.text_marker_list
        idx = txt.text_marker_index
        name = []
        line = []
        content = []
        missing = []
        after = []
        before = []

        nlist = sorted(list, key=lambda x: x.linenumber, reverse=False)
        for n in nlist:
            name.append(str(n.name))
            line.append(str(n.linenumber))
            content.append(n.linecontent)
            missing.append(n.linemissing)
            after.append(n.linesafter)
            before.append(n.linesbefore)

        for i in range(len(list) - 1, -1, -1):
            list.remove(i)

        for n in name:
            new = list.add()
            new.name = n
            new.linenumber = int(line[name.index(n)])
            new.linecontent = content[name.index(n)]
            new.linemissing = missing[name.index(n)]
            new.linesafter = after[name.index(n)]
            new.linesbefore = before[name.index(n)]

        return {"FINISHED"}
    