from .. common import *

def anim_entry(reader) -> None:
    name = reader.numstring()
    f1 = reader.float32()
    f2 = reader.float32()

def read_anim(reader, super: bool) -> None:
    version = reader.int32()
    print("version", version)
    read_metadata(reader, super)
    if version > 1:
        frame = reader.float32()
        print("frame", frame)
    if version < 4:
        if version > 2:
            unknown = reader.milo_bool()
            print("unknown", unknown)
    else:
        rate = reader.uint32()
        print("rate", rate)
        return
    anim_entry_count = reader.int32()
    for _ in range(anim_entry_count):
        anim_entry(reader)
    anim_count = reader.int32()
    for _ in range(anim_count):
        anim_object = reader.numstring()