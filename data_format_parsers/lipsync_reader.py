import bpy
import mathutils
from .. readers import *
from .. common import *
from .. bpy_util_funcs import *
from . trans_reader import *


def read_lipsync(self):
    reader = Reader(open(self.filepath, "rb").read(), self.filepath)
    get_endian(reader)
    version = reader.int32()
    print("lipsync", "version", version)
    always2 = reader.int32()
    dtaImport = reader.numstring()
    embedDtb = reader.byte()
    unknown1 = reader.int32()
    print("always2", always2, "dtaImport", dtaImport, "embedDtb", embedDtb, "unknown1", unknown1, )
    VisemeCount = reader.int32()
    visemeNames = []
    for x in range(VisemeCount):
        visemeName = reader.numstring()
        visemeNames.append(visemeName)
    print("VisemeCount", VisemeCount, "visemeNames", visemeNames)
    keyFrameCount = reader.int32()
    print("keyFrameCount", keyFrameCount)
    byteCount = reader.int32()
    print("byteCount", byteCount)
  # ^^^^^^^^^  how many bytes/how long the frame data is
    frames = []
    for x in range(keyFrameCount):
        current_frame = bpy.data.scenes[0].frame_current
        print("current_frame", current_frame)
        bpy.context.scene.frame_set(current_frame + 1)
        changeCount = reader.byte()
       # changeCount = int.from_bytes(changeCount1, "big")
        print("changeCount", changeCount)
        for x in range(changeCount):
            extension = ".vsm"
           # extension = ".ccs"
            visemeIndex = reader.byte()
           # visemeIndex = int.from_bytes(visemeIndex1, "big")
            print("visemeIndex", visemeIndex)
            Weight1 = reader.byte()
            Weight = Weight1 / 255
            print("Weight, Weight1", Weight, Weight1)
          # ^^^^^^  divide by 255 for -1/0/1 value
           # print("changeCount", changeCount, changeCount1, "visemeIndex", visemeIndex, "visemeNames", visemeNames[visemeIndex], "Weight", Weight)
    #   if nla track name is not in the viseme name list then set animation influence to 0
    #    no clue how to do this
            selarmature = bpy.context.object
            try:
                bpy.context.object.animation_data.nla_tracks[visemeNames[visemeIndex] + extension].strips[visemeNames[visemeIndex] + extension].frame_end_ui = keyFrameCount

                bpy.data.scenes["Scene"].frame_end = keyFrameCount 

               # bpy.context.object.animation_data.nla_tracks[visemeNames[visemeIndex] + extension].strips[visemeNames[visemeIndex] + extension].extrapolation = ‘NOTHING’
               # bpy.context.object.animation_data.nla_tracks[visemeNames[visemeIndex] + extension].strips[visemeNames[visemeIndex] + extension].blend_type = ‘COMBINE’

                bpy.context.object.animation_data.nla_tracks[visemeNames[visemeIndex] + extension].strips[visemeNames[visemeIndex] + extension].use_animated_influence

                bpy.context.object.animation_data.nla_tracks[visemeNames[visemeIndex] + extension].strips[visemeNames[visemeIndex] + extension].influence = Weight

                bpy.context.object.animation_data.nla_tracks[visemeNames[visemeIndex] + extension].strips[visemeNames[visemeIndex] + extension].keyframe_insert(data_path='influence', frame=current_frame)
            except:
                print("viseme doesnt exist", visemeNames[visemeIndex], visemeIndex,"skipping", visemeNames[visemeIndex] + extension)

#       COMMENT BLOB
#       woohoo
#       10/10 developers
#       
#       
#              NOTES
#       viseme animation system abuses animation smoothing
#       so not every frame has animation data
#       divide weights by 255 for -1/0/1 value