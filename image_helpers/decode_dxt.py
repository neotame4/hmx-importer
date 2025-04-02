import struct

def linear_offset(x: int, y: int, w: int) -> int:
    return (y * (w << 2)) + (x << 2)

def c2a(a: int, b: int) -> int:
    return (2 * a + b) // 3

def c2b(a: int, b: int) -> int:
    return (a + b) // 2

def c3(a: int, b: int) -> int:
    return (2 * b + a) // 3

def unpack_24_bit_indices(packed: int) -> list:
    indices = []
    indices.append(packed & 0b0111)
    indices.append(((packed & (0b0111 <<  3)) >>  3))
    indices.append(((packed & (0b0111 <<  6)) >>  6))
    indices.append(((packed & (0b0111 <<  9)) >>  9))
    indices.append(((packed & (0b0111 <<  12)) >>  12))
    indices.append(((packed & (0b0111 <<  15)) >>  15))
    indices.append(((packed & (0b0111 <<  18)) >>  18))
    indices.append(((packed & (0b0111 <<  21)) >>  21))
    return indices

def interpolate_colors(c0: int, c1: int) -> list:
    colors = []
    if c0 > c1:
        colors.append(c0)
        colors.append(c1)
        colors.append((((6.0 / 7.0) * c0) + ((1.0 / 7.0) * c1)))
        colors.append((((5.0 / 7.0) * c0) + ((2.0 / 7.0) * c1)))
        colors.append((((4.0 / 7.0) * c0) + ((3.0 / 7.0) * c1)))
        colors.append((((3.0 / 7.0) * c0) + ((4.0 / 7.0) * c1)))
        colors.append((((2.0 / 7.0) * c0) + ((5.0 / 7.0) * c1)))
        colors.append((((1.0 / 7.0) * c0) + ((6.0 / 7.0) * c1)))
    else:
        colors.append(c0)
        colors.append(c1)
        colors.append((((4.0 / 5.0) * c0) + ((1.0 / 5.0) * c1)))
        colors.append((((3.0 / 5.0) * c0) + ((2.0 / 5.0) * c1)))
        colors.append((((2.0 / 5.0) * c0) + ((3.0 / 5.0) * c1)))
        colors.append((((1.0 / 5.0) * c0) + ((4.0 / 5.0) * c1)))
        colors.append(0x00)
        colors.append(0xFF)
    return colors

def unpack_indexed_interpolated_colors(bitmap: bytes, i: int) -> list:
    pixels = [0] * 16
    colors = interpolate_colors(bitmap[i], bitmap[i + 1])
    packed_0 = (bitmap[i + 4] << 16) | (bitmap[i + 3] << 8) | (bitmap[i + 2])
    packed_1 = (bitmap[i + 7] << 16) | (bitmap[i + 6] << 8) | (bitmap[i + 5])
    indices = unpack_24_bit_indices(packed_0)
    pixels[0] = colors[indices[0]]
    pixels[1] = colors[indices[1]]
    pixels[2] = colors[indices[2]]
    pixels[3] = colors[indices[3]]
    pixels[4] = colors[indices[4]]
    pixels[5] = colors[indices[5]]
    pixels[6] = colors[indices[6]]
    pixels[7] = colors[indices[7]]
    indices = unpack_24_bit_indices(packed_1)
    pixels[8] = colors[indices[0]]
    pixels[9] = colors[indices[1]]
    pixels[10] = colors[indices[2]]
    pixels[11] = colors[indices[3]]
    pixels[12] = colors[indices[4]]
    pixels[13] = colors[indices[5]]
    pixels[14] = colors[indices[6]]
    pixels[15] = colors[indices[7]]
    return pixels

def unpack_rgb565(c: int) -> tuple[int, int, int]:
    r = ((c >> 11) & 0x1F) << 3
    g = ((c >> 5) & 0x3F) << 2
    b = (c & 0x1F) << 3
    return r, g, b

def dxtc_alpha(alpha_0: int, alpha_1: int, alpha_c_0: int, alpha_c_1: int, ai: int) -> int:
    if ai <= 12:
        alpha_c = (alpha_c_0 >> ai) & 7
    elif ai == 15:
        alpha_c = (alpha_c_0 >> 15) | ((alpha_c_1 << 1) & 6)
    else:
        alpha_c = (alpha_c_1 >> (ai - 16)) & 7
    if alpha_c == 0:
        alpha = alpha_0
    elif alpha_c == 1:
        alpha = alpha_1
    elif alpha_0 > alpha_1:
        alpha = ((8 - alpha_c) * alpha_0 + (alpha_c - 1) * alpha_1) // 7
    elif alpha_c == 6:
        alpha = 0
    elif alpha_c == 7:
        alpha = 0xFF
    else:
        alpha = ((6 - alpha_c) * alpha_0 + (alpha_c - 1) * alpha_1) // 5
    return alpha

