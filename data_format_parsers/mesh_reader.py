import bpy
import mathutils
from .. common import *
from .. bpy_util_funcs import *
from . trans_reader import *
from . draw_reader import *
    
def bsp_node(reader) -> None:
    has_value = reader.milo_bool()
    if has_value == True:
        vec = reader.vec4f()
        bsp_node(reader)
        bsp_node(reader)

def faces(reader) -> list:
    face_count = reader.int32()
    faces = []
    for _ in range(face_count):
        faces.append(reader.vec3us())
    return faces

def vertices(reader, version: int) -> list:
    # rb3 wii you are so funny!!!!
    if version == 393254:
        reader.little_endian = True
        # FF FF FF FF, probably padding or vertex color?
        padding = reader.read_bytes(4)
        unknown = reader.read_bytes(8)
    vertex_count = reader.int32()
    is_ng = False
    is_og_ng = False
    if version >= 36:
        is_ng = reader.milo_bool()
        if is_ng == True:
            vert_size = reader.int32()
            compression_type = reader.int32()
        if (reader.platform != "Wii") and (is_ng == False):
            is_og_ng = True
    vertices = []
    normals = []
    uvs = []
    bone_weights = []
    bone_ids = []
    for i in range(vertex_count):
        vertices.append(reader.vec3f())
        if (version == 34 and reader.little_endian == False) or (version == 36 and is_og_ng == True):
            w = reader.float32()
        if version <= 10:
            normals.append((reader.vec3f()))
            uvs.append(invert_uv_map(reader.vec2f()))
            bone_weights.append(reader.vec4f())
            bone_ids.append(reader.vec4us())
        elif version <= 22:
            weight_0, weight_1 = reader.vec2f()
            weight_2 = 1.0 - (weight_0 + weight_1)
            bone_weights.append((weight_0, weight_1, weight_2))
            normals.append((reader.vec3f()))
            unknown_0, unknown_1, unknown_2, unknown_3 = reader.vec4f()
            uvs.append(invert_uv_map(reader.vec2f()))
            bone_ids.append((0, 1, 2))
        elif version <= 25:
            normals.append(reader.vec3f())
            bone_weights.append(reader.vec4f())
            uvs.append(invert_uv_map(reader.vec2f()))
            bone_ids.append((0, 1, 2, 3)) 
        elif (version < 35) or (is_ng == False):
            if version == 38:
                packed_1 = reader.uint32()
                unknown_1 = reader.float32()
                packed_2 = reader.uint32()
                unknown_2 = reader.float32()
            normals.append(reader.vec3f())
            if (version == 34 and reader.little_endian == False) or (version == 36 and is_og_ng == True):
                nw = reader.float32()
            if version == 38:
                uv = invert_uv_map(reader.vec2f())
                uvs.append(uv)
                bone_weights.append(reader.vec4f()) 
            else:
                bone_weights.append(reader.vec4f())       
                uv = invert_uv_map(reader.vec2f())
                uvs.append(uv)
            if version >= 34:
                if version == 393254:
                    always_1 = reader.float32()
                    always_0 = reader.float32()
                    always_0_2 = reader.float32()
                    always_0_3 = reader.float32()
                bone_ids.append(reader.vec4us())   
                if version >= 38:
                    packed_3 = reader.uint32()
                    packed_4 = reader.uint32()
                    neg_1 = reader.float32()
                    pos_1 = reader.float32()
                else:
                    tangent_0 = reader.float32()    
                    tangent_1 = reader.float32()
                    tangent_2 = reader.float32()
                    tangent_3 = reader.float32()  
            else:
                bone_ids.append((0, 1, 2, 3))
        else:
            if reader.platform == "X360":
                always_ff_1 = reader.uint32()
            uvs.append(invert_uv_map(reader.vec2hf()))
     
            normal_value = reader.uint32()
           # print("normal_value", normal_value)
           # normalsv = signed_compressed_vec4(normal_value)
           # normals.append(normalsv)
           # print("normalsv", normalsv)

            tangent_value = reader.uint32()
           # print("tangent_value", tangent_value)
           # tangentsv = signed_compressed_vec4(tangent_value)
           # print("tangentsv", tangentsv)

            if reader.platform == "X360":
                bone_weights.append(unsigned_compressed_vec4(reader.uint32()))
                bone_ids.append(reverse_vector(reader.vec4ub()))
            else:
                weight = reader.uint32()
            #    print("weight", weight)
                weights = unsigned_compressed_vec4(weight)
            #    print("weights", weights)
                bone_weights.append(weights)
                if compression_type == 2:
                    unknown = reader.uint32()
                ids = reader.vec4us()
             #   print("ids", ids)
                bone_ids.append(ids)     
    if version == 393254:
        reader.little_endian = False
    return vertices, normals, uvs, bone_weights, bone_ids 

