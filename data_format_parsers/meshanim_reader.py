import bpy
import mathutils
from .. common import *
from .. bpy_util_funcs import *
from . anim_reader import *
from . draw_reader import *
    

def VertPointKey(reader, name) -> list:
    PointKey_count = reader.uint32()
    print("PointKey_count", PointKey_count)
    VertPoints = []
    for _ in range(PointKey_count):
        verts = reader.vec3f()
       # print("verts", verts)
        VertPoints.append(verts)
    pos = reader.float32() 
   # print("pos", pos)
    mesh = bpy.data.meshes.new(name= name + str(pos))
    obj = bpy.data.objects.new(name + str(pos), mesh)  
    bpy.context.scene.collection.objects.link(obj)
    faces = []
    mesh.from_pydata(VertPoints, [], faces)
    mesh.update() 
    return VertPoints, pos

def VertTextKey(reader) -> list:
    TextKey_count = reader.uint32()
    print("TextKey_count", TextKey_count)
    VertTexts = []
    for _ in range(TextKey_count):
        if version >= 2: 
            texts = reader.vec3f()
        else:
            texts = reader.vec2f()
        print("texts", texts)
        VertTexts.append(texts)
    pos = reader.float32() 
    print("pos", pos)
    return VertTexts, pos

def VertColorKey(reader) -> list:
    ColorKey_count = reader.uint32()
    print("ColorKey_count", ColorKey_count)
    VertColors = []
    for _ in range(ColorKey_count):
        colors = reader.vec4f()
        print("colors", colors)
        VertColors.append(colors)
    pos = reader.float32() 
    print("pos", pos)
    return VertColors, pos

def read_meshanim(reader, name: str, self) -> tuple:
    meshanim_data = {}
    meshanim_data["mesh_name"] = name
    print("Reading meshanim", name, "at offset", reader.tell())
    version = reader.int32()
    print("meshanim_version", version)
    meshanim_data["version"] = version
    geom_owner = ""
    parent_name = ""
    if version >= 1:
        read_metadata(reader, False)    
    anim = read_anim(reader, True)
    print("anim", anim)             
    meshname = reader.numstring()  
    print("meshname", meshname)
          
    VertPoint = reader.uint32()
    print("VertPoint", VertPoint)
    for _ in range(VertPoint):
        VertPoints = VertPointKey(reader, name)
       # print("VertPoints", VertPoints)
   # meshanim_data["vertices"] = VertPoints
   # create_mesh(mesh_data)

    VertText = reader.uint32()
    print("VertText", VertText)
    for _ in range(VertText):
        VertTexts = VertTextKey(reader)
       # print("VertText", VertText)

    VertColor = reader.uint32()
    print("VertColor", VertColor)
    for _ in range(VertColor):
        VertColors = VertColorKey(reader)
       # print("VertColors", VertColors)
   # meshanim_data["vertices"] = VertPoints

    keys_owner = reader.numstring()  
    print("keys_owner", keys_owner)

    return name

#def create_mesh(mesh_data) -> None:
#    mesh_name = meshanim_data["mesh_name"]
#    mesh_version = meshanim_data["version"]
#    verts = meshanim_data["vertices"]
#    print("Creating mesh:", mesh_name)

#    mesh.update()             
#    obj.select_set(False)