def decode_dxt1(reader, width: int, height: int) -> list:
    image = [0] * (width * height * 4)
    for y in range(0, height, 4):
        for x in range(0, width, 4):
            color_0, color_1, bits = struct.unpack("HHI", reader.read_bytes(8))
            r0, g0, b0 = unpack_rgb565(color_0)
            r1, g1, b1 = unpack_rgb565(color_1)
            for j in range(4):
                for i in range(4):
                    control = bits & 3
                    bits = bits >> 2
                    if control == 0:
                        r, g, b = r0, g0, b0
                    elif control == 1:
                        r, g, b = r1, g1, b1
                    elif control == 2:
                        if color_0 > color_1:
                            r, g, b = c2a(r0, r1), c2a(g0, g1), c2a(b0, b1)
                        else:
                            r, g, b = c2b(r0, r1), c2b(g0, g1), c2a(b0, b1)
                    elif control == 3:
                        if color_0 > color_1:
                            r, g, b = c3(r0, r1), c3(g0, g1), c3(b0, b1)
                        else:
                            r, g, b = 0, 0, 0
                    idx = 4 * ((y + j) * width + x + i)
                    image[idx:idx + 4] = struct.pack("4B", r, g, b, 255)
    return image

def decode_dxt5(reader, width: int, height: int) -> list:
    image = [0] * (width * height * 4)
    for y in range(0, height, 4):
        for x in range(0, width, 4):
            alpha_0, alpha_1, alpha_c_0, alpha_c_1, color_0, color_1, code = struct.unpack("2BHI2HI", reader.read_bytes(16))
            r0, g0, b0 = unpack_rgb565(color_0)
            r1, g1, b1 = unpack_rgb565(color_1)
            for j in range(4):
                for i in range(4):
                    ai = 3 * (4 * j + i)
                    alpha = dxtc_alpha(alpha_0, alpha_1, alpha_c_0, alpha_c_1, ai)
                    color_c = (code >> 2 * (4 * j + i)) & 3
                    if color_c == 0:
                        r, g, b = r0, g0, b0
                    elif color_c == 1:
                        r, g, b = r1, g1, b1
                    elif color_c == 2:
                        r, g, b = c2a(r0, r1), c2a(g0, g1), c2a(b0, b1)
                    elif color_c == 3:
                        r, g, b = c3(r0, r1), c3(g0, g1), c3(b0, b1)
                    idx = 4 * ((y + j) * width + x + i)
                    image[idx:idx + 4] = struct.pack("4B", r, g, b, alpha)      
    return image

def decode_ati2(reader, width: int, height: int) -> list:
    bitmap = reader.read_bytes(reader.size())
    image = [0] * (width * height * 4)
    blocks_x = width >> 2
    blocks_y = height >> 2
    block_size = 8
    i = 0
    for by in range(blocks_y):
        for bx in range(blocks_x):
            x = bx << 2
            y = by << 2
            reds = unpack_indexed_interpolated_colors(bitmap, i)
            greens = unpack_indexed_interpolated_colors(bitmap, i + 8)
            normal_colors = [0] * 64
            for c in range(len(reds)):
                normal_colors[(c << 2)] = reds[c]
                normal_colors[(c << 2) + 1] = greens[c]
                normal_colors[(c << 2) + 2] = 0x00
                normal_colors[(c << 2) + 3] = 0xFF
            image[linear_offset(x, y, width):linear_offset(x, y, width) + 4] = normal_colors[0:4]
            image[linear_offset(x + 1, y, width):linear_offset(x + 1, y, width) + 4] = normal_colors[4:8]
            image[linear_offset(x + 2, y, width):linear_offset(x + 2, y, width) + 4] = normal_colors[8:12]
            image[linear_offset(x + 3, y, width):linear_offset(x + 3, y, width) + 4] = normal_colors[12:16]
            image[linear_offset(x, y + 1, width):linear_offset(x, y + 1, width) + 4] = normal_colors[16:20]
            image[linear_offset(x + 1, y + 1, width):linear_offset(x + 1, y + 1, width) + 4] = normal_colors[20:24]
            image[linear_offset(x + 2, y + 1, width):linear_offset(x + 2, y + 1, width) + 4] = normal_colors[24:28]
            image[linear_offset(x + 3, y + 1, width):linear_offset(x + 3, y + 1, width) + 4] = normal_colors[28:32]
            image[linear_offset(x, y + 2, width):linear_offset(x, y + 2, width) + 4] = normal_colors[32:36]
            image[linear_offset(x + 1, y + 2, width):linear_offset(x + 1, y + 2, width) + 4] = normal_colors[36:40]
            image[linear_offset(x + 2, y + 2, width):linear_offset(x + 2, y + 2, width) + 4] = normal_colors[40:44]
            image[linear_offset(x + 3, y + 2, width):linear_offset(x + 3, y + 2, width) + 4] = normal_colors[44:48]     
            image[linear_offset(x, y + 3, width):linear_offset(x, y + 3, width) + 4] = normal_colors[48:52]
            image[linear_offset(x + 1, y + 3, width):linear_offset(x + 1, y + 3, width) + 4] = normal_colors[52:56]
            image[linear_offset(x + 2, y + 3, width):linear_offset(x + 2, y + 3, width) + 4] = normal_colors[56:60]
            image[linear_offset(x + 3, y + 3, width):linear_offset(x + 3, y + 3, width) + 4] = normal_colors[60:64]     
            i += block_size << 1   
    for i in range(len(image)):
        if isinstance(image[i], float):
            image[i] = int(image[i])
    return image