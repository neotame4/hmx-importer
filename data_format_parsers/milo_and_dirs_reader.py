import os
from .. readers import *
from .. common import *
from . anim_reader import *
from . character_reader import *

# largest files
#lrb/cutscenes/audition_2_vocal/audition_2_vocal.milo  180mb
#lrb/cutscenes/audition_1_guitar/audition_1_guitar.milo  215.6mb

# just here as a general base for new formats
from . filler_reader import *		#.



#from . bandcharacter_reader import *	#no extension

from . compression import *
from . coll_reader import *

from . cam_reader import *		#.cam
from . camshot_reader import *		#no extension or .shot
from . bandcamshot_reader import *	#.shot
#from . camanim_reader import *		#.cnm			#gdrb


from . mat_reader import *

from . matanim_reader import *		#.mnm

from . group_reader import *		#.grp

from . light_reader import *		#.lit
from . spotlight_reader import *	#.spot
#from . light_preset_reader import * 	#.pst
from . lightanim_reader import *	#.lnm

from . mesh_reader import *
from . meshanim_reader import *		#.msnm or .meshanim

#from . meshblend_reader import *	#.blend
#from . meshblendanim_reader import *	#.blendanim
from . multimesh_reader import *	#.mm
#from . line_reader import *		#.lie
#from . blendshapedriver_reader import *	#.bdrv		#lrb


from . charbone_reader import *	#.mesh or .cb

from . poll_reader import *
from . prop_anim_reader import *	#.anim
#from . synth_dir_reader import *	#no extension
from . synth_sample_reader import *	#.wav
#from . synth_fader_reader import *	#.fade
#from . texrenderer_reader import *	#.rndtex		#gdrb
from . tex_reader import *
from . trans_anim_reader import *	#.tnm or .anim
from . trans_reader import *		#.trans or .mesh
from . world_crowd_reader import *	#.crd

from . particlesys_reader import *	#.part
from . particlesysanim_reader import *	#.panim
#from . environ_reader import *		#.env
#from . envanim_reader import *		#.enm
#from . eventtrigger_reader import *	#.trig
#from . eventanim_reader import *	#.eventanm		#lrb
#from . animfilter_reader import *	#.filt
#from . set_reader import *		#.set
#from . postproc_reader import *	#.pp
from . waypoint_reader import *	#.way
#from . cubetex_reader import *		#.cube
from . view_reader import *		#no extension or .view
#from . font_reader import *		#.font
#from . text_reader import *		#.txt
#from . bandlabel_reader import *	#.lbl
#from . uitrigger_reader import *	#.trig
#from . uiproxy_reader import *		#no extension
from . flare_reader import *		#.flare
#from . mem_reader import *		#.mem
#from . hair_reader import *		#.hair
#from . walk_reader import *		#no extension
#from . servo_reader import *		#.servo			#CharServoBone,FaceFXLip
#from . faceservo_reader import *	#.faceservo

#from . uppertwist_reader import *	#.ik
#from . foretwist_reader import *	#.ik
#from . necktwist_reader import *	#.
#from . ikhand_reader import *		#.ik
#from . ikmidi_reader import *		#.ik
#from . ikhead_reader import *		#.ikhead
#from . ikfoot_reader import *		#.ikfoot
#from . _reader import *		#.
#from . _reader import *		#.
#from . _reader import *		#.
#from . ikrod_reader import *		#.rod

#from . lookat_reader import *		#.lookat		#EYES
#from . eyes_reader import *		#.eyes			#EVEN MORE EYES
#from . weightsetter_reader import *	#.weight
#from . driver_reader import *		#.drv			#CharDriver,CharDriverMidi
#from . posconstraint_reader import *	#.pcon
#from . outfit_reader import *		#.outfit
#from . outfitconfig_reader import *	#.cfg
#from . fxsendreverb_reader import *	#.send
from . interest_reader import *	#.intr
#from . p9character_reader import *	#no extension
#from . lipsync_reader import *		#.lipsync
#from . lipsyncdriver_reader import *	#.lipdrv

#from . chartrigger_reader import *	#.ctrig
#from . charclipset_reader import *	#.set or no extension	#lrb snake told me .set
#from . charclipgroup_reader import *	#.clipgrp or no extension	#lrb told me .cligrp
#from . charclipfilter_reader import *	#.ccf or no extension	#lrb told me .ccf
#from . _reader import *		#.

