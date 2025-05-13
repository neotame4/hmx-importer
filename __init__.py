import bpy
from . import_export_def import *

bl_info = {
    "name": "HMX Importer",
    "description": "A plugin to import and convert files from HMX games on the milo engine.",
    "author": "alliwantisyou3471, neotame4",
    "version": (1, 0),
    "blender": (4, 2, 3),
    "location": "File > Import",
    "warning": "", # used for warning icon and text in addons panel
    "doc_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
    "category": "Import-Export",
}

def menu_func_import(self, context):
    self.layout.operator(ImportMilo.bl_idname, text="Import HMX Milo")
    self.layout.operator(ImportACP.bl_idname, text="Import ACP Animation")
    self.layout.operator(ImportLipSync.bl_idname, text="Import LipSync Animation")
    self.layout.operator(ImportCCS.bl_idname, text="Import CCS Animation")
    self.layout.operator(ImportCharClip.bl_idname, text="Import CharClip Animation")
    self.layout.operator(ConvertHMXImage.bl_idname, text="Convert HMX Image")
    self.layout.operator(ConvertHMXAudio.bl_idname, text="Convert HMX Audio")

def menu_func_export(self, context):
    self.layout.operator(ExportMilo.bl_idname, text="Export HMX Milo")

def register():
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.utils.register_class(ImportMilo)
    bpy.utils.register_class(ImportACP)
    bpy.utils.register_class(ImportLipSync)
    bpy.utils.register_class(ImportCCS)
    bpy.utils.register_class(ImportCharClip)
    bpy.utils.register_class(ConvertHMXImage)
    bpy.utils.register_class(ConvertHMXAudio)
    bpy.utils.register_class(ExportMilo)

def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import) 
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.utils.unregister_class(ImportMilo)
    bpy.utils.unregister_class(ImportACP)
    bpy.utils.unregister_class(ImportLipSync)
    bpy.utils.unregister_class(ImportCCS)
    bpy.utils.unregister_class(ImportCharClip)
    bpy.utils.unregister_class(ConvertHMXImage)
    bpy.utils.unregister_class(ConvertHMXAudio)
    bpy.utils.unregister_class(ExportMilo)

if __name__ == "__main__":
    register()