import os
from .. data_format_parsers.bitmap_reader import *
from .. image_helpers.compress_dxt import *
from .. image_helpers.swap_x360_bytes import *
from .. image_helpers.dxt1_to_tpl import *

def write_bitmap(writer, filepath: str, width: int, height: int, encoding: str, is_rgba: bool):
    dirname = os.path.dirname(filepath)
    filename = filepath.rsplit(".", 1)[0]   
    path = os.path.join(dirname, filename)
    if writer.game in ["Frequency", "Amplitude", "Karaoke Revolution"]:
        writer.byte(0)
    elif not writer.game == "DC2 / DC3":
        writer.byte(1)
    else:
        writer.byte(2)
    if is_rgba == False:
        writer.ubyte(4)
    elif is_rgba == True:
        writer.ubyte(8)
    if not (writer.platform == "Wii") and (is_rgba == False):
        writer.uint32(8)
    elif not (writer.platform == "Wii") and (is_rgba == True):
        writer.uint32(24)
    elif (writer.platform == "Wii") and (is_rgba == False):
        writer.uint32(72)
    elif (writer.platform == "Wii") and (is_rgba == True):
        writer.uint32(328)
    if not writer.game in ["Frequency", "Amplitude", "Karaoke Revolution"]:
        writer.ubyte(0)
    writer.ushort(width)
    writer.ushort(height)
    # thx pikmin
    if is_rgba == True:
        writer.ushort((width * 8) // 8)
    else:
        writer.ushort((width * 4) // 8)
    # write wii alpha num
    # 4 in RB2 wii when using alpha
    #if (writer.game == "RB1 / RB2") and (writer.platform == "Wii"):
    writer.ushort(0)
    # write padding
    if writer.game in ["Frequency", "Amplitude", "Karaoke Revolution"]:
        writer.write("6b", *([0] * 6))
    elif writer.game == "DC2 / DC3":
        writer.write("13b", *([0] * 13))
    else:
        writer.write("17b", *([0] * 17))
    if not writer.platform == "PS2":
        compressed_image = compress_image(filepath, encoding)
    if writer.platform == "X360":
        writer.write_bytes(swap_x360_bytes(compressed_image))
    elif writer.platform == "PS3":
        writer.write_bytes(compressed_image)
    elif writer.platform == "Wii":
        writer.write_bytes(shuffle_wii_blocks(compressed_image, width, height))