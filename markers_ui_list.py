import bpy

# UILIST
class TEXTMARKER_UL_ui_list(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data,
                  active_propname):
        layout.prop(item, "name", text="", emboss=False, translate=False)
        if context.space_data.text.text_marker_show_lines:
            layout.label(text=str(item.linenumber))
        if item.linemissing:
            layout.label(icon='ERROR')