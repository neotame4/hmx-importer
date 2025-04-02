from .. common import *

def write_draw(writer) -> None:
    if (writer.game == "Frequency") or (writer.game == "Amplitude"):
        writer.int32(0)
    elif (writer.game == "AntiGrav") or (writer.game == "GH1"):
        writer.int32(1)
    elif writer.game != "GDRB":
        writer.int32(3)
    else:
        writer.int32(4)
    write_metadata(writer, True)
    writer.milo_bool(True)
    if writer.game in ["Frequency", "Amplitude", "AntiGrav", "GH1"]:
        writer.int32(0)
    if not (writer.game == "Frequency") or (writer.game == "Amplitude"):
        writer.vec4f((0.0, 0.0, 0.0, 0.0))
    if writer.game not in ["Frequency", "Amplitude", "AntiGrav", "GH1"]:    
        writer.float32(0)
    if writer.game == "GDRB":
        writer.int32(0)