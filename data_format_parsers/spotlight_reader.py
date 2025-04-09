import bpy
import mathutils
from .. common import *
from .. bpy_util_funcs import *
from . trans_reader import *
from . draw_reader import *

def read_spotlight(reader, name: str, self) -> None:
    print("Reading Spotlight", name, "at offset", reader.tell())
    version = reader.int32()
    print("version", version)
    if version > 3:
        read_metadata(reader, False)
    read_draw(reader, True)
    parent, local_xfm, world_xfm = read_trans(reader, True, name)
    print("parent, local_xfm, world_xfm", parent, local_xfm, world_xfm)
   # trans_version, trans_count, trans_objects, parent, local_xfm, world_xfm = read_trans(reader, True, name)
   # print("trans_version, trans_count, trans_objects, parent, local_xfm, world_xfm", trans_version, trans_count, trans_objects, parent, local_xfm, world_xfm)
    ignore_data = reader.uint32()
    ignore_data2 = reader.uint32()
    ignore_data3 = reader.uint32()
    ignore_data4 = reader.uint32()
    ignore_data5 = reader.uint32()
    ignore_data6 = reader.uint32()
    ignore_data7 = reader.uint32()
    ignore_data8 = reader.byte()
    ignore_data9 = reader.uint32()
    print("ignore_data, ignore_data2, ignore_data3, ignore_data4, ignore_data5, ignore_data6, ignore_data7, ignore_data8, ignore_data9", ignore_data, ignore_data2, ignore_data3, ignore_data4, ignore_data5, ignore_data6, ignore_data7, ignore_data8, ignore_data9)
    Material = reader.numstring()
    print("Material", Material)

    ignore_data = reader.uint32()
    ignore_data2 = reader.uint32()
    ignore_data3 = reader.uint32()
    ignore_data4 = reader.uint32()
    ignore_data5 = reader.uint32()
    ignore_data6 = reader.uint32()
    ignore_data7 = reader.uint32()
    print("ignore_data, ignore_data2, ignore_data3, ignore_data4, ignore_data5, ignore_data6, ignore_data7", ignore_data, ignore_data2, ignore_data3, ignore_data4, ignore_data5, ignore_data6, ignore_data7)

    meshname = reader.numstring()
    print("meshname", meshname)
    Target = reader.numstring()
    print("Target", Target)

    filler = reader.vec3f()
    print("filler", filler)
    if meshname != None:
        mesh = bpy.data.meshes.get(meshname)
        print("mesh, meshname", mesh, meshname)
    else:
        print("mesh", mesh, "doesnt exist, Creating", meshname)
        mesh = bpy.data.meshes.new(meshname)
    print("name, mesh, meshname", name, mesh, meshname)
    spotlight_obj = bpy.data.objects.new(name, mesh)
   # spotlight_obj = bpy.data.objects.get(name, mesh)  
    if len(parent) > 0 and "bone" not in parent:
        try:
            o = bpy.data.objects.get(parent)
            if o:
                spotlight_obj.parent = o
            else:
                o = bpy.data.objects.new(parent, None)
                bpy.context.scene.collection.objects.link(o)
                o.empty_display_size = 2
                o.empty_display_type = 'PLAIN_AXES'
                spotlight_obj.parent = o
        except:
            pass
    bpy.context.scene.collection.objects.link(spotlight_obj)
    if spotlight_obj.parent != None:
        spotlight_obj.matrix_local = mathutils.Matrix((
            (local_xfm[0], local_xfm[3], local_xfm[6], local_xfm[9],),
            (local_xfm[1], local_xfm[4], local_xfm[7], local_xfm[10],),
            (local_xfm[2], local_xfm[5], local_xfm[8], local_xfm[11],),
            (0.0, 0.0, 0.0, 1.0),
        ))  
    else:
        spotlight_obj.matrix_world = mathutils.Matrix((
            (world_xfm[0], world_xfm[3], world_xfm[6], world_xfm[9],),
            (world_xfm[1], world_xfm[4], world_xfm[7], world_xfm[10],),
            (world_xfm[2], world_xfm[5], world_xfm[8], world_xfm[11],),
            (0.0, 0.0, 0.0, 1.0),
        ))
   # o = bpy.data.objects.get(parent)
    obj = bpy.ops.object.light_add(type='SPOT', rotation=(1.5707964, 0.0, 0.0))
    light = bpy.context.object
   # light.data.type = 'SPOT'
   # light.data.color = color
   # light.data.energy = intensity
    light.name = name
  #  if light.parent != None:
  #      light.matrix_world = mathutils.Matrix((
  #          (world_xfm[0], world_xfm[3], world_xfm[6], 0.0,),
  #          (world_xfm[1], world_xfm[4], world_xfm[7], 0.0,),
  #          (world_xfm[2], world_xfm[5], world_xfm[8], 0.0,),
  #         # (world_xfm[0], world_xfm[3], world_xfm[6], world_xfm[9],),
  #         # (world_xfm[1], world_xfm[4], world_xfm[7], world_xfm[10],),
  #         # (world_xfm[2], world_xfm[5], world_xfm[8], world_xfm[11],),
  #          (0.0, 0.0, 0.0, 1.0),
  #      ))
   # obj = bpy.data.objects.new(meshname, mesh)  
   # try:
   # o = bpy.data.objects.get(spotlight_obj)
    o = bpy.data.objects.get(name)
    print("light object, o, is", o)
    if o:
        light.parent = o
    else:
        print("light parent doesnt exist, Creating")
        o = bpy.data.objects.new(spotlight_obj, None)
        bpy.context.scene.collection.objects.link(o)
        o.empty_display_size = 2
        o.empty_display_type = 'PLAIN_AXES'
        light.parent = o
    bpy.context.scene.collection.objects.link(light)
   # except:
   #     print("light parent failed")
   #     pass
    print("Imported SpotLight:", name)
   # file_size = 
    find_next_file(reader)
   # print("file_size", file_size)
   # if file_size == -1:
   #     return
   # file = f.read(file_size)
   # return
# very hacky
# 10/10 