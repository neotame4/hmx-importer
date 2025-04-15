def default_transform() -> tuple:
    return (1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0)

def get_endian(reader) -> None:
    reader.little_endian = True
    value = reader.int32()
    reader.seek(-4)
    if (value > 255) or (value < 0) or (value == 0):
        reader.little_endian = False

def get_version(reader) -> int:
    return reader.int32()

def get_platform(filepath: str) -> str:
    extension = filepath.rsplit(".", 1)[1]
    if (extension == "rnd") or (extension.endswith("_ps2")):
        return "PS2"
    elif extension.endswith("_ps3"):
        return "PS3"
    elif extension.endswith("_xbox"):
        return "X360"
    elif extension.endswith("_wii"):
        return "Wii"
    elif extension.endswith("_gc"):
        return "GameCube"
    elif extension.endswith("_pc"):
        return "PC"
        
def dtb_parent(reader) -> None:
    child_count = reader.ushort()
    parent_id = reader.uint32()
    dtb_node(reader, child_count)

def dtb_node(reader, count: int) -> None:
    for _ in range(count):
        child_type = reader.int32()
        if child_type == 0:
            value = reader.uint32()
        elif child_type == 1:
            value = reader.float32()
        elif child_type in [2, 3, 4, 5, 7, 8, 9, 18, 32, 33, 34, 35, 36, 37]:
            value = reader.numstring()
        elif child_type in [16, 17, 19]:
            dtb_parent(reader)
        elif child_type == 20:
            size = reader.ushort()
            reader.read_bytes(size)

def dtb(reader) -> None:
    has_tree = reader.milo_bool()
    if has_tree == True:
        dtb_parent(reader)

def write_dtb(writer) -> None:
    writer.milo_bool(False)

def return_file_size(reader):
    start = reader.tell()
    end = reader.size()
    data = reader.read_bytes(end - start)
    result = data.find(b"\xAD\xDE\xAD\xDE")
    if result == -1:
        return
    reader.skip(start)
    return result
    
def find_next_file(reader) -> None:
    start = reader.tell()
    end = reader.size()
    data = reader.read_bytes(end - start)
    result = data.find(b"\xAD\xDE\xAD\xDE")
    if result == -1:
        return
    reader.skip(start)
    reader.read_bytes(result)

def metadata(reader) -> None:
    revision = reader.int32()
    print("revision", revision)
    metadata_type = reader.numstring()
    print("metadata_type", metadata_type)
    dtb(reader)
    if revision > 0:
        note = reader.numstring()
        print("note", note)

def metadatadetailed(reader) -> None:
    revision = reader.int32()
    print("revision", revision)
    metadata_type = reader.numstring()
    print("metadata_type", metadata_type)
    dtb(reader)
    if revision > 0:
        note = reader.numstring()
        print("note", note)
    return revision, metadata_type

def read_metadata(reader, super: bool) -> None:
    if super == True:
        return
    metadata(reader)

def read_metadatadetailed(reader, super: bool) -> None:
    if super == True:
        return
    revision, metadata_type = metadatadetailed(reader)
    print("metadata_type, revision", metadata_type, revision)
    return revision, metadata_type

def write_metadata(writer, super: bool) -> None:
    if super == True:
        return
    if writer.platform == "PS2":
        writer.int32(1)
    else:
        writer.int32(2)
    writer.numstring("")
    write_dtb(writer)
    writer.numstring("")