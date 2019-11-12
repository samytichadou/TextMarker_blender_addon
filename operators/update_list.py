import bpy

from difflib import SequenceMatcher

# Update List
class TEXTMARKER_OT_update(bpy.types.Operator):
    bl_idname = "textmarker.update"
    bl_label = ""
    bl_description = "Update Markers according to Text changes"
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
        idx = txt.text_marker_index
        possible = []
        simila = []
        similb = []
        testdupe = []

        for l in list:
            del possible[:]
            del simila[:]
            del similb[:]
            line = 0
            chk = 0
            for li in txt.lines:
                line = line + 1
                if txt.text_marker_ignoreindent:
                    if l.linecontent in li.body:
                        chk = 1
                        possible.append(line)
                elif not txt.text_marker_ignoreindent:
                    l2 = l.linecontent.replace("    ", "")
                    if l2 in li.body:
                        chk = 1
                        possible.append(line)
            for p in possible:
                before = ''
                after = ''
                for ln in range(p - 11, p - 1):
                    if ln >= 0:
                        before += txt.lines[ln].body
                for ln in range(p, p + 10):
                    if ln < len(txt.lines):
                        after += txt.lines[ln].body
                pctb = SequenceMatcher(None, before, l.linesbefore).ratio()
                pcta = SequenceMatcher(None, after, l.linesafter).ratio()
                similb.append(pctb)
                simila.append(pcta)

            if len(possible) > 0:
                oka = max(simila)
                okb = max(similb)
                if simila.index(oka) == similb.index(okb):
                    okidx = simila.index(oka)
                else:
                    if oka > okb:
                        okidx = simila.index(oka)
                    else:
                        okidx = similb.index(okb)
            if chk == 0:
                l.linemissing = True
            elif chk == 1:
                l.linenumber = possible[okidx]
                l.linecontent = txt.lines[possible[okidx] - 1].body
                beforecontent = ''
                aftercontent = ''
                for n in range(1, 11):
                    if (l.linenumber - 1) - n >= 0:
                        beforecontent = beforecontent + txt.lines[(
                            l.linenumber - 1) - n].body
                    if (l.linenumber - 1) + n < len(txt.lines):
                        aftercontent = aftercontent + txt.lines[(
                            l.linenumber - 1) + n].body
                l.linesafter = aftercontent
                l.linesbefore = beforecontent

                if l.linemissing:
                    l.linemissing = False

        for l in list:
            testdupe.append(l.linenumber)
        idx = -1
        for l in list:
            idx = idx + 1
            chk = 0
            for n in testdupe:
                if l.linenumber == n:
                    chk = chk + 1
            if chk >= 2:
                list.remove(idx)

        return {"FINISHED"}