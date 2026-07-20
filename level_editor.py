import bpy
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
    
classes = (
    MYADDON_OT_stretch_vertex,
    TOPBAR_MT_my_menu,
    MYADDON_OT_create_ico_sphere,
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
   