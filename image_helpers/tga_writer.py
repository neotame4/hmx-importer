from .. writers import *

def fix_colors(image: list) -> list:
    new_image = image
    buffer = [0] * 4
    for i in range(0, len(new_image), 4):
        buffer[:] = new_image[i:i + 4]
        # BGRA
        new_image[i + 0] = buffer[2]
        new_image[i + 1] = buffer[1]
        new_image[i + 2] = buffer[0]
        new_image[i + 3] = buffer[3]
    return new_image

def fix_rows(image: list, width: int, height: int) -> bytearray:
    row_size = width * 4
    fixed_image = bytearray()
    for row in range(height):
        start = (height - 1 - row) * row_size
        fixed_image.extend(image[start:start + row_size])
    return fixed_image

def fix_image(image: list, width: int, height: int) -> bytearray:
    new_image = fix_colors(image)
    new_image = fix_rows(new_image, width, height)
    return new_image

def write_tga(output_path: str, width: int, height: int, image: bytes) -> None:
    with open(output_path, "wb") as f:
        writer = Writer(f)
        for _ in range(2):
            writer.ubyte(0)
        writer.ubyte(2)
        for _ in range(2):
            writer.short(0)
        writer.ubyte(0)
        for _ in range(2):
            writer.short(0)
        writer.short(width)
        writer.short(height)
        writer.ubyte(32)
        writer.ubyte(0)
        image = list(image)
        fixed_image = fix_image(image, width, height)
        writer.write_bytes(fixed_image)