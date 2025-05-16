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

def create_anim(self, reader):
    reader = Reader(open(self.filepath, "rb").read(), self.filepath)
    get_endian(reader)
    version = get_version(reader)
    reader.version = version
    bone_count = reader.int32()
    char_bones = []
    for _ in range(bone_count):
        char_bone = reader.numstring()
        weight = reader.float32()
        char_bones.append(char_bone)
    if version > 15:
        count_size = 7
    else:
        count_size = 10
    counts = []
    for _ in range(count_size):
        counts.append(reader.uint32())
    compression = reader.int32()
    sample_size = 0
    if compression < 2:
        sample_size += 12 * counts[1]
    else:
        sample_size += 6 * counts[1]
    if compression == 0:
        sample_size += 16 * (counts[3] - counts[1])
    elif compression < 3:
        sample_size += 8 * (counts[3] - counts[1])
    else:
        sample_size += 4 * (counts[3] - counts[1])
    if compression == 0:
        sample_size += 4 * (counts[6] - counts[3])
    else:
        sample_size += 2 * (counts[6] - counts[3])
    sample_size = (sample_size + 0xF) & 0xFFFFFFF
    num_samples = reader.int32()
    num_frames = reader.int32()
    if version > 11:
        for _ in range(num_frames):
            frame = reader.float32()
    for i in range(num_samples):
        armature = bpy.context.active_object
        bpy.data.scenes["Scene"].frame_start = 0
        bpy.data.scenes["Scene"].frame_end = num_samples - 1
        current_frame = bpy.data.scenes[0].frame_current
        bpy.context.scene.frame_set(i)
        bpy.context.scene.render.fps = 30
        start = reader.tell()
        for name in char_bones:
            if ".pos" in name:
                name = name.replace(".pos", ".mesh")
                bone = armature.pose.bones.get(name)
                if compression < 2:
                    x, y, z = reader.vec3f()
                    if version >= 17:
                        w = reader.float32()
                    if version > 12:
                        x, y, z = pos_math(reader.vec)
                        if version >= 17:
                            pos4 = (pos44 / 32767) * 1280
                    else:
                        pos1 = pos11
                        pos2 = pos12
                        pos3 = pos13
                        if version3 >= 17:
                            pos4 = pos44
                        if bone:
                            # just for viseme anim import
                          #  bone.location[2] = ( pos1 / 32767 ) * 1280
                          #  bone.location[1] = ( pos2 / 32767 ) * 1280
                          #  bone.location[0] = ( pos3 / 32767 ) * 1280

                            bone.location[0] = ( pos1 / 32767 ) * 1280
                            bone.location[1] = ( pos2 / 32767 ) * 1280
                            bone.location[2] = ( pos3 / 32767 ) * 1280
                          # bone.location = pos
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
                      #  bone.location[2] = ( pos1 / 32767 ) * 1280
                      #  bone.location[1] = ( pos2 / 32767 ) * 1280
                      #  bone.location[0] = ( pos3 / 32767 ) * 1280
                        bone.location[0] = ( pos1 / 32767 ) * 1280
                        bone.location[1] = ( pos2 / 32767 ) * 1280
                        bone.location[2] = ( pos3 / 32767 ) * 1280
                       # bone.location = pos
                        bone.keyframe_insert("location")
           # for name, quat in quat_samples:
           # for name in quat_samples:
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
                  #  bone.rotation_quaternion = (quat[3], quat[1], quat[2], quat[3])
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

