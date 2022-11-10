import os
import bpy
import zipfile

from os.path import basename
from bpy import context
from PIL import Image

#Setting I/O Path & File Extension
file_loc_export = os.getcwd() + '//'
file_loc_import = os.getcwd() + '//'
fileEx = r'.ply'
fileList = [file for file in os.listdir(file_loc_import) if file.endswith(fileEx)]

#Need To Export thumbnail.png
scene = bpy.context.scene
scene.render.resolution_y = 900
scene.render.resolution_x = 1200
scene.render.film_transparent = True
scene.render.filepath = file_loc_export + 'thumbnail.png'

#Need when using bat
bpy.ops.object.delete()

#Add Light
light_data = bpy.data.lights.new(name="Light2", type='POINT')
light_data.energy = 1200
light_object = bpy.data.objects.new(name="Light2", object_data=light_data)
bpy.context.collection.objects.link(light_object)
light_object.location = (-4, -1, 6)

for model in fileList:
    print(model)
    imported_object = bpy.ops.import_mesh.ply(filepath=file_loc_import+model)

    #Making empty image to bake texture
    image_name = bpy.context.active_object.name + '_tex'
    img = bpy.data.images.new(image_name,2048,2048)

    #Resizing
    dimX = bpy.context.object.dimensions.x
    dimY = bpy.context.object.dimensions.y
    dimZ = bpy.context.object.dimensions.z

    dimMax = dimX if dimX > dimY else dimY
    dimMax = dimZ if dimZ > dimMax else dimMax

    bpy.context.object.scale[0] = 1 / dimMax
    bpy.context.object.scale[1] = 1 / dimMax
    bpy.context.object.scale[2] = 1 / dimMax

    #Allocating material
    mat = bpy.data.materials.get("Material")
    
    if len(bpy.context.active_object.data.materials) == 0:
        bpy.context.active_object.data.materials.append(bpy.data.materials['Material'])
    else:
        bpy.context.active_object.data.materials[0] = bpy.data.materials['Material']

    #Ready to bake
    if mat:
        mat.node_tree.nodes.new("ShaderNodeVertexColor")
        base_node = mat.node_tree.nodes['Principled BSDF']
        base_node.inputs['Roughness'].default_value = 1
        mat.node_tree.links.new(mat.node_tree.nodes[2].outputs['Color'], base_node.inputs['Base Color'])

        mat.use_nodes = True
        texture_node =mat.node_tree.nodes.new('ShaderNodeTexImage')
        texture_node.name = 'Bake_node'
        texture_node.select = True
        mat.node_tree.nodes.active = texture_node
        texture_node.image = img #Assign the image to the node
    
    #UV Mapping
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=1.55334)
    bpy.ops.object.editmode_toggle()

    #Baking Texture and save
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.bake_type = 'DIFFUSE'
    bpy.context.scene.render.bake.use_pass_direct = False
    bpy.context.scene.render.bake.use_pass_indirect = False
    bpy.context.scene.render.bake.margin = 0

    bpy.context.view_layer.objects.active = bpy.context.active_object
    bpy.ops.object.bake(type='DIFFUSE', save_mode='EXTERNAL')

    img.save_render(file_loc_export+'scene.png')
    
    if mat:
        mat.node_tree.links.new(texture_node.outputs['Color'], base_node.inputs['Base Color'])

    #Making .zip file
    zip_file = zipfile.ZipFile(file_loc_export+os.path.splitext(model)[0]+'.zip', "w")
    #zip_file.write(file_loc_export + 'scene.png', basename(file_loc_export + 'scene.png'), compress_type=zipfile.ZIP_DEFLATED)

    #Rendering thumbnail
    bpy.ops.view3d.camera_to_view_selected()
    bpy.ops.render.render(write_still = 1)   

    #Creating gray-background thumnnail.png file
    im = Image.open(scene.render.filepath)
    nim = Image.new(mode = "RGBA", size = im.size, color = (240, 240, 240))
    nim.paste(im, (0, 0), im)
    nim.save(scene.render.filepath)
    zip_file.write(scene.render.filepath, basename(scene.render.filepath), compress_type=zipfile.ZIP_DEFLATED)

    #Exporting .glb file
    bpy.ops.export_scene.gltf(filepath=file_loc_export+'scene.glb', export_materials='EXPORT', export_format='GLB')
    zip_file.write(file_loc_export + 'scene.glb', basename(file_loc_export + 'scene.glb'), compress_type=zipfile.ZIP_DEFLATED)

    #Clearing material
    for mat in bpy.context.active_object.data.materials:
        for n in mat.node_tree.nodes:
            if n.name == 'Bake_node':
                mat.node_tree.nodes.remove(n)

    bpy.ops.object.delete()
    zip_file.close()