#from . compositechar_reader import *	#no extension		#lrb
#from . colorpalette_reader import *	#.pal
#from . cutscenedriver_reader import *	#.cutdrv		#lrb

#from . distort_reader import *		#.lie			#lrb
#from . bandcrowdmeterdir_reader import *
#from . endingbonusdir_reader import *
#from . gemtrackdir_reader import *
#from . scoreboarddir_reader import *
#from . trackpaneldir_reader import *
#from . vocaltrackdir_reader import *
#from . h2htrackpaneldir_reader import *
#from . dir_reader import *
#from . dir_reader import *
    # WHAT WERE THE LRB DEVS DOING
#from . object_reader import *		#no extension		#lrb
#from . trackwidget_reader import *	#.wid
#from . crowdmetericon_reader import *	#no extension		#lrb
#from . crowdextrasmanager_reader import *	#.cdm		#gdrb
#from . triggergroup_reader import *	#.tgrp			#gdrb
#from . _reader import *		#.
#from . _reader import *		#.
#from . _reader import *		#.
#from . _reader import *		#.
#from . _reader import *		#.
#from . _reader import *		#.
#from . _reader import *		#.
#from . _reader import *		#.
#from . _reader import *		#.
#from . _reader import *		#.
#from . _reader import *		#.
#from . _reader import *		#.
#from . _reader import *		#.
#from . _reader import *		#.
#from . _reader import *		#.
#from . _reader import *		#.
#from . _reader import *		#.
#from . _reader import *		#.
#from . _reader import *		#.
#from . _reader import *		#.
#from . _reader import *		#.
#from . _reader import *		#.
#from . _reader import *		#.
#from . _reader import *		#.
#from . _reader import *		#.
#from . _reader import *		#.
#from . _reader import *		#.
#from . _reader import *		#.
#from . _reader import *		#.
#from . _reader import *		#.
#from . _reader import *		#.
#from . _reader import *		#.
#from . _reader import *		#.

def compression_type(magic: bytes) -> str:
    if magic == b"\xAF\xDE\xBE\xCA":
        return "Uncompressed"
    elif magic == b"\xAF\xDE\xBE\xCB":
        return "ZLIB"
    elif magic == b"\xAF\xDE\xBE\xCC":
        return "GZIP"    
    elif magic == b"\xAF\xDE\xBE\xCD":
        return "ZLIB Alt"
    
def read_character(reader, name: str, inlined: bool, is_entry: bool, self):
    o = bpy.data.objects.new(name, None)
    bpy.context.scene.collection.objects.link(o)
    o.empty_display_size = 2
    o.empty_display_type = "PLAIN_AXES"
    version = reader.int32()
    inline_proxy = read_rnd_dir(reader, inlined, self)[0]
    if (version >= 17) and (is_entry == True):
        character_test(reader)
    padding = reader.read_bytes(4)
    if padding == b"\xAD\xDE\xAD\xDE":
        reader.seek(-4)
        return inline_proxy
    reader.seek(-4)
    if version == 7:
        filler = reader.uint32()
    lod_targets(reader, version)
    if version < 18:
        shadow = reader.numstring()
    else:
        shadow_count = reader.uint32()
        for _ in range(shadow_count):
            shadow = reader.numstring()
    self_shadow = reader.milo_bool()
    sphere_base = reader.numstring()
    if version <= 9:
        return inline_proxy
    if version > 10:
        bounding = reader.vec4f()
        if version > 12:
            frozen = reader.milo_bool()
            force_lod = reader.int32()
    if (version == 17) and (is_entry == False):
        # thx compvir
        unknown_grp = reader.numstring()
    if (version <= 15) or (version == 17 and is_entry == False):
        character_test(reader)
        return inline_proxy
    if version < 17:
        always_10 = reader.int32()
    else:
        always_0 = reader.int32()
        if version == 21:
            unknown = reader.read_bytes(4)
        always_15 = reader.int32()
    unknown = reader.numstring()
    empty_bytes_1 = reader.read_bytes(16)
    str_1 = reader.numstring()
    always_0 = reader.int32()
    always_true = reader.milo_bool()
    if version >= 17:
        empty_bytes_2 = reader.read_bytes(8)
        return inline_proxy
    empty_bytes_2 = reader.read_bytes(7)
    str_2 = reader.numstring()
    always_0 = reader.short()
    always_120 = reader.int32()
    unk_vec = reader.vec3f()
    return inline_proxy

