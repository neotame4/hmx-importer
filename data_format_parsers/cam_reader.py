import bpy
import mathutils
from .. common import *
from .. bpy_util_funcs import *
from . trans_reader import *
from . draw_reader import *


def read_cam(reader, name, super: bool) -> None:
    version = reader.int32()
    print("name, version", name, version)
    if version > 10:
        metadata = read_metadata(reader, False) 
   # parent, local_xfm, world_xfm = read_trans(reader, True, name)
   # print("parent, local_xfm, world_xfm", parent, local_xfm, world_xfm)
    trans_version, trans_count, trans_objects, parent, local_xfm, world_xfm = read_trans(reader, True, name)
   # print("trans_version, trans_count, trans_objects, parent, local_xfm, world_xfm", trans_version, trans_count, trans_objects, parent, local_xfm, world_xfm)
    if version < 10:
        read_draw(reader, True)
    near_plane = reader.float32()
    far_plane = reader.float32()
    y_fov = reader.float32()
    screen_rect = reader.vec4f()
    z_range = reader.vec2f()
    target_tex = reader.numstring()  
    print("near_plane, far_plane, y_fov, screen_rect, z_range, target_tex", near_plane, far_plane, y_fov, screen_rect, z_range, target_tex)
    bpy.ops.object.camera_add()
    camera = bpy.context.object
    camera.name = name
    camera.data.clip_start = near_plane
    camera.data.clip_end = far_plane
    camera.data.angle_y = y_fov
    obj = camera
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
    if obj.parent != None:
        camera.matrix_local = mathutils.Matrix((
            (local_xfm[0], local_xfm[3], local_xfm[6], local_xfm[9],),
            (local_xfm[1], local_xfm[4], local_xfm[7], local_xfm[10],),
            (local_xfm[2], local_xfm[5], local_xfm[8], local_xfm[11],),
            (0.0, 0.0, 0.0, 1.0),
        ))  
    else:
        camera.matrix_world = mathutils.Matrix((
            (world_xfm[0], world_xfm[3], world_xfm[6], world_xfm[9],),
            (world_xfm[1], world_xfm[4], world_xfm[7], world_xfm[10],),
            (world_xfm[2], world_xfm[5], world_xfm[8], world_xfm[11],),
            (0.0, 0.0, 0.0, 1.0),
        ))
    camera.rotation_euler[0] = camera.rotation_euler[0] + 1.5707964
    print("Imported Camera:", name)