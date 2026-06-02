import bpy
bl_info={
    "name":"",
    "author":"Taro Kamata",
    "version":(1,0),
    "blender":(3,3,1),
    "location":"",
    "descripton":"",
    "wiki_url":"",
    "tracker_utl":"",
    "category":"Object"
}

def register():
    print("レベルエディタが有効化されました")

def unregister():
    print("レベルエディタが無効化されました")
    
if __name__ == "__main__":
    register()