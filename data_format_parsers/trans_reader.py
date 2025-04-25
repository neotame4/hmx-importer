import bpy
import mathutils
from .. common import *

def read_trans(reader, super: bool, name: str = "", character_name: str = "") -> tuple[str, tuple, tuple]:
    trans_data = {}
    trans_data["bone_name"] = name
    trans_data["character_name"] = character_name
    version = reader.int32()
    trans_data["trans_version"] = version
    trans_version = version
    trans_count = 0
    trans_objects = None
    print("trans_VERSION", version)
    read_metadata(reader, super)
    local_xfm = reader.matrix()
    world_xfm = reader.matrix()
    trans_data["local_xfm"] = local_xfm
    trans_data["world_xfm"] = world_xfm
    if version < 9:
        trans_count = reader.int32()
        trans_data["trans_count"] = trans_count
        print("trans_count", trans_count)
        trans_objects = []
        for _ in range(trans_count):
            if reader.version <= 6:
                trans_object = reader.string()
                print("trans_object", trans_object)
                trans_objects.append(trans_object)
            else:
                trans_object = reader.numstring()
                print("trans_object", trans_object)
                trans_objects.append(trans_object)
        trans_data["trans_objects"] = trans_objects
    if version >= 6:
        constraint = reader.uint32()
    elif version < 3:
        if version > 0:
            some_number = reader.uint32()
    elif version in [3, 4, 5]:
        some_flags = reader.uint32()
    if version < 7:
        unknown_1 = reader.uint32()
        unknown_2 = reader.uint32()
        unknown_3 = reader.uint32()
    if version < 5:
        unknown_bool = reader.milo_bool()
    if version < 2:
        unknown_floats = reader.vec4f()
    if version > 7:
        target = reader.numstring()
    if version == 7:
        unknown = reader.float32()
        unknown_2 = reader.float32()
        unknown_3 = reader.float32()
        unknown_4 = reader.float32()
        unknown_5 = reader.float32()
    if version > 6:
        preserve_scale = reader.milo_bool()
    parent = ""
    if version >= 7:
        parent = reader.numstring()
        print("parent", parent)
        trans_data["parent"] = parent
    if super == False:
       # if version < 9:
       #     create_trans(trans_data, version, trans_objects, trans_count)
       # else:
        create_trans(trans_data)
    return trans_version, trans_count, trans_objects, parent, local_xfm, world_xfm
   # return parent, local_xfm, world_xfm
#, version

