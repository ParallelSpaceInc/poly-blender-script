# How to Hanpac

Hanpac은 모델 자동 가공 과정 중 주요 기능들을 모듈화한 파이썬 패키지이다.

먼저 해당 패키지를 Blender가 설치된 폴더의 python/lib/site-packages 경로에 넣어야 한다. 그리고 Blender의 Script 탭에서 각 함수를 직접 Hanpac.func.XXXX() 형식으로 기입해 사용하거나, 아니면 직접 작성한 스크립트에 해당 모듈을 임포트하여 사용할 수도 있다.

## 1. resize_obj

```
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
```

3D 모델 obj를 주어진 sz 파라미터 비율에 맞추어 모델의 xyz 크기를 축소시킨다. 축소는 Bounding Box에 기반한다.

## 2. rotate_obj

```
def rotate_obj(obj, x=0, y=0, z=0):
    obj.rotation_euler[0] = math.radians(x)
    obj.rotation_euler[1] = math.radians(y)
    obj.rotation_euler[2] = math.radians(z)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
```

3D 모델 obj의 x, y, z를 각각 각도에 맞추어 회전시킨다. 예를 들어 x에 90을 넣으면 모델은 x축 기준으로 90도 만큼 회전한다.

## 3. remesh_obj

```
def remesh_obj(obj, ratio=1):
    mod = obj.modifiers.new(name='decimate', type='DECIMATE')
    mod.ratio = ratio
    bpy.ops.object.modifier_apply(modifier='decimate')
```

3D 모델 obj를 ratio 비율에 맞추어 decimating한다. vertex 수가 줄어들어 디테일이 손상되는 대신 모델의 용량이 축소된다.

## 4. reexport_obj

```
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
```

3D 모델 obj를 불러와 지정된 path에 다시 내보낸다. 이때 이름 name과 확장자 type을 결정할 수 있다.

## 5. bake_obj

```
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
```

3D 모델 obj의 Vertex Color를 Bake해 텍스쳐를 추출한 뒤 매핑한다. 모델에 Vertex Color가 존재하지 않으면 까맣게만 나온다. UV 매핑을 겸하기 때문에 일정 Vertex 수 이상의 고용량 모델(약 20MB)은 작동하지 않는다. 파라미터로 받은 img가 없으면 따로 하나 생성하며 텍스쳐를 매핑한 뒤 리턴한다.

## 6. make_thumbnail

```
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
```

3D 모델 obj의 썸네일 이미지를 생성한다. 광원이나 카메라 각도 등은 미리 설정해 두어야 한다. path와 name으로 이미지가 저장될 경로를 지정할 수 있고 x, y로 이미지의 가로 세로 크기를 정할 수 있다. grey 값을 True로 설정하면 썸네일 이미지의 배경을 밝은 회색으로 설정한다.