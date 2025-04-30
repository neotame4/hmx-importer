import bpy
import mathutils
from .. common import *
from . anim_reader import *
from .. bpy_util_funcs import *
from . trans_reader import *
from . draw_reader import *


def read_group(reader, name, super: bool) -> None:
    print("Reading Group", name, "at offset", reader.tell())
    version = reader.int32()
    print("name, version", name, version)
    if version > 7:
        read_metadata(reader, False)
    read_anim(reader, True)
   # parent, local_xfm, world_xfm = read_trans(reader, True, name)
   # print("parent, local_xfm, world_xfm", parent, local_xfm, world_xfm)
    trans_version, trans_count, trans_objects, parent, local_xfm, world_xfm = read_trans(reader, True, name)
    print("trans_version, trans_count, trans_objects, parent, local_xfm, world_xfm", trans_version, trans_count, trans_objects, parent, local_xfm, world_xfm)
    read_draw(reader, True)
    if version > 10:
        objects = []
        objects_count = reader.int32()
        print("objects_count", objects_count)
        for _ in range(objects_count):
            object = reader.numstring()
            print("object", object)
        if version < 16:
            environ = reader.numstring()
            print("environ", environ)
        if version < 13:
            print("Releases some object resource here...")
    #   this was just for PHASE
       # elif version == 13:
       #     egg = reader.int32()
       #     return
        else:
            draw_only = reader.numstring()
            print("draw_only", draw_only)
    if version > 11 and version < 16:
        lod = reader.numstring()
        lod_screen_size = reader.float32()
        print("lod, lod_screen_size", lod, lod_screen_size)
    elif version == 4:
        some_number_1 = reader.uint32()
        objects = []
        objects_count = reader.int32()
        for _ in range(objects_count):
            object = reader.numstring()
            print("object", object)
        some_name = reader.numstring()
        some_number_2 = reader.uint32()
        some_number_3 = reader.uint32()

    elif version == 7:
        some_name = reader.numstring()
        lod_width = reader.float32()
        lod_height = reader.float32()
        print("some_name, lod_width, lod_height", some_name, lod_width, lod_height)
    if version > 13:
        sort_in_world = reader.milo_bool()
        print("sort_in_world", sort_in_world)
    obj = bpy.data.objects.get(name)
    if obj == None:
        obj = bpy.data.objects.new(name, None)  
        obj.empty_display_size = 2
        obj.empty_display_type = 'PLAIN_AXES'
    if len(parent) > 0 and "bone" not in parent:
        try:
            o = bpy.data.objects.get(parent)
            if o:
                obj.parent = o
            else:
                o = bpy.data.objects.new(parent, None)
                bpy.context.scene.collection.objects.link(o)
                o.empty_display_size = 2
                o.empty_display_type = 'PLAIN_AXES'
                obj.parent = o
        except:
            pass
    try:
        bpy.context.scene.collection.objects.link(obj)
    except:
        print(obj, "Object already in collection 'Scene Collection'")
        pass
    if obj.parent != None:
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
   # return