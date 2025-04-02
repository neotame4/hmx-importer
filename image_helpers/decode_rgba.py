def decode_rgba(bitmap: bytes, width: int, height: int, bpp: int, color_palette: bytes = None) -> list:
    image = [0] * (width * height * 4)
    if bpp == 4:
        o = (len(color_palette) // 32) * 32
        bitmap = color_palette + bitmap
        r = 0
        p1 = p2 = p3 = p4 = 0
        for i in range(0, len(image), 16):
            p1 = (bitmap[o + r] & 0x0F) << 2
            p2 = (bitmap[o + r] & 0xF0) >> 2
            p3 = (bitmap[o + r + 1] & 0X0F) << 2
            p4 = (bitmap[o + r + 1] & 0xF0) >> 2
            image[i] = color_palette[p1]
            image[i + 1] = color_palette[p1 + 1]
            image[i + 2] = color_palette[p1 + 2]
            image[i + 3] = color_palette[p1 + 3]
            image[i + 4] = color_palette[p2]
            image[i + 5] = color_palette[p2 + 1]
            image[i + 6] = color_palette[p2 + 2]
            image[i + 7] = color_palette[p2 + 3]            
            image[i + 8] = color_palette[p3]
            image[i + 9] = color_palette[p3 + 1]
            image[i + 10] = color_palette[p3 + 2]
            image[i + 11] = color_palette[p3 + 3]
            image[i + 12] = color_palette[p4]
            image[i + 13] = color_palette[p4 + 1]
            image[i + 14] = color_palette[p4 + 2]
            image[i + 15] = color_palette[p4 + 3]
            r += 2
        image = fix_alpha(image)
    elif bpp == 8:
        o = (len(color_palette) // 32) * 32
        bitmap = color_palette + bitmap
        r = 0
        p1 = p2 = p3 = p4 = 0     
        for i in range(0, len(image), 16):
            p1 = ((0xE7 & bitmap[o + r])) + ((0x08 & bitmap[o + r]) << 1) + ((0x10 & bitmap[o + r]) >> 1) << 2
            p2 = ((0xE7 & bitmap[o + r + 1])) + ((0x08 & bitmap[o + r + 1]) << 1) + ((0x10 & bitmap[o + r + 1]) >> 1) << 2
            p3 = ((0xE7 & bitmap[o + r + 2])) + ((0x08 & bitmap[o + r + 2]) << 1) + ((0x10 & bitmap[o + r + 2]) >> 1) << 2
            p4 = ((0xE7 & bitmap[o + r + 3])) + ((0x08 & bitmap[o + r + 3]) << 1) + ((0x10 & bitmap[o + r + 3]) >> 1) << 2
            image[i] = color_palette[p1]
            image[i + 1] = color_palette[p1 + 1]
            image[i + 2] = color_palette[p1 + 2]
            image[i + 3] = color_palette[p1 + 3]
            image[i + 4] = color_palette[p2]
            image[i + 5] = color_palette[p2 + 1]
            image[i + 6] = color_palette[p2 + 2]
            image[i + 7] = color_palette[p2 + 3]            
            image[i + 8] = color_palette[p3]
            image[i + 9] = color_palette[p3 + 1]
            image[i + 10] = color_palette[p3 + 2]
            image[i + 11] = color_palette[p3 + 3]
            image[i + 12] = color_palette[p4]
            image[i + 13] = color_palette[p4 + 1]
            image[i + 14] = color_palette[p4 + 2]
            image[i + 15] = color_palette[p4 + 3]
            r += 4      
        image = fix_alpha(image)
    elif bpp == 24:
        r = 0
        for i in range(0, len(image), 16):
            image[i] = bitmap[r + 2]
            image[i + 1] = bitmap[r + 1]
            image[i + 2] = bitmap[r]
            image[i + 3] = 0xFF
            image[i + 4] = bitmap[r + 5]
            image[i + 5] = bitmap[r + 4]
            image[i + 6] = bitmap[r + 3]
            image[i + 7] = 0xFF
            image[i + 8] = bitmap[r + 8]
            image[i + 9] = bitmap[r + 7]
            image[i + 10] = bitmap[r + 6]
            image[i + 11] = 0xFF
            image[i + 12] = bitmap[r + 11]
            image[i + 13] = bitmap[r + 10]
            image[i + 14] = bitmap[r + 9]
            image[i + 15] = 0xFF
            r += 12
    return image

def fix_alpha(image: list) -> list:
    for i in range(3, len(image), 4):
        alpha = image[i]
        if alpha & 0x80:
            image[i] = 0xFF
        else:
            image[i] = alpha << 1
    return image