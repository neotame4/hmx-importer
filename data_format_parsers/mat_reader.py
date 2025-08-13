import bpy
from .. common import *

def texture_entry(reader) -> str:
    unknown = reader.int32()
    print("unknown", unknown)
    map_type = reader.int32()
    print("map_type", map_type)
    tex_xfm = reader.matrix()
    print("tex_xfm", tex_xfm)
    tex_wrap = reader.int32()
    print("tex_wrap", tex_wrap)
    tex_name = reader.numstring()
    print("tex_name", tex_name)
    return tex_name

def texture_entry_amp(reader, version: int) -> str:
    map_type = reader.int32()
    print("map_type", map_type)
    tex_xfm = reader.matrix()
    print("tex_xfm", tex_xfm)
    reader.read_bytes(13)
    if version <= 7:
        tex_name = reader.string()
    else:
        tex_name = reader.numstring()
    print("tex_name", tex_name)
    return tex_name
    
def texture_entry_amp(reader, version: int) -> str:
    map_type = reader.int32()
    print("map_type", map_type)
   # tex_xfm = reader.matrix()
   # print("tex_xfm", tex_xfm)
    reader.read_bytes( 21)
    if version <= 7:
        tex_name = reader.string()
    else:
        tex_name = reader.numstring()
    print("tex_name", tex_name)
    return tex_name

