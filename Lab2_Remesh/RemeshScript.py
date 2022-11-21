import os
import bpy
import zipfile

from os.path import basename
from bpy import context
from PIL import Image

file_loc_export = 'C:\\Users\\USER\\Downloads\\Remesh\\Old\\RemeshedGlb\\'
file_loc_import = 'C:\\Users\\USER\\Downloads\\Remesh\\Old\\Models1-3\\'
fileEx = r'.ply'
fileList = [file for file in os.listdir(file_loc_import) if file.endswith(fileEx)]

scene = bpy.context.scene
scene.render.resolution_y = 900
scene.render.resolution_x = 1200
scene.render.film_transparent = True
scene.render.filepath = file_loc_export + 'thumbnail.png'

for model in fileList:
    imported_object = bpy.ops.import_mesh.ply(filepath=file_loc_import+model)
    #bpy.context.camera.data.lens = 130

    bpy.context.object.scale[0] = 0.010
    bpy.context.object.scale[1] = 0.010
    bpy.context.object.scale[2] = 0.010
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
        mat.node_tree.links.new(mat.node_tree.nodes[2].outputs['Color'], mat.node_tree.nodes[1].inputs['Base Color'])
        
    zip_file = zipfile.ZipFile(file_loc_export+os.path.splitext(model)[0]+'.zip', "w")
    bpy.ops.view3d.camera_to_view_selected()
    bpy.ops.render.render(write_still = 1)   

    im = Image.open(scene.render.filepath)
    nim = Image.new(mode = "RGBA", size = im.size, color = (221, 221, 221))
    nim.paste(im, (0, 0), im)
    nim.save(scene.render.filepath)
    zip_file.write(scene.render.filepath, basename(scene.render.filepath), compress_type=zipfile.ZIP_DEFLATED)

    #bpy.ops.export_scene.obj(filepath=file_loc_export+os.path.splitext(model)[0]+'_resized.obj')
    #bpy.ops.export_mesh.ply(filepath=file_loc_export+os.path.splitext(model)[0]+'_resized.ply')
    #bpy.ops.export_scene.gltf(filepath=file_loc_export+os.path.splitext(model)[0]+'_remeshed.gltf', export_materials='EXPORT', export_format='GLTF_EMBEDDED')
    bpy.ops.export_scene.gltf(filepath=file_loc_export+'scene.gltf', export_materials='EXPORT', export_format='GLB')
    bpy.ops.object.delete()
    zip_file.write(file_loc_export + 'scene.glb', basename(file_loc_export + 'scene.gltf'), compress_type=zipfile.ZIP_DEFLATED)

    zip_file.close()