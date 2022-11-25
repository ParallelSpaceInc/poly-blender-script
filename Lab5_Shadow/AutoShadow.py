import os
import bpy

from bpy import context

file_loc_export = 'C:\\Users\\USER\\Downloads\\Remesh\\Shadow\\'
file_loc_import = 'C:\\Users\\USER\\Downloads\\Remesh\\Temp\\'
fileEx = r'.ply'
fileList = [file for file in os.listdir(file_loc_import) if file.endswith(fileEx)]

scene = bpy.context.scene

for model in fileList:
    bpy.ops.import_mesh.ply(filepath=file_loc_import+model)
    modelName = os.path.splitext(model)[0]
    imported_object = bpy.context.object
    img = bpy.data.images.new(modelName + '_shadow', 1024, 1024)

    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    bpy.context.object.location[0] = 0
    bpy.context.object.location[1] = 0
    bpy.context.object.location[2] = 0

    bpy.data.objects['Plane'].scale[0] = bpy.context.object.dimensions.x * 1.5
    bpy.data.objects['Plane'].scale[1] = bpy.context.object.dimensions.y * 1.5
    bpy.data.objects['Plane'].location[0] = 0
    bpy.data.objects['Plane'].location[1] = 0
    bpy.data.objects['Plane'].location[2] = -bpy.context.object.dimensions.z * 0.5
    
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['Plane'].select_set(True)

    mat = bpy.data.materials.get("Material")

    if mat:
        mat.use_nodes = True
        base_node = mat.node_tree.nodes[1]
        shadow_node = mat.node_tree.nodes[3] #Need to custom Shadow Image Node

        shadow_node.name = 'Shadow'
        shadow_node.select = True
        mat.node_tree.nodes.active = shadow_node
        shadow_node.image = img #To assign the image to the node

    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.bake_type = 'SHADOW'
    bpy.context.scene.render.bake.margin = 0
    bpy.context.view_layer.objects.active = bpy.context.active_object
    bpy.ops.object.bake(type='SHADOW', save_mode='EXTERNAL')

    bpy.context.scene.node_tree.nodes['Image'].image = img
    bpy.context.scene.node_tree.nodes['File Output'].base_path = file_loc_export
    bpy.ops.render.render(write_still = 1)
    bpy.data.images['Viewer Node'].save_render(file_loc_export + modelName + '_shadow.png')

    if mat:
        shadow_node.image = bpy.data.images.load(file_loc_export + modelName + '_shadow.png')
        l1 = mat.node_tree.links.new(shadow_node.outputs['Color'], base_node.inputs['Base Color'])
        l2 = mat.node_tree.links.new(shadow_node.outputs['Alpha'], base_node.inputs['Alpha'])

    bpy.ops.export_scene.gltf(filepath=file_loc_export+modelName+'.glb', export_materials='EXPORT', export_format='GLB')

    if mat:
        mat.node_tree.links.remove(l1)
        mat.node_tree.links.remove(l2)

    bpy.data.objects.remove(imported_object)