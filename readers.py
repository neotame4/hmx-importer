import struct

# Credit: Dodylectable
class Reader():
    def __init__(self, buffer: bytes, filepath: str) -> None:
        self.offset: int = 0
        self.data: bytes = buffer
        self.filepath = filepath
        self.length: int = len(buffer)
        self.little_endian: bool = True

    def size(self) -> int:
        return self.length

    def tell(self) -> int:
        return self.offset
    
    def seek(self, num: int) -> None:
        if num > 0:
            self.offset += num
        else:
            num = abs(num)
            self.offset -= num

    def skip(self, pos: int) -> None:
        self.offset = pos

    def read(self, fmt) -> tuple:
        result = struct.unpack_from(("" if self.little_endian else ">") + fmt, self.data, self.offset)
        self.offset += struct.calcsize(fmt)
        return result
    
    def read_bytes(self, length: int) -> bytes:
        result = self.read_bytes_at(0, length)
        self.offset += length
        return result
    
    def read_bytes_at(self, offset: int, length: int) -> bytes:
        return bytes(self.data)[self.offset + offset:self.offset + offset + length]


    def ubyte(self) -> int:
        return self.read("B")[0]
    
    def byte(self) -> int:
        return self.read("b")[0]
    

    def ushort(self) -> int:
        return self.read("H")[0]
    
    def short(self) -> int:
        return self.read("h")[0]
    

    def uint32(self) -> int:
        return self.read("I")[0]
    
    def int32(self) -> int:
        return self.read("i")[0]
    

    def hfloat16(self) -> float:
        return self.read("e")[0]
    
    def float32(self) -> float:
        return self.read("f")[0]
    

    def numstring(self) -> str:
        length = self.uint32()
        result = self.read_bytes(length)
        return result.decode("utf-8")
    
    def string(self) -> str:
        chars = []
        while True:
            byte = self.read_bytes(1)
            if byte == b"\x00" or not byte:
                break
            chars.append(byte)
        return b"".join(chars).decode("utf-8")      
    

    def milo_bool(self) -> bool:
        return self.read("?")[0]


    def vec2hf(self) -> tuple[float, float]:
        return self.read("2e")
    
    def vec2f(self) -> tuple[float, float]:
        return self.read("2f")
    
    def vec3us(self) -> tuple[int, int, int]:
        return self.read("3H")
    
    def vec3hf(self) -> tuple[float, float, float]:
        return self.read("3e")
    
    def vec3f(self) -> tuple[float, float, float]:
        return self.read("3f")
    
    def vec4s(self) -> tuple[int, int, int, int]:
        return self.read("4h")
    
    def vec4us(self) -> tuple[int, int, int, int]:
        return self.read("4H")
    
    def vec4ub(self) -> tuple[int, int, int, int]:
        return self.read("4B")
    
    def vec4hf(self) -> tuple[float, float, float, float]:
        return self.read("4e")
    
    def vec4f(self) -> tuple[float, float, float, float]:
        return self.read("4f")
    
    def vec8f(self) -> tuple[float, ...]:
        return self.read("8f")
    
    def matrix(self) -> tuple[float, ...]:
        return self.read("12f")