def read_char_clip_set(reader, inlined: bool, is_entry: bool, self):
    version = reader.int32()
    inline_proxy = read_obj_dir(reader, True, inlined, self)[0]
    padding = reader.read_bytes(4)
    if padding == b"\xAD\xDE\xAD\xDE":
        reader.seek(-4)
        return inline_proxy
    reader.seek(-4)
    if (version == 23) and (is_entry == True):
        string_count = reader.int32()
        for _ in range(string_count):
            some_string = reader.numstring()
        return inline_proxy
    char_file_path = reader.numstring()
    preview_clip = reader.numstring()
    filter_flags = reader.uint32()
    bpm = reader.int32()
    preview_walk = reader.milo_bool()
    still_clip = reader.numstring()
    if version >= 25:
        unk = reader.numstring()
    return inline_proxy

def read_flow(reader, super: bool, is_entry: bool, self):
    version = reader.int32()
    read_obj_dir(reader, super, False, self)
    # just read rest of file here
    find_next_file(reader) 

def read_obj_dir(reader, super: bool, inlined: bool, self):
    meshes = []
    dir_name = ""
    version = reader.int32()
    if (version >= 2) and (version < 17):
        read_metadata(reader, super)
    elif version >= 22:
        revision = reader.int32()
        obj_dir_type = reader.numstring()
    if version > 1:
        if version >= 27:
            # i think always 0, probably padding?
            padding = reader.read_bytes(8)
        viewport_count = reader.int32()
        for _ in range(viewport_count):
            viewport = reader.matrix()
            if version <= 17:
                padding = reader.read_bytes(4)
        curr_viewport_index = reader.int32()
    if version > 12:
        if version > 19:
            inline_proxy = reader.milo_bool()
        else:
            inline_proxy = False
        proxy_file = reader.numstring()
        if (len(proxy_file) > 0) and (inline_proxy == False):
            print("Loading proxy file:", proxy_file)
            og_proxy_file = proxy_file
            if proxy_file.startswith("../../../"):
                up_count = 3
                print("up_count", up_count)
                proxy_file = proxy_file.replace("../../../", "")
            elif proxy_file.startswith("../../"):
                up_count = 3
                print("up_count", up_count)
                proxy_file = proxy_file.replace("../../", "")  
            elif proxy_file.startswith("../"):
                up_count = 3
                print("up_count", up_count)
                proxy_file = proxy_file.replace("../", "") 
            proxy_file = proxy_file.replace("/", "\\")
            dirname = os.path.dirname(proxy_file)
            basename = os.path.basename(proxy_file)
            current_path = os.path.dirname(reader.filepath)
            for _ in range(up_count):
                current_path = os.path.dirname(current_path)
            current_directory = os.path.join(current_path, dirname)
            os.chdir(current_directory)
            for root, dirs, files in os.walk(current_directory):
                for file in files:
                    if basename in file: 
                        final_path = os.path.join(root, file)
                        read_milo(reader, False, final_path, self)
            print("Successfully loaded proxy file:", og_proxy_file)
    if (version >= 2) and (version < 11):
        some_object_1 = reader.numstring()
    if (version >= 4) and (version < 11):
        some_object_2 = reader.numstring()
    if version == 5:
        ignore_string = reader.numstring()
    if version > 2:
        subdir_count = reader.int32()
        subdirs = []
        for _ in range(subdir_count):
            subdirs.append(reader.numstring())
        if self.import_external == True:
            for subdir in subdirs:
                if len(subdir) > 0:
                    print("Loading subdir:", subdir)
                    # keep original subdir string
                    og_subdir = subdir
                    if subdir.startswith("../../"):
                        up_count = 3
                        subdir = subdir.replace("../../", "")
                    else:
                        up_count = 2
                        subdir = subdir.replace("../", "")
                    subdir = subdir.replace("/", "\\")
                    dirname = os.path.dirname(subdir)
                    basename = os.path.basename(subdir)
                    current_path = os.path.dirname(reader.filepath)
                    for _ in range(up_count):
                        current_path = os.path.dirname(current_path)
                    current_directory = os.path.join(current_path, dirname)
                    os.chdir(current_directory)
                    for root, dirs, files in os.walk(current_directory):
                        for file in files:
                            if basename in file: 
                                final_path = os.path.join(root, file)
                                read_milo(reader, False, final_path, self)    
                    print("Successfully loaded subdir:", og_subdir)
        if version >= 21:
            inline_subdir = reader.milo_bool()
            inline_subdir_count = reader.int32()
            for _ in range(inline_subdir_count):
                inline_subdir_name = reader.numstring()
            if version >= 27:
                for _ in range(inline_subdir_count):
                    reference_type = reader.byte()
                for _ in range(inline_subdir_count):
                    reference_type_alt = reader.byte()
            for _ in range(inline_subdir_count):
                read_milo(reader, True, self.filepath, self)
    if version < 19:
        if version < 16:
            if version > 14:
                ignore_string_2 = reader.numstring()
        else:
            ignore_string_3 = reader.numstring()
    if version > 10:
        if inlined == True:
            no_idea_bool = reader.milo_bool()
            if no_idea_bool == False:
                meshes, dir_name = read_milo(reader, True, self.filepath, self)
        some_string_1 = reader.numstring()
        print("some_string_1", some_string_1)
        some_string_2 = reader.numstring()
        print("some_string_2", some_string_1)
    if version < 22:
        if version > 16:
            metadata = read_metadata(reader, super)
    else:
        props = dtb(reader)
        note = reader.numstring()
    return inline_proxy, dir_name, meshes

