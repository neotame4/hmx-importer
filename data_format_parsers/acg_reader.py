import bpy
from .. readers import *
from .. common import *
from .. bpy_util_funcs import *

def AcgEntry2(reader):
    unknown = reader.int32()	# Frame count? - Matches acpentry index when entry count2 = 1
    f1 = reader.float32()	# Full?
    f2 = reader.float32()	# One?
    print("unknown, f1, f2", unknown, f1, f2)
   # return unknown, f1, f2

def AcgEntry1(reader):
    count2 = reader.int32()
    print("count2", count2)
    for _ in range(count2):
        AcgEntry2(reader)
   # return count_per_sample2, bone_names2

def read_acg(self):
    reader = Reader(open(self.filepath, "rb").read(), self.filepath)
    get_endian(reader)
    version = reader.int32()	# Always 1
    count1 = reader.int32()
    print("version, count1", version, count1)
    for _ in range(count1):
        AcgEntry1(reader)      