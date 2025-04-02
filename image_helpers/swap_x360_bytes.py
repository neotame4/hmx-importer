def swap_x360_bytes(bitmap: bytes) -> bytes:
    flipped_bitmap = []
    for i in range(0, len(bitmap), 2):
        if i + 1 < len(bitmap):
            flipped_bitmap.append(bitmap[i + 1])
            flipped_bitmap.append(bitmap[i])
        else:
            flipped_bitmap.append(bitmap[i])
    return bytes(flipped_bitmap)