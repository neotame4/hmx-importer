import bpy
import mathutils
from .. common import *
from .. bpy_util_funcs import *
from . trans_reader import *
from . anim_reader import *


def read_particlesys(reader, name, super: bool) -> None:
    version = reader.int32()
   # read_metadata(reader, super)
   # read_anim(reader, True)

   # if version == 30
    print("particlesys", "name, version", name, version)
    find_next_file(reader)
    return