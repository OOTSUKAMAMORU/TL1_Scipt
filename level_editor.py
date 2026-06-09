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

def draw_menu_manual(self,context):
    self.layout.operator("wm.url_open_preset",text="Manual",icon="HELP")

class TOPBAR_MT_my_menu(bpy.types.Menu):
    bl_idname="TOPBAR_MT_my_menu"
    bl_label="MyMenu"
    bl_description="拡張メニュー　by"+bl_info["author"]

    def draw(self,context):
        self.layout.operator("wm.url_open_preset",text="Manual",icon='HELP')

    def submenu(self,context):
        self.layout.menu(TOPBAR_MT_my_menu.bl_idname) 

classes = (
    TOPBAR_MT_my_menu,
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