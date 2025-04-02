from .. common import *

def write_anim(writer, self):
    if writer.game in ["Frequency", "Amplitude", "Karaoke Revolution", "GH1"]:
        writer.int32(0)
    else:
        writer.int32(4)
    write_metadata(writer, True)
    if writer.game not in ["Frequency", "Amplitude", "Karaoke Revolution", "GH1"]:
        writer.float32(0)
        writer.int32(0)
        return
    writer.write("2I", *([0] * 2))