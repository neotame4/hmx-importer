import bpy
import mathutils
from .. common import *
from .. bpy_util_funcs import *
from . trans_reader import *


def read_flare(reader, name, super: bool) -> None:
    version = reader.int32()
    print("flare", "name, version", name, version)
    find_next_file(reader)
    return