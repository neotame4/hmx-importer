import bpy
import mathutils
from .. common import *
from .. bpy_util_funcs import *
from . trans_reader import *
from . draw_reader import *

def read_lit(reader, name: str, self) -> None:
    print("Reading Light", name, "at offset", reader.tell())
    version = reader.int32()
    if version > 3:
        read_metadata(reader, False)
     # trans
    parent, local_xfm, world_xfm = read_trans(reader, True, name)
    print("parent, local_xfm, world_xfm", parent, local_xfm, world_xfm)
    color = reader.vec3f()
    print("color", color)
    if version <= 3:
        intensity = reader.int32()
    else:
        intensity = reader.float32()

    if version < 2:
        ignore_datac1 = 8
        for _ in range(ignore_datac1):
            ignore_data_1 = reader.float32()
    if version < 3:
        ignore_datac2 = 2
        for _ in range(ignore_datac2):
            ignore_data_2 = reader.float32()
    Range = reader.float32()
    if version < 3:
        ignore_datac3 = 3
        for _ in range(ignore_datac3):
            ignore_data_3 = reader.float32()

    if version > 0:
        light_type_enum = reader.float32()
# light_type_enum / light types in game
#    kLightPoint,
#    kLightDirectional,
#    kLightFakeSpot,
#    kLightFloorSpot,
#    kLightShadowRef

    if version > 11:
        falloff_start = reader.float32()
    if version > 5:
        animate_color_from_preset = reader.milo_bool()
        animate_position_from_preset = reader.milo_bool()
    if version > 6:
        topradius = reader.float32()
        botradius = reader.float32()
        smoothness = reader.float32()
        sisplacement = reader.float32()
    if version > 7:
        texture = reader.numstring()
        if version == 9:
            string_count = reader.uint32()
            for _ in range(string_count):
                some_strings = reader.numstring()
        elif version == 9:
            string_count = reader.uint32()
            for _ in range(string_count):
                some_strings = reader.numstring()
    if version > 10:
        color_owner = reader.numstring()
    if version > 12:
        tex_xfm = reader.matrix()
    if version > 13:
        only_projection = reader.milo_bool()
    obj = bpy.ops.object.light_add(type='POINT')
    light = bpy.context.object
    light.data.type = 'POINT'
    light.data.color = color
    light.data.energy = intensity
    light.name = name
    light.matrix_world = mathutils.Matrix((
        (world_xfm[0], world_xfm[3], world_xfm[6], world_xfm[9],),
        (world_xfm[1], world_xfm[4], world_xfm[7], world_xfm[10],),
        (world_xfm[2], world_xfm[5], world_xfm[8], world_xfm[11],),
        (0.0, 0.0, 0.0, 1.0),
    ))
    light.rotation_euler[0] = light.rotation_euler[0] + 1.5707964
    print("Imported Light:", name)