def read_panel_dir(reader, is_entry: bool, inlined: bool, self):
    version = reader.int32()
    read_rnd_dir(reader, inlined, self)
    if is_entry == False:
        cam = reader.numstring()
    if version <= 1:
        return
    if version == 2:
        test_event = reader.numstring()
        return
    elif version <= 7:
        can_end_world = reader.milo_bool()
    else:
        use_specified_cam = reader.milo_bool()
    front_view_only_panel_count = reader.int32()
    for _ in range(front_view_only_panel_count):
        front_view_only_panel = reader.numstring()
    back_view_only_panel_count = reader.int32()
    for _ in range(back_view_only_panel_count):
        back_view_only_panel = reader.numstring()
    if version >= 8:
        postprocs_before_draw = reader.milo_bool()
    show_view_only_panels = reader.milo_bool()

def read_rnd_dir(reader, inlined: bool, self):
    version = reader.int32()
    inline_proxy, dir_name, meshes = read_obj_dir(reader, False, inlined, self)
    read_anim(reader, True)
    read_draw(reader, True)
    parent, local_xfm, world_xfm = read_trans(reader, True)
    if version < 9:
        read_poll(reader)
        some_string_1 = reader.numstring()
        print("some_string_1", some_string_1)
        some_string_2 = reader.numstring()
        print("some_string_2", some_string_2)
    else:
        environ = reader.numstring()
        if version >= 10:
            test_event = reader.numstring()
    if version == 6:
        for _ in range(8):
            some_float = reader.float32()
    return inline_proxy, world_xfm, parent, dir_name, meshes

def read_synth_dir(reader, inlined: bool, self) -> None:
    version = reader.int32()
    read_obj_dir(reader, False, inlined, self)

def read_world_dir(reader, inlined: bool, self) -> None:
    def wd_replacement(reader) -> tuple:
        original = reader.numstring()
        replacement = reader.numstring()
        return original, replacement
    version = reader.int32()
    if version != 0 and version < 5:
        cam = reader.numstring()    
    if version >= 2 and version <= 20:
        always_0 = reader.float32()
        always_1 = reader.float32()
    if version > 9:
        hud_filename = reader.numstring()
    read_panel_dir(reader, inlined, False, self)
    if version == 5:
        cam_reference = reader.numstring()
    if version < 25:
        if version > 10:
            xfm = reader.matrix()
        elif version > 6:
            cam_trans = read_trans(reader, True)
    if version > 11:
        hide_override_count = reader.uint32()
        for _ in range(hide_override_count):
            hide_override = reader.numstring()
        bitmap_override_size = reader.int32()
        for _ in range(bitmap_override_size):
            original, replacement = replacement(reader)
    if version > 13:
        mat_override_size = reader.int32()
        for _ in range(mat_override_size):
            mesh, mat = wd_replacement(reader) 
    if version > 14:
        preset_override_size = reader.int32()
        for _ in range(preset_override_size):
            preset, hue = wd_replacement(reader)
    if version > 15:
        cam_shot_override_count = reader.uint32()
        for _ in range(cam_shot_override_count):
            cam_shot = reader.numstring()
    if (version > 16) and (version != 23):
        ps3_per_pixel_hides_count = reader.uint32()
        for _ in range(ps3_per_pixel_hides_count):
            per_pixel_hide = reader.numstring()
        ps3_per_pixel_shows_count = reader.uint32()
        for _ in range(ps3_per_pixel_shows_count):
            per_pixel_show = reader.numstring()
    if version in [18, 19, 20, 21]:
        spotlight = reader.numstring()
    if version > 18:
        m_test_preset_1 = reader.numstring()
        m_test_preset_2 = reader.numstring()
        m_test_animation_time = reader.float32()
    if version > 19:
        hud = reader.numstring()

