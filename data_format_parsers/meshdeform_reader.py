import bpy
import mathutils
from .. common import *
from .. bpy_util_funcs import *
from . trans_reader import *


def read_meshdeform(reader, name, super: bool) -> None:
    version = reader.int32()
#   1(), 2,(), 3(KR),
    print("meshdeform", "name, version", name, version)
    mesh_target = reader.numstring()
# this doesnt really do anything so
#          ¯\_(ツ)_/¯
    find_next_file(reader)
    return