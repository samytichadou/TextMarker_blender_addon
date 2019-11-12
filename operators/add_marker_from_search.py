import bpy

# Add Marker from term search
class TEXTMARKER_OT_add_from_search(bpy.types.Operator):
    bl_idname = "textmarker.add_fromsearch"
    bl_label = ""
    bl_description = "Search in Text for term and automatically create Markers"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        txt = bpy.context.space_data.text
        text = bpy.data.texts
        return txt.text_marker_searchterm != '' and len(text) > 0

    def execute(self, context):
        txt = bpy.context.space_data.text
        list = txt.text_marker_list
        term = txt.text_marker_searchterm
        nb = 0
        line = 0
        for li in txt.lines:
            line = line + 1
            if term in li.body:
                chk = 0
                for l in list:
                    if l.linenumber == line:
                        chk = 1
                if chk == 0:
                    nb = nb + 1
                    newmarker = list.add()

                    content = li.body.lstrip()
                    newmarker.name = content[:35]
                    # newmarker.name = term + " " + str(nb)
                    newmarker.linecontent = li.body
                    newmarker.linenumber = line
                    beforecontent = ''
                    aftercontent = ''
                    for n in range(1, 11):
                        if (newmarker.linenumber - 1) - n >= 0:
                            beforecontent = beforecontent + txt.lines[(
                                newmarker.linenumber - 1) - n].body
                        if (newmarker.linenumber - 1) + n < len(txt.lines):
                            aftercontent = aftercontent + txt.lines[(
                                newmarker.linenumber - 1) + n].body
                    newmarker.linesbefore = beforecontent
                    newmarker.linesafter = aftercontent

        return {"FINISHED"}