def read_mat(reader, name: str, self) -> None:
    mat_data = {}
    mat_data["mat_name"] = name
    print("Reading material", name, "at offset", reader.tell())
    version = reader.int32()
    print("version", version)
    if version == 43:
        junk = reader.int32()
        print("junk", junk)
        beans = reader.short()
        print("beans", junk)
        beans2 = reader.milo_bool()
        print("beans2", beans2)
        junk1 = reader.int32()
        print("junk1", junk1)
        junk2 = reader.int32()
        print("junk2", junk2)
        junk3 = reader.int32()
        print("junk3", junk3)
        junk4 = reader.int32()
        print("junk4", junk4)
        junk5 = reader.int32()
        print("junk5", junk5)
        tex_count = reader.short()
        print("tex_count", tex_count)
        texs = []
        for _ in range(tex_count):
            tex_name = reader.numstring()
            print("tex_name", tex_name)
            texs.append(tex_name)
        if len(texs) > 0:
            diffuse_tex = texs[0].rsplit(".", 1)[0] + f".{self.texture_format}"
            mat_data["diffuse"] = diffuse_tex
        else:
            mat_data["diffuse"] = ""
            create_mat(mat_data, reader.platform)
        HUh = reader.int32()
        print("HUh", HUh)
        return
    elif version <= 9:
        tex_count = reader.int32()
        print("tex_count", tex_count)
        texs = []
        for _ in range(tex_count):
            tex_name = texture_entry_amp(reader, version)
            print("tex_name", tex_name)
            texs.append(tex_name)
        if len(texs) > 0:
            diffuse_tex = texs[0].rsplit(".", 1)[0] + f".{self.texture_format}"
            mat_data["diffuse"] = diffuse_tex
        else:
            mat_data["diffuse"] = ""
    elif version <= 21:
        tex_count = reader.int32()
        print("tex_count", tex_count)
        texs = []
        for _ in range(tex_count):
            tex_name = texture_entry(reader)
            print("tex_name", tex_name)
            texs.append(tex_name)
        if len(texs) > 0:
            diffuse_tex = texs[0].rsplit(".", 1)[0] + f".{self.texture_format}"
            mat_data["diffuse"] = diffuse_tex
        else:
            mat_data["diffuse"] = ""
    else:
        if version >= 70:
            always_5 = reader.uint32()
            print("always_5", always_5)
        read_metadata(reader, False)
       # print("tex_name", tex_name)
    blend = reader.int32()
    print("blend", blend)
    if version <= 7:
        return
    if version <= 7:
        # anyone know what this is?
        unknown = reader.read_bytes(30)
        print("unknown", unknown)
    r, g, b = reader.vec3f()
    print("r, g, b", r, g, b)
    alpha = reader.float32()
    print("alpha", alpha)
    if version <= 7:
        some_float = reader.float32()
        print("some_float", some_float)
        f1 = reader.float32()
        f2 = reader.float32()
        f3 = reader.float32()
        print("f1, f2, f3", f1, f2, f3)
    mat_data["r"] = r
    mat_data["g"] = g
    mat_data["b"] = b
    mat_data["alpha"] = alpha
    if version <= 15:
        if version > 7:
            color_2 = reader.vec3f()
            print("color_2", color_2)
            alpha_2 = reader.float32()
            print("alpha_2", alpha_2)
            some_float = reader.float32()
            print("some_float", some_float)
            f1 = reader.float32()
            f2 = reader.float32()
            f3 = reader.float32()
            print("f1, f2, f3", f1, f2, f3)
            if version > 12:
                some_bool = reader.milo_bool()
                print("some_bool", some_bool)
            zeros = reader.read_bytes(14)
            print("zeros", zeros)
            if (version > 9) and (version != 12):
                unknown_num = reader.uint32()
                print("unknown_num", unknown_num)
            if version == 9:
                some_bool = reader.milo_bool()
                print("some_bool", some_bool)
            create_mat(mat_data, reader.platform)
            return
    elif version <= 21:
        always_1 = reader.byte()
        print("always_1", always_1)
        always_0 = reader.short()
        print(" always_0",  always_0)
        always_1_0 = reader.int32()
        print("always_1_0", always_1_0)
        always_0_0 = reader.short()
        print("always_0_0", always_0_0)
        blend = reader.int32()
        print("blend", blend)
        always_0_1 = reader.short()
        print("always_0_1", always_0_1)
        create_mat(mat_data, reader.platform)
        return
    if version <= 7:
        unknown_bool = reader.milo_bool()
        print("unknown_bool", unknown_bool)
        unknown_bool_2 = reader.milo_bool()
        print("unknown_bool_2", unknown_bool_2)
    prelit = reader.milo_bool()
    print("prelit", prelit)
    use_environ = reader.milo_bool()
    print("use_environ", use_environ)
    z_mode = reader.uint32()
    print("z_mode", z_mode)
    alpha_cut = reader.milo_bool()
    print("alpha_cut", alpha_cut)
    if version > 37:
        alpha_threshold = reader.int32()
        print("alpha_threshold", alpha_threshold)
    alpha_write = reader.milo_bool()
    print("alpha_write", alpha_write)
    tex_gen = reader.uint32()
    print("tex_gen", tex_gen)
    tex_wrap = reader.uint32()
    print("tex_wrap", tex_wrap)
    if version <= 7:
        create_mat(mat_data)
       # create_mat(mat_data, reader.platform)
        return
    tex_xfm = reader.matrix()
    print("tex_xfm", tex_xfm)
    diffuse_tex = reader.numstring().rsplit(".", 1)[0] + f".{self.texture_format}"
    print("diffuse_tex", diffuse_tex)
    mat_data["diffuse"] = diffuse_tex
    next_pass = reader.numstring()
    print("next_pass", next_pass)
    intensify = reader.milo_bool()
    print("intensify", intensify)
    cull = reader.milo_bool()
    print("cull", cull)
    if version >= 70:
        recv_proj_lights = reader.milo_bool()
        print("recv_proj_lights", recv_proj_lights)
        recv_point_cube_tex = reader.milo_bool()
        print("recv_point_cube_tex", recv_point_cube_tex)
        ps3_force_trilinear = reader.milo_bool()
        print("ps3_force_trilinear", ps3_force_trilinear)
    emissive_multiplier = reader.float32()
    mat_data["emissive_multiplier"] = emissive_multiplier
    print("emissive_multiplier", emissive_multiplier)
    specular_rgb = reader.vec3f()
    print("specular_rgb", specular_rgb)
    mat_data["specular_rgb"] = specular_rgb
    specular_power = reader.float32()
    print("specular_power", specular_power)
    mat_data["specular_power"] = specular_power
    normal_map = reader.numstring().rsplit(".", 1)[0] + f".{self.texture_format}"
    print("normal_map", normal_map)
    mat_data["normal"] = normal_map
    emissive_map = reader.numstring()
    print("emissive_map", emissive_map)
    mat_data["emissive"] = emissive_map
    specular_map = reader.numstring().rsplit(".", 1)[0] + f".{self.texture_format}"
    print("specular_map", specular_map)
    mat_data["specular"] = specular_map    
    if version < 51:
        some_string = reader.numstring()
        print("some_string", some_string)
    environ_map = reader.numstring()
    print("environ_map", environ_map)
    if version > 25:
        if (version <= 55) or (version > 56):
            per_pixel_lit = reader.milo_bool()
            print("per_pixel_lit", per_pixel_lit)
        else:
            per_pixel_lit = reader.uint32()
            print("per_pixel_lit", per_pixel_lit)
    if version >= 68:
        # TODO RB3 and on mat
        find_next_file(reader)
        create_mat(mat_data, reader.platform)
        return
    if (version >= 27) and (version < 50):
        ignored_bool = reader.milo_bool()
        print("ignored_bool", ignored_bool)
    if version > 27:
        stencil_mode = reader.uint32()
        print("stencil_mode", stencil_mode)
    if (version >= 29) and (version < 41):
        ignore_string = reader.numstring()
        print("ignore_string", ignore_string)
    if version > 33:
        fur = reader.numstring()
        print("fur", fur)
    if (version >= 34) and (version < 49):
        ignored_bool_2 = reader.milo_bool()
        print("ignored_bool_2", ignored_bool_2)
        ignored_color = reader.vec3f()
        print("ignored_color", ignored_color)
        ignored_alpha = reader.float32()
        print("ignored_alpha", ignored_alpha)
        if version > 34:
            some_string_2 = reader.numstring()
            print("some_string_2", some_string_2)
    if version > 35:
        de_normal = reader.float32()
        print("de_normal", de_normal)
        anisotropy = reader.float32()
        print("anisotropy", anisotropy)
    if version > 38:
        if version < 42:
            ignored_bool_3 = reader.milo_bool()
            print("ignored_bool_3", ignored_bool_3)
        norm_detail_tiling = reader.float32()
        print("norm_detail_tiling", norm_detail_tiling)
        norm_detail_strength = reader.float32()
        print("norm_detail_strength", norm_detail_strength)
        if version < 42:
            for _ in range(5):
                some_ignored_float = reader.float32()
                print("some_ignored_float", some_ignored_float)
        norm_detail_map = reader.numstring()
        print("norm_detail_map", norm_detail_map)
        if version < 42:
            some_string_3 = reader.numstring()
            print("some_string_3", some_string_3)
    if version > 42:
        if version < 45:
            some_bitfield = reader.uint32()
            print("some_bitfield", some_bitfield)
        else:
            point_lights = reader.milo_bool()
            print("point_lights", point_lights)
        proj_lights = reader.milo_bool()
        print("proj_lights", proj_lights)
        fog = reader.milo_bool()
        print("fog", fog)
        fade_out = reader.milo_bool()
        print("fade_out", fade_out)
        if version > 46:
            color_adjust = reader.milo_bool()
            print("color_adjust", color_adjust)
    if version > 47:
        rim_rgb = reader.vec3f()
        print("rim_rgb", rim_rgb)
        rim_power = reader.float32()
        print("rim_power", rim_power)
        rim_map = reader.numstring()
        print("rim_map", rim_map)
        rim_always_show = reader.milo_bool()
        print("rim_always_show", rim_always_show)
    if version > 48:
        screen_aligned = reader.milo_bool()
        print("screen_aligned", screen_aligned)
    if version == 50:
        legacy_shader_variation = reader.ubyte()
        print("legacy_shader_variation", legacy_shader_variation)
    elif version > 50:
        shader_variation = reader.uint32()
        print("shader_variation", shader_variation)
        specular2_rgb = reader.vec3f()
        print("specular2_rgb", specular2_rgb)
        specular2_power = reader.float32()
        print("specular2_power", specular2_power)
    if version > 51:
        if version == 52:
            ignored_bool_4 = reader.milo_bool()
            print("ignored_bool_4", ignored_bool_4)
        else:
            val_0x160 = reader.float32()
            print("val_0x160", val_0x160)
        if version > 54:
            val_0x170 = reader.float32()
            val_0x174 = reader.float32()
            val_0x178 = reader.float32()
            val_0x17c = reader.float32()
            print("val_0x170, val_0x174, val_0x178, val_0x17c", val_0x170, val_0x174, val_0x178, val_0x17c)
    if version > 53:
        alpha_mask = reader.numstring()
        print("alpha_mask", alpha_mask)
    if version > 54:
        ps3_force_trilinear = reader.milo_bool()
        print("ps3_force_trilinear", ps3_force_trilinear)        
    create_mat(mat_data, reader.platform)

