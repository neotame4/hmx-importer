from .. common import *

def lod_target(reader, version) -> None:
    screen_size = reader.float32()
    if version < 18:
        group = reader.numstring()
        if version >= 15:
            trans_group = reader.numstring()
    else:
        opaque_count = reader.uint32()
        for _ in range(opaque_count):
            opaque = reader.numstring()
        translucent_count = reader.uint32()
        for _ in range(translucent_count):
            translucent = reader.numstring() 

def lod_targets(reader, version) -> None:
    lod_count = reader.int32()
    for _ in range(lod_count):
        lod_target(reader, version)

def character_test(reader) -> None:
    version = reader.int32()
    driver = reader.numstring()
    clip1 = reader.numstring()
    clip2 = reader.numstring()
    teleport_to = reader.numstring()
    teleport_from = reader.numstring()
    dist_map = reader.numstring()
    value_0x7c = reader.int32()
    value_0x80 = reader.milo_bool()
    value_0x90 = reader.int32()
    if version == 8:
        force_lod = reader.int32()
    value_0x81 = reader.milo_bool()
    value_0x82 = reader.milo_bool()
    value_0x83 = reader.milo_bool()
    if version <= 6:
        unknown = reader.uint32()
    if version >= 15:
        value_0x84 = reader.milo_bool()
        return
    else:
        value_0x84 = reader.numstring()
    value_0x88 = reader.milo_bool()
    value_0x89 = reader.milo_bool()
    bpm = reader.int32()
    if version <= 6:
        return
    value_0x98 = reader.numstring()
    value_0x9c = reader.float32()
    if version > 8:
        value_0x54 = reader.numstring()