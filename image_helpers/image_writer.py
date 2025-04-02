from . png_writer import write_png
from . tga_writer import write_tga

def write_image(output_path: str, width: int, height: int, image_data: list) -> None:
    if output_path.endswith(".png"):
        write_png(output_path, width, height, image_data)
    else:
        write_tga(output_path, width, height, image_data)