def read_ccs(self):
    reader = Reader(open(self.filepath, "rb").read(), self.filepath)
    get_endian(reader)

  #  vinit = get_version(reader)
  #  print("vinit", vinit)

    version = get_version(reader)
    reader.version = version
    print("version", version)
    if version == 0:
        version = get_version(reader)
        reader.version = version
        print("version", version)
        if version == 19:
            reader.seek(-4)
            
    # char clip
    version2 = get_version(reader)
    reader.version2 = version2
    print("version2", version2)
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
        reader.seek(4)
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
                            if version >= 16:
                            #   W
                                pos44 = reader.float32()
                                print("pos44", pos44)
                            if version3 > 12:
                                pos1 = pos11
                                pos2 = pos22
                                pos3 = pos33
                                if version >= 16:
                                    pos4 = pos44
                                if bone:
                                    bone.location[0] = pos1
                                    bone.location[1] = pos2
                                    bone.location[2] = pos3 
                                    bone.keyframe_insert("location")
                            else:
                                pos1 = pos11
                                pos2 = pos12
                                pos3 = pos13
                                if version >= 16:
                                    pos4 = pos44
                                if bone:
                                    # just for viseme anim import
                                    if (metadata_type == "viseme") and (version == 15):
                                        bone.location[2] = ( pos1 / 32767 ) * 1280
                                        bone.location[1] = ( pos2 / 32767 ) * 1280
                                        bone.location[0] = ( pos3 / 32767 ) * 1280
                                    else:
                                        bone.location[0] = ( pos1 / 32767 ) * 1280
                                        bone.location[1] = ( pos2 / 32767 ) * 1280
                                        bone.location[2] = ( pos3 / 32767 ) * 1280
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
                                if (metadata_type == "viseme") and (version == 15):
                                    bone.location[2] = ( pos1 / 32767 ) * 1280
                                    bone.location[1] = ( pos2 / 32767 ) * 1280
                                    bone.location[0] = ( pos3 / 32767 ) * 1280
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
                            pos11 = reader.float32()
                            print("pos11", pos11)
                            pos22 = reader.float32()
                            print("pos22", pos22)
                            pos33 = reader.float32()
                            print("pos33", pos33)
                            if version2 >= 17:
                            #   W
                                pos44 = reader.float32()
                                print("pos44", pos44)
                            if version3 > 12:
                                pos1 = pos11
                                pos2 = pos22
                                pos3 = pos33
                                if version2 >= 17:
                                    pos4 = pos44
                                if bone:
                                    if (metadata_type == "viseme") and (version == 15):
                                        bone.location[2] = pos1
                                        bone.location[1] = pos2
                                        bone.location[0] = pos3
                                    else:
                                        bone.location[0] = pos1
                                        bone.location[1] = pos2
                                        bone.location[2] = pos3 
                                    bone.keyframe_insert("location")
                            else:
                                pos1 = pos11
                                pos2 = pos12
                                pos3 = pos13
                                if version2 >= 17:
                                    pos4 = pos44
                                if bone:
                                    # just for viseme anim import
                                    if (metadata_type == "viseme") and (version == 15):
                                        bone.location[2] = ( pos1 / 32767 ) * 1280
                                        bone.location[1] = ( pos2 / 32767 ) * 1280
                                        bone.location[0] = ( pos3 / 32767 ) * 1280
                                    else:
                                        bone.location[0] = ( pos1 / 32767 ) * 1280
                                        bone.location[1] = ( pos2 / 32767 ) * 1280
                                        bone.location[2] = ( pos3 / 32767 ) * 1280
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
                                if (metadata_type == "viseme") and (version == 15):
                                    bone.location[2] = ( pos1 / 32767 ) * 1280
                                    bone.location[1] = ( pos2 / 32767 ) * 1280
                                    bone.location[0] = ( pos3 / 32767 ) * 1280
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
                          # dont know what the real values are sooo
                          # ¯\_(ツ)_/¯
                           # rotz = (rot1 / 32767.0) / 0.512 * 10.24
                            print("rotz", rotz)
                        if bone:
                            bone.rotation_mode = "XYZ"
                            bone.rotation_euler[2] = rotz
                            bone.keyframe_insert("rotation_euler")
        return
    flags = reader.uint32()
    print("flags", flags)
    play_flags = reader.uint32()
    print("play_flags", play_flags)
    blend_width = reader.float32()
    print("blend_width", blend_width)

    if version2 > 3:
        range1 = reader.float32()
        print("range1", range1)
    if version2 == 5:
        unknown_bool_1 = reader.milo_bool()
        print("unknown_bool_1", unknown_bool_1)
    elif version2 > 5:
        relative = reader.numstring()
        print("relative", relative)
    if ((version2 - 9) < 2):
