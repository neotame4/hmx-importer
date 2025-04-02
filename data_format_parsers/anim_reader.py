from .. common import *

def anim_entry(reader) -> None:
    name = reader.numstring()
    f1 = reader.float32()
    f2 = reader.float32()

def read_anim(reader, super: bool) -> None:
    version = reader.int32()
    read_metadata(reader, super)
    if version > 1:
        frame = reader.float32()
    if version == 3:
        unknown = reader.milo_bool()
    else:
        rate = reader.uint32()
        return
    anim_entry_count = reader.int32()
    for _ in range(anim_entry_count):
        anim_entry(reader)
    anim_count = reader.int32()
    for _ in range(anim_count):
        anim_object = reader.numstring()