def read_world_instance(reader, is_entry: bool, inlined: bool, name: str, self) -> int:
    version = reader.int32()
    if version != 0:
        instance_file = reader.numstring()
    else:
        directory = reader.numstring()
    world_xfm, parent, dir_name, meshes = read_rnd_dir(reader, inlined, self)[1:]
    # starting with version 2, worldinstance gets really dumb
    # thank you compvir for figuring out the following... **thing**
    if (version >= 2) and (is_entry == True):
        if version >= 3:
            # the fucking stuff from a milo...?
            string_table_string_count = reader.uint32()
            string_table_used_size = reader.uint32()
        object_count = reader.int32()
        dirs = []
        filenames = []
        for _ in range(object_count):
            dirs.append(reader.numstring())
            filenames.append(reader.numstring())
        for directory, name in zip(dirs, filenames):
            if directory == "Mesh":
                read_mesh(reader, name)
    else:
        if len(meshes) > 0:
            o = bpy.data.objects.new(dir_name, None)
            bpy.context.scene.collection.objects.link(o)
            o.empty_display_size = 2
            o.empty_display_type = "PLAIN_AXES"
            o.matrix_world = mathutils.Matrix((
                (world_xfm[0], world_xfm[3], world_xfm[6], world_xfm[9]),
                (world_xfm[1], world_xfm[4], world_xfm[7], world_xfm[10]),
                (world_xfm[2], world_xfm[5], world_xfm[8], world_xfm[11]),
                (0.0, 0.0, 0.0, 1.0),
            ))    
            for obj in bpy.data.objects:
                for mesh in meshes:
                    if (mesh in obj.name) and not (obj.parent) and (obj.data) and (len(obj.data.vertices) > 0):
                        obj.parent = o
            parent_obj = bpy.data.objects.get(parent)
            if parent_obj:
                o.parent = parent_obj
        else:
            if len(instance_file) > 0:
                print("Loading venue item:", instance_file)
                if instance_file.startswith("../../"):
                    up_count = 4
                    instance_file = instance_file.replace("../../", "")
                else:
                    up_count = 3
                    instance_file = instance_file.replace("../", "")
                instance_file = instance_file.replace("/", "\\")
                dirname = os.path.dirname(instance_file)
                basename = os.path.basename(instance_file)
                current_path = reader.filepath
                for _ in range(up_count):
                    current_path = os.path.dirname(current_path)
                current_directory = os.path.join(current_path, dirname)
                os.chdir(current_directory)
                for root, dirs, files in os.walk(current_directory):
                    for file in files:
                        if basename in file: 
                            final_path = os.path.join(root, file)
                            meshes, dir_name = read_milo(reader, False, final_path, self)
                            o = bpy.data.objects.new(dir_name, None)
                            bpy.context.scene.collection.objects.link(o)
                            o.empty_display_size = 2
                            o.empty_display_type = "PLAIN_AXES"
                            o.matrix_world = mathutils.Matrix((
                                (world_xfm[0], world_xfm[3], world_xfm[6], world_xfm[9]),
                                (world_xfm[1], world_xfm[4], world_xfm[7], world_xfm[10]),
                                (world_xfm[2], world_xfm[5], world_xfm[8], world_xfm[11]),
                                (0.0, 0.0, 0.0, 1.0),
                            )) 
                            for obj in bpy.data.objects:
                                for mesh in meshes:
                                    if (mesh in obj.name) and not (obj.parent) and (obj.data) and (len(obj.data.vertices) > 0):
                                        obj.parent = o
                            parent_obj = bpy.data.objects.get(parent)
                            if parent_obj:
                                o.parent = parent_obj
                    print("Successfully loaded venue item:", instance_file)        
    return version

