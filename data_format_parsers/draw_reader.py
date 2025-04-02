from .. common import *

def read_draw(reader, super: bool) -> None:
    version = reader.int32()
    print("draw version", version)
   # read_metadata(reader, super)
   # print("read_metadata", read_metadata)
    showing = reader.milo_bool()
    print("showing", showing)
    if version < 2:
        draw_count = reader.int32()
        print("draw_count", draw_count)
        for _ in range(draw_count):
            if reader.version <= 6:
                draw_object = reader.string()
                print("draw_object", draw_object)
            else:
                draw_object = reader.numstring()
                print("draw_object", draw_object)
    if version > 0:
        sphere = reader.vec4f()
        print("sphere", sphere)
    if version > 2:
        draw_order = reader.float32()
        print("draw_order", draw_order)
    if version >= 4:
        override_include_in_depth_only_pass = reader.uint32()
       # print("override_include_in_depth_only_pass", override_include_in_depth_only_pass)