def group_section(reader, count: int) -> None:
    for _ in range(count):
        section_count = reader.int32()
        vert_count = reader.int32()
        for _ in range(section_count):
            section = reader.int32()
        for _ in range(vert_count):
            vert_offset = reader.ushort()

def group_section_ag(reader) -> None:
    group_count = reader.uint32()
    for _ in range(group_count):
        some_number = reader.uint32() 
        short_count = reader.uint32()            
        for _ in range(short_count):
            short = reader.ushort()
        int_count = reader.uint32()            
        for _ in range(int_count):
            int = reader.int32()

def bone_trans(reader, version: int) -> list:
    bone_count = reader.int32()
    if version <= 28:
        if bone_count > 0:
            reader.seek(-4)
            bone_count = 4
    bone_names = []
    for _ in range(bone_count):
        if version > 22:
            bone_name = reader.numstring()
           # print("bone_name", bone_name)
            bone_names.append(bone_name)
        if version >= 34:        
            matrix = reader.matrix()
          #  print("matrix", matrix)
    if (version <= 28) and (bone_count > 0):
        for _ in range(4):
            bone_transform = reader.matrix()
    # old gh games have some empty
    index = 0
    for i in range(len(bone_names)):
        if len(bone_names[i]) == 0:
            bone_names[i] = "Group" + f"_{index}"
            index += 1
    return bone_names  

def read_mesh(reader, name: str, character_name: str, self) -> tuple:
    mesh_data = {}
    mesh_data["mesh_name"] = name
    mesh_data["character_name"] = character_name
    print("Reading mesh", name, "at offset", reader.tell())
    version = reader.int32()
    print("mesh_version", version)
    mesh_data["version"] = version
    geom_owner = ""
    parent_name = ""
    if self.import_shadow == False:   
        if "shadow" in name:
            find_next_file(reader)
            return geom_owner, parent_name, name
    if self.import_lod == False:
        if version == 37:
            if "LOD01" in name:
                find_next_file(reader)
                return geom_owner, parent_name, name
            if reader.platform != "Wii":
                if "LOD02" in name:
                    find_next_file(reader)
                    return geom_owner, parent_name, name
        else:
            if ("lod01" in name) or ("lod1" in name) or ("lod02" in name):
                find_next_file(reader)  
                return geom_owner, parent_name, name             
        if name.startswith("Blend"):
            print("blend mesh found", name)
            find_next_file(reader)
            return geom_owner, parent_name, name
    if version > 25:
        read_metadata(reader, False)           
    trans_version, trans_count, trans_objects, parent, local_xfm, world_xfm = read_trans(reader, True, name)
   # parent, local_xfm, world_xfm = read_trans(reader, True, name)
   # print("parent, local_xfm, world_xfm", parent, local_xfm, world_xfm)
    mesh_data["parent"] = parent
    if version == 25:
        parent_name = parent
    mesh_data["local_xfm"] = local_xfm
    mesh_data["world_xfm"] = world_xfm
   # mesh_data["local_xfm"] = world_xfm
   # mesh_data["world_xfm"] = local_xfm
    read_draw(reader, True)
   # print("VERSION", version)
    if version < 15:
       # print("VERSION", version)
        always_0 = reader.uint32()
       # print("always_0", always_0)
        bones_count = reader.int32()
       # print("bones_count", bones_count)
        for _ in range(bones_count):
            if version <= 10:
                bone = reader.string()
            else:
                bone = reader.numstring()               
    if version < 20:
        num_1 = reader.uint32()
        num_2 = reader.uint32()
    if version < 3:
        some_value = reader.numstring()
    if version <= 10:
        mat = reader.string()
    else:
        mat = reader.numstring()
    mesh_data["mat_name"] = mat
    if version == 27:
        mat_2 = reader.numstring()
    if version <= 10:
        geom_owner = reader.string()
    else:
        geom_owner = reader.numstring()
    mesh_data["geom_owner"] = geom_owner
    if version < 13:
        if version <= 10:
            alt_geom_owner = reader.string()
        else:
            alt_geom_owner = reader.numstring()        
    if version < 15:
        if version <= 10:
            trans_parent = reader.string()
        else:
            trans_parent = reader.numstring()     
    if version < 14:
        if version <= 10:
            trans_1 = reader.string()
            trans_2 = reader.string()
        else:
            trans_1 = reader.numstring() 
            trans_2 = reader.numstring() 
    if version < 3:
        some_vector = reader.vec3f()
    if version < 15:
        sphere = reader.vec4f()
    if version < 8:
        some_bool = reader.milo_bool()
    if version < 15:
        if version <= 10:
            some_string = reader.string()
        else:
            some_string = reader.numstring()       
        some_float = reader.float32()    
    if version < 16:
        if version > 11:
            some_bool = reader.milo_bool()
    else:
        mutable = reader.uint32()
        if version == 17:
            unknown = reader.uint32()
            unknown_2 = reader.uint32()
    if version > 17:
        volume = reader.uint32()
    if version > 18:
        bsp_node(reader)
    if version == 7:
        some_bool = reader.milo_bool()
    if version < 11:
        some_number = reader.uint32()
    verts, normals, uvs, weights, indices = vertices(reader, version)
    mesh_data["vertices"] = verts
    mesh_data["normals"] = normals
    mesh_data["uvs"] = uvs
    mesh_data["weights"] = weights
    mesh_data["indices"] = indices
    mesh_faces = faces(reader)
    mesh_data["faces"] = mesh_faces
    if version < 24:
        short_count = reader.uint32()
        for _ in range(short_count * 2):
            some_short = reader.ushort()
        if version >= 22:
            group_section_ag(reader)
        if version == 16 or version == 17:
            unknown_3 = reader.numstring()
        if version <= 22:
            bone_1 = reader.numstring()
            bone_names = []
            bone_names.append(parent)
            bone_count = 1
            if len(bone_1) > 5:
                bone_count = 2
                bone_names.append(bone_1)
                bone_2 = reader.numstring()
                if len(bone_2) > 5:
                    bone_names.append(bone_2)
                    bone_count = 3
                bone_1_xfm = reader.matrix()
                bone_2_xfm = reader.matrix()
            mesh_data["bone_names"] = bone_names
        if version >= 14:
            if version >= 25:
                bone_names = bone_trans(reader, 4, version)
                mesh_data["bone_names"] = bone_names
            create_mesh(mesh_data)
            return geom_owner, parent_name, name
        create_mesh(mesh_data)
        return geom_owner, parent_name, name
    group_sizes_count = reader.uint32()
    print("group_sizes_count", group_sizes_count)
    group_sizes = []
    for _ in range(group_sizes_count):
        group_size = reader.ubyte()
        print("group_size", group_size)
        print("group_size", group_size)
        group_sizes.append(group_size)
    charcount = reader.int32()
    print("charcount", charcount)
    reader.seek(-4)
    bone_names = []
    if charcount > 0:
        if version >= 34:
            bone_count = reader.uint32()
            print("bone_count", bone_count)
            for _ in range(bone_count):
                bone_name = reader.numstring()
