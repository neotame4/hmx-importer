import bpy
from .. readers import *
from .. common import *
from .. bpy_util_funcs import *

def sample_set_header(reader):
    bone_count = reader.int32()
    bone_names = []
    for _ in range(bone_count):
        bone_names.append(reader.numstring())
    count_per_sample = reader.int32()
    always_1 = reader.int32()
    return count_per_sample, bone_names

def sample_set_header2(reader):
    bone_count2 = reader.int32()
    bone_names2 = []
    for _ in range(bone_count2):
        bone_names2.append(reader.numstring())
    count_per_sample2= reader.int32()
    always_12 = reader.int32()
    return count_per_sample2, bone_names2

def anim_clip(reader):
    version = reader.int32()
    count_per_sample, bone_names = sample_set_header(reader)
    count_per_sample2, bone_names2 = sample_set_header2(reader)
   # sample_set_header(reader)
    return count_per_sample, bone_names, count_per_sample2, bone_names2

def create_acp_anim(self):
    reader = Reader(open(self.filepath, "rb").read(), self.filepath)
    get_endian(reader)
    anim_type = reader.numstring()
    anim_name = reader.numstring()
    version = get_version(reader)
    reader.version = version
    f1 = reader.float32()
    f2 = reader.float32()
    f3 = reader.float32()
    f4 = reader.float32()
    unknown = reader.int32()
    max_1 = reader.float32()
    count_per_sample, bone_names, count_per_sample2, bone_names2 = anim_clip(reader)
    for i in range(count_per_sample):
        armature = bpy.context.active_object
        bpy.data.scenes["Scene"].frame_end = count_per_sample - 1
        bpy.context.scene.render.fps = 30
        current_frame = bpy.data.scenes[0].frame_current
        bpy.context.scene.frame_set(i)
        for name in bone_names:
            if ".pos" in name:
                name = name.replace(".pos", ".mesh")
                bone = armature.pose.bones.get(name)
                pos = reader.vec3f()
                print("pos", pos, name)
                if bone:
                    bone.location[0] = pos[0]
                    bone.location[1] = pos[1]
                    bone.location[2] = pos[2]
                    bone.keyframe_insert("location")
            elif ".quat" in name:
                name = name.replace(".quat", ".mesh")
                bone = armature.pose.bones.get(name)
                quat = quat_math4(reader.vec4s())
                print("quat, name", quat, name)
                if bone:
                    bone.rotation_mode = "QUATERNION"
                   # bone.rotation_quaternion = quat
                    bone.rotation_quaternion = (quat[3], quat[0], quat[1], quat[2])
                    bone.keyframe_insert("rotation_quaternion")
            elif ".rotz" in name:
                name = name.replace(".rotz", ".mesh")
                bone = armature.pose.bones.get(name)
                rotz = rotz_math(reader.short())
                print("rotz, name", rotz, name)
                if bone:
                    bone.rotation_mode = "XYZ"
                    bone.rotation_euler[2] = rotz
                    bone.keyframe_insert("rotation_euler")        