#and ((version2 - 9) > 0):
        print("version2 - 9", version2 - 9)
        unknown_bool_2 = reader.milo_bool()
        print("unknown_bool_2", unknown_bool_2)
    if version2 > 9:
        usually_neg_1 = reader.int32()
        print("usually_neg_1", usually_neg_1)
    if version2 > 11:
        do_not_decompress = reader.milo_bool()
        print("do_not_decompress", do_not_decompress)
    if version2 < 8:
        node_count = reader.uint32()
        print("node_count", node_count)
        for i in range(node_count):
            name = reader.numstring()
            print("name", name)
            float_count = reader.uint32()
            print("float_count", float_count)
            for i in range(float_count):
                frame = reader.float32()
                weight = reader.float32()
                print("frame, weight", frame, weight)
    else:
        node_size = reader.uint32()
        print("node_size", node_size)
        node_count = reader.uint32()
        print("node_count", node_count)
        for i in range(node_count):
            name = reader.numstring()
            print("name", name)
            float_count = reader.uint32()
            print("float_count", float_count)
            for i in range(float_count):
                frame = reader.float32()
                weight = reader.float32()
                print("frame, weight", frame, weight)
    if version2 < 3:
        some_string_count = reader.int32()
        for i in range(some_string_count):
            a = reader.numstring()
    if version2 < 7:
        enter_event = reader.numstring()
        print("enter_event", enter_event)
        exit_event = reader.numstring()
        print("exit_event", exit_event)
        event_count = reader.int32()
        print("event_count", event_count)
        for i in range(event_count):
            frame = reader.float32()
            script = reader.numstring()
            print("frame, script", frame, script)
    else:
        event_count = reader.int32()
        print("event_count", event_count)
        for i in range(event_count):
            frame = reader.float32()
            script = reader.numstring()
            print("frame, script", frame, script)

    if version >= 16:
        some_bool = reader.milo_bool()
        print("some_bool", some_bool)
    if version < 13:
       # create_anim(self, reader)
        print("full", "'CharBonesSamples' gets called here'")
        bone_count1 = reader.int32()
        print("bone_count1", bone_count1)
        char_bones1 = []
        for i in range(bone_count1):
            char_bone1 = reader.numstring()
            print("char_bone1", char_bone1)
            weight1 = reader.float32()
            print("weight1", weight1)
            char_bones1.append(char_bone1)
        print("char_bones1", char_bones1)
        Counts1 = []
        count_size1 = 10
        for i in range(count_size1):
            Count1 = reader.uint32()
            print("Count1", Count1)
            Counts1.append(Count1)
        compression1 = reader.int32()
        print("compression1", compression1)
        num_samples1 = reader.int32()
        print("num_samples1", num_samples1)

        print("one", "'CharBonesSamples' gets called here'")

        bone_count2 = reader.int32()
        print("bone_count2", bone_count2)
        char_bones2 = []
        for i in range(bone_count2):
            char_bone2 = reader.numstring()
            print("char_bone2", char_bone2)
            weight2 = reader.float32()
            print("weight2", weight2)
            char_bones2.append(char_bone2)
        print("char_bones2", char_bones2)
        Counts2 = []
        count_size2 = 10
        for i in range(count_size2):
            Count2 = reader.uint32()
            print("Count2", Count2)
            Counts2.append(Count2)
        compression2 = reader.int32()
        print("compression2", compression2)
        num_samples2 = reader.int32()
        print("num_samples2", num_samples2)
       # create_anim(self, reader)

        if version > 7:
            print("ignore", "'CharBonesSamples' gets called here'")
            bone_count3 = reader.int32()
            print("bone_count3", bone_count3)
            char_bones3 = []
            for i in range(bone_count3):
                char_bone3 = reader.numstring()
                print("char_bone3", char_bone3)
                weight3 = reader.float32()
                print("weight3", weight3)
                char_bones3.append(char_bone3)
            print("char_bones3", char_bones3)
            Counts3 = []
            count_size3 = 10
            for i in range(count_size3):
                Count3 = reader.uint32()
                print("Count3", Count3)
                Counts3.append(Count3)
            compression3 = reader.int32()
            print("compression3", compression3)
            num_samples3 = reader.int32()
            print("num_samples3", num_samples3)

        print("full_data", "'CharBonesSamplesdata' gets called here'")
       # create_anim(self, reader)
        for i in range(num_samples1):
            print("frame", i)
            armature = bpy.context.active_object
            bpy.data.scenes["Scene"].frame_start = 0
            bpy.data.scenes["Scene"].frame_end = num_samples1 - 1
            current_frame = bpy.data.scenes[0].frame_current
            bpy.context.scene.frame_set(i)
            for name in char_bones1:
                if ".pos" in name:
                    print("name", name)
                    name = name.replace(".pos", ".mesh")
                    bone = armature.pose.bones.get(name)
                    if compression1 < 2:
                        pos1 = reader.float32()
                        print("pos1", pos1)
                        pos2 = reader.float32()
                        print("pos2", pos2)
                        pos3 = reader.float32()
                        print("pos3", pos3)
                        if bone:
                            if (metadata_type == "viseme") and (version == 15):
                                bone.location[2] = pos1
                                bone.location[1] = pos2
                                bone.location[0] = pos3 
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
                            if (metadata_type == "viseme") and (version == 15):
                                bone.location[2] = ( pos1 / 32767 ) * 1280
                                bone.location[1] = ( pos2 / 32767 ) * 1280
                                bone.location[0] = ( pos3 / 32767 ) * 1280
                            else:
                                bone.location[0] = ( pos1 / 32767 ) * 1280
                                bone.location[1] = ( pos2 / 32767 ) * 1280
                                bone.location[2] = ( pos3 / 32767 ) * 1280
                            bone.keyframe_insert("location")
                elif ".quat" in name:
                    print("name", name)
                    name = name.replace(".quat", ".mesh")
                    bone = armature.pose.bones.get(name)
                    if compression1 == 0:
                        quat1 = quat_math(reader.float32())
                        print("quat1", quat1)
                        quat2 = quat_math(reader.float32())
                        print("quat2", quat2)
                        quat3 = quat_math(reader.float32())
                        print("quat3", quat3)
                        quat4 = quat_math(reader.float32())
                        print("quat4", quat4)
                    elif compression1 < 3:
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
                elif ".rotx" in name:
                    print("rotX found")
                    print("rotX found")
                    print("rotX found")
                    print("rotX found")
                    print("rotX found")
                    print("rotX found")
                    print("rotX found")
                    print("rotX found")
                    print("rotX found")
                    print("rotX found")
                    print("name", name)
                    name = name.replace(".rotx", ".mesh")
                    bone = armature.pose.bones.get(name)
                    if compression == 0:
                        rotx = reader.float32()
                        print("rotx", rotx)
                    else:
                        rot1 = reader.short()
                        rotx = (rot1 / 32767.0) / 0.5 * 10.0
                      # dont know what the real values are sooo
                      # ¯\_(ツ)_/¯
                       # rotx = (rot1 / 32767.0) / 0.512 * 10.24
                        print("rotx", rotx)
                    if bone:
                        bone.rotation_mode = "XYZ"
                        bone.rotation_euler[0] = rotx
                        bone.keyframe_insert("rotation_euler") 
                elif ".roty" in name:
                    print("rotY found")
                    print("rotY found")
                    print("rotY found")
                    print("rotY found")
                    print("rotY found")
                    print("rotY found")
                    print("rotY found")
                    print("rotY found")
                    print("rotY found")
                    print("rotY found")
                    print("name", name)
                    name = name.replace(".roty", ".mesh")
                    bone = armature.pose.bones.get(name)
                    if compression == 0:
                        roty = reader.float32()
                        print("roty", roty)
                    else:
                        rot1 = reader.short()
                        roty = (rot1 / 32767.0) / 0.5 * 10.0
                      # dont know what the real values are sooo
                      # ¯\_(ツ)_/¯
                       # roty = (rot1 / 32767.0) / 0.512 * 10.24
                        print("roty", roty)
                    if bone:
                        bone.rotation_mode = "XYZ"
                        bone.rotation_euler[1] = roty
                        bone.keyframe_insert("rotation_euler") 
                elif ".rotz" in name:
                    print("name", name)
                    name = name.replace(".rotz", ".mesh")
                    bone = armature.pose.bones.get(name)
                    if compression1 == 0:
                        rotz = reader.float32()
                        print("rotz", rotz)
                    else:
                        rot1 = reader.short()
                        rotz = (rot1 / 32767.0) / 0.5 * 10.0
                        print("rotz", rotz, rot1)
                    if bone:
                        bone.rotation_mode = "XYZ"
                        bone.rotation_euler[2] = rotz
                        bone.keyframe_insert("rotation_euler") 

        print("one_data", "'CharBonesSamplesdata' gets called here'")
        for i in range(num_samples2):
            print("frame", i)
            armature = bpy.context.active_object
           # bpy.data.scenes["Scene"].frame_start = 0
           # bpy.data.scenes["Scene"].frame_end = num_samples1 - 1
            current_frame = bpy.data.scenes[0].frame_current
            bpy.context.scene.frame_set(i)
            for name in char_bones2:
                if ".pos" in name:
                    print("name", name)
                    name = name.replace(".pos", ".mesh")
                    bone = armature.pose.bones.get(name)
                    if compression2 < 2:
                        pos1 = reader.float32()
                        print("pos1", pos1)
                        pos2 = reader.float32()
                        print("pos2", pos2)
                        pos3 = reader.float32()
                        print("pos3", pos3)
                        if bone:
                           # bone.location[2] = pos1
                           # bone.location[1] = pos2
                           # bone.location[0] = pos3
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
                            if (metadata_type == "viseme") and (version == 15):
                                bone.location[2] = ( pos1 / 32767 ) * 1280
                                bone.location[1] = ( pos2 / 32767 ) * 1280
                                bone.location[0] = ( pos3 / 32767 ) * 1280
                            else:
                                bone.location[0] = ( pos1 / 32767 ) * 1280
                                bone.location[1] = ( pos2 / 32767 ) * 1280
                                bone.location[2] = ( pos3 / 32767 ) * 1280
                            bone.keyframe_insert("location")
                elif ".quat" in name:
                    print("name", name)
                    name = name.replace(".quat", ".mesh")
                    bone = armature.pose.bones.get(name)
                    if compression2 == 0:
                        quat1 = quat_math(reader.float32())
                        print("quat1", quat1)
                        quat2 = quat_math(reader.float32())
                        print("quat2", quat2)
                        quat3 = quat_math(reader.float32())
                        print("quat3", quat3)
                        quat4 = quat_math(reader.float32())
                        print("quat4", quat4)
                    elif compression2 < 3:
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
                elif ".rotx" in name:
                    print("rotX found")
                    print("rotX found")
                    print("rotX found")
                    print("rotX found")
                    print("rotX found")
                    print("rotX found")
                    print("rotX found")
                    print("rotX found")
                    print("rotX found")
                    print("rotX found")
                    print("name", name)
                    name = name.replace(".rotx", ".mesh")
                    bone = armature.pose.bones.get(name)
                    if compression == 0:
                        rotx = reader.float32()
                        print("rotx", rotx)
                    else:
                        rot1 = reader.short()
                        rotx = (rot1 / 32767.0) / 0.5 * 10.0
                      # dont know what the real values are sooo
                      # ¯\_(ツ)_/¯
                       # rotx = (rot1 / 32767.0) / 0.512 * 10.24
                        print("rotx", rotx)
                    if bone:
                        bone.rotation_mode = "XYZ"
                        bone.rotation_euler[0] = rotx
                        bone.keyframe_insert("rotation_euler") 
                elif ".roty" in name:
                    print("rotY found")
                    print("rotY found")
                    print("rotY found")
                    print("rotY found")
                    print("rotY found")
                    print("rotY found")
                    print("rotY found")
                    print("rotY found")
                    print("rotY found")
                    print("rotY found")
                    print("name", name)
                    name = name.replace(".roty", ".mesh")
                    bone = armature.pose.bones.get(name)
                    if compression == 0:
                        roty = reader.float32()
                        print("roty", roty)
                    else:
                        rot1 = reader.short()
                        roty = (rot1 / 32767.0) / 0.5 * 10.0
                      # dont know what the real values are sooo
                      # ¯\_(ツ)_/¯
                       # roty = (rot1 / 32767.0) / 0.512 * 10.24
                        print("roty", roty)
                    if bone:
                        bone.rotation_mode = "XYZ"
                        bone.rotation_euler[1] = roty
                        bone.keyframe_insert("rotation_euler") 
                elif ".rotz" in name:
                    print("name", name)
                    name = name.replace(".rotz", ".mesh")
                    bone = armature.pose.bones.get(name)
                    if compression2 == 0:
                        rotz = reader.float32()
                        print("rotz", rotz)
                    else:
                        rot1 = reader.short()
                        rotz = (rot1 / 32767.0) / 0.5 * 10.0
                        print("rotz", rotz, rot1)
                    if bone:
                        bone.rotation_mode = "XYZ"
                        bone.rotation_euler[2] = rotz
                        bone.keyframe_insert("rotation_euler")
    else:
       # vinit = get_version(reader)
       # print("vinit", vinit)
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
                            if version3 >= 16:
                            #   W
                                pos44 = reader.float32()
                                print("pos44", pos44)
                            if version3 > 12:
                                pos1 = pos11
                                pos2 = pos22
                                pos3 = pos33
                                if version3 >= 16:
                                    pos4 = pos44
                                if bone:
                                    if (metadata_type == "viseme") and (version == 15):
                                        bone.location[2] = ( pos1 / 32767 ) * 1280
                                        bone.location[1] = ( pos2 / 32767 ) * 1280
                                        bone.location[0] = ( pos3 / 32767 ) * 1280
                                    else:
                                        bone.location[0] = ( pos1 / 32767 ) * 1280
                                        bone.location[1] = ( pos2 / 32767 ) * 1280
                                        bone.location[2] = ( pos3 / 32767 ) * 1280
                                  # bone.location = pos
                                    bone.keyframe_insert("location")
                            else:
                                pos1 = pos11
                                pos2 = pos12
                                pos3 = pos13
                                if version3 >= 16:
                                    pos4 = pos44
                                if bone:
                                    if (metadata_type == "viseme") and (version == 15):
                                        bone.location[2] = ( pos1 / 32767 ) * 1280
                                        bone.location[1] = ( pos2 / 32767 ) * 1280
                                        bone.location[0] = ( pos3 / 32767 ) * 1280
                                    else:
                                        bone.location[0] = ( pos1 / 32767 ) * 1280
                                        bone.location[1] = ( pos2 / 32767 ) * 1280
                                        bone.location[2] = ( pos3 / 32767 ) * 1280
                                  # bone.location = pos
                                    bone.keyframe_insert("location")
                        else:
                            pos1 = reader.short()
                            print("pos1", pos1)
                            pos2 = reader.short()
                            print("pos2", pos2)
                            pos3 = reader.short()
                            print("pos3", pos3)
                            if bone:
                                if (metadata_type == "viseme") and (version == 15):
                                    bone.location[2] = ( pos1 / 32767 ) * 1280
                                    bone.location[1] = ( pos2 / 32767 ) * 1280
                                    bone.location[0] = ( pos3 / 32767 ) * 1280
                                else:
                                    bone.location[0] = ( pos1 / 32767 ) * 1280
                                    bone.location[1] = ( pos2 / 32767 ) * 1280
                                    bone.location[2] = ( pos3 / 32767 ) * 1280
                               # bone.location = pos
                                bone.keyframe_insert("location")
                   # for name, quat in quat_samples:
                   # for name in quat_samples:
                    elif ".quat" in name:
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
                          #  bone.rotation_quaternion = (quat[3], quat[1], quat[2], quat[3])
                            bone.rotation_quaternion = (quat4, quat1, quat2, quat3)
                            bone.keyframe_insert("rotation_quaternion")
                    elif ".rotx" in name:
                        print("rotX found")
                        print("rotX found")
                        print("rotX found")
                        print("rotX found")
                        print("rotX found")
                        print("rotX found")
                        print("rotX found")
                        print("rotX found")
                        print("rotX found")
                        print("rotX found")
                        print("name", name)
                        name = name.replace(".rotx", ".mesh")
                        bone = armature.pose.bones.get(name)
                        if compression == 0:
                            rotx = reader.float32()
                            print("rotx", rotx)
                        else:
                            rot1 = reader.short()
                            rotx = (rot1 / 32767.0) / 0.5 * 10.0
                          # dont know what the real values are sooo
                          # ¯\_(ツ)_/¯
                           # rotx = (rot1 / 32767.0) / 0.512 * 10.24
                            print("rotx", rotx)
                        if bone:
                            bone.rotation_mode = "XYZ"
                            bone.rotation_euler[0] = rotx
                            bone.keyframe_insert("rotation_euler") 
                    elif ".roty" in name:
                        print("rotY found")
                        print("rotY found")
                        print("rotY found")
                        print("rotY found")
                        print("rotY found")
                        print("rotY found")
                        print("rotY found")
                        print("rotY found")
                        print("rotY found")
                        print("rotY found")
                        print("name", name)
                        name = name.replace(".roty", ".mesh")
                        bone = armature.pose.bones.get(name)
                        if compression == 0:
                            roty = reader.float32()
                            print("roty", roty)
                        else:
                            rot1 = reader.short()
                            roty = (rot1 / 32767.0) / 0.5 * 10.0
                          # dont know what the real values are sooo
                          # ¯\_(ツ)_/¯
                           # roty = (rot1 / 32767.0) / 0.512 * 10.24
                            print("roty", roty)
                        if bone:
                            bone.rotation_mode = "XYZ"
                            bone.rotation_euler[1] = roty
                            bone.keyframe_insert("rotation_euler") 
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
                bpy.data.scenes["Scene"].frame_start = 0
               # bpy.data.scenes["Scene"].frame_end = num_samples - 1
               # current_frame = bpy.data.scenes[0].frame_current
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
                            if version3 >= 16:
                            #   W
                                pos44 = reader.float32()
                                print("pos44", pos44)
                            if version3 > 12:
                                pos1 = pos11
                                pos2 = pos22
                                pos3 = pos33
                                if version3 >= 16:
                                    pos4 = pos44
                            else:
                                pos1 = pos11
                                pos2 = pos12
                                pos3 = pos13
                                if version3 >= 16:
                                    pos4 = pos44
                                if bone:
                                    # just for viseme anim import
                                    if (metadata_type == "viseme") and (version == 15):
                                        bone.location[2] = ( pos1 / 32767 ) * 1280
                                        bone.location[1] = ( pos2 / 32767 ) * 1280
                                        bone.location[0] = ( pos3 / 32767 ) * 1280
                                    else:
                                        bone.location[0] = ( pos1 / 32767 ) * 1280
                                        bone.location[1] = ( pos2 / 32767 ) * 1280
                                        bone.location[2] = ( pos3 / 32767 ) * 1280
                                  # bone.location = pos
                                    bone.keyframe_insert("location")
                        else:
                            pos1 = reader.short()
                            print("pos1", pos1)
                            pos2 = reader.short()
                            print("pos2", pos2)
                            pos3 = reader.short()
                            print("pos3", pos3)
                            if bone:
                                if (metadata_type == "viseme") and (version == 15):
                                    bone.location[2] = ( pos1 / 32767 ) * 1280
                                    bone.location[1] = ( pos2 / 32767 ) * 1280
                                    bone.location[0] = ( pos3 / 32767 ) * 1280
                                else:
                                    bone.location[0] = ( pos1 / 32767 ) * 1280
                                    bone.location[1] = ( pos2 / 32767 ) * 1280
                                    bone.location[2] = ( pos3 / 32767 ) * 1280
                               # bone.location = pos
                                bone.keyframe_insert("location")
                   # for name, quat in quat_samples:
                   # for name in quat_samples:
                    elif ".quat" in name:
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
                          #  bone.rotation_quaternion = (quat[3], quat[1], quat[2], quat[3])
                            bone.rotation_quaternion = (quat4, quat1, quat2, quat3)
                            bone.keyframe_insert("rotation_quaternion")
                    elif ".rotx" in name:
                        print("rotX found")
                        print("rotX found")
                        print("rotX found")
                        print("rotX found")
                        print("rotX found")
                        print("rotX found")
                        print("rotX found")
                        print("rotX found")
                        print("rotX found")
                        print("rotX found")
                        print("name", name)
                        name = name.replace(".rotx", ".mesh")
                        bone = armature.pose.bones.get(name)
                        if compression == 0:
                            rotx = reader.float32()
                            print("rotx", rotx)
                        else:
                            rot1 = reader.short()
                            rotx = (rot1 / 32767.0) / 0.5 * 10.0
                          # dont know what the real values are sooo
                          # ¯\_(ツ)_/¯
                           # rotx = (rot1 / 32767.0) / 0.512 * 10.24
                            print("rotx", rotx)
                        if bone:
                            bone.rotation_mode = "XYZ"
                            bone.rotation_euler[0] = rotx
                            bone.keyframe_insert("rotation_euler") 
                    elif ".roty" in name:
                        print("rotY found")
                        print("rotY found")
                        print("rotY found")
                        print("rotY found")
                        print("rotY found")
                        print("rotY found")
                        print("rotY found")
                        print("rotY found")
                        print("rotY found")
                        print("rotY found")
                        print("name", name)
                        name = name.replace(".roty", ".mesh")
                        bone = armature.pose.bones.get(name)
                        if compression == 0:
                            roty = reader.float32()
                            print("roty", roty)
                        else:
                            rot1 = reader.short()
                            roty = (rot1 / 32767.0) / 0.5 * 10.0
                          # dont know what the real values are sooo
                          # ¯\_(ツ)_/¯
                           # roty = (rot1 / 32767.0) / 0.512 * 10.24
                            print("roty", roty)
                        if bone:
                            bone.rotation_mode = "XYZ"
                            bone.rotation_euler[1] = roty
                            bone.keyframe_insert("rotation_euler") 
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
                        print("unknown bone suffix", name)
                        print("unknown bone suffix", name)
                        print("unknown bone suffix", name)
                        print("unknown bone suffix", name)
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

    if version > 14:
        bone_count = reader.int32()
        print("bone_count", bone_count)
        char_bones2 = []
        for i in range(bone_count):
            char_bone = reader.numstring()
            print("char_bone", char_bone)
            weight = reader.float32()
            print("weight", weight)
            char_bones2.append(char_bone)
    if (metadata_type == "viseme"):
        extension = ".vsm"
       # extension = ".ccs"
        bpy.data.actions["ArmatureAction"].name = os.path.splitext(os.path.basename(self.filepath))[0] + extension
        print("file", bpy.path.basename(os.path.splitext(os.path.basename(self.filepath))[0] + extension))
    else:
       # bpy.data.actions["ArmatureAction"].name = bpy.path.basename(self.filepath)
        print("file", bpy.path.basename(self.filepath))
   # bpy.ops.nla.action_pushdown(track_index=1)
   # bpy.ops.action.push_down()
   # create_anim(self, reader)