#bone_trans(reader, version)
               # print("bone_name", bone_name)
                bone_names.append(bone_name)
                bone_transform = reader.matrix()
              #  print("bone_transform", bone_transform)
                mesh_data["bone_names"] = bone_names
        else:
            bone_count = 4
            bone_names = []
            for _ in range(bone_count):
                bone_name = reader.numstring()
                print("bone_name", bone_name)
                bone_names.append(bone_name)
            for _ in range(bone_count):
                matrix = reader.matrix()
                print("matrix", matrix)
           # bone_name = bone_trans(reader, version)
           # print("bone_name", bone_name)
           # bone_names.append(bone_name)
           # print("bone_name", bone_name)
            mesh_data["bone_names"] = bone_names
    else:
        noBones = reader.uint32()
        print("noBones", noBones)
   # bone_names = bone_trans(reader, version)
   # print("bone_names", bone_names)
   # mesh_data["bone_names"] = bone_names
    if version == 393254:
        # data that looks like faces, but model is fine without them, so just gonna skip it here
        find_next_file(reader)
        create_mesh(mesh_data)
        return geom_owner, parent_name, name
    if version >= 36:
        keep_mesh_data = reader.milo_bool()
    if version == 37:
        exclude_from_self_shadow = reader.milo_bool()
    if version >= 38:
        has_ao_calculation = reader.milo_bool()
    # KR rooftop shows that vert count needs to be more than 4 to have this
   # print("group_sizes_count", group_sizes_count)
   # print("group_sizes[0]", group_sizes[0])
   # print("version", version)
   # if (group_sizes_count > 0) and (group_sizes[0] > 0) and (reader.platform == "PS2") and (len(verts) > 4):
    if (group_sizes_count > 0) and (group_sizes[0] > 0) and (reader.platform == "PS2"):
    #                                                        ^^^^^^^^^ IF MILO VERSION < 25
    #                                                     WHY HARMONIX MUST YOU DO IT THIS WAY
