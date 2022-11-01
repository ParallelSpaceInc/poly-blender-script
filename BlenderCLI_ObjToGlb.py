import os
import bpy
import zipfile

from os.path import basename
from bpy import context
from PIL import Image

#Setting I/O Path & File Extension
file_loc_export = os.getcwd() + '//'
file_loc_import = os.getcwd() + '//'
fileEx = r'.obj'
fileList = [file for file in os.listdir(file_loc_import) if file.endswith(fileEx)]

#Need To Export thumbnail.png
scene = bpy.context.scene
scene.render.resolution_y = 900
scene.render.resolution_x = 1200
scene.render.film_transparent = True
scene.render.filepath = file_loc_export + 'thumbnail.png'

#Need when using bat
bpy.ops.object.delete()

for model in fileList:
    print(model)
    imported_object = bpy.ops.import_scene.obj(filepath=file_loc_import+model)

    #Obj resizing & adjust angle
    bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
    bpy.context.object.scale[0] = 0.001
    bpy.context.object.scale[1] = 0.001
    bpy.context.object.scale[2] = 0.001
    bpy.context.object.rotation_euler[0] = 0

    #Changing material roughness
    mat = bpy.context.object.data.materials[0]
    base_node = mat.node_tree.nodes['Principled BSDF']
    base_node.inputs['Roughness'].default_value = 1

    #Making .zip file and rendering thumbnail
    zip_file = zipfile.ZipFile(file_loc_export+os.path.splitext(model)[0]+'.zip', "w")
    bpy.ops.view3d.camera_to_view_selected()
    bpy.ops.render.render(write_still = 1)   

    #Creating gray-background thumnnail.png file
    im = Image.open(scene.render.filepath)
    nim = Image.new(mode = "RGBA", size = im.size, color = (240, 240, 240))
    nim.paste(im, (0, 0), im)
    nim.save(scene.render.filepath)
    zip_file.write(scene.render.filepath, basename(scene.render.filepath), compress_type=zipfile.ZIP_DEFLATED)

    #Exporting .glb file
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    bpy.ops.export_scene.gltf(filepath=file_loc_export+'scene.glb', export_materials='EXPORT', export_format='GLB')
    bpy.ops.object.delete()
    zip_file.write(file_loc_export + 'scene.glb', basename(file_loc_export + 'scene.glb'), compress_type=zipfile.ZIP_DEFLATED)

    zip_file.close()