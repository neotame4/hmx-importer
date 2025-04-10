from . data_format_parsers.acp_reader import create_acp_anim
from . data_format_parsers.acg_reader import read_acg
from . data_format_parsers.char_clip_samples_reader import read_ccs
from . data_format_parsers.bitmap_reader import read_bitmap
from . data_format_parsers.milo_and_dirs_reader import read_milo
from . data_format_parsers.str_reader import read_str
from . import_export_helpers.milo_exporter import export_milo
from . readers import *
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator

class ImportMilo(Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "import.milo"
    bl_label = "Import HMX Milo"

    filepath = StringProperty(subtype="FILE_PATH")

    filter_glob: StringProperty(
        default="*.milo_ps3;*.milo_xbox;*.milo_wii;*.rnd_ps2;*.milo_ps2;*.rnd_gc;*.rnd;*.ccs;*.vsm;*.vss;*.lipsync",
        options={"HIDDEN"},
    )

    texture_selection: EnumProperty(
        name="Texture Selection",
        description="Select the texture from the game you're importing.",
        items=[
            ("RB1", "RB1", "Import textures from RB1."),
            ("LRB", "LRB", "Import textures from LRB."),
            ("GDRB", "GDRB", "Import textures from GDRB."),
        ],
        default="RB1",
    )
    
    texture_format: EnumProperty(
        name="Texture Export Format",
        description="Select the format to export the textures to.",
        items=[
            ("png", "png", "Export textures to png."),
            ("tga", "tga", "Export textures to tga."),
        ],
        default="tga",
    )

    import_shadow: BoolProperty(
        name="Import Shadow Mesh",
        description="Import shadow mesh from character models.",
        default=False,
    )

    import_lod: BoolProperty(
        name="Import LOD Meshes",
        description="Import lower quality LOD meshes.",
        default=False,
    )

    import_trans_anim: BoolProperty(
        name="Import TransAnim Animations",
        description="Import TransAnim animations (common in venues).",
        default=False,
    )

    import_prop_anim: BoolProperty(
        name="Import PropAnim Animations",
        description="Import PropAnim animations (common in venues).",
        default=False,
    )

    import_external: BoolProperty(
        name="Import External Milos",
        description="Import external milos for RB characters.",
        default=False,
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "texture_selection")
        layout.prop(self, "texture_format")
        layout.prop(self, "import_shadow")
        layout.prop(self, "import_lod")
        layout.prop(self, "import_trans_anim")
        layout.prop(self, "import_prop_anim")
        layout.prop(self, "import_external")

    def execute(self, context):
        read_milo(None, False, self.filepath, self)
        self.report({"INFO"}, "Successfully imported milo!")
        return {"FINISHED"} 

class ImportACP(Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "import.acp"
    bl_label = "Import ACP"

    filepath = StringProperty(subtype="FILE_PATH")

    filter_glob: StringProperty(
        default="*.acp;*.acg",
        options={"HIDDEN"},
    )

    def execute(self, context):
        if self.filepath.endswith(".acp"):
            create_acp_anim(self)
            self.report({"INFO"}, "Successfully imported ACP animation!")
        elif self.filepath.endswith(".acg"):
            read_acg(self)
            self.report({"INFO"}, "Successfully read ACG file!")
        return {"FINISHED"}

class ImportCCS(Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "import.ccs"
    bl_label = "Import CCS"

    filepath = StringProperty(subtype="FILE_PATH")

    filter_glob: StringProperty(
        default="*.ccs;*.clip",
        options={"HIDDEN"},
    )

    def execute(self, context):
        read_ccs(self)
        self.report({"INFO"}, "Successfully imported CCS animation!")
        return {"FINISHED"}

class ConvertHMXImage(Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "convert.image"
    bl_label = "Convert HMX Image"

    filepath = StringProperty(subtype="FILE_PATH")

    filter_glob: StringProperty(
        default="*.bmp_ps2;*.png_ps2;*.bmp_ps3;*.png_ps3;*.bmp_xbox;*.png_xbox;*.bmp_wii;*.png_wii;*.bmp_gc;*.png_gc",
        options={"HIDDEN"},
    )

    texture_selection: EnumProperty(
        name="Texture Selection",
        description="Select the texture from the game you're importing.",
        items=[
            ("RB1", "RB1", "Import textures from RB1."),
            ("LRB", "LRB", "Import textures from LRB."),
            ("GDRB", "GDRB", "Import textures from GDRB."),
            ("RB3 Wii", "RB3 Wii", "Import textures from RB3 Wii"),
            ("DC2 / DC3", "DC2 / DC3", "Import textures from DC2 / DC3.")
        ],
        default="RB1",
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "texture_selection")

    def execute(self, context):
        read_bitmap(self, self.filepath)
        self.report({"INFO"}, "Successfully converted image file!")
        return {"FINISHED"} 

class ConvertHMXAudio(Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "convert.audio"
    bl_label = "Convert HMX Audio"

    filepath = StringProperty(subtype="FILE_PATH")

    filter_glob: StringProperty(
        default="*.str;*.vgs",
        options={"HIDDEN"},
    )

    def execute(self, context):
        if self.filepath.endswith(".str"):
            read_str(self)
        #elif self.filepath.endswith(".vgs")
        self.report({"INFO"}, "Successfully converted audio file!")
        return {"FINISHED"} 
    
class ExportMilo(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "export.milo"
    bl_label = "Export HMX Milo"

    filepath = StringProperty(subtype="FILE_PATH")

    filename_ext = ".milo"

    filter_glob: StringProperty(
        default="*.milo_ps3;*.milo_xbox;*.rnd_xbox;*.milo_wii;*.rnd_ps2;*.milo_ps2;*.rnd;*.rnd_gc;*.milo_pc",
        options={"HIDDEN"},
    )

    game_selection: EnumProperty(
        name="Game Selection",
        description="Select the game you're exporting for.",
        items=[
            ("Frequency", "Frequency", "Export a milo for Frequency."),
            ("Amplitude", "Amplitude", "Export a milo for Amplitude."),
            ("TBRB", "TBRB", "Export a milo for TBRB."),
        ],
        default="TBRB",
    )

    platform_selection: EnumProperty(
        name="Platform Selection",
        description="Select the platform you're exporting for.",
        items=[
            ("X360", "X360", "Export a milo for X360."),
            ("PS2", "PS2", "Export a milo for PS2."),
            ("PS3", "PS3", "Export a milo for PS3."),
            ("Wii", "Wii", "Export a milo for Wii."),
           # ("GC", "GC", "Export a rnd for GC."),
           # ("XBOX", "XBOX", "Export a rnd for og XBOX."),
           # ("PC", "PC", "Export a milo for PC."),
        ],
        default="X360",
    )

    directory_name: StringProperty(
        name="Directory Name",
        description="The name of the milo directory, set to whatever you want.",
        default="",
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "game_selection")
        layout.prop(self, "platform_selection")
        layout.prop(self, "directory_name")

    def execute(self, context):
        export_milo(False, self.filepath, self)
        self.report({"INFO"}, "Successfully exported milo!")
        return {"FINISHED"} 