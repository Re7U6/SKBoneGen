import bpy
from .op_bone_gen import SkBoneGenOperator
from .panel import VIEW3D_PT_SkBoneGenPanel

bl_info = {
    "name": "SK Bone Generator",
    "author": "Re7U6",
    "version": (1, 0, 0),
    "blender": (3, 60, 0),
    "location": "View 3D > Sidebar > Edit Tab / Edit Mode Context Menu",
    "description": "スカートのボーンを生成を楽にするアドオン",
    "support": "COMMUNITY",
    "category": "Mesh"
}

classes = [
    SkBoneGenOperator,
    VIEW3D_PT_SkBoneGenPanel
]

def register():
    for c in classes:
        bpy.utils.register_class(c)
    print(f"アドオン『{bl_info['name']}』が有効化されました")


def unregister():
    for c in classes:
        bpy.utils.register_class(c)
    print(f"アドオン『{bl_info['name']}』が無効化されました")

if __name__ == "__main__":
    register()
