import os
import wave
from .. readers import *

def read_str(self) -> None:
    chunk_size = 512 * 2
    reader = Reader(open(self.filepath, "rb").read(), self.filepath)
    str_file = list(reader.read_bytes(reader.size()))
    fixed_str = [0] * (chunk_size)
    for i in range(0, len(str_file), chunk_size):
        chunk = str_file[i:i + chunk_size]
        half_size = len(chunk) // 2
        for j, d in enumerate(chunk[:half_size]):
            fixed_str[((j >> 1) * 4) + (j & 1)] = d
        for j, d in enumerate(chunk[half_size:]):
            fixed_str[((j >> 1) * 4) + (j & 1) + 2] = d
        str_file[i:i + chunk_size] = fixed_str[:len(chunk)]
    str_file = bytes(str_file)
    samples = convert_to_samples(str_file)
    create_wav(samples, self)
    
def convert_to_samples(str_file: bytes) -> bytes:
    samples = [0] * (len(str_file) // 2)
    for i in range(0, len(samples), 2):
        samples[i // 2] = str_file[i:i+2]
    for i in range(len(samples)):
        if not isinstance(samples[i], bytes):
            samples[i] = bytes(samples[i])
    return b"".join(samples)

def create_wav(samples: bytes, self) -> None:
    dirname = os.path.dirname(self.filepath)
    out_name = self.filepath.rsplit(".", 1)[0]
    path = os.path.join(dirname, out_name + ".wav")   
    with wave.open(path, "wb") as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(48000)
        wav.writeframes(samples)