# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; version 3
#  of the License.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


    
bl_info = {  
 "name": "Text Markers",  
 "author": "Samy Tichadou (tonton)",  
 "version": (1, 1),  
 "blender": (2, 7, 8),  
 "location": "Text Editor > ToolShelf > Text Markers",  
 "description": "Use Text Markers to keep your scripts organised", 
  "wiki_url": "https://github.com/samytichadou/TextMarker-blender-addon/wiki",  
 "tracker_url": "https://github.com/samytichadou/TextMarker-blender-addon/issues/new",  
 "category": "Development"}
 
import bpy
from bpy.props import IntProperty, CollectionProperty , StringProperty , BoolProperty
from difflib import SequenceMatcher

# UILIST
class TextMarkerUIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        
        
        layout.prop(item, "name", text="", emboss=False, translate=False)
        if item.linemissing==False:
            layout.label(str(item.linenumber))
        else:
            layout.label(str(item.linenumber), icon='ERROR')
        
# Draw Panel
class TextMarkerPanel(bpy.types.Panel):
    bl_space_type = "TEXT_EDITOR"
    bl_region_type = "UI"
    bl_label = "Text Markers"
    
    def draw(self, context):
        layout = self.layout
        text=bpy.data.texts
        if len(text)>0:
            txt=bpy.context.space_data.text
            list=txt.text_marker_list
            idx=txt.text_marker_index
            
            row = layout.row()
            row.template_list("TextMarkerUIList", "", txt, "text_marker_list", txt, "text_marker_index", rows=6)
            col = row.column(align=True)
            col.operator("textmarker.actions", icon='ZOOMIN', text="").action = 'ADD'
            col.operator("textmarker.actions", icon='ZOOMOUT', text="").action = 'DEL'
            col.separator()
            col.operator("textmarker.actions", icon='TRIA_UP', text="").action = 'UP'
            col.operator("textmarker.actions", icon='TRIA_DOWN', text="").action = 'DOWN'
            col.separator()
            col.operator("textmarker.actions", icon='REW', text="").action = 'PREVIOUS'
            col.operator("textmarker.actions", icon='FF', text="").action = 'NEXT'
            col.prop(txt, 'text_marker_autojump', icon='AUTO', text='')
            if len(list)!=0 and idx<len(list):
                row=layout.row()
                row.label("Line : "+(list[idx].linecontent).replace("    ",""))
                        
            row=layout.row(align=True)
            if txt.text_marker_autojump==False:
                row.operator("textmarker.jump_to", icon='OUTLINER_DATA_FONT', text="")
            row.operator("textmarker.sort", icon='SORTSIZE', text='')
            row.separator()
            row.prop(txt, 'text_marker_ignoreindent', icon='NOCURVE', text='Indent')
            row.operator("textmarker.update", icon='FILE_REFRESH', text='Update')
            row.separator()
            row.operator("textmarker.clear_missing", icon='DISCLOSURE_TRI_DOWN', text='Clear Missing')
            row.separator()
            row.operator("call.deleteall_menu", icon='X', text='')
            row=layout.row(align=True)
            row.operator("textmarker.add_fromsearch", icon='PLUS', text="Add Markers with")
            row.prop(txt, 'text_marker_searchterm', text='')
            
        else:
            row = layout.row()
            row.label('No Text Block loaded', icon='INFO')
            
        
