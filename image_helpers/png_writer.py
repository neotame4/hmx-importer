import zlib
import struct
from .. writers import *

def get_checksum(chunk_type: bytes, chunk_data: bytes) -> int:
    checksum = zlib.crc32(chunk_type)
    checksum = zlib.crc32(chunk_data, checksum)
    return checksum

def write_chunk(writer, chunk_type: bytes, chunk_data: bytes):
    writer.uint32(len(chunk_data))
    writer.write_bytes(chunk_type)
    writer.write_bytes(chunk_data)
    writer.uint32(get_checksum(chunk_type, chunk_data))

def make_ihdr(width: int, height: int) -> bytes:
    return struct.pack('>2I5B', width, height, 8, 6, 0, 0, 0)

def encode_image(image_data: list, width: int) -> list:
    encoded_image = []
    for row_start in range(0, len(image_data), width * 4):
        row = image_data[row_start:row_start + width * 4]
        filtered_row = bytes([0]) + bytes(row)
        encoded_image.append(filtered_row)
    return encoded_image

def compress_image(image_data: list) -> bytes:
    return zlib.compress(b"".join(image_data))

def make_idat(image_data: list, width: int) -> bytes:
    encoded_image = encode_image(image_data, width)
    compressed_image = compress_image(encoded_image)
    return compressed_image

def write_png(output_path: str, width: int, height: int, image_data: list) -> None:
    with open(output_path, "wb") as f:
        writer = Writer(f)
        writer.little_endian = False
        writer.write_bytes(b"\x89PNG\r\n\x1A\n")
        ihdr = make_ihdr(width, height)
        write_chunk(writer, b"IHDR", ihdr)
        compressed_image = make_idat(image_data, width)
        write_chunk(writer, b"IDAT", compressed_image)
        write_chunk(writer, b"IEND", b"")