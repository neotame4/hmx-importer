def create_block_map(map: list) -> None:
    half_size = len(map) // 2
    for i in range(half_size):
        map[i] = i * 2
    for i in range(half_size, len(map)):
        map[i] = ((i % half_size) * 2) + 1
    
def shuffle_wii_blocks(bitmap: bytes, width: int, height: int) -> bytes:
    blocks_x = width // 4
    blocks_y = height // 4
    total_grouped_blocks = (blocks_x * blocks_y) // 2
    block_map = [0] * blocks_x
    create_block_map(block_map)
    orig_data = [0] * (blocks_x * 16)
    bitmap = list(bitmap)
    for i in range(total_grouped_blocks):
        o = i // blocks_x
        x = i % blocks_x
        current_working_index = o * blocks_x
        current_index = x * 16
        new_index = block_map[x] * 16
        if x == 0:
            working_start = o * (blocks_x * 16)
            orig_data[:] = bitmap[working_start:working_start + blocks_x * 16]
        bitmap[current_working_index * 16 + new_index:current_working_index * 16 + new_index + 16] = orig_data[current_index:current_index + 16]
    bitmap = fix_colors_and_indices(bitmap)
    return bitmap

def fix_colors_and_indices(bitmap: list):
    buffer = [0] * 8
    for i in range(0, len(bitmap), 8):
        buffer[:] = bitmap[i:i + 4]
        bitmap[i + 0] = buffer[1]
        bitmap[i + 1] = buffer[0]
        bitmap[i + 2] = buffer[3]
        bitmap[i + 3] = buffer[2]
        buffer[:] = bitmap[i + 4:i + 8]
        bitmap[i + 4] = reverse_index_row(buffer[0])
        bitmap[i + 5] = reverse_index_row(buffer[1])
        bitmap[i + 6] = reverse_index_row(buffer[2])
        bitmap[i + 7] = reverse_index_row(buffer[3])       
    return bytes(bitmap)

def reverse_index_row(byte: int) -> int:
    return (((byte & 0b00_00_00_11) << 6) | ((byte & 0b00_00_11_00) << 2) | ((byte & 0b00_11_00_00) >> 2) | ((byte & 0b11_00_00_00) >> 6))