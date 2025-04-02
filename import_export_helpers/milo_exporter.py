import bpy
import os
from .. writers import *
from .. common import *
from . anim_writer import *
from . character_writer import *
from . draw_writer import *
from . mat_writer import *
from . mesh_writer import *
from . poll_writer import *
from . tex_writer import *
from . trans_writer import *

def get_num_objects() -> int:
    num_meshes = len([obj for obj in bpy.context.scene.objects if obj.type == "MESH"])
    num_bones = 0
    num_materials = 0
    num_textures = 0
    material_names = set()
    texture_names = set()
    for obj in bpy.context.scene.objects:
        if obj.type == "MESH":
            if obj.material_slots:
                if obj.material_slots[0].name not in material_names:
                    material_names.add(obj.material_slots[0].name)
                    num_materials += 1
                    material = obj.material_slots[0].material
                    if material.use_nodes:
                        for node in material.node_tree.nodes:
                            if node.type == "TEX_IMAGE":
                                if node.image.name not in texture_names:
                                    texture_names.add(node.image.name)
                                    num_textures += 1
            if obj.modifiers:
                for modifier in obj.modifiers:
                    if modifier.type == "ARMATURE":
                        num_bones += len(modifier.object.data.bones)
    num_objects = num_textures + num_materials + num_meshes + num_bones
    return num_objects

def get_object_names() -> list:
    mesh_names = [obj.name for obj in bpy.context.scene.objects if obj.type == "MESH"]
    bone_names = []
    material_names = set()
    texture_filepaths = set()
    for obj in bpy.context.scene.objects:
        if obj.type == "MESH":
            if obj.material_slots:
                if obj.material_slots[0].name not in material_names:
                    material_names.add(obj.material_slots[0].name)
                    material = obj.material_slots[0].material
                    if material.use_nodes:
                        for node in material.node_tree.nodes:
                            if node.type == "TEX_IMAGE":
                                filepath = bpy.path.abspath(node.image.filepath)
                                if filepath not in texture_filepaths:
                                    texture_filepaths.add(filepath)
            if obj.modifiers:
                for modifier in obj.modifiers:
                    if modifier.type == "ARMATURE":
                        bone_names.append(bone.name for bone in modifier.object.data.bones)
    material_names = list(material_names)
    texture_filepaths = list(filepath for filepath in texture_filepaths)
    return texture_filepaths, material_names, mesh_names, bone_names

def write_character(writer, is_entry: bool, self):
    if (writer.game == "GH2 PS2") or (writer.game == "GH80s"):
        # random int, always 1?
        writer.int32(1)
        writer.int32(9)
    elif writer.game == "GH2 X360":
        writer.int32(10)
    elif writer.game == "RB1 / RB2":
        writer.int32(12)
    elif writer.game in ["TBRB", "LRB", "GDRB"]:
        writer.int32(15)
    elif writer.game == "RB3 / DC1":
        writer.int32(17)
    else:
        writer.int32(18)
    write_rnd_dir(writer, self)
    if (writer.game == "RB3 / DC1") or ((writer.game == "DC2 / DC3") and (is_entry == True)):
        write_character_test(writer, self)
    if is_entry == True:
        writer.write_bytes(b"\xAD\xDE\xAD\xDE")
        return
    writer.int32(0)
    if not writer.game == "DC2 / DC3":
        writer.numstring("")
    else:
        writer.uint32(0)
    writer.milo_bool(False)
    writer.numstring(self.directory_name)
    if not writer.game in ["GH2 PS2", "GH2 X360", "GH80s"]:
        writer.vec4f((0.0, 0.0, 0.0, 0.0))
        if not writer.game == "RB1 / RB2":
            writer.milo_bool(False)
            writer.int32(-1)
    if (writer.game == "RB3 / DC1") and (is_entry == False):
        writer.numstring("")
    if not (writer.game == "DC2 / DC3") or ((writer.game == "RB3 / DC1") and (is_entry == False)):
        write_character_test(writer)
        return
    
def write_obj_dir(writer, self):
    if (writer.game == "GH2 PS2") or (writer.game == "GH80s"):
        writer.int32(16)
    elif writer.game == "GH2 X360":
        writer.int32(17)
    elif writer.game == "RB1 / RB2":
        writer.int32(20)
    elif (writer.game == "TBRB") or (writer.game == "GDRB"):
        writer.int32(22)
    elif writer.game == "RB3 / DC1":
        writer.int32(27)
    else:
        writer.int32(28)
    if (writer.game == "GH2 PS2") or (writer.game == "GH80s"):
        write_metadata(writer, False, self)
    else:
        if writer.game == "GH2 X360":
            writer.int32(1)
        else:
            writer.int32(2)
    writer.numstring("")
    if (writer.game == "RB3 / DC1") or (writer.game == "DC2 / DC3"):
        # random padding?
        for _ in range(8):
            writer.write_bytes(b"\x00")
    writer.int32(7)
    for _ in range(7):
        writer.matrix(default_transform())
    writer.int32(6)
    if writer.game not in ["GH2 PS2", "GH2 X360", "GH80s", "RB1 / RB2"]:
        writer.milo_bool(False)    
    writer.numstring("")
    writer.int32(0)
    if writer.game not in ["GH2 PS2", "GH2 X360", "GH80s", "RB1 / RB2"]:
        writer.milo_bool(False)
        writer.int32(0)
    if writer.game in ["GH2 PS2", "GH2 X360", "GH80s"]:
        writer.numstring("")
    for _ in range(2):
        writer.numstring("")
    if (writer.game == "GH2 X360") or (writer.game == "RB1 / RB2"):
        write_metadata(writer, False, self)
    else:
        write_dtb(writer)
        if writer.game in ["RB1 / RB2", "TBRB", "LRB", "GDRB"]:
            writer.numstring("")

