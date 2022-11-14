import os
import bpy
import math

from PIL import Image

def resize_obj(obj, sz=1):
    dimX = obj.dimensions.x
    dimY = obj.dimensions.y
    dimZ = obj.dimensions.z

    dimMax = dimX if dimX > dimY else dimY
    dimMax = dimZ if dimZ > dimMax else dimMax

    obj.scale[0] = sz / dimMax
    obj.scale[1] = sz / dimMax
    obj.scale[2] = sz / dimMax
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

def rotate_obj(obj, x=0, y=0, z=0):
    obj.rotation_euler[0] = math.radians(x)
    obj.rotation_euler[1] = math.radians(y)
    obj.rotation_euler[2] = math.radians(z)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

def remesh_obj(obj, ratio=1):
    mod = obj.modifiers.new(name='decimate', type='DECIMATE')
    mod.ratio = ratio
    bpy.ops.object.modifier_apply(modifier='decimate')

def reexport_obj(obj, path=None, name=None, type='obj'):
    if path == None:
        path = os.getcwd()
    
    if name == None:
        name = obj.name

    if type == 'ply':
        bpy.ops.export_mesh.ply(filepath=path+'//'+name+'.ply')
    
    if type == 'obj':
        bpy.ops.export_scene.obj(filepath=path+'//'+name+'.obj')

    if type == 'glb':
        bpy.ops.export_scene.gltf(filepath=path+'//'+name+'.glb', export_materials='EXPORT', export_format='GLB')

    if type == 'gltf':
        bpy.ops.export_scene.gltf(filepath=path+'//'+name+'.gltf', export_materials='EXPORT', export_format='GLTF_EMBEDDED')

    if type == 'fbx':
        bpy.ops.import_scene.fbx(filepath=path+'//'+name+'.fbx') 

def bake_obj(obj, img=None):
    if img == None:
        image_name = obj.name + '_tex'
        img = bpy.data.images.new(image_name,2048,2048)

    mat = obj.active_material

    if mat:
        color_node = mat.node_tree.nodes.new("ShaderNodeVertexColor")
        base_node = mat.node_tree.nodes['Principled BSDF']
        mat.node_tree.links.new(color_node.outputs['Color'], base_node.inputs['Base Color'])

        mat.use_nodes = True
        texture_node = mat.node_tree.nodes.new('ShaderNodeTexImage')
        texture_node.name = 'Bake_node'
        texture_node.select = True
        mat.node_tree.nodes.active = texture_node
        texture_node.image = img #Assign the image to the node
    
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=1.55334)
    bpy.ops.object.editmode_toggle()

    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.bake_type = 'DIFFUSE'
    scene.render.bake.use_pass_direct = False
    scene.render.bake.use_pass_indirect = False
    scene.render.bake.margin = 0

    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.bake(type='DIFFUSE', save_mode='EXTERNAL')

    if mat:
        mat.node_tree.links.new(texture_node.outputs['Color'], base_node.inputs['Base Color'])
    
    return img    
    
def make_thumbnail(obj, path=None, name=None, x=1200, y=900, grey=False):
    scene = bpy.context.scene
    scene.render.resolution_x = x
    scene.render.resolution_y = y
    scene.render.film_transparent = True

    if path == None:
        path = os.getcwd()

    if name == None:
        name = obj.name

    scene.render.filepath = path + '//' + name + '.png'

    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.view3d.camera_to_view_selected()
    bpy.ops.render.render(write_still = 1)

    if grey:
        im = Image.open(scene.render.filepath)
        nim = Image.new(mode = "RGBA", size = im.size, color = (240, 240, 240))
        nim.paste(im, (0, 0), im)
        nim.save(scene.render.filepath)