def create_mat(mat_data: dict, platform: str) -> None:
    mat_name = mat_data["mat_name"]
    diffuse = mat_data["diffuse"]
    normal = mat_data.get("normal", "")
    emissive = mat_data.get("emissive", "")
    emissive_multiplier = mat_data.get("emissive_multiplier", "")
    specular = mat_data.get("specular", "")
    specular_rgb = mat_data.get("specular_rgb", ())
    r = mat_data["r"]
    g = mat_data["g"]
    b = mat_data["b"]
    specular_power = mat_data.get("specular_power", "")
    alpha = mat_data["alpha"]
    # im looking at you rooftop + abbey road studios
    mat = bpy.data.materials.get(mat_name)
    index = 0
    if mat:
        mat.name = mat.name + f"_{index}"
        index += 1
    mat = bpy.data.materials.new(mat_name)
    mat.diffuse_color = (r, g, b, alpha)
    diffuse_tex = bpy.data.textures.get(diffuse)
    if diffuse_tex:
        if mat.use_nodes == False:
            mat.use_nodes = True
            mat.blend_method = "HASHED"
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            tex_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
            tex_node.image = diffuse_tex.image
            tex_node.location = (-345.0820, 318.2288)
            links = mat.node_tree.links
            links.new(bsdf.inputs["Base Color"], tex_node.outputs["Color"])
            links.new(bsdf.inputs["Alpha"], tex_node.outputs["Alpha"])
           # links.new(tex_node.outputs["Alpha"], bsdf.inputs["Alpha"])
            image = diffuse_tex.image
            image.alpha_mode = "CHANNEL_PACKED"
    normal_tex = bpy.data.textures.get(normal)
    if normal_tex:
        if mat.use_nodes == False:
            mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            normal_map_node = mat.node_tree.nodes.new("ShaderNodeNormalMap")
            normal_map_node.location = (-261.7965, 32.9038)
            tex_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
            tex_node.image = normal_tex.image
            tex_node.location = (-1221.9069, -21.5945)
            separate_color = mat.node_tree.nodes.new("ShaderNodeSeparateColor")
            separate_color.location = (-742.4393, -75.2079)
            combine_color = mat.node_tree.nodes.new("ShaderNodeCombineColor")
            combine_color.location = (-511.2123, -73.1929)
            invert_color = mat.node_tree.nodes.new("ShaderNodeInvert")
            # create 2nd one if x360
            if platform == "X360":
                invert_color.location = (-744.0405, -237.4729)
                invert_color_2 = mat.node_tree.nodes.new("ShaderNodeInvert")
                invert_color_2.location = (-512.2188, -236.2577)
            else:
                invert_color.location = (-629.6825, -237.2079)
            links = mat.node_tree.links
            node_tree = mat.node_tree
            links.new(tex_node.outputs["Color"], separate_color.inputs[0])
            links.new(separate_color.outputs[0], combine_color.inputs[0])
            if platform == "X360":
                links.new(separate_color.outputs[1], invert_color.inputs[1])
                links.new(invert_color.outputs[0], combine_color.inputs[1])
                links.new(separate_color.outputs[2], invert_color_2.inputs[1])
                links.new(invert_color_2.outputs[0], combine_color.inputs[2])
            else:
                links.new(separate_color.outputs[1], invert_color.inputs[1])
                links.new(invert_color.outputs[0], combine_color.inputs[1])
                links.new(separate_color.outputs[2], combine_color.inputs[2])
            links.new(combine_color.outputs[0], normal_map_node.inputs[1])
            normal_map_node.uv_map = "UVMap"
            links.new(normal_map_node.outputs[0], bsdf.inputs["Normal"])
    specular_tex = bpy.data.textures.get(specular)
    if specular_tex:
        if mat.use_nodes == False:
            mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            tex_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
            tex_node.image = specular_tex.image
            tex_node.location = (-352.1719, -131.3825)
            try:
                bsdf.inputs[13].default_value = (specular_rgb[0], specular_rgb[1], specular_rgb[2], 1.0)
                bsdf.inputs[12].default_value = (specular_power / 100)
            except:
                print("specular RGB broke, ripperoni, L, skill issue")
# blender is weird
# need to divide the specular power by 100 to get a USABLE value
            links = mat.node_tree.links
            links.new(tex_node.outputs["Color"], bsdf.inputs[13])
            image = specular_tex.image
            image.alpha_mode = "CHANNEL_PACKED"
            image.colorspace_settings.name = "Non-Color"
            node_tree = mat.node_tree
    # WHY DOESNT GH2 USE EMISSION PROPERLY 
    emissive_tex = bpy.data.textures.get(emissive)
    if emissive_tex:
        if mat.use_nodes == False:
            mat.use_nodes = True
            mat.blend_method = "HASHED"
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            tex_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
            tex_node.image = emissive_tex.image
            tex_node.location = (-352.1719, -151.3825)
            bsdf.inputs[27].default_value = emissive_multiplier
            links = mat.node_tree.links
           # links.new(bsdf.inputs[26], tex_node.outputs["Color"])
            links.new(tex_node.outputs["Color"], bsdf.inputs[26])
            image = emissive_tex.image
            image.alpha_mode = "CHANNEL_PACKED"
            image.colorspace_settings.name = "Non-Color"
            node_tree = mat.node_tree