def milo_entries(reader) -> tuple[dict, list]:
    entries = {}
    dirs = []
    filenames = []
    if reader.version > 10:
        dir_type = reader.numstring()
        dir_name = reader.numstring()
        entries["dir_type"] = dir_type
        entries["dir_name"] = dir_name
        string_table_string_count = reader.uint32()
        string_table_used_size = reader.uint32()
        if reader.version >= 32:
            unknown = reader.milo_bool()
    entry_count = reader.int32()
    entries["entry_count"] = entry_count
    for _ in range(entry_count):
        if reader.version <= 6:
            dirs.append(reader.string())
            filenames.append(reader.string())
            unknown_bool = reader.milo_bool()
        else:
            dirs.append(reader.numstring())
            filenames.append(reader.numstring())
    entries["dirs"] = dirs
    entries["names"] = filenames
    meshes = []
    for name in filenames:
        if name.endswith(".mesh"):
            meshes.append(name)
    return entries, meshes

def ext_resources(reader, self) -> None:
    ext_count = reader.int32()
    ext_paths = []
    for _ in range(ext_count):
        ext_paths.append(reader.numstring())  
    for path in ext_paths:
        if len(path) > 0:
            dirname = os.path.dirname(reader.filepath)
            path = path.replace("/", "\\")
            path_dir = os.path.dirname(path)
            path_name = os.path.basename(path)
            os.chdir(os.path.join(dirname, path_dir))
            for root, dirs, files in os.walk(os.getcwd()):
                for file in files:
                    if path_name in file:
                        final_path = os.path.join(root, file)
                        if os.path.exists(final_path):
                            if (final_path.endswith(".gz")) or (final_path.endswith(".z")):
                                print("Found external path:", final_path)
                                read_bitmap(self, final_path)
                                print("Successfully opened external path:", final_path)                     
    
