import bpy
import mathutils
from mathutils import Vector, Quaternion, Matrix
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

def get_edit_bone_world_matrix(armature_obj, bone_name):
    bpy.context.view_layer.objects.active = armature_obj
    bpy.ops.object.mode_set(mode='EDIT')
    eb = armature_obj.data.edit_bones.get(bone_name)
    if not eb:
        bpy.ops.object.mode_set(mode='POSE')
        return None
    mat = eb.matrix.copy()
    parent = eb.parent
    while parent:
        mat = parent.matrix @ mat
        parent = parent.parent
    bpy.ops.object.mode_set(mode='POSE')
    return mat

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
       # reader.seek(17)
        egg1 = reader.int32()     # node count
        egg2 = reader.numstring()  # clip
        egg3 = reader.int32()     # node count
        egg4 = reader.int32()     # node count
        egg5 = reader.byte()     # node count
        print("egg1, egg2, egg3, egg4, egg5", egg1, egg2, egg3, egg4, egg5)
        transitions_count = reader.uint32()
        for _ in range(transitions_count):
            reader.numstring()  # clip
            reader.uint32()     # node count
            reader.float32()    # cur_beat
            reader.float32()    # next_beat
        reader.uint32()         # Junk1
        if metadata_type == "viseme":
            reader.uint32()     # Junk2

    get_version(reader)  # version3
    bone_count = reader.int32()
    char_bones = []
    for _ in range(bone_count):
        reader.numstring() 
#for _ in range(bone_count)
        reader.float32()  # weight

    count_size = 7 if version >= 16 else 10
    Counts = [reader.uint32() for _ in range(count_size)]
    compression = reader.int32()
    SampleSize = 0
    if compression < 2:
        SampleSize += 12 * Counts[1]
    else:
        SampleSize += 6 * Counts[1]
    SampleSize += (16 if compression == 0 else 8 if compression < 3 else 4) * (Counts[3] - Counts[1])
    SampleSize += (4 if compression == 0 else 2) * (Counts[6] - Counts[3])
    SampleSizet = (SampleSize + 0xF) & 0xFFFFFFF

    num_samples = reader.int32()
    num_frames = reader.int32()
    if version >= 12:
        for _ in range(num_frames):
            reader.float32()

    armature = bpy.context.active_object
    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = num_samples - 1

    # Get rest pose matrices once
    edit_bone_matrices = {
        name.replace(".quat", ".mesh").replace(".pos", ".mesh").replace(".rotz", ".mesh"): 
        get_edit_bone_world_matrix(armature, name.replace(".quat", ".mesh").replace(".pos", ".mesh").replace(".rotz", ".mesh"))
        for name in char_bones
    }

    bone_states = {}

    for frame in range(num_samples):
        bpy.context.scene.frame_set(frame)
        Start = reader.tell()

        for name in char_bones:
            base_name = name.replace(".pos", ".mesh").replace(".quat", ".mesh").replace(".rotz", ".mesh")
            bone = armature.pose.bones.get(base_name)
            if not bone:
                continue

            bone_state = bone_states.setdefault(base_name, {"pos": None, "quat": None})

            # Read and decode
            if ".pos" in name:
                if compression < 2:
                    x, y, z, _ = reader.float32(), reader.float32(), reader.float32(), reader.float32()
                else:
                    x, y, z = reader.short(), reader.short(), reader.short()
                    x, y, z = pos_math(x), pos_math(y), pos_math(z)
                bone_state["pos"] = Vector((x, y, z))

            elif ".quat" in name:
                if compression == 0:
                    qx, qy, qz, qw = reader.float32(), reader.float32(), reader.float32(), reader.float32()
                elif compression < 3:
                    qx, qy, qz, qw = [quat_math(reader.short()) for _ in range(4)]
                else:
                    qx, qy, qz, qw = [quat_math(reader.byte()) for _ in range(4)]
                bone_state["quat"] = Quaternion((qw, qx, qy, qz))

            elif ".rotz" in name:
                rotz = reader.float32() if compression == 0 else rotz_math(reader.short())
                bone_state["quat"] = mathutils.Euler((0, 0, rotz), 'XYZ').to_quaternion()

            # Construct matrix from state
            if bone_state["pos"] and bone_state["quat"]:
                t = bone_state["pos"]
                q = bone_state["quat"]
                anim_world_matrix = Matrix.Translation(t) @ q.to_matrix().to_4x4()

                rest_world = edit_bone_matrices.get(base_name)
                if rest_world:
                    local_matrix = rest_world.inverted() @ anim_world_matrix
                    bone.matrix_basis = local_matrix
                    bone.keyframe_insert("location", frame=frame)
                    bone.keyframe_insert("rotation_quaternion", frame=frame)

        End = reader.tell()
        computed_sizes = [0] * count_size
        for i in range(count_size - 1):
            curr = Counts[i]
            next_ = Counts[i + 1]
            type_size = 16 if compression == 0 and i == 2 else get_type_size(compression, i)
            computed_sizes[i + 1] = computed_sizes[i] + (next_ - curr) * type_size
        final_sample_size = (computed_sizes[-1] + 0xF) & 0xFFFFFFF0
        reader.seek(final_sample_size - (End - Start))

    print("Finished importing:", bpy.path.basename(self.filepath))
