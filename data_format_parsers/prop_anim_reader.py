import bpy
from .. common import *
from . anim_reader import *

def AnimEventFloat(reader):
    value = reader.float32()
    pos = reader.float32()
    print("pos", pos)
    return value, pos

def AnimEventColor(reader):
    value = reader.color4()
    pos = reader.float32()
    print("pos", pos)
    return value, pos

def AnimEventObject(reader):
    text1 = reader.numstring()
    text2 = reader.numstring()
    pos = reader.float32()
    print("pos", pos)
    return text1, text2, pos

def AnimEventBool(reader):
    value = reader.milo_bool()
    pos = reader.float32()
    print("pos", pos)
    return value, pos

def AnimEventQuat(reader):
    value = reader.quat4()
    pos = reader.float32()
    print("pos", pos)
    return value, pos

def AnimEventVector3(reader):
    value = reader.vec3f()
    pos = reader.float32()
    print("pos", pos)
    return value, pos

def AnimEventSymbol(reader):
    text = reader.numstring()
    pos = reader.float32()
    print("pos", pos)
    return text, pos


def read_prop_anim(reader, name, super: bool):
    version = reader.int32()
    print("prop_anim", "name, version", name, version)
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
        print("values", values)
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
                amb_color = reader.vec4f()
                pos = reader.float32()
                print("pos", pos)
            elif values[0] == "shot":
                shot = reader.numstring()
                pos = reader.float32()
                print("pos", pos)
            elif values[0] == "emit_rate":
                emit_value = reader.float32()
                pos = reader.float32()
                print("pos", pos)
            elif values[0] == "color":
                color_value = reader.color4()
                pos = reader.float32()
                print("color_value", color_value)
                print("pos", pos)
           # if values[1] == "x":
           #     print("X") 
           # elif values[1] == "y":
           #     print("Y") 
           # elif values[1] == "z":
           #     print("Z") 
            else:
                print("value not found", value)
                if type1 == 0:			#kPropFloat
                    value = reader.float32()
                    pos = reader.float32()
                    print("pos", pos)
                elif type1 == 1:		#kPropColor
                   value = reader.color4()
                   pos = reader.float32()
                   print("pos", pos) 
                elif type1 == 2:		#kPropObject
                    text1 = reader.numstring()
                    text2 = reader.numstring()
                    pos = reader.float32()
                    print("pos", pos)
                elif type1 == 3:		#kPropBool
                    value = reader.milo_bool()
                    pos = reader.float32()
                    print("pos", pos)
                elif type1 == 4:		#kPropQuat
                    value = reader.quat4()
                    pos = reader.float32()
                    print("pos", pos) 
                elif type1 == 5:		#kPropVector3
                    value = reader.vec3f()
                    pos = reader.float32()
                    print("pos", pos)
                elif type1 == 6:		#kPropSymbol
                    text = reader.numstring()
                    pos = reader.float32()
                    print("pos", pos)
                else:
                    print("type not found", type1)
    if version >= 13:
        unknown_bool2 = reader.milo_bool()
        print("unknown_bool2", unknown_bool2)