def write_rnd_dir(writer, self):
    if (writer.game == "GH2 PS2") or (writer.game == "GH80s"):
        writer.int32(8)
    elif writer.game == "GH2 X360":
        writer.int32(9)
    else:
        writer.int32(10)
    write_obj_dir(writer, self)
    write_anim(writer, self)
    write_draw(writer)
    write_trans(writer, True, (0.0, 0.0, 0.0), (0.0, 0.0, 0.0))
    if (writer.game == "GH2 PS2") or (writer.game == "GH80s"):
        write_poll(writer)
        for _ in range(2):
            writer.numstring("")
    else:
        writer.numstring("")
        if not writer.game == "GH2 X360":
            writer.numstring("")

def export_milo(inline: bool, filepath: str, self):
    with open(filepath, "wb") as f:
        writer = Writer(f)
        writer.platform = self.platform_selection
        writer.game = self.game_selection
        if (writer.game != "Frequency") or (inline == False):
            writer.write_bytes(b"\xAF\xDE\xBE\xCA")
            if writer.game == "Amplitude":
                writer.uint32(216)
            elif writer.game == "Karaoke Revolution":
                writer.uint32(272)
            elif writer.game in ["GH1", "GH2 PS2", "GH80s"]:
                writer.uint32(528)
            # GH2 x360 was the first game to use 2064 as starting offset
            else:
                writer.uint32(2064)
            writer.int32(1)
            # override with actual file sizes later
            for _ in range(2):
                writer.int32(0)
            if writer.game == "Amplitude":
                writer.write("196b", *([0] * 196))
            elif writer.game == "Karaoke Revolution":
                writer.write("252b", *([0] * 252))
            elif writer.game in ["GH1", "GH2 PS2", "GH80s"]:
                writer.write("508b", *([0] * 508))
            else:
                writer.write("2044b", *([0] * 2044))
        if writer.game == "Frequency":
            writer.int32(6)
        elif writer.game in ["Amplitude", "Karaoke Revolution", "GH1"]:
            writer.int32(10)
            # external resources
            writer.int32(0)
        elif (writer.game == "GH2 PS2") or (writer.game == "GH80s"):
            writer.int32(24)
        elif writer.game in ["GH2 X360", "RB1 / RB2", "TBRB", "LRB", "GDRB"]:
            if writer.game != "GH2 X360":
                writer.little_endian = False
            writer.int32(25)
        elif writer.game == "RB3 / DC1":
            writer.little_endian = False
            writer.int32(28)
        else:
            writer.little_endian = False
            writer.int32(32)
        if not writer.game in ["Frequency", "Amplitude", "Karaoke Revolution", "GH1"]:
            if (writer.game == "GH2 PS2") or (writer.game == "GH80s"):
                writer.numstring("BandCharacter")
            else:
                writer.numstring("Character")
            writer.numstring(self.directory_name)
        num_objects = get_num_objects()
        texture_filepaths, material_names, mesh_names, bone_names = get_object_names()
        # thx compvir
        if not writer.game in ["Frequency", "Amplitude", "Karaoke Revolution", "GH1"]:
            writer.uint32(num_objects * 2)
            writer.uint32(num_objects * 2 * 16)
        writer.int32(num_objects)
        for texture_name in texture_filepaths:
            writer.numstring("Tex")
            writer.numstring(convert_image_name(os.path.basename(texture_name)))
        for material_name in material_names:
            writer.numstring("Mat")
            writer.numstring(material_name)
        for mesh_name in mesh_names:
            writer.numstring("Mesh")
            writer.numstring(mesh_name)
        for bone_name in bone_names:
            writer.numstring("Trans")
            writer.numstring(bone_name)
        write_character(writer, False, self)        
        writer.write_bytes(b"\xAD\xDE\xAD\xDE")
        for filepath in texture_filepaths:
            write_tex(writer, filepath)
            writer.write_bytes(b"\xAD\xDE\xAD\xDE")
        for mat_name in material_names:
            write_mat(writer, mat_name)
            writer.write_bytes(b"\xAD\xDE\xAD\xDE")
        for mesh_name in mesh_names:
            write_mesh(writer, mesh_name)
            writer.write_bytes(b"\xAD\xDE\xAD\xDE")