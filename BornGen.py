import bpy
from mathutils import Vector
import bmesh

bl_info = {
    "name": "SK Born Generator",
    "blender": (2, 80, 0),
    "category": "Mesh",
}

class SkBornGenOperator(bpy.types.Operator):
    bl_idname = "born.skborngen"
    bl_label = "頂点に沿ってボーンを生成"
    bl_description = "選択した頂点に沿ってボーンを生成します"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = bpy.context.object
        bm = bmesh.from_edit_mesh(obj.data)

        # blenderのバージョンが2.73以上の時に必要
        if bpy.app.version[0] >= 2 and bpy.app.version[1] >= 73:
            bm.verts.ensure_lookup_table()
        
        selected_verts = []
        selected_normal = []

        # 頂点の選択順序を表示
        for v in bm.select_history:
            if isinstance(v, bmesh.types.BMVert) and v.select:
                selected_verts.append(v.co.copy())
                selected_normal.append(v.normal)
    #    print(selected_verts)   
        print(selected_normal)     
        bm.free()

        armature = bpy.data.armatures.new(name='BoneArmature')
        armature_obj = bpy.data.objects.new('BoneArmature', armature)
        bpy.context.collection.objects.link(armature_obj)
        bpy.context.view_layer.objects.active = armature_obj
        armature_obj.select_set(True)
        bpy.ops.object.mode_set(mode='EDIT')

        # 選択された頂点の座標に沿ってボーンを配置
        for i in range(len(selected_verts) - 1):
            if i == 0:
                bone_head = selected_verts[i]
                bone_tail = selected_verts[i + 1]
                bone_roll = selected_normal[i]
                bpy.ops.armature.bone_primitive_add()
                edit_bone = armature_obj.data.edit_bones[-1]
                edit_bone.head = bone_head
                edit_bone.tail = bone_tail
                edit_bone.align_roll(bone_roll)
            else:
                bone_tail = selected_verts[i + 1]
                bone_roll = selected_normal[i + 1]
                vec = selected_verts[i + 1]
                bpy.ops.armature.extrude_move()
                edit_bone = armature_obj.data.edit_bones[-1]
                edit_bone.tail = bone_tail
                edit_bone.align_roll(bone_roll)

        return {'FINISHED'}

class VIEW3D_PT_SkBornGenPanel(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_SkBornGenPanel"
    bl_label = "SKBornGen"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        op = layout.operator(SkBornGenOperator.bl_idname, text="Gen")
        op.name = scene.name
        op.vertical = scene.vertical
        op.horizontal = scene.horizontal

        layout.prop(scene, "vertical")
        layout.prop(scene, "horizontal")


    def register_properties():
        scene = bpy.types.Scene
        scene.name = bpy.props.StringProperty(
            name="BoneName",
            description="ボーンの名前",
            default="SK_bone"
        )
        scene.vertical = bpy.props.IntProperty(
            name="vertical",
            description="縦軸の数",
            default="8",
            min="1"
        )
        scene.horizontal = bpy.props.IntProperty(
            name="horizontal",
            description="横軸の数",
            default="5",
            min="2"
        )
    
    def unregister_properties():
        scene = bpy.types.Scene
        del scene.name
        del scene.vertical
        del scene.horizantal


classes = [
    SkBornGenOperator,
    VIEW3D_PT_SkBornGenPanel
]
    
def register():
    for c in classes:
        bpy.utils.register_class(c)
    register_properties()
    print(f"アドオン『{bl_info['name']}』が有効化されました")
    

def unregister():
    unregister_properties()
    for c in classes:
        bpy.utils.register_class(c)
    print(f"アドオン『{bl_info['name']}』が無効化されました")

if __name__ == "__main__":
    register()
