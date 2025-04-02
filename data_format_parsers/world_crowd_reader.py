import bpy
import mathutils
from .. common import *
from . draw_reader import *

def change_color(material, color: tuple) -> None:
    # Thx dody!   
    node_tree = material.node_tree
    bsdf = node_tree.nodes.get("Principled BSDF")
    for node in node_tree.nodes:
        if node.type == "TEX_IMAGE":
            tex_node = node
    rgb_node = node_tree.nodes.new("ShaderNodeRGB")
    rgb_node.outputs[0].default_value[0] = color[0]
    rgb_node.outputs[0].default_value[1] = color[1]
    rgb_node.outputs[0].default_value[2] = color[2]
    mix_lighten_node = node_tree.nodes.new("ShaderNodeMix")
    mix_lighten_node.data_type = "RGBA"
    mix_lighten_node.blend_type = "LIGHTEN"
    mix_lighten_node.inputs[0].default_value = 1.0
    links = node_tree.links
    links.new(rgb_node.outputs["Color"], mix_lighten_node.inputs[7])
    mix_multiply_node = node_tree.nodes.new("ShaderNodeMix")
    mix_multiply_node.data_type = "RGBA"
    mix_multiply_node.blend_type = "MULTIPLY"
    mix_multiply_node.inputs[0].default_value = 1.0
    links.new(mix_lighten_node.outputs["Result"], mix_multiply_node.inputs[7])
    links.new(tex_node.outputs["Alpha"], mix_lighten_node.inputs[6])
    links.new(tex_node.outputs["Color"], mix_multiply_node.inputs[6])
    links.new(mix_multiply_node.outputs["Result"], bsdf.inputs["Base Color"])

def old_multi_mesh_instance(reader, version: int) -> tuple[tuple, tuple]:
    old_xfm = reader.matrix()
    old_color = ()
    if version > 6:
        old_color = reader.vec4f()
    return old_xfm, old_color

def char_def(reader, version: int) -> tuple[str, float]:
    character = reader.numstring()
    height = reader.float32()
    density = reader.float32()
    if version > 1:
        radius = reader.float32()
    if version > 8:
        use_random_color = reader.milo_bool()
    return character, height

def read_world_crowd(reader, name: str, super: bool) -> list:
    print("Reading crowd locations", name, "at offset", reader.tell())
    xfms = []
    # tbrb rooftop? breh?
    if "fill" in name:
        find_next_file(reader)
        return xfms
    version = reader.int32()
    read_draw(reader, True)
    target_mesh = reader.numstring()
    crowd_platform_mesh = bpy.data.objects.get(target_mesh)
    if version < 3:
        unk_int_1 = reader.uint32()
    num = reader.uint32()
    if version < 8:
        unk_bool_1 = reader.milo_bool()
    char_count = reader.uint32()
    characters = []
    heights = []
    for _ in range(char_count):
        character, height = char_def(reader, version)
        characters.append(character)
        heights.append(height)
    if version > 6:
        environ = reader.numstring()
    if version > 9:
        environ3D = reader.numstring()
    if version > 1:
        if version < 14:
            for i in range(char_count):                
                old_mm_count = reader.int32()
                # read then duplicate?
                for x in range(old_mm_count):
                    xfm, color = old_multi_mesh_instance(reader, version)
                    xfms.append((characters[i], heights[i], xfm, color))       
                    crowd_obj = bpy.data.objects.get(characters[i])
                    if crowd_obj:
                        crowd_obj.matrix_world = mathutils.Matrix((
                            (xfm[0], xfm[3], xfm[6], xfm[9]),
                            (xfm[1], xfm[4], xfm[7], xfm[10]),
                            (xfm[2], xfm[5], xfm[8], xfm[11]),
                            (0.0, 0.0, 0.0, 1.0),
                        ))    
                    char_obj = bpy.data.objects.new(characters[i], None)
                    bpy.context.scene.collection.objects.link(char_obj)
                    char_obj.empty_display_size = 2
                    char_obj.empty_display_type = "PLAIN_AXES"
                    char_obj.matrix_world = mathutils.Matrix((
                        (xfm[0], xfm[3], xfm[6], xfm[9]),
                        (xfm[1], xfm[4], xfm[7], xfm[10]),
                        (xfm[2], xfm[5], xfm[8], xfm[11]),
                        (0.0, 0.0, 0.0, 1.0),
                    ))   
        else:
            transform_count = []
            for i in range(char_count):
                transform_count.append(reader.int32())
                if transform_count[i] > 0:
                    transforms_list = []
                    for x in range(transform_count[i]):
                        xfm = reader.matrix()
                        xfms.append((characters[i], heights[i], xfm, ()))
                        crowd_obj = bpy.data.objects.get(characters[i])
                        if crowd_obj:
                            crowd_obj.matrix_world = mathutils.Matrix((
                                (xfm[0], xfm[3], xfm[6], xfm[9]),
                                (xfm[1], xfm[4], xfm[7], xfm[10]),
                                (xfm[2], xfm[5], xfm[8], xfm[11]),
                                (0.0, 0.0, 0.0, 1.0),
                            ))    
                        char_obj = bpy.data.objects.new(characters[i], None)
                        bpy.context.scene.collection.objects.link(char_obj)
                        char_obj.empty_display_size = 2
                        char_obj.empty_display_type = "PLAIN_AXES"
                        char_obj.matrix_world = mathutils.Matrix((
                            (xfm[0], xfm[3], xfm[6], xfm[9]),
                            (xfm[1], xfm[4], xfm[7], xfm[10]),
                            (xfm[2], xfm[5], xfm[8], xfm[11]),
                            (0.0, 0.0, 0.0, 1.0),
                        ))                         
    if version > 4:
        modify_stamp = reader.int32()
    if version > 12:
        force_3D_crowd = reader.milo_bool()
    if version > 5:
        show_3D_only = reader.milo_bool()
    if version > 11:
        focus = reader.numstring()     
    if version >= 16:
        always_ff = reader.uint32()
        some_int = reader.int32()       
    read_metadata(reader, super)
    return xfms