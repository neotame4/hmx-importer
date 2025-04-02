# credits to dody
def invert_uv_map(uvs: tuple[float, float]) -> tuple[float, float]:
    return (uvs[0], 1 - uvs[1])

def reverse_vector(vector: tuple) -> tuple:
    return (vector[3], vector[2], vector[1], vector[0])

def unsigned_compressed_vec4(value: int) -> tuple[float, float, float, float]:
    w_bits = int(value >> 30 & 3)
    z_bits = int(value >> 20 & 1023)
    y_bits = int(value >> 10 & 1023)
    x_bits = int(value & 1023)
    x = float(x_bits / float(1023))
    y = float(y_bits / float(1023))
    z = float(z_bits / float(1023))
    w = float(w_bits / float(3))
    return (x, y, z, w)

def ps3_weights_math(weights: tuple[int, int, int, int]) -> tuple[float, float, float, float]:
    return (weights[0] / 255.0, weights[1] / 255.0, weights[2] / 255.0, weights[3] / 255.0)

def pos_math(pos: int) -> float:
    return (pos / 32767.0)

def pos_math3(pos: tuple[int, int, int]) -> tuple[float, float, float]:
    return ((pos[0] / 32767.0 * 1280), (pos[1] / 32767.0 * 1280), (pos[2] / 32767.0 * 1280))

def quat_math(quat: int) -> float:
    return (quat / 32767.0)

def quat_math4(quat: tuple[int, int, int, int]) -> tuple[float, float, float, float]:
    return (quat[0] / 32767.0, quat[1] / 32767.0, quat[2] / 32767.0, quat[3] / 32767.0)

def rotz_math(rotz: int) -> float:
    return (rotz / 32767.0) / 0.5 * 10