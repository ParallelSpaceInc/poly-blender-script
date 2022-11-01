import os
import bpy
import zipfile

from os.path import basename
from bpy import context
from PIL import Image

file_loc_export = os.getcwd() + '//'
file_loc_import = os.getcwd() + '//'
fileEx = r'.obj'
fileList = [file for file in os.listdir(file_loc_import) if file.endswith(fileEx)]

scene = bpy.context.scene
scene.render.resolution_y = 900
scene.render.resolution_x = 1200
scene.render.film_transparent = True
scene.render.filepath = file_loc_export + 'thumbnail.png'

#using bat
bpy.ops.object.delete()

for model in fileList:
    print(model)
    imported_object = bpy.ops.import_scene.obj(filepath=file_loc_import+model)
    bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
    
    dimX = bpy.context.object.dimensions.x
    dimY = bpy.context.object.dimensions.y
    dimZ = bpy.context.object.dimensions.z

    dimMax = dimX if dimX > dimY else dimY
    dimMax = dimZ if dimZ > dimMax else dimMax

    bpy.context.object.scale[0] = 1 / dimMax
    bpy.context.object.scale[1] = 1 / dimMax
    bpy.context.object.scale[2] = 1 / dimMax
    bpy.context.object.rotation_euler[0] = 0
    
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')
    bpy.context.object.location[0] = 0
    bpy.context.object.location[1] = 0
    bpy.context.object.location[2] = 0

    mat = bpy.context.object.data.materials[0]
    base_node = mat.node_tree.nodes['Principled BSDF']
    base_node.inputs['Roughness'].default_value = 1

    zip_file = zipfile.ZipFile(file_loc_export+os.path.splitext(model)[0]+'.zip', "w")
    bpy.ops.view3d.camera_to_view_selected()
    bpy.ops.render.render(write_still = 1)   

    im = Image.open(scene.render.filepath)
    nim = Image.new(mode = "RGBA", size = im.size, color = (240, 240, 240))
    nim.paste(im, (0, 0), im)
    nim.save(scene.render.filepath)
    zip_file.write(scene.render.filepath, basename(scene.render.filepath), compress_type=zipfile.ZIP_DEFLATED)

    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    bpy.ops.export_scene.gltf(filepath=file_loc_export+'scene.glb', export_materials='EXPORT', export_format='GLB')
    bpy.ops.object.delete()
    zip_file.write(file_loc_export + 'scene.glb', basename(file_loc_export + 'scene.glb'), compress_type=zipfile.ZIP_DEFLATED)

    zip_file.close()