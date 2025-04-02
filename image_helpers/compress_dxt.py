import os
import subprocess

#if platform == "Linux":
    #dxt_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "texconv", "libs", "linux", "lib_stb_dxt.so")
#else:
texconv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "texconv", "texconv.exe")

def compress_image(input_path: str, encoding: str) -> bytes:
    output_path = input_path.rsplit(".", 1)[0] + ".dds"
    dirname = os.path.dirname(input_path)
    command = [
        f'"{str(texconv_path)}"',
        "-y",
        "-ft DDS",
        "-f", encoding,
        "-m 1",
        "-o", f'"{str(dirname)}"',
        f'"{str(input_path)}"',
    ]
    subprocess.run(" ".join(command))
    compressed_image = open(output_path, "rb").read()
    return compressed_image[128:]