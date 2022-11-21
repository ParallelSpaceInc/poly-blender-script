import os
import bpy
import zipfile
import math

from os.path import basename
from bpy import context
from PIL import Image

file_loc_export = 'C:\\Users\\USER\\Downloads\\Remesh\\Pngs\\'
file_loc_import = 'C:\\Users\\USER\\Downloads\\Remesh\\Old\\Models15\\'
fileEx = r'.ply'
fileList = [file for file in os.listdir(file_loc_import) if file.endswith(fileEx)]

scene = bpy.context.scene
scene.render.resolution_y = 900
scene.render.resolution_x = 1200
scene.render.film_transparent = True

cam = bpy.data.objects['Camera']

for model in fileList:
    imported_object = bpy.ops.import_mesh.ply(filepath=file_loc_import+model)
    #bpy.context.camera.data.lens = 130

    dimX = bpy.context.object.dimensions.x
    dimY = bpy.context.object.dimensions.y
    dimZ = bpy.context.object.dimensions.z

    dimMax = dimX if dimX > dimY else dimY
    dimMax = dimZ if dimZ > dimMax else dimMax

    bpy.context.object.scale[0] = 1 / dimMax
    bpy.context.object.scale[1] = 1 / dimMax
    bpy.context.object.scale[2] = 1 / dimMax
    bpy.context.object.rotation_euler[0] = 1.5708
    
    #mod = bpy.context.object.modifiers.new(name='decimate', type='DECIMATE')
    #mod.ratio = 0.1
    #bpy.ops.object.modifier_apply(modifier='decimate')
    
    mat = bpy.data.materials.get("Material")
    
    if len(bpy.context.active_object.data.materials) == 0:
        bpy.context.active_object.data.materials.append(bpy.data.materials['Material'])
    else:
        bpy.context.active_object.data.materials[0] = bpy.data.materials['Material']
    
    if mat:
        mat.node_tree.nodes.new("ShaderNodeVertexColor")
        mat.node_tree.links.new(mat.node_tree.nodes[2].outputs['Color'], mat.node_tree.nodes[0].inputs['Base Color'])
        
    zip_file = zipfile.ZipFile(file_loc_export+os.path.splitext(model)[0]+'.zip', "w")

    for i in range(0, 8):
        scene.render.filepath = file_loc_export + 'thumbnail'+str(i)+'.png'
        cam.rotation_euler[2] = math.radians(i*45)
        bpy.ops.view3d.camera_to_view_selected()
        bpy.ops.render.render(write_still = 1) 

        impath = scene.render.filepath
        im = Image.open(impath)
        nim = Image.new(mode = "RGBA", size = im.size, color = (221, 221, 221))
        nim.paste(im, (0, 0), im)
        nim.save(impath)
        zip_file.write(impath, basename(impath), compress_type=zipfile.ZIP_DEFLATED)
        

    bpy.ops.object.delete()
    #bpy.ops.export_scene.gltf(filepath=file_loc_export+'scene.gltf', export_materials='EXPORT', export_format='GLB')
    #bpy.ops.object.delete()
    #zip_file.write(file_loc_export + 'scene.glb', basename(file_loc_export + 'scene.gltf'), compress_type=zipfile.ZIP_DEFLATED)

    zip_file.close()