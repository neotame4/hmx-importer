import os
from . bitmap_writer import *
from .. common import *
from .. readers import *

def convert_image_name(name: str) -> str:
    name = name.rsplit(".", 1)[0]
    return name + ".tex"

def get_width_and_height(filepath: str) -> tuple[int, int, bool]:
    # png
    if filepath.endswith(".png"):
        reader = Reader(open(filepath, "rb").read(), filepath)
        reader.little_endian = False
        is_rgba = False
        reader.seek(16)
        width = reader.uint32()
        height = reader.uint32()
        reader.seek(1)
        color_type = reader.byte()
        if color_type == 6:
            is_rgba = True
    # jpg/jpeg
    elif (filepath.endswith(".jpg")) or (filepath.endswith(".jpeg")):
        reader = Reader(open(filepath, "rb").read(), filepath)
        reader.little_endian = False
        is_rgba = False
        reader.seek(224)
        height = reader.int32()
        width = reader.int32()
    # bmp
    elif filepath.endswith(".bmp"):
        reader = Reader(open(filepath, "rb").read(), filepath)
        is_rgba = False
        reader.seek(18)
        width = reader.ushort()
        height = reader.ushort()
    # tga
    elif filepath.endswith(".tga"):
        reader = Reader(open(filepath, "rb").read(), filepath)
        is_rgba = False
        reader.seek(12)
        width = reader.short()
        height = reader.short()
        pixel_depth = reader.ubyte()
        if pixel_depth == 32:
            is_rgba = True
    return width, height, is_rgba

def write_tex(writer, filepath: str) -> None:
    if writer.game == "Amplitude":
        writer.int32(5)
    elif writer.game == "AntiGrav":
        writer.int32(7)
    elif (writer.game == "Karaoke Revolution") or (writer.game == "GH1"):
        writer.int32(8)
    elif writer.game not in ["LRB", "GDRB", "RB3 / DC1", "DC2 / DC3"]:
        writer.int32(10)
    else:
        writer.int32(11)
    if not writer.game in ["Frequency", "Amplitude", "AntiGrav", "Karaoke Revolution", "GH1"]:
        write_metadata(writer, False)
    # lol green day so weird!!!
    if writer.game == "GDRB":
        writer.milo_bool(False)
    width, height, is_rgba = get_width_and_height(filepath)
    writer.uint32(width)
    writer.uint32(height)
    encoding = ""
    if is_rgba == True:
        writer.uint32(8)
        encoding = "DXT5"
    else:
        writer.uint32(4)
        encoding = "DXT1"
    writer.numstring(os.path.basename(filepath))
    writer.float32(0)
    writer.uint32(1)
    writer.milo_bool(False)
    write_bitmap(writer, filepath, width, height, encoding, is_rgba)