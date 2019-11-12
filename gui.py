import bpy

# Draw Panel
class TEXTMARKER_PT_panel(bpy.types.Panel):
    bl_space_type = "TEXT_EDITOR"
    bl_region_type = "UI"
    bl_label = "Text Markers"

    def draw(self, context):
        layout = self.layout
        text = bpy.data.texts
        if len(text) > 0:
            txt = bpy.context.space_data.text
            list = txt.text_marker_list
            idx = txt.text_marker_index

            row = layout.row()
            row.template_list(
                "TEXTMARKER_UL_ui_list",
                "",
                txt,
                "text_marker_list",
                txt,
                "text_marker_index",
                rows=10)
            col = row.column(align=True)
            col.operator(
                "textmarker.actions", icon='ADD', text="").action = 'ADD'
            col.operator(
                "textmarker.actions", icon='REMOVE', text="").action = 'DEL'

            col.separator()

            col.operator(
                "textmarker.actions", icon='TRIA_UP', text="").action = 'UP'
            col.operator(
                "textmarker.actions", icon='TRIA_DOWN',
                text="").action = 'DOWN'

            col.separator()

            col.operator(
                "textmarker.actions", icon='TRIA_LEFT',
                text="").action = 'PREVIOUS'
            col.operator(
                "textmarker.actions", icon='TRIA_RIGHT',
                text="").action = 'NEXT'

            col.separator()

            col.prop(txt, 'text_marker_autojump', icon='AUTO', text='')

            if not txt.text_marker_autojump:
                col.operator(
                    "textmarker.jump_to", icon='OUTLINER_DATA_FONT', text="")

            col.separator()

            col.operator("textmarker.sort", icon='SORTSIZE', text='')

            col.separator()

            col.prop(txt, 'text_marker_show_lines', icon='LINENUMBERS_ON', text="")

            if len(list) != 0 and idx < len(list):
                row = layout.row()
                box = row.box()
                box.label(
                    text=("" +
                          (list[idx].linecontent).replace("    ", "")))
                
            row = layout.row(align=True)

            row.prop(
                txt, 'text_marker_ignoreindent', icon='NOCURVE', text='Indent')
            row.operator(
                "textmarker.update", icon='FILE_REFRESH', text='Update')
            row.operator(
                "textmarker.clear_missing",
                icon='DISCLOSURE_TRI_DOWN',
                text='Clear Missing')
            row.operator("call.deleteall_menu", icon='X', text='Delete All')
            row = layout.row(align=True)
            row.operator(
                "textmarker.add_fromsearch",
                icon='PLUS',
                text="Add Markers with")
            row.prop(txt, 'text_marker_searchterm', text='')

        else:
            row = layout.row()
            row.label(text='No Text Block loaded', icon='INFO')