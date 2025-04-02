import os
import wave
from .. common import *
from .. readers import *
from .. writers import *

def read_sample_data(reader, name: str, self) -> None:
    sample_data = {}
    version = reader.int32()
    if version == 16:
        unknown = reader.uint32()
    encoding = reader.int32()
    sample_data["encoding"] = encoding
    sample_count = reader.int32()
    sample_data["sample_count"] = sample_count
    sample_rate = reader.int32()
    sample_data["sample_rate"] = sample_rate
    samples_size = reader.int32()
    sample_data["samples_size"] = samples_size
    read_samples = reader.milo_bool()
    samples = reader.read_bytes(samples_size)
    # dance central bruh...?
    if version >= 14:
        unknown_int = reader.int32()
    find_next_file(reader)
    create_wav(samples, sample_data, name, self)

def create_wav(samples: bytes, sample_data: dict, filepath: str, self) -> None:
    encoding = sample_data["encoding"]
    sample_count = sample_data["sample_count"]
    sample_rate = sample_data["sample_rate"]
    samples_size = sample_data["samples_size"]
    dirname = os.path.dirname(self.filepath)
    if encoding == 3:
        basename = filepath.rsplit(".", 1)[0] + ".xma"
    else:
        basename = filepath
    dirname = os.path.dirname(dirname) + "\\samples"
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    path = os.path.join(dirname, basename)   
    if encoding == 1:
        with wave.open(path, "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate)
            wav.writeframes(samples)
    elif encoding == 3:
        with open(path, "wb") as f:
            writer = Writer(f)
            writer.utf8_string("RIFF")
            writer.int32(samples_size + 72)
            writer.utf8_string("WAVE")
            writer.utf8_string("fmt")
            writer.write_bytes(b"\x20")
            writer.int32(52)
            writer.short(358)
            writer.ushort(1)
            for _ in range(2):
                writer.uint32(sample_rate)
            writer.ushort(2)
            writer.ushort(16)
            writer.ushort(34)
            writer.ushort(1)
            writer.uint32(4)
            writer.uint32(sample_count)
            writer.uint32(65536)
            writer.uint32(0)
            writer.uint32(sample_count)
            for _ in range(2):
                writer.uint32(0)
            writer.ubyte(0)
            writer.ubyte(4)
            writer.ushort(samples_size // 2048)
            writer.utf8_string("data")
            writer.int32(samples_size)
            writer.write_bytes(samples)
    elif encoding == 5:
        with open(path, "wb") as f:
            writer = Writer(f)
            writer.int32(sample_rate)
            writer.int32(samples_size)
            writer.write_bytes(samples)