def obj(reader, obj_type: str, name: str, character_name: str, is_entry: bool, self) -> tuple[str, str, str, list]:   
    read_milo_file = False
    geom_owner = ""
    parent = ""
    mesh_name = ""
    xfms = []
    if obj_type == "Character":
        inline_proxy = read_character(reader, name, False, is_entry, self)
        if inline_proxy == True:
            read_milo_file = True
    elif obj_type == "CharClipSet":
        inline_proxy = read_char_clip_set(reader, False, is_entry, self)
        if inline_proxy == True:
            read_milo_file = True
    elif obj_type == "CharCollide":
        read_coll(reader, name, self)
    elif obj_type == "WayPoint":
        read_waypoint(reader, name, self)
    elif obj_type == "View":
        read_view(reader, name, self)
    elif obj_type == "Group":
        read_group(reader, name, self)
    elif obj_type == "Cam":
        read_cam(reader, name, self)
    elif obj_type == "CharBone":
        read_charbone(reader, name, self)
    elif obj_type == "Flow":
        read_flow(reader, False, is_entry, self)
        if is_entry == True:
            read_milo_file = True
    elif obj_type == "Mat":
        read_mat(reader, name, self)
    elif obj_type == "MatAnim":
        read_matanim(reader, name, self)
    elif obj_type == "Mesh":
        geom_owner, parent, mesh_name = read_mesh(reader, name, character_name, self)
    elif obj_type == "MeshAnim":
        read_meshanim(reader, name, self)
    elif obj_type == "MultiMesh":
        read_multimesh(reader, name, self)
   # elif obj_type == "MeshBlend":
   #     read_meshblend(reader, name, self)
    elif obj_type == "ObjectDir":
        read_obj_dir(reader, False, False, self)
    elif obj_type == "PanelDir":
        read_panel_dir(reader, is_entry, False, self)
    elif obj_type == "PropAnim":
        if self.import_prop_anim == True:
            read_prop_anim(reader, name, False)
        else:
            find_next_file(reader)
    elif obj_type == "RndDir":
        inline_proxy = read_rnd_dir(reader, False, self)[0]
        if inline_proxy == True:
            read_milo_file = True
    elif obj_type == "SynthDir":
        read_synth_dir(reader, False, self)
        read_milo_file = True
    elif obj_type == "SynthSample":
        read_synth_sample(reader, name, self)
    elif obj_type == "Tex":
        read_tex(reader, name, self)
    elif obj_type == "Light":
        read_lit(reader, name, self)

    elif obj_type == "Spotlight":
        read_spotlight(reader, name, self)
    # lego rock band has some broken ones, WHY Tt GAMES
    # sowwy cant fix :3 -neo

   # elif obj_type == "LightPreset":
   #     read_lightpreset(reader, name, self)
    elif obj_type == "LightAnim":
        read_lightanim(reader, name, self)
    elif obj_type == "Flare":
        read_flare(reader, name, self)


   # elif obj_type == "EventTrigger":
   #     read_eventtrigger(reader, name, self)
   # elif obj_type == "LightPreset":
   #     read_lightpreset(reader, name, self)
   # elif obj_type == "Set":
   #     read_set(reader, name, self)
    elif obj_type == "ParticleSys":
        read_particlesys(reader, name, self)
    elif obj_type == "ParticleSysAnim":
        read_particlesysanim(reader, name, self)
    elif obj_type == "CamShot":
        read_caamshot(reader, name, self)
   # elif obj_type == "Environ":
   #     read_environ(reader, name, self)
   # elif obj_type == "EnvAnim":
   #     read_envanim(reader, name, self)
   # elif obj_type == "CubeTex":
   #     read_cubetex(reader, name, self)
   # elif obj_type == "AnimFilter":
   #     read_animfilter(reader, name, self)
   # elif obj_type == "PostProc":
   #     read_postprocess(reader, name, self)
   # elif obj_type == "Filler":
   #     read_(reader, name, self)
   # elif obj_type == "Filler":
   #     read_(reader, name, self)
   # elif obj_type == "Filler":
   #     read_(reader, name, self)
   # elif obj_type == "Filler":
   #     read_(reader, name, self)
   # elif obj_type == "Filler":
   #     read_(reader, name, self)
   # elif obj_type == "Filler":
   #     read_(reader, name, self)
   # elif obj_type == "Filler":
   #     read_(reader, name, self)
   # elif obj_type == "Filler":
   #     read_(reader, name, self)

    elif obj_type == "Trans":
        read_trans(reader, False, name, character_name)
    elif obj_type == "TransAnim":
        if self.import_trans_anim == True:
            read_trans_anim(name, reader, False)
        else:
            find_next_file(reader)
    elif obj_type == "WorldCrowd":
        xfms = read_world_crowd(reader, name, False)
    elif obj_type == "WorldDir":
        read_world_dir(reader, False, self)
    elif obj_type == "WorldInstance":
        version = read_world_instance(reader, is_entry, True, name, self)
        if (version >= 3) and (is_entry == True):
            read_milo_file = True
    else:
        find_next_file(reader)
    padding = reader.read_bytes(4)   
    current_offset = reader.tell()
    try:
        if (read_milo_file == True) and (is_entry == True):
            read_milo(reader, True, self.filepath, self)
    except:
        reader.skip(current_offset)
    return geom_owner, parent, mesh_name, xfms

def read_milo_files(reader, entries: dict, character_name: str, self) -> tuple:
    entry_count = entries["entry_count"]
    dirs = entries["dirs"]
    names = entries["names"]
    geom_owner_names = []
    parent_names = []
    character_xfms = []
    for i in range(entry_count):
        obj_type = dirs[i]
        obj_name = names[i]
        geom_owner, parent, mesh_name, xfms = obj(reader, obj_type, obj_name, character_name, True, self)
        geom_owner_names.append((geom_owner, mesh_name))
        parent_names.append((parent, mesh_name))
        character_xfms.append(xfms)
    return geom_owner_names, parent_names, character_xfms

