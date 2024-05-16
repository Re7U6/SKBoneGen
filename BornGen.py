import bpy
from mathutils import Vector
import bmesh

bl_info = {
    "name": "SK Bone Generator",
    "blender": (3, 60, 0),
    "category": "Mesh",
}

class SkBoneGenOperator(bpy.types.Operator):
    bl_idname = "bone.skbonegen"
    bl_label = "頂点に沿ってボーンを生成"
    bl_description = "選択した頂点に沿ってボーンを生成します"
    bl_options = {'REGISTER', 'UNDO'}
    
    bone_name: bpy.props.StringProperty(
        name="BoneName",
        description="ボーンの名前",
        default="SK_bone"
    )

    vertical: bpy.props.IntProperty(
        name="Vertical",
        description="縦辺の数",
        default=8,
        min=3
    )

    horizontal: bpy.props.IntProperty(
        name="Horizontal",
        description="横辺の数",
        default=4,
        min=2
    )
    

    def execute(self, context):
        bone_name = self.bone_name

        obj = bpy.context.object

        bm = bmesh.from_edit_mesh(obj.data)

        # blenderのバージョンが2.73以上の時に必要
        if bpy.app.version[0] >= 2 and bpy.app.version[1] >= 73:
            bm.verts.ensure_lookup_table()
        
        # 頂点座標、頂点ノーマルを取得
        selected_verts = []
        selected_normal = []

        # 頂点の選択順序を表示
        for v in bm.select_history:
            if isinstance(v, bmesh.types.BMVert) and v.select:
                selected_verts.append(v.co.copy())
                selected_normal.append(v.normal)
        # print(selected_verts)   
        # print(selected_normal)     
        bm.free()


        # アーマチュアを生成
        armature = bpy.data.armatures.new(name='BoneGen.000')
        armature_obj = bpy.data.objects.new('BoneGen.000', armature)
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
                bpy.ops.armature.bone_primitive_add(name=bone_name +'_1')
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
                edit_bone.name = bone_name + '_' + str(i + 1)
                edit_bone.tail = bone_tail
                edit_bone.align_roll(bone_roll)

        return {'FINISHED'}

class VIEW3D_PT_SkBoneGenPanel(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_SkBoneGenPanel"
    bl_label = "SKBoneGen"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        op = layout.operator(SkBoneGenOperator.bl_idname, text="Gen")


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
