import bpy
import os
from . compression import *
from .. readers import *
from .. writers import *
from .. common import *
from .. image_helpers.image_writer import write_image
from .. image_helpers.decode_dxt import decode_dxt1, decode_dxt5, decode_ati2
#from .. image_helpers.decode_rgb import decode_rgb
from .. image_helpers.decode_rgba import decode_rgba
from .. image_helpers.tpl_to_dxt1 import shuffle_wii_blocks
from .. image_helpers.swap_x360_bytes import swap_x360_bytes

def bitmap_encoding(encoding: int) -> str:
    if encoding == 1:
        print("encoding = 1", "ARGB")
        return "ARGB"
    elif (encoding == 0) or (encoding == 2) or (encoding == 3) or (encoding == 259) or (encoding == 515):
        print("encoding = 0/2/3/259/515", "RGBA")
        return "RGBA"
    elif encoding == 8:
        print("encoding = 8", "DXT1")
        return "DXT1"
    elif encoding == 24:
        print("encoding = 24", "DXT5")
        return "DXT5"
    elif encoding == 32:
        print("encoding = 32", "ATI2")
        return "ATI2"
    elif (encoding == 72) or (encoding == 583):
        print("encoding = 72/583", "CMP")
        return "CMP"
    elif encoding == 328:
        print("encoding = 328", "CMP_ALPHA")
        return "CMP_ALPHA"
   # elif encoding == 583:
   #     return "CMP_2"