# version < 25:
        sectionCount1 = reader.int32()
        print("sectionCount1", sectionCount1)
        reader.seek(-4)
        if sectionCount1 == -559030611:
            print("sectionCount1", sectionCount1)
        elif sectionCount1 != -559030611:
           # group_section(reader, group_sizes_count)
            for _ in range(group_sizes_count):
                sectionCount = reader.int32()
                print("sectionCount", sectionCount)
                vertCount = reader.int32()
                print("vertCount", vertCount)
                for _ in range(sectionCount):
                    sections = reader.int32()
                    print("sections", sections)
                for _ in range(vertCount):
                    vertOffsets = reader.ushort()
                    print("vertOffsets", vertOffsets)
    if "bone" not in name:
        create_mesh(mesh_data)
    else:
        mesh_data["bone_name"] = name
        mesh_data["trans_version"] = trans_version
        if trans_version < 9:
            mesh_data["trans_count"] = trans_count
            mesh_data["trans_objects"] = trans_objects
        mesh_data["parent"] = parent
        # flip transforms
        mesh_data["local_xfm"] = local_xfm
        mesh_data["world_xfm"] = world_xfm
        create_mesh(mesh_data)
        create_trans(mesh_data)
    return geom_owner, parent_name, name

def create_mesh(mesh_data) -> None:
    mesh_name = mesh_data["mesh_name"]
    mat_name = mesh_data["mat_name"]
    parent = mesh_data["parent"]
    character_name = mesh_data["character_name"]
    geom_owner = mesh_data["geom_owner"]
    mesh_version = mesh_data["version"]
    local_xfm = mesh_data["local_xfm"]
    world_xfm = mesh_data["world_xfm"]
    verts = mesh_data["vertices"]
    faces = mesh_data["faces"]
    normals = mesh_data["normals"]
    uvs = mesh_data["uvs"]
    weights = mesh_data["weights"]
    indices = mesh_data["indices"]
    bone_names = mesh_data.get("bone_names", [])
    print("Creating mesh:", mesh_name)
   # mesh = bpy.data.meshes.new(name=geom_owner)
   # mesh = bpy.data.meshes.get(geom_owner)
    mesh = bpy.data.meshes.get(geom_owner)
    if mesh is None:
        mesh = bpy.data.meshes.new(name=geom_owner)

 #   index = 0
 #   if mesh:
 #       mesh.name = mesh.name + f"_{index}"
 #       index += 1
   # mesh = bpy.data.meshes.new(name=geom_owner)
   # mesh = bpy.data.meshes.get(geom_owner)


