from .. common import *

# credits to compvir for a lot of the code here

def write_matrix(writer, translation: tuple[float, float, float]) -> None:
    writer.vec3f((1.0, 0.0, 0.0))
    writer.vec3f((0.0, 1.0, 0.0))
    writer.vec3f((0.0, 0.0, 1.0))
    for value in translation:
        writer.float32(value)
    
def write_trans(writer, super: bool, local_translation: tuple[float, float, float], world_translation: tuple[float, float, float], parent: str = ""):
    if (writer.game == "Frequency") or (writer.game == "Amplitude"):
        writer.int32(5)
    elif writer.game == "Karaoke Revolution":
        writer.int32(7)
    elif (writer.game == "AntiGrav") or (writer.game == "GH1"):
        writer.int32(8)
    else:
        writer.int32(9)
    write_metadata(writer, super)
    write_matrix(writer, local_translation)
    write_matrix(writer, world_translation)
    if writer.game in ["Frequency", "Amplitude", "AntiGrav", "Karaoke Revolution", "GH1"]:
        writer.int32(0)
    writer.uint32(0)
    if (writer.game == "Frequency") or (writer.game == "Amplitude"):
        for _ in range(4):
            writer.uint32(0)
    if not writer.game in ["Frequency", "Amplitude", "Karaoke Revolution"]:
        writer.numstring("")
    if writer.game == "Karaoke Revolution":
        for _ in range(5):
            writer.float32(0)
    if not (writer.game == "Frequency") or (writer.game == "Amplitude"):
        writer.milo_bool(False)
        writer.numstring(parent)