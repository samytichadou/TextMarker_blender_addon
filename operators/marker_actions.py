import bpy

# ui list category actions
class TEXTMARKER_MT_actions(bpy.types.Operator):
    bl_idname = "textmarker.actions"
    bl_label = ""
    bl_description = "Text Markers actions"

    action: bpy.props.EnumProperty(
        items=(
            ('ADD', "Add", ""),
            ('DEL', "Del", ""),
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('NEXT', "Next", ""),
            ('PREVIOUS', "Previous", ""),
        ))

    def invoke(self, context, event):
        txt = bpy.context.space_data.text
        idx = txt.text_marker_index
        items = txt.text_marker_list

        if self.action == 'ADD':
            chk = 0
            for i in items:
                if i.linenumber == txt.current_line_index + 1:
                    info = i.name + ' Marker already exists for this line'
                    self.report({'INFO'}, info)
                    chk = 1
            if chk == 0:
                newmarker = items.add()
                content = txt.lines[txt.current_line_index].body.lstrip()
                if content[:28]: 
                    newmarker.name = content[:28]  # "Text Marker " + str(len(items))
                else:
                    newmarker.name = "empty_line"
                newmarker.linenumber = txt.current_line_index + 1

                beforecontent = ""
                aftercontent = ""
                for n in range(1, 11):
                    if txt.current_line_index - n >= 0:
                        beforecontent = beforecontent + txt.lines[txt.current_line_index - n].body
                    if txt.current_line_index + n < len(txt.lines):
                        aftercontent = aftercontent + txt.lines[txt.current_line_index + n].body

                newmarker.linecontent = content
                newmarker.linesafter = aftercontent
                newmarker.linesbefore = beforecontent

                txt.text_marker_index = len(items) - 1
        try:
            txt.text_marker_list[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DEL':
                items.remove(idx)
                if idx >= len(items) and idx != 0:
                    txt.text_marker_index = len(items) - 1

            elif self.action == 'DOWN' and idx != len(items) - 1:
                items.move(idx, idx + 1)
                txt.text_marker_index = idx + 1

            elif self.action == 'UP' and idx != 0:
                items.move(idx, idx - 1)
                txt.text_marker_index = idx - 1

            elif self.action == 'NEXT':
                if idx < len(items) - 1:
                    txt.text_marker_index = idx + 1
                    txt.current_line_index = items[txt.text_marker_index].linenumber - 1

            elif self.action == 'PREVIOUS':
                if idx < len(items) and idx > 0:
                    txt.text_marker_index = idx - 1
                    txt.current_line_index = items[txt.text_marker_index].linenumber - 1

        return {"FINISHED"}