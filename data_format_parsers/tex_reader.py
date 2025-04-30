from .. common import *
from . bitmap_reader import *

def read_tex(reader, name: str, self) -> None:
    version = reader.int32()
    print("Reading texture", name, "at offset", reader.tell(), "version", version)
    if version > 8:
        read_metadata(reader, False)
    if self.texture_selection == "GDRB":
        some_bool = reader.milo_bool()
    width = reader.uint32()
    height = reader.uint32()
    bpp = reader.uint32()
    if self.texture_selection == "LRB":
        # always empty
        always_empty = reader.uint32()
    if version <= 4:
        ext_path = reader.string()
    else:
        ext_path = reader.numstring()
    if version >= 8:
        index_f = reader.float32()
    index = reader.uint32()
    if reader.version >= 28:
        some_bool = reader.milo_bool()
    if (version == 7) or (version == 4):
        use_ext_path = reader.uint32()
    else:
        use_ext_path = reader.milo_bool()
    padding = reader.read_bytes(4)
    if padding == b"\xAD\xDE\xAD\xDE":
        reader.seek(-4)
        return
    reader.seek(-4)
    if (reader.version == 28) and (reader.platform == "Wii"):
        unknown_byte = reader.byte()
        unknown_byte_2 = reader.byte()
    bitmap(reader, name, self)