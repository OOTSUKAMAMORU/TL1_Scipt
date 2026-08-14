import bpy
import math
import bpy_extras
bl_info={
    "name":"レベルエディタ",
    "author":"Taro Kamata",
    "version":(1,0),
    "blender":(3,3,1),
    "location":"",
    "descripton":"レベルエディタ",
    "wiki_url":"",
    "tracker_utl":"",
    "category":"Object"
}
   
class TOPBAR_MT_my_menu(bpy.types.Menu):
    bl_idname="TOPBAR_MT_my_menu"
    bl_label="MyMenu"
    bl_description="拡張メニュー　by"+bl_info["author"]

    def draw(self,context):
        self.layout.operator(MYADDON_OT_stretch_vertex.bl_idname,text=MYADDON_OT_stretch_vertex.bl_label)
        self.layout.operator(MYADDON_OT_create_ico_sphere.bl_idname,text=MYADDON_OT_create_ico_sphere.bl_label)
        self.layout.operator(MYADDON_OT_export_scene.bl_idname,text=MYADDON_OT_export_scene.bl_label)
        self.layout.operator("wm.url_open_preset",text="Manual",icon='HELP')

    def submenu(self,context):
        self.layout.menu(TOPBAR_MT_my_menu.bl_idname)

class MYADDON_OT_stretch_vertex(bpy.types.Operator):
    bl_idname="myaddon.stretch_vertex"
    bl_label="頂点を伸ばす"
    bl_description="頂点を引っ張って伸ばします"
    bl_options={'REGISTER','UNDO'}

    #メニューを実行したときに呼ばれるコールバック関数
    def execute(self,context):
        bpy.data.objects['Cube'].data.vertices[0].co.x+=1.0
        print("頂点を伸ばしました")
        
        #オペレーターの命令終了を通知
        return {'FINISHED'}
    
#オペレーター　ICO球生成     
class MYADDON_OT_create_ico_sphere(bpy.types.Operator):
    bl_idname="myaddon.create_ico_sphere_object"
    bl_label="ICO球を生成"
    bl_description="ICO球を生成します"
    bl_options={'REGISTER','UNDO'}

    #メニューを実行したときに呼ばれる関数
    def execute(self,context):
        bpy.ops.mesh.primitive_ico_sphere_add()
        print("ICO球を生成しました")
        return {'FINISHED'}
    
class MYADDON_OT_export_scene(bpy.types.Operator,bpy_extras.io_utils.ExportHelper):
    bl_idname = "myddon.myaddon_ot_export_scene"
    bl_label="シーン出力"
    bl_description="シーン情報をExportします"
    filename_ext=".scene"
    def execute(self,context):
        
        print("シーン情報Exportします")

        self.export()
        
        

        print("シーン情報をExportしました")

        self.report({'INFO'},"シーン情報をExoprtしました")
        return{'FINISHED'}

    def export(self):
            """ファイルに入力"""
            print("シーン情報出力開始... %r" % self.filepath)
            with open(self.filepath,"wt") as file:
                self.write_and_print(file,"SCENE\n")
                #シーン内の全オブジェクトについて
                for object in bpy.context.scene.objects:

                    if object.parent:
                        continue
                    self.parse_secene_recursive(file,object,0)

    def parse_secene_recursive(self,file,object,level):
        """シーン解析用再帰関数"""
        indent=''
        for i in range(level):
            indent += "\t"

        self.write_and_print(file, indent + object.type)
        trans,rot,scale=object.matrix_local.decompose()
        rot=rot.to_euler()
        rot.x=math.degrees(rot.x)
        rot.y=math.degrees(rot.y)
        rot.z=math.degrees(rot.z)

        self.write_and_print(file, indent + "T %f %f %f" % (trans.x,trans.y,trans.z))
        self.write_and_print(file, indent + "R %f %f %f" % (rot.x,rot.y,rot.z))
        self.write_and_print(file, indent + "S %f %f %f" % (scale.x,scale.y,scale.z))

        if "file_name" in object:
            self.write_and_print(file, indent + "N %s" % object["file_name"])
        self.write_and_print(file,indent+'END')
        self.write_and_print(file,'')
        
        for child in object.children:
            self.parse_secene_recursive(file,child,level + 1)

    def write_and_print(self,file,str):
        print(str)

        file.write(str)
        file.write('\n')

class OBJECT_PT_file_name(bpy.types.Panel):
    """オブジェクトのファイルネームパネル"""
    bl_idname="OBJECT_PT_file_name"
    bl_label="FileName"
    bl_space_type="PROPERTIES"
    bl_region_type="WINDOW"
    bl_context="object"

    def draw(self,context):
        if "file_name"in context.object:
            self.layout.prop(context.object,'["file_name"]',text=self.bl_label)
        else:
            self.layout.operator(MYADDON_OT_add_filename.bl_idname)

class MYADDON_OT_add_filename(bpy.types.Operator):
    bl_idname="myaddon.myaddon_ot_add_filename"
    bl_label="FileName 追加"
    bl_description="['file_name']カスタムプロパティを追加します"
    bl_options={"REGISTER","UNDO"}
    def execute(self,context):
        context.object["file_name"]=""
        return{"FINISHED"}

class MYADDON_OT_scene(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_export_scene"
    bl_label = "シーン出力"
    bl_description = "シーン情報をExportします"
    
    def execute(self,context):
        print("シーン情報をExportします")
        
        for object in bpy.context.scene.objects:
            print(object.type + " - " + object.name)
        
        print("シーン情報をExportしました")
        self.report({'INFO'},"シーン情報をExportしました")
        
        return{'FINISHED'}      

classes = (
    MYADDON_OT_stretch_vertex,
    TOPBAR_MT_my_menu,
    MYADDON_OT_create_ico_sphere,
    MYADDON_OT_export_scene,
    MYADDON_OT_add_filename,
    OBJECT_PT_file_name,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    print("レベルエディタが有効化されました")
    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_my_menu.submenu)

def unregister():
    print("レベルエディタが無効化されました")
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_my_menu.submenu)
    for cls in classes:
        bpy.utils.unregister_class(cls) 
if __name__ == "__main__":
    register()