def export_bitmap(reader, bitmap_data: dict, platform: str, filepath: str, name: str, self) -> None:
    width = bitmap_data["width"]
    height = bitmap_data["height"]
    print("width, height", width, height)
    bpp = bitmap_data["bpp"]
    print("bpp", bpp)
    encoding = bitmap_encoding(bitmap_data["encoding"])
    print("encoding", encoding)
    mip_maps = bitmap_data.get("mip_maps", 0)
    print("mip_maps", mip_maps)
    wii_alpha_num = bitmap_data.get("wii_alpha_num", 0)
    print("wii_alpha_num", wii_alpha_num)
    dirname = os.path.dirname(filepath)
    out_name = name.rsplit(".", 1)[0]
    output_path = os.path.join(dirname, out_name + f".{self.texture_format}")
   # output_path = os.path.join(dirname, out_name + f".{self.texture_selection}")
    if encoding == "RGBA":
        if (bpp == 4) or (bpp == 8):
            color_palette = reader.read_bytes(1 << (bpp + 2))
        i = 0
        w = width
        h = height
        if (width == 0) and (height == 0):
            return
        bitmaps = []
        while i <= mip_maps:
            bitmaps.append(reader.read_bytes((w * h * bpp) // 8))
            w >>= 1
            h >>= 1
            i += 1
        if (bpp == 4) or (bpp == 8):
            bitmap = decode_rgba(bitmaps[0], width, height, bpp, color_palette)
        elif (bpp == 16) or (bpp == 24):
            bitmap = decode_rgba(bitmaps[0], width, height, bpp)
        else:
            bitmap = bitmaps[0]
        write_image(output_path, width, height, bitmap)
        texture = bpy.data.textures.new(os.path.basename(output_path), type="IMAGE")
        img = bpy.data.images.load(output_path)
        texture.image = img                  
    else:
        i = 0
        w = width
        h = height
        if (width == 0) and (height == 0):
            return
        bitmaps = []
        while i <= mip_maps:
            bitmaps.append(reader.read_bytes((w * h * bpp) // 8))
            w >>= 1
            h >>= 1
            i += 1
        # Swap x360 bytes
        if platform == "X360":
            for i in range(len(bitmaps)):
                bitmaps[i] = swap_x360_bytes(bitmaps[i])
        if (encoding == "DXT1") or (encoding == "CMP") or (encoding == "CMP_ALPHA"):
            # shuffle wii blocks + reverse colors and indices
            if encoding == "CMP":
                w = width
                h = height
                for i in range(len(bitmaps)):
                    bitmaps[i] = shuffle_wii_blocks(bitmaps[i], w, h)       
                    w >>= 1
                    h >>= 1             
            elif encoding == "CMP_ALPHA":
                w = width
                h = height
                rgb_bytes = []
                alpha_bytes = []
                for i in range(len(bitmaps)):
                    bitmap = bitmaps[i]
                    rgb = bitmap[:len(bitmap) // 2]
                    alpha = bitmap[len(bitmap) // 2:]
                    rgb_bytes.append(shuffle_wii_blocks(rgb, w, h))
                    alpha_bytes.append(shuffle_wii_blocks(alpha, w, h))   
                    w >>= 1
                    h >>= 1 
            if not encoding == "CMP_ALPHA":  
                bitmap_reader = Reader(b"".join(bitmaps), filepath)
                decoded_image = decode_dxt1(bitmap_reader, width, height)
                write_image(output_path, width, height, decoded_image)
                texture = bpy.data.textures.new(os.path.basename(output_path), type="IMAGE")
                img = bpy.data.images.load(output_path)
                texture.image = img 
            else:
                rgb_reader = Reader(b"".join(rgb_bytes), filepath)
                alpha_reader = Reader(b"".join(alpha_bytes), filepath)
                decoded_rgb = list(decode_dxt1(rgb_reader, width, height))
                decoded_alpha = decode_dxt1(alpha_reader, width, height)
                for i in range(0, len(decoded_rgb), 4):
                    decoded_rgb[i + 3] = decoded_alpha[i + 1]
                decoded_image = bytes(decoded_rgb)
                write_image(output_path, width, height, decoded_image)
                texture = bpy.data.textures.new(os.path.basename(output_path), type="IMAGE")
                img = bpy.data.images.load(output_path)
                texture.image = img                 
        elif encoding == "DXT5":
            bitmap_reader = Reader(b"".join(bitmaps), filepath)
            decoded_image = decode_dxt5(bitmap_reader, width, height)
            write_image(output_path, width, height, decoded_image)
            texture = bpy.data.textures.new(os.path.basename(output_path), type="IMAGE")
            img = bpy.data.images.load(output_path)
            texture.image = img 
        elif encoding == "ATI2":
            bitmap_reader = Reader(b"".join(bitmaps), filepath)
            decoded_image = decode_ati2(bitmap_reader, width, height)            
            write_image(output_path, width, height, decoded_image)
            texture = bpy.data.textures.new(os.path.basename(output_path), type="IMAGE")
            img = bpy.data.images.load(output_path)
            texture.image = img 
    print("Exported texture to: ", output_path)
    
def bitmap(reader, filepath: str, self) -> None:
    bitmap_data = {}
    if (reader.version == 28 and reader.platform == "Wii") or (self.texture_selection == "RB3 Wii"):
        reader.little_endian = True
    version = reader.byte()
    if reader.version == 0:
        reader.version = version
    if (reader.version == 32) or (self.texture_selection == "DC2 / DC3"):
        hash = reader.uint32()
    bpp = reader.byte()
    bitmap_data["bpp"] = bpp
    if version == 0:
        encoding = reader.ushort()
    else:
        encoding = reader.uint32()
    bitmap_data["encoding"] = encoding
    if version > 0:
        mip_maps = reader.byte()
        bitmap_data["mip_maps"] = mip_maps
    width = reader.ushort()
    bitmap_data["width"] = width
    height = reader.ushort()
    bitmap_data["height"] = height
    bpl = reader.ushort()
    if version > 0:
        if (self.texture_selection == "PHASE"):
            bitmap_data["wii_alpha_num"] = 0
        else:
            wii_alpha_num = reader.ushort()
            bitmap_data["wii_alpha_num"] = wii_alpha_num
    if (reader.version == 32) or (self.texture_selection == "DC2 / DC3"):
        padding = reader.read_bytes(13)
    else:
        if version == 0:
            padding = reader.read_bytes(6)         
        else:
            padding = reader.read_bytes(17)
    export_bitmap(reader, bitmap_data, reader.platform, reader.filepath, filepath, self)
    if (reader.version == 28 and reader.platform == "Wii") or (self.texture_selection == "RB3 Wii"):
        # set back to big endian
        reader.little_endian = False
        always_negative_8 = reader.float32()
        always_1 = reader.int32()
        unknown_byte = reader.byte()
        unknown_byte_2 = reader.byte()

def read_bitmap(self, filepath: str):
    if filepath.endswith(".gz"):
        reader = Reader(decompress_gzip(open(filepath, "rb").read()), filepath)
    elif filepath.endswith(".z"):
        reader = Reader(decompress_zlib_deflate(open(filepath, "rb").read()), filepath)
    else:
        reader = Reader(open(filepath, "rb").read(), filepath)
    platform = get_platform(filepath)
    reader.platform = platform
    reader.version = 0
    bitmap(reader, filepath, self)