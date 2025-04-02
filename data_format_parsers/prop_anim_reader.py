import bpy
from .. common import *
from . anim_reader import *

def read_prop_anim(reader, super: bool):
    version = reader.int32()
    print("version", version)
    metadata = read_metadata(reader, super)
    anim = read_anim(reader, True)
    if version == 12:
        usually_false = reader.milo_bool()
        print("usually_false", usually_false)
    prop_keys_count = reader.int32()
    print("prop_keys_count", prop_keys_count)
    for _ in range(prop_keys_count):
        type1 = reader.int32()
        print("type1", type1)
        type2 = reader.int32()
        print("type2", type2)
        target = reader.numstring()
        print("target", target)
        obj = bpy.data.objects.get(target)
        if obj is None:
            obj = bpy.data.objects.new(target, None)
            bpy.context.scene.collection.objects.link(obj)
            obj.empty_display_size = 2
            obj.empty_display_type = 'PLAIN_AXES'
        has_tree = reader.milo_bool()
        print("has_tree", has_tree)
        if has_tree == True:
            child_count = reader.short()
            print("child_count", child_count)
            id = reader.int32()
            print("id", id)
            values = []
            for x in range(child_count):
                child_type = reader.int32()
                print("child_type", child_type)
                value = reader.numstring()
                print("value", value)
                values.append(value)
        if version > 9:
            interpolation = reader.int32()
            print("interpolation", interpolation)
            interp_handler = reader.numstring()
            print("interp_handler", interp_handler)
        unknown_enum = reader.int32()
        print("unknown_enum", unknown_enum)
        if version >= 13:
            unknown_bool = reader.milo_bool()
            print("unknown_bool", unknown_bool)
        event_count = reader.int32()
        print("event_count", event_count)
        for x in range(event_count):
            if values[0] == "position":
                location = reader.vec3f()
                pos = reader.float32()
                print("pos", pos)
                obj.location = location
                obj.keyframe_insert("location", frame=pos)
            elif values[0] == "rotation":
                quat = reader.vec4f()
                pos = reader.float32()
                print("pos", pos)
                obj.rotation_mode = "QUATERNION"
                obj.rotation_quaternion = (quat[3], quat[0], quat[1], quat[2])
                obj.keyframe_insert("rotation_quaternion", frame=pos)
            elif values[0] == "scale":
                scale = reader.vec3f()
                pos = reader.float32()
                print("pos", pos)
                obj.scale = scale
                obj.keyframe_insert("scale", frame=pos)
            elif values[0] == "showing":
                obj_showing = reader.milo_bool()
                pos = reader.float32()
                print("pos", pos)
            elif values[0] == "mat":
                text1 = reader.numstring()
                text2 = reader.numstring()
                pos = reader.float32()
                print("pos", pos)
            elif values[0] == "alpha":
                alpha_value = reader.float32()
                pos = reader.float32()
                print("pos", pos)
            elif values[0] == "emissive_multiplier":
                emissive_value = reader.float32()
                print("emissive_value", emissive_value)
                pos = reader.float32()
                print("pos", pos)
            elif values[0] == "tex_xfm":
                tex_xfm_value = reader.float32()
                pos = reader.float32()
                print("pos", pos)
            elif values[0] == "hue":
                hue_value = reader.float32()
                pos = reader.float32()
                print("pos", pos)
            elif values[0] == "ambient_color":
                scale = reader.vec4f()
                pos = reader.float32()
                print("pos", pos)
            else:
                print("value not found", value)
    if version >= 13:
        unknown_bool2 = reader.milo_bool()
        print("unknown_bool2", unknown_bool2)
