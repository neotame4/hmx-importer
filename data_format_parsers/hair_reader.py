import bpy
import mathutils
from .. common import *
from .. bpy_util_funcs import *
from . trans_reader import *
from . draw_reader import *

def CharHairPointTBRB(reader) -> list:
    unknown1_1 = reader.float32()
    unknown1_2 = reader.float32()
    unknown1_3 = reader.float32()
    print("unknown1_1, unknown1_2, unknown1_3", unknown1_1, unknown1_2, unknown1_3)

    bone = reader.numstring()		# hair bone we set the transform of
    print("bone", bone)

    unknown2_1 = reader.float32()
    unknown2_2 = reader.float32()
    unknown2_3 = reader.float32()
    unknown2_4 = reader.float32()
    print("unknown2_1, unknown2_2, unknown2_3, unknown2_4", unknown2_1, unknown2_2, unknown2_3, unknown2_4)

    unknown3_1 = reader.float32()
    unknown3_2 = reader.float32()
    unknown3_3 = reader.float32()
    print("unknown3_1, unknown3_2, unknown3_3", unknown3_1, unknown3_2, unknown3_3)

def CharHairStrandTBRB(reader) -> list:
    root = reader.numstring()		# Trans - The root Trans for the hair strand
    print("root", root)
    angle = reader.float32()		# Angle in degrees of starting flip
    print("angle", angle)

    points_count = reader.int32()
    print("points_count", points_count)
    for _ in range(points_count):
        print("count", _)
        CharHairPointTBRB(reader)

    # Contains rotation + scale data
    # Note: Both values are usually the same
    mat_1 = reader.matrix3()		# ??? 0x20
    print("mat_1", mat_1)
    mat_2 = reader.matrix3()		# root_mat 0x50
    print("mat_2", mat_2)

    unknown_int = reader.int32()	# 0, 1, 65, 68, 76, 129, 141, 193
    print("unknown_int", unknown_int)

def CharHairPoint(reader) -> list:
    unknown_floats = reader.vec3f()	# Origin?
    print("unknown_floats", unknown_floats)
    bone = reader.numstring()		# Trans - Hair bone we set the transform of
    print("bone", bone)

    length = reader.float32()		# The length of this strand bone
    print("length", length)
    collide_type = reader.int32()	# Type of collision
    print("collide_type", collide_type)
    collision = reader.numstring()	# Trans - Collision sphere
    print("collision", collision)

    distance = reader.float32()		# Collision radius (0.0, 5.0, 6.5)
    print("distance", distance)
    # If positive, is the distance the bone should start aligning itself with the collision primitive,
    #  so that once touching it, it will be totally flattened against it.
    # Values: 0.0
    align_dist = reader.float32()
    print("align_dist", align_dist)

    # No "show_collide" bool? Probably just not encoded in binary.


def CharHairStrand(reader) -> list:
    root = reader.numstring()		# Trans - The root Trans for the hair strand
    print("root", root)
    angle = reader.float32()		# Angle in degrees of starting flip
    print("angle", angle)

    points_count = reader.int32()
    print("points_count", points_count)
    for _ in range(points_count):
        print("count", _)
        CharHairPoint(reader)

    # Contains rotation + scale data
    # Note: Both values are usually the same
    mat_1 = reader.matrix3()		# ??? 0x20
    print("mat_1", mat_1)
    mat_2 = reader.matrix3()		# root_mat 0x50
    print("mat_2", mat_2)

def read_hair(reader, name, super: bool) -> None:
    version = reader.int32()
    print("hair", "name, version", name, version)
    read_metadata(reader, False)   

    stiffness = reader.float32()	# stiffness of each strand
    torsion = reader.float32()		# rotational stiffness of each strand
    inertia = reader.float32()		# Inertia of the hair, zero means none
    gravity = reader.float32()		# Gravity of the hair, one is normal

    weight = reader.float32()		# Gravity of the hair, one is normal (duplicate dev comment?)
    friction = reader.float32()		# Hair friction against each other
    print("stiffness, torsion, inertia, gravity, weight, friction", stiffness, torsion, inertia, gravity, weight, friction)
    if version >=11:
        min_slack = reader.float32()	# If using sides, determines how far in it could go
        max_slack = reader.float32()	# If using sides, determines how far out it could go
        print("min_slack, max_slack", min_slack, max_slack)
    strand_count = reader.int32()
    print("strand_count", strand_count)
    for _ in range(strand_count):
        print("count", _)
        if version >=11:
            CharHairStrandTBRB(reader)
        else:
            CharHairStrand(reader)
    simulate = reader.milo_bool()	# Simulate physics or not
    print("simulate", simulate)

    if version >=11:
        wind = reader.numstring()	# wind object to use
        print("wind", wind)
   # find_next_file(reader)
    return