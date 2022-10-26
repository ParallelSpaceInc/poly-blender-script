import os
import bpy
import zipfile

from os.path import basename
from bpy import context
from PIL import Image

file_loc_export = 'C:\\Users\\USER\\Downloads\\Remesh\\Cup\\'
file_loc_import = 'C:\\Users\\USER\\Downloads\\Remesh\\Cup\\'
fileEx = r'.ply'
fileList = [file for file in os.listdir(file_loc_import) if file.endswith(fileEx)]

scene = bpy.context.scene
scene.render.resolution_y = 900
scene.render.resolution_x = 1200
scene.render.film_transparent = True
scene.render.filepath = file_loc_export + 'thumbnail.png'

for model in fileList:
    imported_object = bpy.ops.import_mesh.ply(filepath=file_loc_import+model)

    bpy.context.object.scale[0] = 0.001
    bpy.context.object.scale[1] = 0.001
    bpy.context.object.scale[2] = 0.001
    bpy.context.object.rotation_euler[0] = 1.5708
    
    mod = bpy.context.object.modifiers.new(name='decimate', type='DECIMATE')
    mod.ratio = 0.1
    bpy.ops.object.modifier_apply(modifier='decimate')
    
    mat = bpy.data.materials.get("Material")
    
    if len(bpy.context.active_object.data.materials) == 0:
        bpy.context.active_object.data.materials.append(bpy.data.materials['Material'])
    else:
        bpy.context.active_object.data.materials[0] = bpy.data.materials['Material']
    
    if mat:
        mat.node_tree.nodes.new("ShaderNodeVertexColor")
        mat.node_tree.links.new(mat.node_tree.nodes[2].outputs['Color'], mat.node_tree.nodes[0].inputs['Base Color'])
        
    
    bpy.ops.view3d.camera_to_view_selected()
    bpy.ops.render.render(write_still = 1)
    
    bpy.ops.export_scene.gltf(filepath=file_loc_export+'scene.glb', export_materials='EXPORT', export_format='GLB')
    
    for i in range(1, 11):
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = i
        bpy.ops.render.render(write_still = 1)
        zip_file = zipfile.ZipFile(file_loc_export+os.path.splitext(model)[0]+str(i).zfill(2)+'.zip', "w")
        zip_file.write(scene.render.filepath, basename(scene.render.filepath), compress_type=zipfile.ZIP_DEFLATED)
        zip_file.write(file_loc_export + 'scene.glb', basename(file_loc_export + 'scene.glb'), compress_type=zipfile.ZIP_DEFLATED)
        zip_file.close()
        
    bpy.ops.object.delete()
