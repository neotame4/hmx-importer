import bpy
from .. common import *
from . anim_reader import *

def read_trans_anim(name, reader, super: bool) -> None:
    trans_anim_data = {}
    version = reader.int32()
    print("trans_anim", "name, version", name, version)
    if version > 4:
        read_metadata(reader, super)
    readanim = read_anim(reader, True)
    if version < 6:
        version_min = reader.int32()
        print("version_min", version_min)
        unknown = reader.milo_bool()
        print("unknown", unknown)
        if version_min < 2:
            string_count = reader.uint32()
            print("string_count", string_count)
            for _ in range(string_count):
                some_string = reader.numstring()
                print("some_string", some_string)
        if version_min > 0:
            num_1 = reader.int32()
            num_2 = reader.int32()
            num_3 = reader.int32()
            num_4 = reader.int32()
        if version_min > 2:
            num_5 = reader.int32()
        if version_min > 3:
            drawable = reader.numstring()
    trans_object = reader.numstring()
    obj = bpy.data.objects.get(trans_object)
    if (obj is None) and (".cam" in trans_object):
        bpy.ops.object.camera_add()
        camera = bpy.context.object
        camera.name = name
       # bpy.context.scene.collection.objects.link(obj)
       # obj.empty_display_size = 2
       # obj.empty_display_type = 'PLAIN_AXES'
    elif obj is None:
        obj = bpy.data.objects.new(trans_object, None)
        bpy.context.scene.collection.objects.link(obj)
        obj.empty_display_size = 2
        obj.empty_display_type = 'PLAIN_AXES'
   # if len(trans_object) < 4:
   #     obj = bpy.data.objects.new(name, None)
   #     bpy.context.scene.collection.objects.link(obj)
   #     obj.empty_display_size = 2
   #     obj.empty_display_type = 'PLAIN_AXES'
    trans_anim_data["object"] = obj
    if version != 2:
        rot_keys_count = reader.int32()
        rot_keys = []
        for _ in range(rot_keys_count):
            rot_keys.append((reader.vec4f(), reader.float32()))
        trans_anim_data["rot_keys"] = rot_keys
        pos_keys_count = reader.int32()
        pos_keys = []
        for _ in range(pos_keys_count):
            pos_keys.append((reader.vec3f(), reader.float32()))  
        trans_anim_data["pos_keys"] = pos_keys          
    trans_anim_owner = reader.numstring()
    if version < 4:
        trans_spline = reader.uint32()
    else:
        trans_spline = reader.milo_bool()
    repeat_trans = reader.milo_bool()
    if version < 4:
        print("TODO")
    else:
        scale_keys_count = reader.int32()
        scale_keys = []
        for _ in range(scale_keys_count):
            scale_keys.append((reader.vec3f(), reader.float32()))     
        trans_anim_data["scale_keys"] = scale_keys
        scale_spline = reader.milo_bool()
    if version < 2:
        print("TODO, Determine by keys_owner? (0x4c)")
    else:
        follow_path = reader.milo_bool()
        if follow_path == True:
            vec4 = reader.vec4f()
    if version > 3:
        rot_slerp = reader.milo_bool()
    if version == 3:
        bone1 = reader.uint32()
        bone2 = reader.uint32()
    if version > 6:
        rot_spline = reader.milo_bool()
    create_anim(trans_anim_data)

def create_anim(trans_anim_data: dict) -> None:
    obj = trans_anim_data["object"]
    rot_keys = trans_anim_data.get("rot_keys", [])
    pos_keys = trans_anim_data.get("pos_keys", [])
    scale_keys = trans_anim_data.get("scale_keys", [])
    for key, pos in rot_keys:
        obj.rotation_mode == "QUATERNION"
        obj.rotation_quaternion = (key[3], key[0], key[1], key[2])
        obj.keyframe_insert("rotation_quaternion", frame=pos)
    for key, pos in pos_keys:
        obj.location = key
        obj.keyframe_insert("location", frame=pos)
    for key, pos in scale_keys:
        obj.scale = key
        obj.keyframe_insert("scale", frame=pos)