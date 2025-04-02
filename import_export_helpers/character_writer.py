def write_character_test(writer):
    if writer.game == "GH2 X360":
        writer.int32(6)
    elif writer.game == "RB1 / RB2":
        writer.int32(8)
    elif writer.game != "RB3 / DC1":
        writer.int32(10)
    else:
        writer.int32(15)
    for _ in range(5):
        writer.numstring("")
    if writer.game == "GH2 X360":
        return
    writer.numstring("none")
    writer.int32(0)
    writer.milo_bool(False)
    writer.int32(0)
    if writer.game == "RB1 / RB2":
        writer.int32(-1)
    for _ in range(3):
        writer.milo_bool(False)
    if writer.game == "RB3 / DC1":
        writer.milo_bool(False)
        return
    else:
        writer.numstring("none")
    for _ in range(2):
        writer.milo_bool(False)
    writer.int32(120)
    writer.numstring("")
    writer.float32(3)
    if not (writer.game == "GH2 X360") or (writer.game == "RB1 / RB2"):
        writer.numstring("")