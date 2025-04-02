import os
import wave
from .. readers import *

def channel_info(reader):
    sample_rate = reader.uint32()
    block_count = reader.uint32()
    return sample_rate

def read_vgs(self):
    reader = Reader(open(self.filepath, "rb").read(), self.filepath)
    magic = reader.read_bytes(4)
    version = reader.int32()
    for _ in range(15):
        sample_rate = channel_info(reader)

def create_wav(samples: bytes, self):
    dirname = os.path.dirname(self.filepath)
    out_name = self.filepath.rsplit(".", 1)[0]
    path = os.path.join(dirname, out_name + ".wav")   
    with wave.open(path, "wb") as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(48000)
        wav.writeframes(samples)