def read_milo(reader, inline: bool, filepath: str, self) -> list:    
    if inline == False:
        reader = Reader(open(filepath, "rb").read(), filepath)
        magic = reader.read_bytes(4)
        compression = compression_type(magic)
        # Uncompressed
        if compression == "Uncompressed":
            print("Uncompressed milo. Continuing reading as normal.")
            start_offset = reader.uint32()
            block_count = reader.uint32()
            largest_block = reader.uint32()
            for _ in range(block_count):
                block_size = reader.uint32()
            padding = reader.read_bytes(start_offset - reader.tell())
        # Zlib
        elif compression == "ZLIB":
            print("Compressed with zlib. Decompressing...")
            start_offset = reader.uint32()
            block_count = reader.uint32()
            largest_block = reader.uint32()
            block_sizes = []
            decompressed = []
            for _ in range(block_count):
                block_sizes.append(reader.uint32())
            padding = reader.read_bytes(start_offset - reader.tell())
            for size in block_sizes:
                decompressed.append(decompress_zlib_deflate(reader.read_bytes(size)))
            decompressed_bytes = b"".join(decompressed)
            reader = Reader(decompressed_bytes, filepath)
        # Gzip
        elif compression == "GZIP":
            print("Compressed with gzip. Decompressing...")
            start_offset = reader.uint32()
            block_count = reader.uint32()
            largest_block = reader.uint32()
            block_sizes = []
            decompressed = []
            for _ in range(block_count):
                block_sizes.append(reader.uint32())
            padding = reader.read_bytes(start_offset - reader.tell())
            for size in block_sizes:
                decompressed.append(decompress_gzip(reader.read_bytes(size)))
            decompressed_bytes = b"".join(decompressed)
            reader = Reader(decompressed_bytes, filepath)  
        elif compression == "ZLIB Alt":
            print("Compressed with zlib. Decompressing...")
            start_offset = reader.uint32()
            block_count = reader.uint32()
            largest_block = reader.uint32()
            block_sizes = []
            decompressed = []
            for _ in range(block_count):
                block_sizes.append(reader.uint32())
            padding = reader.read_bytes(start_offset - reader.tell())
            # bruh
            for size in block_sizes:
                compressed = size & 0xFF000000 == 0
                block_size = size & 0x00FFFFFF
                block = reader.read_bytes(block_size)
                if compressed == True:
                    decompressed.append(decompress_zlib_deflate(block[4:]))
                else:
                    decompressed.append(block)
            decompressed_bytes = b"".join(decompressed)
            reader = Reader(decompressed_bytes, filepath)              
        # Frequency / Phase / Script uncompressed milos
        else:
            reader.skip(0)
    meshes = []
    get_endian(reader)
    version = get_version(reader)
    reader.version = version
    platform = get_platform(filepath)
    reader.platform = platform
    # DC1 bruh...
    if version == 0:
        reader.seek(-4)
        return meshes
    entries, meshes = milo_entries(reader)
    dir_type = entries.get("dir_type", "")
    dir_name = entries.get("dir_name", "")
    character_name = ""
    if (dir_type == "Character") or (dir_type == "BandCharacter"):
        character_name = dir_name
    if version == 10:
        ext_resources(reader, self)
    elif version > 10:
        obj(reader, dir_type, dir_name, character_name, False, self)
    geom_owner_names, parent_names, character_xfms = read_milo_files(reader, entries, character_name, self)
    character_xfms = [char_xfm for list in character_xfms for char_xfm in list]
    # Link up the geom_owner and parent
    for object in bpy.data.objects:
        for (geom_owner, mesh_name) in geom_owner_names:
            if mesh_name in object.name:
                if geom_owner != mesh_name:
                    geom_owner_obj = bpy.data.objects.get(geom_owner)
                    if geom_owner_obj:
                        geom_owner_copy = geom_owner_obj.copy()
                        geom_owner_copy.data = geom_owner_obj.data.copy()
                        bpy.context.scene.collection.objects.link(geom_owner_copy)
                        geom_owner_copy.matrix_world = object.matrix_world       
        for (parent, mesh_name) in parent_names:           
            if mesh_name in object.name:
                if (parent != mesh_name) and ("bone" not in parent):
                    parent_obj = bpy.data.objects.get(parent)
                    if parent_obj:
                        object.parent = parent_obj
    # Link up remaining crowd locations
    crowd_names = set()
    for (char_name, char_height, char_xfm, char_color) in character_xfms:
        if char_name not in crowd_names:
            crowd_names.add(char_name)
    objects_without_children = []
    for object in bpy.data.objects:
        for name in crowd_names:
            if (name in object.name) and not (object.children) and (object.type == "EMPTY"):
                objects_without_children.append(object)
    for name in crowd_names:
        crowd_obj = bpy.data.objects.get(name)
        if crowd_obj:
            for w_child in objects_without_children:
                if name in w_child.name:
                    for child in crowd_obj.children:
                        child_copy = child.copy()
                        child_copy.data = child.data.copy()
                        bpy.context.scene.collection.objects.link(child_copy)
                        child_copy.parent = w_child        
    return meshes, dir_name