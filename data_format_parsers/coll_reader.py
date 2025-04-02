from .. common import *
from .. bpy_util_funcs import *
from . trans_reader import *
import bmesh

def read_coll(reader, name: str, self) -> None:
   # coll_data["coll_name"] = name
    print("Reading coll", name, "at offset", reader.tell())
    version = reader.int32()
    read_metadata(reader, super)
    parent, local_xfm, world_xfm = read_trans(reader, True, name)
    mShape = reader.int32()
    mOrigRadius0 = reader.float32()
    mOrigLength0 = reader.float32()
    mOrigLength1 = reader.float32()
    mFlags = reader.int32()
    mCurRadius0 = reader.float32()
    if version > 6:
        mOrigRadius1 = reader.float32()
        mCurLength0 = reader.float32()
        mCurLength1 = reader.float32()
        unk148 = reader.matrix()
        mMesh = reader.numstring()
        mDigest = reader.float32()
        mMeshYBias = reader.milo_bool()
        unk18c = reader.float32()
        unk180 = reader.float32()
    if mShape == 0: # kPlane
        print("flat plane")
        bm = bmesh.new()
        bmesh.ops.create_grid(bm, x_segments=4, y_segments=4, size= mOrigRadius0)
       # name = name
        mesh = bpy.data.meshes.new(name)
        bm.to_mesh(mesh)
        mesh.update()
        bm.free()
        obj = bpy.data.objects.new(name, mesh)
        bpy.context.scene.collection.objects.link(obj)
        obj.matrix_world = mathutils.Matrix((
            (local_xfm[0], local_xfm[3], local_xfm[6], local_xfm[9],),
            (local_xfm[1], local_xfm[4], local_xfm[7], local_xfm[10],),
            (local_xfm[2], local_xfm[5], local_xfm[8], local_xfm[11],),
            (0.0, 0.0, 0.0, 1.0),
        ))
    elif mShape == 1: # kSphere
        print("Sphere")
        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=8, v_segments=9, radius= mOrigRadius0)
       # name = name
        mesh = bpy.data.meshes.new(name)
        bm.to_mesh(mesh)
        mesh.update()
        bm.free()
        obj = bpy.data.objects.new(name, mesh)
        bpy.context.scene.collection.objects.link(obj)
        obj.matrix_world = mathutils.Matrix((
            (local_xfm[0], local_xfm[3], local_xfm[6], local_xfm[9],),
            (local_xfm[1], local_xfm[4], local_xfm[7], local_xfm[10],),
            (local_xfm[2], local_xfm[5], local_xfm[8], local_xfm[11],),
            (0.0, 0.0, 0.0, 1.0),
        ))
    elif mShape == 2: # kInsideSphere
        print("inside out Sphere")
        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=8, v_segments=9, radius= -mOrigRadius0)
       # name = name
        mesh = bpy.data.meshes.new(name)
        bm.to_mesh(mesh)
        mesh.update()
        bm.free()
        obj = bpy.data.objects.new(name, mesh)
        bpy.context.scene.collection.objects.link(obj)
        obj.matrix_world = mathutils.Matrix((
            (local_xfm[0], local_xfm[3], local_xfm[6], local_xfm[9],),
            (local_xfm[1], local_xfm[4], local_xfm[7], local_xfm[10],),
            (local_xfm[2], local_xfm[5], local_xfm[8], local_xfm[11],),
            (0.0, 0.0, 0.0, 1.0),
        ))
    elif mShape == 3: # kCigar
        print("Cigar")
        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=8, v_segments=9, radius= mOrigRadius0)
        delta_Z = mOrigLength1
        bm.verts.ensure_lookup_table()
        for vert in bm.verts:
            if vert.co[2] < 0:
                vert.co[2] -= delta_Z
            elif vert.co[2] > 0:
                vert.co[2] += delta_Z
       # name = name
        mesh = bpy.data.meshes.new(name)
        bm.to_mesh(mesh)
        mesh.update()
        bm.free()
        obj = bpy.data.objects.new(name, mesh)
        bpy.context.scene.collection.objects.link(obj)
        obj.matrix_world = mathutils.Matrix((
            (local_xfm[0], local_xfm[3], local_xfm[6], local_xfm[9],),
            (local_xfm[1], local_xfm[4], local_xfm[7], local_xfm[10],),
            (local_xfm[2], local_xfm[5], local_xfm[8], local_xfm[11],),
            (0.0, 0.0, 0.0, 1.0),
        ))
    elif mShape == 4: # kInsideCigar
        print("inside out Cigar")
        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=8, v_segments=9, radius= -mOrigRadius0)
        delta_Z = mOrigLength1
        bm.verts.ensure_lookup_table()
        for vert in bm.verts:
            if vert.co[2] < 0:
                vert.co[2] -= delta_Z
            elif vert.co[2] > 0:
                vert.co[2] += delta_Z
       # name = name
        mesh = bpy.data.meshes.new(name)
        bm.to_mesh(mesh)
        mesh.update()
        bm.free()
        obj = bpy.data.objects.new(name, mesh)
        bpy.context.scene.collection.objects.link(obj)
        obj.matrix_world = mathutils.Matrix((
            (local_xfm[0], local_xfm[3], local_xfm[6], local_xfm[9],),
            (local_xfm[1], local_xfm[4], local_xfm[7], local_xfm[10],),
            (local_xfm[2], local_xfm[5], local_xfm[8], local_xfm[11],),
            (0.0, 0.0, 0.0, 1.0),
        ))
    find_next_file(reader)