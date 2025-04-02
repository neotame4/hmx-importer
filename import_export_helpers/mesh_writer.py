import bpy
import numpy as np
from . draw_writer import *
from . trans_writer import *
from .. bpy_util_funcs import *
from .. common import *

def get_weights_and_indices(mesh, modifier) -> list:
    bone_names = [bone.name for bone in modifier.object.data.bones]
    bone_ids = {name: index for index, name in enumerate(bone_names)}
    weights_and_indices = [[[], []] for _ in range(len(mesh.data.vertices))]
    for group in mesh.vertex_groups:
        bone_index = bone_ids.get(group.name)
        if bone_index:
            for vertex in mesh.data.vertices:
                try:
                    weight = group.weight(vertex.index)
                    weights[vertex.index][1] = weight
                    indices[vertex.index][0] = bone_index
                except RuntimeError:
                    pass
    for i, (indices, weights) in enumerate(weights_and_indices):
        if len(weights) > 4:
            top_indices_weights = sorted(zip(indices, weights), key=lambda x: x[1], reverse=True)[:4]
            indices, weights = zip(*top_indices_weights)
        else:
            top_indices_weights = zip(indices, weights)
        indices, weights = list(indices), list(weights)
        indices.reverse()
        weights.reverse()
        indices += [0] * (4 - len(indices))
        weights += [0.0] * (4 - len(weights))
        total_weight = sum(weights) if sum(weights) > 0 else 1
        weights = [weight / total_weight for weight in weights]
        weights_and_indices[i] = [weights, indices]        
    return weights_and_indices

def write_vertices(writer, obj, mesh) -> None:
    writer.int32(len(mesh.vertices))
    vertices = [(vert.co.x, vert.co.y, vert.co.z) for vert in mesh.vertices]
    normals = [(vert.normal.x, vert.normal.y, vert.normal.z) for vert in mesh.vertices]
    uv_layer = None
    if len(mesh.uv_layers) > 0:
        uv_layer = mesh.uv_layers.active
    if obj.modifiers:
        for modifier in obj.modifiers:
            if modifier.type == "ARMATURE":
                weights_and_indices = get_weights_and_indices(mesh, modifier)
    else:
        weights_and_indices = [([0.0, 0.0, 0.0, 0.0], [0, 0, 0, 0]) for _ in range(len(mesh.vertices))]
    for (vertex, normal), (weights, indices) in zip(zip(vertices, normals), weights_and_indices):
        writer.vec3f(vertex)
        if (writer.game in ["RB1", "RB2", "TBRB", "LRB", "GDRB"]) and not (writer.platform == "Wii"):
            writer.float32(0)
        if writer.game == "Frequency":
            writer.vec3f(normal)
            writer.vec2f((0.0, 0.0))
            writer.vec4f(weights)
            writer.vec4us(indices)
        elif (writer.game == "Amplitude") or (writer.game == "AntiGrav"):
            writer.vec4us(indices)
            writer.vec3f(normal)
            writer.vec4f(weights)
            writer.vec2f((0.0, 0.0))
        else:
            writer.vec3f(normal)
            if (writer.game in ["RB1", "RB2", "TBRB", "LRB", "GDRB"]) and not (writer.platform == "Wii"):
                writer.float32(0)
            writer.vec4f(weights)
            writer.vec2f((0.0, 0.0))
            if writer.game in ["RB1", "RB2", "TBRB", "LRB", "GDRB"]:
                writer.vec4us(indices)
                writer.vec4f((-1.0, 0.0, 0.0, 1.0))

def write_faces(writer, mesh) -> None:
    faces = [p.vertices for p in mesh.polygons if len(p.vertices) == 3]
    writer.int32(len(faces))
    for face in faces:
        writer.vec3us(face)

def write_bone_trans(writer, modifier):
    armature = modifier.object
    writer.int32(len(armature.data.bones))
    for bone in armature.data.bones:
        writer.numstring(bone.name)
        inverse_matrix = np.linalg.inv(bone.matrix)
        print(inverse_matrix)

def write_mesh(writer, mesh_name: str) -> None:
    if writer.game == "Frequency":
        writer.int32(10)
    elif writer.game == "Amplitude":
        writer.int32(14)
    elif writer.game == "AntiGrav":
        writer.int32(22)
    elif (writer.game == "Karaoke Revolution") or (writer.game == "GH1"):
        writer.int32(25)
    elif (writer.game == "GH2 PS2") or (writer.game == "GH2 X360") or (writer.game == "GH80s"):
        writer.int32(28)
    # im not even gonna bother with new gen... ugh
    else:
        writer.int32(34)
    obj = bpy.data.objects.get(mesh_name)
    mesh = obj.data
    if not writer.game in ["Frequency", "Amplitude", "AntiGrav", "Karoke Revolution", "GH1"]:
        write_metadata(writer, False)
    write_trans(writer, True, (0.0, 0.0, 0.0), (obj.location.x, obj.location.y, obj.location.z))
    write_draw(writer)
    if (writer.game == "Frequency") or (writer.game == "Amplitude"):
        writer.uint32(0)
        writer.int32(0)
        writer.uint32(2)
        writer.uint32(1)
    material_name = ""
    if obj.material_slots[0].material:
        material_name = obj.material_slots[0].material.name
    if writer.game == "Frequency":
        writer.string(material_name)
    else:
        writer.numstring(material_name)        
    if writer.game == "Frequency":
        # ???
        for _ in range(3):
            writer.string(obj.name)
    else:
        writer.numstring(obj.name)
        if writer.game == "Amplitude":
            writer.numstring(mesh_name)
    if writer.game == "Frequency":
        for _ in range(2):
            writer.string("")
    if (writer.game == "Frequency") or (writer.game == "Amplitude"):
        writer.vec4f((0.0, 0.0, 0.0, 0.0))
        if writer.game == "Frequency":
            writer.string("")
        else:
            writer.numstring("")
        writer.float32(0)
        if writer.game == "Amplitude":
            writer.milo_bool(False)
    if not (writer.game == "Frequency") or (writer.game == "Amplitude"):
        writer.uint32(0)
        if writer.game == "Karaoke Revolution":
            for _ in range(2):
                writer.uint32(0)
    if not writer.game in ["Frequency", "Amplitude", "Karaoke Revolution"]:
        writer.uint32(1)
        writer.milo_bool(False)
    if writer.game == "Frequency":
        writer.uint32(0)
    write_vertices(writer, obj, mesh)
    write_faces(writer, mesh)
    writer.int32(0)
    if obj.modifiers:
        for modifier in obj.modifiers:
            if modifier.type == "ARMATURE":
                write_bone_trans(writer, modifier)
    else:
        writer.int32(0)