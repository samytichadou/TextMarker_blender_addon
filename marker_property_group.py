import bpy

# Create custom property group
class TEXTMARKER_OT_list(bpy.types.PropertyGroup):
    '''name = StringProperty() '''
    linenumber: bpy.props.IntProperty(name="linenumber")
    linecontent: bpy.props.StringProperty(name="linecontent")
    linesbefore: bpy.props.StringProperty(name="linesbefore")
    linesafter: bpy.props.StringProperty(name="linesafter")
    linemissing: bpy.props.BoolProperty(name="linemissing", default=False)
