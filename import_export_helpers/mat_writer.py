import bpy
from . bitmap_writer import *
from . tex_writer import *
from .. common import *

def texture_entry(writer, diffuse_tex: str) -> None:
    writer.int32(1)
    writer.matrix(default_transform())
    writer.int32(0)
    writer.numstring(diffuse_tex)

def texture_entry_amp(writer, diffuse_tex: str) -> None:
    writer.int32(4)
    writer.matrix(default_transform())
    # write 13 bytes of nothing
    for _ in range(13):
        writer.byte(0)
    if writer.game == "Amplitude":
        writer.numstring(diffuse_tex)
    else:
        writer.string(diffuse_tex)

def write_mat(writer, mat_name: str) -> None:
    if writer.game == "Frequency":
        writer.int32(7)
    elif writer.game == "Amplitude":
        writer.int32(9)
    elif writer.game == "AntiGrav":
        writer.int32(15)
    elif (writer.game == "Karaoke Revolution") or (writer.game == "GH1"):
        writer.int32(21)
    elif (writer.game == "GH2 PS2") or (writer.game == "GH80s"):
        writer.int32(27)
    elif writer.game == "GH2 X360":
        writer.int32(28)
    elif writer.game == "RB1":
        writer.int32(41)
    elif writer.game == "RB2":
        writer.int32(47)
    elif writer.game == "TBRB":
        writer.int32(55)
    elif writer.game == "GDRB":
        writer.int32(56)
    material = bpy.data.materials.get(mat_name)
    diffuse_tex = ""
    diffuse_color = ()
    if material.node_tree:
        for node in material.node_tree.nodes:
            if node.type == "BSDF_PRINCIPLED":
                try:
                    diffuse_tex = node.inputs[0].links[0].from_node.image.name
                except:
                    diffuse_tex = ""
        diffuse_color = material.diffuse_color
    if (writer.game == "Frequency") or (writer.game == "Amplitude"):
        texture_entry_amp(writer, diffuse_tex)
    elif writer.game in ["AntiGrav", "Karaoke Revolution", "GH1"]:
        texture_entry(writer, diffuse_tex)
    else:
        write_metadata(writer, False)
        if writer.game == "DC2 / DC3":
            writer.uint32(5)
    writer.uint32(1)
    if writer.game == "Frequency":
        # write 30 bytes of nothing
        for _ in range(30):
            writer.byte(0)
    writer.vec4f(diffuse_color)
    if writer.game == "Frequency":
        writer.vec4f((0.9, 0.9, 0.9, 0.9))
    if (writer.game == "Amplitude") or (writer.game == "AntiGrav"):
        writer.vec4f((0.0, 0.0, 0.0, 1.0))
        writer.vec4f((0.9, 0.9, 0.9, 0.9))
        writer.milo_bool(False)
        # write 14 bytes of nothing
        for _ in range(14):
            writer.byte(0)
        writer.uint32(0)
        return
    elif (writer.game == "Karaoke Revolution") or (writer.game == "GH1"):
        writer.byte(1)
        writer.short(0)
        writer.int32(1)
        writer.short(0)
        writer.uint32(0)
        writer.short(0)
        return
    if writer.game == "Frequency":
        for _ in range(2):
            writer.milo_bool(False)
    writer.milo_bool(True)
    writer.milo_bool(False)
    writer.uint32(1)
    writer.milo_bool(False)
    writer.int32(0)
    writer.milo_bool(False)
    writer.uint32(0)
    writer.uint32(1)
    if writer.game == "Frequency":
        return
    writer.matrix(default_transform())
    writer.numstring(convert_image_name(diffuse_tex))
    writer.numstring("")
    writer.milo_bool(False)
    writer.milo_bool(True)  
    if writer.game == "DC2 / DC3":
        for _ in range(3):
            writer.milo_bool(False)
    writer.float32(1)
    writer.vec3f((0.0, 0.0, 0.0))
    writer.float32(10)
    for _ in range(3):
        writer.numstring("")
    if writer.game in ["GH2 PS2", "GH2 X360", "GH80s", "RB1", "RB2"]:
        writer.numstring(convert_image_name(diffuse_tex))
    writer.numstring("")
    if not writer.game == "GDRB":
        writer.milo_bool(False)
    else:
        writer.uint32(3)
    if writer.game in ["GH2 X360", "RB1", "RB2"]:
        writer.milo_bool(False)
    if not (writer.game == "GH2 PS2") or (writer.game == "GH80s"):
        writer.uint32(0)
    if (writer.game == "RB1") or (writer.game == "RB2"):
        writer.numstring("")
    if not writer.game in ["GH2 PS2", "GH2 X360", "GH80s"]:
        writer.numstring("")
    if (writer.game == "RB1") or (writer.game == "RB2"):
        writer.milo_bool(False)
        writer.vec4f((0.0, 0.0, 0.0, 1.0))
        writer.numstring("")
    if not writer.game in ["GH2 PS2", "GH2 X360", "GH80s"]:
        for _ in range(2):
            writer.float32(0)
        if writer.game == "RB1":
            writer.milo_bool(False)
        for _ in range(2):
            writer.float32(0)
        if writer.game == "RB1":
            writer.float32(0.25)
            for _ in range(4):
                writer.float32(1)
        writer.numstring("")
        if writer.game == "RB1":
            writer.numstring("")
    if not writer.game in ["GH2 PS2", "GH2 X360", "GH80s", "RB1"]:
        for _ in range(5):
            writer.milo_bool(False)
    if not writer.game in ["GH2 PS2", "GH2 X360", "GH80s", "RB1", "RB2"]:
        writer.vec4f((0.0, 0.0, 0.0, 0.0))
        writer.numstring("")
        for _ in range(2):
            writer.milo_bool(False)
        writer.uint32(0)
        writer.vec3f((0.0, 0.0, 0.0))
        writer.float32(10)
        for _ in range(5):
            writer.float32(1)
        writer.numstring("")
        writer.milo_bool(False)