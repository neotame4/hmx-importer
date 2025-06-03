import bpy
import os 
from .. readers import *
from .. common import *
from .. bpy_util_funcs import *
    
def get_type_size(compression, index):
    if index < 2:
        return 16 if compression < 2 else 6
    if index != 2:
        return 4 if compression == 0 else 2
    if compression > 2:
        return 4
    if compression == 0:
        return 16
    return 8

def read_charclip(self):
    reader = Reader(open(self.filepath, "rb").read(), self.filepath)
    get_endian(reader)

    version = get_version(reader)
    reader.version = version
    print("version", version)
#   ^^^^comment out these three lines to import Dance Central anims
#       hacky fix but it works

    revision, metadata_type = read_metadatadetailed(reader, False) 
    print("revision, metadata_type", revision, metadata_type)
    start_beat = reader.float32()
    print("start_beat", start_beat)
    end_beat = reader.float32()
    print("end_beat", end_beat)
    beats_per_sec = reader.float32()
    print("beats_per_sec", beats_per_sec)
    if version >= 19:
        reader.seek(17)
        transitions_count = reader.uint32()
        print("transitions_count", transitions_count)
        for i in range(transitions_count):
            clip = reader.numstring()
            print("clip", clip)
            node_count = reader.uint32()
            print("node_count", node_count)
            # nodes
            cur_beat = reader.float32()
            print("cur_beat", cur_beat)
            next_beat = reader.float32()
            print("next_beat", next_beat)
        Junk1 = reader.uint32()
        print("Junk1", Junk1)
        if (metadata_type == "viseme"):
            Junk2 = reader.uint32()
            print("Junk2", Junk2)
    
        print("full", "'CharBonesSamples' gets called here")

        version3 = get_version(reader)
        reader.version3 = version3
        print("version3", version3)

        bone_count = reader.int32()
        print("bone_count", bone_count)
        char_bones = []
        for i in range(bone_count):
            char_bone = reader.numstring()
            print("char_bone", char_bone)
            weight = reader.float32()
            print("weight", weight)
            char_bones.append(char_bone)
        print("char_bones", char_bones)

        Counts = []
        if version3 > 15:
            count_size = 7
        else:
            count_size = 10
        for i in range(count_size):
            Count = reader.uint32()
            print("Count", Count)
            Counts.append(Count)
        compression = reader.int32()
        print("compression", compression)
        SampleSize = 0
        if compression < 2:
            SampleSize += 12 * Counts[1]
        else:
            SampleSize += 6 * Counts[1]

        if compression == 0:
            SampleSize += 16 * (Counts[3] - Counts[1])
        elif compression < 3:
            SampleSize += 8 * (Counts[3] - Counts[1])
        else:
            SampleSize += 4 * (Counts[3] - Counts[1])

        if compression == 0:
            SampleSize += 4 * (Counts[6] - Counts[3])
        else:
            SampleSize += 2 * (Counts[6] - Counts[3])
        SampleSizet = (SampleSize + 0xF) & 0xFFFFFFF
        print("SampleSize", SampleSizet)
        num_samples = reader.int32()
        print("num_samples", num_samples)
        num_frames = reader.int32()
        if version3 > 11:
            print("num_frames", num_frames)
            for i in range(num_frames):
                frames = reader.float32()
               # print("frames", frames)

            for i in range(num_samples):
                print("frame", i)
                armature = bpy.context.active_object
                bpy.data.scenes["Scene"].frame_start = 0
                bpy.data.scenes["Scene"].frame_end = num_samples - 1
                current_frame = bpy.data.scenes[0].frame_current
                bpy.context.scene.frame_set(i)
                Start = reader.tell()
                print("start", Start)
                for name in char_bones:
                    if ".pos" in name:
                        print("name", name)
                        name = name.replace(".pos", ".mesh")
                        bone = armature.pose.bones.get(name)
                        if compression < 2:
                            pos11 = reader.float32()
                            print("pos11", pos11)
                            pos22 = reader.float32()
                            print("pos22", pos22)
                            pos33 = reader.float32()
                            print("pos33", pos33)
                            pos44 = reader.float32()
                            print("pos44", pos44)
                            if version3 > 12:
                                pos1 = pos11
                                pos2 = pos22
                                pos3 = pos33
                                if bone:
                                    print("1")
                                    # just for viseme anim import
                                    if (metadata_type == "viseme"):
                                        bone.location[2] = (pos1)
                                        bone.location[1] = (pos2)
                                        bone.location[0] = (pos3) * -1
                                    else:
                                        bone.location[0] = pos1
                                        bone.location[1] = pos2
                                        bone.location[2] = pos3
                                    bone.keyframe_insert("location")
                            else:
                                pos1 = pos11
                                pos2 = pos12
                                pos3 = pos13
                                if bone:
                                    # just for viseme anim import
                                    if (metadata_type == "viseme"):
                                        bone.location[0] = ( pos1 / 32767 ) * 1280
                                        bone.location[1] = ( pos2 / 32767 ) * 1280
                                        bone.location[2] = (( pos3 / 32767 ) * 1280) * -1
                                    else:
                                        bone.location[0] = pos1
                                        bone.location[1] = pos2
                                        bone.location[2] = pos3
                                    bone.keyframe_insert("location")
                        else:
                            pos1 = reader.short()
                            print("pos1", pos1)
                            pos2 = reader.short()
                            print("pos2", pos2)
                            pos3 = reader.short()
                            print("pos3", pos3)
                            if bone:
                                # just for viseme anim import
                                if (metadata_type == "viseme"):
                                    bone.location[2] = ( pos1 / 32767 ) * 1280
                                    bone.location[1] = ( pos2 / 32767 ) * 1280
                                    bone.location[0] = (( pos3 / 32767 ) * 1280) * -1
                                else:
                                    bone.location[0] = ( pos1 / 32767 ) * 1280
                                    bone.location[1] = ( pos2 / 32767 ) * 1280
                                    bone.location[2] = ( pos3 / 32767 ) * 1280
                                bone.keyframe_insert("location")
                    if ".quat" in name:
                        print("name", name)
                        name = name.replace(".quat", ".mesh")
                        bone = armature.pose.bones.get(name)
                        if compression == 0:
                            quat1 = quat_math(reader.float32())
                            print("quat1", quat1)
                            quat2 = quat_math(reader.float32())
                            print("quat2", quat2)
                            quat3 = quat_math(reader.float32())
                            print("quat3", quat3)
                            quat4 = quat_math(reader.float32())
                            print("quat4", quat4)
                        elif compression < 3:
                            quat1 = quat_math(reader.short())
                            print("quat1", quat1)
                            quat2 = quat_math(reader.short())
                            print("quat2", quat2)
                            quat3 = quat_math(reader.short())
                            print("quat3", quat3)
                            quat4 = quat_math(reader.short())
                            print("quat4", quat4)
                        else:
                            quat1 = quat_math(reader.byte())
                            print("quat1", quat1)
                            quat2 = quat_math(reader.byte())
                            print("quat2", quat2)
                            quat3 = quat_math(reader.byte())
                            print("quat3", quat3)
                            quat4 = quat_math(reader.byte())
                            print("quat4", quat4)
                        if bone:
                            bone.rotation_mode = "QUATERNION"
                            bone.rotation_quaternion = (quat4, quat1, quat2, quat3)
                            bone.keyframe_insert("rotation_quaternion")
                    elif ".rotz" in name:
                        print("name", name)
                        name = name.replace(".rotz", ".mesh")
                        bone = armature.pose.bones.get(name)
                        if compression == 0:
                            rotz = reader.float32()
                            print("rotz", rotz)
                        else:
                            rot1 = reader.short()
                            rotz = (rot1 / 32767.0) / 0.5 * 10.0
                          #  rotz = (rot1 / 32767.0)
                          # dont know what the real values are sooo
                          # ¯\_(ツ)_/¯
                           # rotz = (rot1 / 32767.0) / 0.512 * 10.24
                            print("rotz", rotz)
                        if bone:
                            bone.rotation_mode = "XYZ"
                            bone.rotation_euler[2] = rotz
                            bone.keyframe_insert("rotation_euler") 
                End = reader.tell()
                print("end", End)
                datasize = End - Start
                print("datasize", datasize)
                print("Count", Count)
                computed_sizes = [0] * count_size  # Initialize computed_sizes with zeroes
                # Iteratively calculate each computed size
                for i in range(count_size - 1):
                    curr_count = Counts[i]
                    next_count = Counts[i + 1]
                    type_size = get_type_size(compression, i)
                    # Compute size for the current index
                    computed_sizes[i + 1] = computed_sizes[i] + (next_count - curr_count) * type_size
                # print(f"Computed size at index {i + 1}: {computed_sizes[i + 1]}")
                # Compute sample size with alignment
                sample_size = (computed_sizes[-1] + 0xF) & 0xFFFFFFF0
                # print(f"Final sample size (aligned): {sample_size}")
                # print("computed_sizes sample_size", computed_sizes, sample_size)
                Final_value = sample_size - (End - Start)
                print("padding_value", Final_value)
                reader.seek(Final_value)

        print("one", "'CharBonesSamples' gets called here")

        version3 = get_version(reader)
        reader.version3 = version3
        print("version3", version3)

        bone_count = reader.int32()
        print("bone_count", bone_count)
        char_bones = []
        for i in range(bone_count):
            char_bone = reader.numstring()
            print("char_bone", char_bone)
            weight = reader.float32()
            print("weight", weight)
            char_bones.append(char_bone)
        print("char_bones", char_bones)
        Counts = []
        if version3 > 15:
            count_size = 7
        else:
            count_size = 10
        for i in range(count_size):
            Count = reader.uint32()
            print("Count", Count)
            Counts.append(Count)
        compression = reader.int32()
        print("compression", compression)
        SampleSize = 0
        if compression < 2:
            SampleSize += 12 * Counts[1]
        else:
            SampleSize += 6 * Counts[1]

        if compression == 0:
            SampleSize += 16 * (Counts[3] - Counts[1])
        elif compression < 3:
            SampleSize += 8 * (Counts[3] - Counts[1])
        else:
            SampleSize += 4 * (Counts[3] - Counts[1])

        if compression == 0:
            SampleSize += 4 * (Counts[6] - Counts[3])
        else:
            SampleSize += 2 * (Counts[6] - Counts[3])
        SampleSizet = (SampleSize + 0xF) & 0xFFFFFFF
        print("SampleSize", SampleSizet)
        num_samples = reader.int32()
        print("num_samples", num_samples)
        num_frames = reader.int32()
        if version3 > 11:
            print("num_frames", num_frames)
            for i in range(num_frames):
                frames = reader.float32()
               # print("frames", frames)

            for i in range(num_samples):
                print("frame", i)
                armature = bpy.context.active_object
               # bpy.data.scenes["Scene"].frame_start = 0
               # bpy.data.scenes["Scene"].frame_end = num_samples - 1
                current_frame = bpy.data.scenes[0].frame_current
                bpy.context.scene.frame_set(i)
                Start = reader.tell()
                print("start", Start)
                for name in char_bones:
                    if ".pos" in name:
                        print("name", name)
                        name = name.replace(".pos", ".mesh")
                        bone = armature.pose.bones.get(name)
                        if compression < 2:
                            print("reading values as float")
                            pos11 = reader.float32()
                            print("pos11", pos11)
                            pos22 = reader.float32()
                            print("pos22", pos22)
                            pos33 = reader.float32()
                            print("pos33", pos33)
                           # probably breaks alot of anims but it makes viseme anims import correct
                            pos44 = reader.float32()
                            print("pos44", pos44)
                            if version3 > 12:
                                print("version3 > 12", version3)
                                pos1 = pos11
                                pos2 = pos22
                                pos3 = pos33
                                if bone:
                                    if (metadata_type == "viseme"):
                                        bone.location[0] = ( pos1 / 32767 ) * 1280
                                        bone.location[1] = ( pos2 / 32767 ) * 1280
                                        bone.location[2] = (( pos3 / 32767 ) * 1280) * -1
                                    else:
                                        print("egg")
                                        bone.location[0] = pos1
                                        bone.location[1] = pos2
                                        bone.location[2] = pos3 
                                    bone.keyframe_insert("location")
                            else:
                                print("version3 < 12", version3)
                                pos1 = pos11
                                pos2 = pos12
                                pos3 = pos13
                                if bone:
                                    # just for viseme anim import
                                    if (metadata_type == "viseme"):
                                        bone.location[0] = ( pos1 / 32767 ) * 1280
                                        bone.location[1] = ( pos2 / 32767 ) * 1280
                                        bone.location[2] = (( pos3 / 32767 ) * 1280) * -1
                                       # bone.location[2] = ( pos3 / 32767 ) * 1280
                                    else:
                                        bone.location[0] = ( pos1 / 32767 ) * 1280
                                        bone.location[1] = ( pos2 / 32767 ) * 1280
                                        bone.location[2] = ( pos3 / 32767 ) * 1280
                                    bone.keyframe_insert("location")
                        else:
                            print("reading values as shorts")
                            pos1 = reader.short()
                            print("pos1", pos1)
                            pos2 = reader.short()
                            print("pos2", pos2)
                            pos3 = reader.short()
                            print("pos3", pos3)
                            if bone:
                                # just for viseme anim import
                                if (metadata_type == "viseme"):
                                    bone.location[1] = ( pos1 / 32767 ) * 1280
                                    bone.location[2] = ( pos2 / 32767 ) * 1280
                                    bone.location[0] = (( pos3 / 32767 ) * 1280) * -1
                                else:
                                    bone.location[0] = ( pos1 / 32767 ) * 1280
                                    bone.location[1] = ( pos2 / 32767 ) * 1280
                                    bone.location[2] = ( pos3 / 32767 ) * 1280
                                bone.keyframe_insert("location")
                    if ".quat" in name:
                        print("name", name)
                        name = name.replace(".quat", ".mesh")
                        bone = armature.pose.bones.get(name)
                        if compression == 0:
                            quat1 = quat_math(reader.float32())
                            print("quat1", quat1)
                            quat2 = quat_math(reader.float32())
                            print("quat2", quat2)
                            quat3 = quat_math(reader.float32())
                            print("quat3", quat3)
                            quat4 = quat_math(reader.float32())
                            print("quat4", quat4)
                        elif compression < 3:
                            quat1 = quat_math(reader.short())
                            print("quat1", quat1)
                            quat2 = quat_math(reader.short())
                            print("quat2", quat2)
                            quat3 = quat_math(reader.short())
                            print("quat3", quat3)
                            quat4 = quat_math(reader.short())
                            print("quat4", quat4)
                        else:
                            quat1 = quat_math(reader.byte())
                            print("quat1", quat1)
                            quat2 = quat_math(reader.byte())
                            print("quat2", quat2)
                            quat3 = quat_math(reader.byte())
                            print("quat3", quat3)
                            quat4 = quat_math(reader.byte())
                            print("quat4", quat4)
                        if bone:
                            bone.rotation_mode = "QUATERNION"
                            bone.rotation_quaternion = (quat4, quat1, quat2, quat3)
                            bone.keyframe_insert("rotation_quaternion")
                   # for name, rotz in rotz_samples:
                   # for name in rotz_samples:
                    elif ".rotz" in name:
                        print("name", name)
                        name = name.replace(".rotz", ".mesh")
                        bone = armature.pose.bones.get(name)
                        if compression == 0:
                            rotz = reader.float32()
                            print("rotz", rotz)
                        else:
                            rot1 = reader.short()
                            rotz = (rot1 / 32767.0) / 0.5 * 10.0
                          # dont know what the real values are sooo
                          # ¯\_(ツ)_/¯
                           # rotz = (rot1 / 32767.0) / 0.512 * 10.24
                            print("rotz", rotz)
                        if bone:
                            bone.rotation_mode = "XYZ"
                            bone.rotation_euler[2] = rotz
                            bone.keyframe_insert("rotation_euler")
                    else:
                        print("unknown bone suffix", name)
                End = reader.tell()
                print("end", End)
                datasize = End - Start
                print("datasize", datasize)
                print("Count", Count)
                computed_sizes = [0] * count_size  # Initialize computed_sizes with zeroes
                # Iteratively calculate each computed size
                for i in range(count_size - 1):
                    curr_count = Counts[i]
                    next_count = Counts[i + 1]
                    type_size = get_type_size(compression, i)
                    # Compute size for the current index
                    computed_sizes[i + 1] = computed_sizes[i] + (next_count - curr_count) * type_size
                # print(f"Computed size at index {i + 1}: {computed_sizes[i + 1]}")
                # Compute sample size with alignment
                sample_size = (computed_sizes[-1] + 0xF) & 0xFFFFFFF0
                # print(f"Final sample size (aligned): {sample_size}")
                # print("computed_sizes sample_size", computed_sizes, sample_size)
                Final_value = sample_size - (End - Start)
                print("padding_value", Final_value)
                reader.seek(Final_value)


    bone_count = reader.int32()
   # char_bones = []
    for _ in range(bone_count):
        char_bone = reader.numstring()
        weight = reader.float32()
        print("char_bone, weight", char_bone, weight)
       # char_bones.append(char_bone)
    float_count = reader.int32()
    beans = reader.float32()
    print("float_count, beans", float_count, beans)
    for _ in range(float_count * 2):
        value = reader.float32()
        print("value", value)

    if (metadata_type == "viseme"):
        extension = ".vsm"
       # extension = ".ccs"
        bpy.data.actions[bpy.context.active_object.name + "Action"].name = os.path.splitext(os.path.basename(self.filepath))[0] + extension
        print("file", bpy.path.basename(os.path.splitext(os.path.basename(self.filepath))[0] + extension))
    else:
        print("file", bpy.path.basename(self.filepath))

   # bpy.data.actions["ArmatureAction"].name = bpy.path.basename(self.filepath)
   # print("file", bpy.path.basename(self.filepath))
   # bpy.ops.nla.action_pushdown(track_index=1)
   # bpy.ops.action.push_down()
   # create_anim(self, reader)