# ui list category actions
class TextMarkerActions(bpy.types.Operator):
    bl_idname = "textmarker.actions"
    bl_label = ""
    bl_description = "Text Markers actions"

    action = bpy.props.EnumProperty(
        items=(
            ('ADD', "Add", ""),
            ('DEL', "Del", ""),
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('NEXT', "Next", ""),
            ('PREVIOUS', "Previous", ""),))

    def invoke(self, context, event):
        txt=bpy.context.space_data.text
        idx=txt.text_marker_index
        items = txt.text_marker_list
        
        if self.action == 'ADD':
            chk=0
            for i in items:
                if i.linenumber==txt.current_line_index+1:
                    info = i.name + ' Marker already exists for this line'
                    self.report({'INFO'}, info)
                    chk=1
            if chk==0:
                newmarker=items.add()
                newmarker.name="Text Marker "+str(len(items))
                newmarker.linenumber=txt.current_line_index+1
                
                content=txt.lines[txt.current_line_index].body
                beforecontent=""
                aftercontent=""
                for n in range(1, 11):
                    if txt.current_line_index-n>=0:
                        beforecontent=beforecontent+txt.lines[txt.current_line_index-n].body
                    if txt.current_line_index+n<len(txt.lines):
                        aftercontent=aftercontent+txt.lines[txt.current_line_index+n].body
            
                newmarker.linecontent=content
                newmarker.linesafter=aftercontent
                newmarker.linesbefore=beforecontent
                
                txt.text_marker_index=len(items)-1
        try:
            item = txt.text_marker_list[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DEL':
                items.remove(idx)
                if idx>=len(items) and idx!=0:
                    txt.text_marker_index=len(items)-1
                                
            elif self.action == 'DOWN' and idx!=len(items)-1:
                items.move(idx, idx+1)
                txt.text_marker_index=idx+1
                
            elif self.action == 'UP' and idx!=0:
                items.move(idx, idx-1)
                txt.text_marker_index=idx-1
                
            elif self.action == 'NEXT':
                if idx<len(items)-1:
                    txt.text_marker_index=idx+1
                    txt.current_line_index=items[txt.text_marker_index].linenumber-1
                    
            elif self.action == 'PREVIOUS':
                if idx<len(items) and idx>0 :
                    txt.text_marker_index=idx-1
                    txt.current_line_index=items[txt.text_marker_index].linenumber-1
                
        return {"FINISHED"}
    
# Jump to Line
class TextMarkerJumpTo(bpy.types.Operator):
    bl_idname = "textmarker.jump_to"
    bl_label = ""
    bl_description = "Jump to selected Text Marker"
    bl_options = {'UNDO'}
    
    @classmethod
    def poll(cls, context):
        txt=bpy.context.space_data.text
        text=bpy.data.texts
        list=txt.text_marker_list
        idx=txt.text_marker_index
        return len(list)>0 and len(text)>0 and idx<len(list)
    
    def execute(self, context):
        txt=bpy.context.space_data.text
        idx=txt.text_marker_index
        items = txt.text_marker_list
        
        try:
            item = txt.text_marker_list[idx]
        except IndexError:
            pass
        else:
            txt.current_line_index=item.linenumber-1
            
                                    
        return {"FINISHED"}

# update jump to
def jumpto(self, context):
    txt=bpy.context.space_data.text
    if txt.text_marker_autojump==True:
        bpy.ops.textmarker.jump_to()
    
# Sort list by linenumber
class TextMarkerSort(bpy.types.Operator):
    bl_idname = "textmarker.sort"
    bl_label = ""
    bl_description = "Sort Text Markers by Line Number"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        txt=bpy.context.space_data.text
        text=bpy.data.texts
        list=txt.text_marker_list
        return len(list)>0 and len(text)>0
    
    def execute(self, context):
        txt=bpy.context.space_data.text
        list=txt.text_marker_list
        idx=txt.text_marker_index
        name=[]
        line=[]
        content=[]
        missing=[]
        after=[]
        before=[]
        
        nlist = sorted(list, key=lambda x: x.linenumber, reverse=False)
        for n in nlist:
            name.append(str(n.name))
            line.append(str(n.linenumber))
            content.append(n.linecontent)
            missing.append(n.linemissing)
            after.append(n.linesafter)
            before.append(n.linesbefore)
        
        for i in range(len(list)-1,-1,-1):
            list.remove(i)

        for n in name:
            new=list.add()
            new.name=n
            new.linenumber=int(line[name.index(n)])
            new.linecontent=content[name.index(n)]
            new.linemissing=missing[name.index(n)]
            new.linesafter=after[name.index(n)]
            new.linesbefore=before[name.index(n)]
                            
        return {"FINISHED"}
    
# Update List
class TextMarkerUpdate(bpy.types.Operator):
    bl_idname = "textmarker.update"
    bl_label = ""
    bl_description = "Update Markers according to Text changes"
    bl_options = {'UNDO'}
    
    @classmethod
    def poll(cls, context):
        txt=bpy.context.space_data.text
        text=bpy.data.texts
        list=txt.text_marker_list
        return len(list)>0 and len(text)>0

    def execute(self, context):
        txt=bpy.context.space_data.text
        list=txt.text_marker_list
        idx=txt.text_marker_index
        possible=[]
        simila=[]
        similb=[]
        testdupe=[]
        
        for l in list:
            del possible[:]
            del simila[:]
            del similb[:]
            line=0
            chk=0
            for li in txt.lines:
                line=line+1
                if txt.text_marker_ignoreindent==True:
                    if l.linecontent in li.body:
                        chk=1
                        possible.append(line)
                elif txt.text_marker_ignoreindent==False:
                    l2=l.linecontent.replace("    ", "")
                    if l2 in li.body:
                        chk=1
                        possible.append(line)
            for p in possible:
                before=''
                after=''
                for ln in range(p-11, p-1):
                    if ln>=0:
                        before+=txt.lines[ln].body
                for ln in range(p, p+10):
                    if ln<len(txt.lines):
                        after+=txt.lines[ln].body
                pctb=SequenceMatcher(None, before, l.linesbefore).ratio()
                pcta=SequenceMatcher(None, after, l.linesafter).ratio()
                similb.append(pctb)
                simila.append(pcta)

            if len(possible)>0:
                oka=max(simila)
                okb=max(similb)
                if simila.index(oka)==similb.index(okb):
                    okidx=simila.index(oka)
                else:
                    if oka>okb:
                        okidx=simila.index(oka)
                    else:
                        okidx=similb.index(okb)
            if chk==0:
                l.linemissing=True
            elif chk==1:
                l.linenumber=possible[okidx]
                l.linecontent=txt.lines[possible[okidx]-1].body
                beforecontent=''
                aftercontent=''
                for n in range(1, 11):
                    if (l.linenumber-1)-n>=0:
                        beforecontent=beforecontent+txt.lines[(l.linenumber-1)-n].body
                    if (l.linenumber-1)+n<len(txt.lines):
                        aftercontent=aftercontent+txt.lines[(l.linenumber-1)+n].body
                l.linesafter=aftercontent
                l.linesbefore=beforecontent
                
                if l.linemissing==True:
                    l.linemissing=False
            
        for l in list:
            testdupe.append(l.linenumber)
        idx=-1
        for l in list:
            idx=idx+1
            chk=0
            for n in testdupe:
                if l.linenumber==n:
                    chk=chk+1
            if chk>=2:
                list.remove(idx)
            
        return {"FINISHED"}
    
# Clear Missing Lines
class TextMarkerClearMissing(bpy.types.Operator):
    bl_idname = "textmarker.clear_missing"
    bl_label = ""
    bl_description = "Delete missing Markers from list"
    bl_options = {'UNDO'}
    
    @classmethod
    def poll(cls, context):
        txt=bpy.context.space_data.text
        text=bpy.data.texts
        list=txt.text_marker_list
        return len(list)>0 and len(text)>0
    
    def execute(self, context):
        txt=bpy.context.space_data.text
        list=txt.text_marker_list
        idx=-1
        
        for p in list:
            idx=idx+1
            if p.linemissing==True:
                list.remove(idx)
                                    
        return {"FINISHED"}
    
# Add Marker from term search
class TextMarkerAddFromSearch(bpy.types.Operator):
    bl_idname = "textmarker.add_fromsearch"
    bl_label = ""
    bl_description = "Search in Text for term and automatically create Markers"
    bl_options = {'UNDO'}
    
    @classmethod
    def poll(cls, context):
        txt=bpy.context.space_data.text
        text=bpy.data.texts
        return txt.text_marker_searchterm!='' and len(text)>0
    
        
    def execute(self, context):
        txt=bpy.context.space_data.text
        list=txt.text_marker_list
        term=txt.text_marker_searchterm
        nb=0
        line=0
        for li in txt.lines:
            line=line+1
            if term in li.body:
                chk=0
                for l in list:
                    if l.linenumber==line:
                        chk=1
                if chk==0:
                    nb=nb+1
                    newmarker=list.add()
                    newmarker.name=term+" "+str(nb)
                    newmarker.linecontent=li.body
                    newmarker.linenumber=line
                    beforecontent=''
                    aftercontent=''
                    for n in range(1, 11):
                        if (newmarker.linenumber-1)-n>=0:
                            beforecontent=beforecontent+txt.lines[(newmarker.linenumber-1)-n].body
                        if (newmarker.linenumber-1)+n<len(txt.lines):
                            aftercontent=aftercontent+txt.lines[(newmarker.linenumber-1)+n].body
                    newmarker.linesbefore=beforecontent
                    newmarker.linesafter=aftercontent
                        
        return {"FINISHED"}
    
# Clear All Markers
class TextMarkerClearAll(bpy.types.Operator):
    bl_idname = "textmarker.clear_all"
    bl_label = ""
    bl_description = "Delete all Markers from list"
    bl_options = {'UNDO'}
    
    @classmethod
    def poll(cls, context):
        txt=bpy.context.space_data.text
        text=bpy.data.texts
        list=txt.text_marker_list
        return len(list)>0 and len(text)>0
    
    def execute(self, context):
        txt=bpy.context.space_data.text
        list=txt.text_marker_list
        for i in range(len(list)-1,-1,-1):
            list.remove(i)
                                    
        return {"FINISHED"}
    
# Menu Validation Clear All
class TextMarkerDeleteAllMenu(bpy.types.Menu):
    bl_label = "Delete all Text Markers"
    bl_idname = "Menu_DeleteAll_TextMarkers"
    
    def draw(self, context):
        layout = self.layout
        
        layout.operator("textmarker.clear_all",text="Click to Clear All", icon='ERROR')

# Call Validation Clear All Menu
def callclearallmenu (context):
    bpy.ops.wm.call_menu(name=TextMarkerDeleteAllMenu.bl_idname)
    
class TextMarkerCallDeleteAllMenu(bpy.types.Operator):
    """Delete all Text Markers"""
    bl_idname = "call.deleteall_menu"
    bl_label = "Delete all Text Markers"
    
    @classmethod
    def poll(cls, context):
        txt=bpy.context.space_data.text
        text=bpy.data.texts
        list=txt.text_marker_list
        return len(list)>0 and len(text)>0

    def execute(self, context):
        callclearallmenu(context)
        return {'FINISHED'}

# Create custom property group
class TextMarkerList(bpy.types.PropertyGroup):
    '''name = StringProperty() '''
    linenumber = bpy.props.IntProperty(name="linenumber")
    linecontent = bpy.props.StringProperty(name="linecontent")
    linesbefore = bpy.props.StringProperty(name="linesbefore")
    linesafter = bpy.props.StringProperty(name="linesafter")
    linemissing = bpy.props.BoolProperty(name="linemissing", default=False)
    
#register
def register():
    bpy.utils.register_class(TextMarkerUIList)
    bpy.utils.register_class(TextMarkerPanel)
    bpy.utils.register_class(TextMarkerActions)
    bpy.utils.register_class(TextMarkerJumpTo)
    bpy.utils.register_class(TextMarkerSort)
    bpy.utils.register_class(TextMarkerUpdate)
    bpy.utils.register_class(TextMarkerClearMissing)
    bpy.utils.register_class(TextMarkerAddFromSearch)
    bpy.utils.register_class(TextMarkerClearAll)
    bpy.utils.register_class(TextMarkerDeleteAllMenu)
    bpy.utils.register_class(TextMarkerCallDeleteAllMenu)
    bpy.utils.register_class(TextMarkerList)
    bpy.types.Text.text_marker_list = \
        bpy.props.CollectionProperty(type=TextMarkerList)
    bpy.types.Text.text_marker_index = IntProperty(update=jumpto)
    bpy.types.Text.text_marker_ignoreindent = BoolProperty(default=True, description="If False, indent will be ignored for Update")
    bpy.types.Text.text_marker_autojump = BoolProperty(default=True, description="Automatically jump to selected Marker")
    bpy.types.Text.text_marker_searchterm = StringProperty(description="Search Terms for adding Markers")

#unregister
def unregister():
    bpy.utils.unregister_class(TextMarkerUIList)
    bpy.utils.unregister_class(TextMarkerPanel)
    bpy.utils.unregister_class(TextMarkerActions)
    bpy.utils.unregister_class(TextMarkerJumpTo)
    bpy.utils.unregister_class(TextMarkerSort)
    bpy.utils.unregister_class(TextMarkerUpdate)
    bpy.utils.unregister_class(TextMarkerClearMissing)
    bpy.utils.unregister_class(TextMarkerAddFromSearch)
    bpy.utils.unregister_class(TextMarkerClearAll)
    bpy.utils.unregister_class(TextMarkerDeleteAllMenu)
    bpy.utils.unregister_class(TextMarkerCallDeleteAllMenu)
    bpy.utils.unregister_class(TextMarkerList)
    del bpy.types.Text.text_marker_list
    del bpy.types.Text.text_marker_index
    del bpy.types.Text.text_marker_ignoreindent
    del bpy.types.Text.text_marker_autojump
    del bpy.types.Text.text_marker_searchterm
    
if __name__ == "__main__":
    register()
