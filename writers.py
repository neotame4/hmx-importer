import struct

# Credit: Dodylectable
class Writer():
    def __init__(self, out_file) -> None:
        super().__init__()
        self.offset: int = 0
        self.file = out_file
        self.length: int = 0
        self.little_endian: bool = True
        self.platform: str = ""
        self.game: str = ""

    def write(self, fmt, *value) -> bytes:
        packed_value = struct.pack(("" if self.little_endian else ">") + fmt, *value)
        self.file.write(packed_value)
        self.offset += struct.calcsize(fmt)
        self.length = self.offset
        return packed_value
    
    def write_bytes(self, value: bytes) -> None:
        self.file.write(value)



    def ubyte(self, value: int) -> int:
        return self.write("B", value)[0]
    
    def byte(self, value: int) -> int:
        return self.write("b", value)[0]
    

    def ushort(self, value: int) -> int:
        return self.write("H", value)[0]
    
    def short(self, value: int) -> int:
        return self.write("h", value)[0]
    

    def uint32(self, value: int) -> int:
        return self.write("I", value)[0]
    
    def int32(self, value: int) -> int:
        return self.write("i", value)[0]
    

    def hfloat16(self, value: float) -> float:
        return self.write("e", value)[0]
    
    def float32(self, value: float) -> float:
        return self.write("f", value)[0]


    def numstring(self, text: str) -> None:
        self.uint32(len(text))
        encoded = text.encode('utf-8')
        self.write(f"{len(encoded)}s", encoded)

    def utf8_string(self, text: str) -> None:
        encoded = text.encode('utf-8')
        self.write(f"{len(encoded)}s", encoded)

    def string(self, text: str) -> None:
        encoded = text.encode('utf-8')
        self.write(f"{len(encoded)}s", encoded)
        self.byte(0)


    def milo_bool(self, value: bool) -> bool:
        return self.write("?", value)[0]
    

    def vec2hf(self, value: tuple[float, float]) -> tuple[float, float]:
        return self.write("2e", *value)
    
    def vec2f(self, value: tuple[float, float]) -> tuple[float, float]:
        return self.write("2f", *value)
    
    def vec3us(self, value: tuple[int, int, int]) -> tuple[int, int, int]:
        return self.write("3H", *value)
    
    def vec3hf(self, value: tuple[float, float, float]) -> tuple[float, float, float]:
        return self.write("3e", *value)
    
    def vec3f(self, value: tuple[float, float, float]) -> tuple[float, float, float]:
        return self.write("3f", *value)
    
    def vec4s(self, value: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
        return self.write("4h", *value)
    
    def vec4us(self, value: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
        return self.write("4H", *value)
    
    def vec4ub(self, value: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
        return self.write("4B", *value)
    
    def vec4hf(self, value: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
        return self.write("4e", *value)
    
    def vec4f(self, value: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
        return self.write("4f", *value)
    
    def vec8f(self, value: tuple[float, ...]) -> tuple[float, ...]:
        return self.write("8f", *value)
    
    def matrix(self, value: tuple[float, ...]) -> tuple[float, ...]:
        return self.write("12f", *value)