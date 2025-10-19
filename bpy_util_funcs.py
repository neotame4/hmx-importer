# credits to dody
def invert_uv_map(uvs: tuple[float, float]) -> tuple[float, float]:
    return (uvs[0], 1 - uvs[1])

def reverse_vector(vector: tuple) -> tuple:
    return (vector[3], vector[2], vector[1], vector[0])

def signed_compressed_vec4(value: int) -> tuple[float, float, float, float]:
    MAX_2_BIT_SIGNED = (1 << 1) - 1
    MASK_2_BIT = (1 << 2) - 1
    MAX_10_BIT_SIGNED = (1 << 9) - 1
    MASK_10_BIT = (1 << 10) - 1
    w_bits = int(value >> 30 & MASK_2_BIT)
    z_bits = int(value >> 20 & MASK_10_BIT)
    y_bits = int(value >> 10 & MASK_10_BIT)
    x_bits = int(value & MASK_10_BIT)
    if x_bits > MAX_10_BIT_SIGNED:
        x_bits = -1 * (~(x_bits - 1) & (MASK_10_BIT >> 1))
    if y_bits > MAX_10_BIT_SIGNED:
        y_bits = -1 * (~(y_bits - 1) & (MASK_10_BIT >> 1))
    if z_bits > MAX_10_BIT_SIGNED:
        z_bits = -1 * (~(z_bits - 1) & (MASK_10_BIT >> 1))
    if w_bits > MAX_2_BIT_SIGNED:
        w_bits = -1 * (~(w_bits - 1) & (MASK_2_BIT >> 1))
    x = float(x_bits / float(MAX_10_BIT_SIGNED))
    y = float(y_bits / float(MAX_10_BIT_SIGNED))
    z = float(z_bits / float(MAX_10_BIT_SIGNED))
    w = float(w_bits / float(MAX_2_BIT_SIGNED))
    return (x, y, z, w)

def unsigned_compressed_vec4(value: int) -> tuple[float, float, float, float]:
    MAX_2_BIT_UNSIGNED = (1 << 2) - 1
    MASK_2_BIT = (1 << 2) - 1
    MAX_10_BIT_UNSIGNED = (1 << 10) - 1
    MASK_10_BIT = (1 << 10) - 1
    w_bits = int(value >> 30 & MASK_2_BIT)
    z_bits = int(value >> 20 & MASK_10_BIT)
    y_bits = int(value >> 10 & MASK_10_BIT)
    x_bits = int(value & MASK_10_BIT)
    x = float(x_bits / float(MAX_10_BIT_UNSIGNED))
    y = float(y_bits / float(MAX_10_BIT_UNSIGNED))
    z = float(z_bits / float(MAX_10_BIT_UNSIGNED))
    w = float(w_bits / float(MAX_2_BIT_UNSIGNED))
    return (x, y, z, w)

def ps3_weights_math(weights: tuple[int, int, int, int]) -> tuple[float, float, float, float]:
    return (weights[0] / 255.0, weights[1] / 255.0, weights[2] / 255.0, weights[3] / 255.0)

def pos_math(pos: int) -> float:
    return (pos / 32767.0 * 1280)

def pos_math3(pos: tuple[int, int, int]) -> tuple[float, float, float]:
    return ((pos[0] / 32767.0 * 1280), (pos[1] / 32767.0 * 1280), (pos[2] / 32767.0 * 1280))

def quat_math(quat: int) -> float:
    return (quat / 32767.0)

def d256math(value: int) -> float:
    return (value / 256.0)

def d256math4(value: tuple[int, int, int, int]) -> tuple[float, float, float, float]:
    return (value[0] / 256.0, value[1] / 256.0, value[2] / 256.0, value[3] / 256.0)

def quat_math4(quat: tuple[int, int, int, int]) -> tuple[float, float, float, float]:
    return (quat[0] / 32767.0, quat[1] / 32767.0, quat[2] / 32767.0, quat[3] / 32767.0)

def rotz_math(rotz: int) -> float:
    return (rotz / 32767.0) / 0.5 * 10
    
def phase_math(value: int) -> float:
    return (value / 65536.0)
def phase_math2(value: tuple[int, int]) -> tuple[float, float]:
    return ((value[0] / 65536.0), (value[1] / 65536.0))
def phase_math3(value: tuple[int, int, int]) -> tuple[float, float, float]:
    return ((value[0] / 65536.0), (value[1] / 65536.0), (value[2] / 65536.0))
def phase_math4(value: tuple[int, int, int, int]) -> tuple[float, float, float, float]:

    return ((value[0] / 65536.0), (value[1] / 65536.0), (value[2] / 65536.0), (value[3] / 65536.0))
