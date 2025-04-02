import gzip
import zlib

def decompress_gzip(compressed: bytes) -> bytes:
    return gzip.decompress(compressed)

def decompress_zlib_deflate(compressed: bytes) -> bytes:
    return zlib.decompress(compressed, -15)