def create_trans(trans_data) -> None:
    version = trans_data["trans_version"]
    print("create_trans version", version)
    bone_name = trans_data["bone_name"]
    character_name = trans_data["character_name"]
    local_xfm = trans_data["local_xfm"]
    world_xfm = trans_data["world_xfm"]
    parent_name = trans_data.get("parent", "")
    if ".trans" in bone_name:
        obj = bpy.data.objects.get(bone_name)
        if obj == None:  
            obj = bpy.data.objects.new(bone_name, None)  
        if len(parent_name) > 0 and "bone" not in parent_name:
            try:
                o = bpy.data.objects.get(parent_name)
                if o:
                    obj.parent = o
                else:
                    o = bpy.data.objects.new(parent_name, None)
                    bpy.context.scene.collection.objects.link(o)
                    o.empty_display_size = 2
                    o.empty_display_type = 'PLAIN_AXES'
                    obj.parent = o
            except:
                pass
        try:
            bpy.context.scene.collection.objects.link(obj)
        except:
            print(obj, "Already exists")
        if (obj.parent != None) or (parent_name != None):
            obj.matrix_local = mathutils.Matrix((
                (local_xfm[0], local_xfm[3], local_xfm[6], local_xfm[9],),
                (local_xfm[1], local_xfm[4], local_xfm[7], local_xfm[10],),
                (local_xfm[2], local_xfm[5], local_xfm[8], local_xfm[11],),
                (0.0, 0.0, 0.0, 1.0),
            ))  
        else:
            obj.matrix_world = mathutils.Matrix((
                (world_xfm[0], world_xfm[3], world_xfm[6], world_xfm[9],),
                (world_xfm[1], world_xfm[4], world_xfm[7], world_xfm[10],),
                (world_xfm[2], world_xfm[5], world_xfm[8], world_xfm[11],),
                (0.0, 0.0, 0.0, 1.0),
            ))
    if "Armature" in bpy.data.armatures:
        armature_data = bpy.data.armatures["Armature"]
    else:
        armature_data = bpy.data.armatures.new("Armature")
    if "Armature" in bpy.data.objects:
        armature_obj = bpy.data.objects["Armature"]
    else:
        armature_obj = bpy.data.objects.new("Armature", armature_data)
        bpy.context.scene.collection.objects.link(armature_obj)
    bpy.context.view_layer.objects.active = armature_obj
    bpy.ops.object.mode_set(mode="EDIT")
    edit_bone = armature_obj.data.edit_bones.get(bone_name)
    print("edit_bone", edit_bone, bone_name)
    if edit_bone is None:
        edit_bone = armature_obj.data.edit_bones.new(bone_name)
        print("creating", "edit_bone", edit_bone, bone_name)
        edit_bone.head = (0, 0, 0)
        edit_bone.tail = (0, 1, 0)
        edit_bone.use_deform = True
    parent_bone = armature_obj.data.edit_bones.get(parent_name)
    print("parent_bone", parent_bone)
    if parent_bone is None:
        parent_bone = armature_obj.data.edit_bones.new(parent_name)
        print("creating", "parent_bone", parent_bone, bone_name)
        parent_bone.head = (0, 0, 0)
        parent_bone.tail = (0, 1, 0)
        parent_bone.use_deform = True
    
    if version < 9:
        trans_count = trans_data["trans_count"]
        print("trans_count1", trans_count)
        if trans_count > 0:
            trans_objects = []
            trans_objects = trans_data["trans_objects"]
           # children_list = trans_objects
            print("trans_objects1", trans_objects)
            parent_to_bone = bone_name
            print("parent_to_bone", parent_to_bone)
            parent_bone1 = armature_obj.data.edit_bones.get(parent_to_bone)
            print("get", "parent_bone1", parent_bone1, parent_to_bone)
            if parent_bone1 is None:
                parent_bone1 = armature_obj.data.edit_bones.new(parent_to_bone)
                print("creating", "parent_bone1", parent_bone1, parent_to_bone)
                parent_bone1.head = (0, 0, 0)
                parent_bone1.tail = (0, 1, 0)
                parent_bone1.use_deform = True
                print("new", "parent_bone1", parent_bone1, parent_to_bone)
            for i in range(trans_count):
                bone = trans_objects[i]
                print("bone", bone)
               # print("count", i)
                child_bone = armature_obj.data.edit_bones.get(bone)
                print("get", "child_bone", child_bone, bone)
                if child_bone is None:
                    child_bone = armature_obj.data.edit_bones.new(bone)
                    print("new", "child_bone", child_bone, bone)
                    print("creating", "child_bone", child_bone, bone)
                    child_bone.head = (0, 0, 0)
                    child_bone.tail = (0, 1, 0)
                    child_bone.use_deform = True
                parent_bone1_parent = parent_bone1.parent
                print("parent_bone1.parent", parent_bone1.parent, parent_bone1_parent)
                child_bone.parent = parent_bone1

    if parent_bone != bone_name:
        edit_bone.parent = parent_bone
    bpy.ops.object.mode_set(mode="POSE")
    pose_bone = armature_obj.pose.bones.get(bone_name)
    if pose_bone:
       # if trans_count != 0:
        if (pose_bone.parent != None):
            pose_bone.matrix_basis = mathutils.Matrix((
                (local_xfm[0], local_xfm[3], local_xfm[6], local_xfm[9],),
                (local_xfm[1], local_xfm[4], local_xfm[7], local_xfm[10],),
                (local_xfm[2], local_xfm[5], local_xfm[8], local_xfm[11],),
                (0.0, 0.0, 0.0, 1.0),
            ))  
        else:
            pose_bone.matrix_basis = mathutils.Matrix((
               # (world_xfm[0], world_xfm[3], world_xfm[6], world_xfm[9],),
               # (world_xfm[1], world_xfm[4], world_xfm[7], world_xfm[10],),
               # (world_xfm[2], world_xfm[5], world_xfm[8], world_xfm[11],),
                (local_xfm[0], local_xfm[3], local_xfm[6], local_xfm[9],),
                (local_xfm[1], local_xfm[4], local_xfm[7], local_xfm[10],),
                (local_xfm[2], local_xfm[5], local_xfm[8], local_xfm[11],),
                (0.0, 0.0, 0.0, 1.0),
            ))  
       # if (parent_bone == None):
       #     pose_bone.matrix_basis = mathutils.Matrix((
       #         (world_xfm[0], world_xfm[3], world_xfm[6], world_xfm[9],),
       #         (world_xfm[1], world_xfm[4], world_xfm[7], world_xfm[10],),
       #         (world_xfm[2], world_xfm[5], world_xfm[8], world_xfm[11],),
       #        # (local_xfm[0], local_xfm[3], local_xfm[6], local_xfm[9],),
       #        # (local_xfm[1], local_xfm[4], local_xfm[7], local_xfm[10],),
       #        # (local_xfm[2], local_xfm[5], local_xfm[8], local_xfm[11],),
       #         (0.0, 0.0, 0.0, 1.0),
       #     ))  
    else:
        print("pose bone not found", pose_bone)
        print("pose bone not found", pose_bone)
        print("pose bone not found", pose_bone)
        print("pose bone not found", pose_bone)
        print("pose bone not found", pose_bone)
        print("pose bone not found", pose_bone)
        print("pose bone not found", pose_bone)
        print("pose bone not found", pose_bone)
        print("pose bone not found", pose_bone)
        print("pose bone not found", pose_bone)

    bpy.context.view_layer.objects.active = armature_obj
    bpy.ops.object.mode_set(mode="EDIT")


    bpy.ops.object.mode_set(mode="OBJECT")
    character_obj = bpy.data.objects.get(character_name)
   # if character_obj:
   #     armature_obj.parent = character_obj