#    stolen from older script version
    index = 0
    if mesh:
        mesh.name = mesh.name + f"_{index}"
        index += 1
   # mesh = bpy.data.meshes.new(name=mesh_name)
   # obj = bpy.data.objects.new(mesh_name, mesh)  

    obj = bpy.data.objects.get(mesh_name)
    if obj is None:  
        obj = bpy.data.objects.new(mesh_name, mesh)  
   # else:
   #     mesh = bpy.data.meshes.new(name=geom_owner)
   # if len(parent) > 0 and "bone" not in parent:
    if len(parent) > 0:
        try:
            o = bpy.data.objects.get(parent)
            if o:
                obj.parent = o
            else:
                meshparent = bpy.data.meshes.new(name=geom_owner)
                o = bpy.data.objects.new(parent, meshparent)
                bpy.context.scene.collection.objects.link(o)
               # o.empty_display_size = 2
               # o.empty_display_type = 'PLAIN_AXES'
                obj.parent = o
        except:
            pass
    try:
        bpy.context.scene.collection.objects.link(obj)
    except:
        print(obj, "Already exists")
    if (obj.parent != None) or (parent != None) or (parent != mesh_name):
        obj.matrix_local = mathutils.Matrix((
            (local_xfm[0], local_xfm[3], local_xfm[6], local_xfm[9],),
            (local_xfm[1], local_xfm[4], local_xfm[7], local_xfm[10],),
            (local_xfm[2], local_xfm[5], local_xfm[8], local_xfm[11],),
            (0.0, 0.0, 0.0, 1.0),
        ))  
    if "bone" in parent:
        obj.matrix_world = mathutils.Matrix((
            (world_xfm[0], world_xfm[3], world_xfm[6], world_xfm[9],),
            (world_xfm[1], world_xfm[4], world_xfm[7], world_xfm[10],),
            (world_xfm[2], world_xfm[5], world_xfm[8], world_xfm[11],),
            (0.0, 0.0, 0.0, 1.0),
        ))
    character_obj = bpy.data.objects.get(character_name)
   # if character_obj:
   #     obj.parent = character_obj
    mesh.from_pydata(verts, [], faces)
   # index = 0
   # if mesh:
   #     mesh.name = mesh.name + f"_{index}"
   #     index += 1
    obj.data = bpy.data.meshes.get(mesh.name)
    uv_layer = mesh.uv_layers.new(name="UVMap")
    for loop in mesh.loops:
        uv = uvs[loop.vertex_index]
        uv_layer.data[loop.index].uv = (uv[0], uv[1])
    if len(normals) > 0:
        mesh.normals_split_custom_set_from_vertices(normals)
    else:
        for f in mesh.polygons:
            f.use_smooth = True
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    if len(mat_name) > 0:
        print("Adding/creating material:", mat_name)
        material = bpy.data.materials.get(mat_name)
        obj = bpy.context.active_object
        if obj:
            if obj.data.materials:
                obj.data.materials[0] = material
            else:
                obj.data.materials.append(material)
    if len(bone_names) == 0:
        return
    # credits to dody for the following weight code
    print("Adding bone weights to:", mesh_name)
    final_weight_map = {}
    for vertex_index, (id_group, weight_group) in enumerate(zip(indices, weights)):
        for idx, wgt in zip(id_group, weight_group):
       #     if len(bone_names) == 1:
       #        # print("bone_names", bone_names)
       #         group_name = bone_names[0]
       #         print("group_name", group_name)
       #        # group_name = group_name1[0]
       #        # print("group_name", group_name)
       #         if group_name not in final_weight_map:
       #             new_vtx_group = obj.vertex_groups.new(name=group_name)
       #             final_weight_map[group_name] = new_vtx_group
       #         if wgt > 0:
       #             final_weight_map[group_name].add([vertex_index], wgt, "REPLACE")  
       #     elif len(bone_names) == 2:
       #         max_group_name_idx = 2
       #         for idx in range(min(len(bone_names), max_group_name_idx)):
       #             group_name = bone_names[idx]                    
       #             if group_name not in final_weight_map:
       #                 new_vtx_group = obj.vertex_groups.new(name=group_name)
       #                 final_weight_map[group_name] = new_vtx_group
       #             if wgt > 0:
       #                 final_weight_map[group_name].add([vertex_index], wgt, "REPLACE") 
       #     elif len(bone_names) == 3:
       #         max_group_name_idx = 3
       #         for idx in range(min(len(bone_names), max_group_name_idx)):
       #             group_name = bone_names[idx]
       #             if group_name not in final_weight_map:
       #                 new_vtx_group = obj.vertex_groups.new(name=group_name)
       #                 final_weight_map[group_name] = new_vtx_group
       #             if wgt > 0:
       #                 final_weight_map[group_name].add([vertex_index], wgt, "REPLACE") 
       #     else:
             try:
                group_name = bone_names[idx]                  
                if group_name not in final_weight_map:
                    new_vtx_group = obj.vertex_groups.new(name=group_name)
                    final_weight_map[group_name] = new_vtx_group
                if wgt > 0:
                    final_weight_map[group_name].add([vertex_index], wgt, "REPLACE")
             except:
                 print("issue happened")
    if mesh_version <= 22:
        for vertex_index, (id_group, weight_group) in enumerate(zip(indices, weights)):
            for idx, wgt in zip(id_group, weight_group):
                if len(bone_names) == 1:
                    group_name = bone_names[0]
                    if group_name not in final_weight_map:
                        new_vtx_group = obj.vertex_groups.new(name=group_name)
                        final_weight_map[group_name] = new_vtx_group
                    if wgt > 0:
                        final_weight_map[group_name].add([vertex_index], wgt, "REPLACE") 
                else:
                    max_group_name_idx = 3
                    for idx in range(min(len(bone_names), max_group_name_idx)):
                        group_name = bone_names[idx]
                        weight1 = weight_group[idx]
                        if group_name not in final_weight_map:
                            new_vtx_group = obj.vertex_groups.new(name=group_name)
                            final_weight_map[group_name] = new_vtx_group
                        if wgt > 0:
                            final_weight_map[group_name].add([vertex_index], weight1, "REPLACE") 
    mesh.update()
    print("Bone weights assigned to:", mesh_name)                
    obj.select_set(False)