import os
from .. readers import *
from .. writers import *

# credits to xorloser

x360_key = [0x37, 0xB2, 0xE2, 0xB9, 0x1C, 0x74, 0xFA, 0x9E, 0x38, 0x81, 0x08, 0xEA, 0x36, 0x23, 0xDB, 0xE4]

def read_mogg(self):
    reader = Reader(open(self.filepath, "rb").read(), self.filepath)
    mogg_data = {}
    version = reader.int32()
    ogg_offset = reader.int32()
    mogg_data["ogg_offset"] = ogg_offset
    num_channels = reader.int32()
    mogg_data["num_channels"] = num_channels
    unknown = reader.int32()
    mogg_data["unknown"] = unknown
    num_entries = reader.int32()
    mogg_data["num_entries"] = num_entries
    entries = []
    for _ in range(num_entries):
        entries.append((reader.int32(), reader.int32()))
    mogg_data["entries"] = entries
    # https://milo.ipg.pw/index.php/MOGG_File_Format#Encryption
    aes_iv = reader.read_bytes(16)

def create_mogg(decrypted: bytes, mogg_data: dict, self):
    ogg_offset = mogg_data["ogg_offset"]
    num_channels = mogg_data["num_channels"]
    unknown = mogg_data["unknown"]
    num_entries = mogg_data["num_entries"]
    entries = mogg_data["entries"]
    dirname = os.path.dirname(self.filepath)
    out_name = self.filepath.rsplit(".", 1)[0]
    path = os.path.join(dirname, out_name + "_dec.mogg")   
    with open(path, "wb") as f:
        writer = Writer(f)
        # 10 = unencrypted
        writer.int32(10)
        writer.int32(ogg_offset)
        writer.int32(num_channels)
        writer.int32(unknown)
        writer.int32(num_entries)
        writer.write_bytes(b"".join(entries))