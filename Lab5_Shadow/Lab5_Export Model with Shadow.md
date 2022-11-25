# Export Model with Shadow
****

 Blender를 사용해 모델 하단부에 투명한 그림자 텍스쳐를 추가하여 .glb 형식으로 내보낼 수 있다. 해당 스크립트를 실행하기 위해선 먼저 그림자 파일 출력을 위해 Blender의 Compositing 탭에서 Composite 노드와 File Output 노드를 추가해야 한다.

 자세한 사항은 [이 문서](https://parallelspaces.atlassian.net/l/cp/25ErgNSG) 를 참조하면 좋다.

***

## 1. AutoShadow.py

```
import os
import bpy

from bpy import context

file_loc_export = 'C:\\Users\\USER\\Downloads\\Remesh\\Shadow\\'
file_loc_import = 'C:\\Users\\USER\\Downloads\\Remesh\\Temp\\'
fileEx = r'.ply'
fileList = [file for file in os.listdir(file_loc_import) if file.endswith(fileEx)]

scene = bpy.context.scene
```

먼저 필요한 파이썬 모듈을 임포트한 뒤 파일 입출력 경로를 설정한다. `file_loc_import` 는 불러올 .ply 모델 파일들이 저장된 경로, `file_loc_export` 는 그림자 .png 파일과 그림자가 추가된 모델 .glb 파일을 내보낼 경로이다.  `fileEx` 변수 와 import 함수를 수정하는 것으로 모델 파일의 확장자를 변경할 수 있다.

```
for model in fileList:
    bpy.ops.import_mesh.ply(filepath=file_loc_import+model)
    modelName = os.path.splitext(model)[0]
    imported_object = bpy.context.object
    img = bpy.data.images.new(modelName + '_shadow', 1024, 1024,)

    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    bpy.context.object.location[0] = 0
    bpy.context.object.location[1] = 0
    bpy.context.object.location[2] = 0

    bpy.data.objects['Plane'].scale[0] = bpy.context.object.dimensions.x * 1.5
    bpy.data.objects['Plane'].scale[1] = bpy.context.object.dimensions.y * 1.5
    bpy.data.objects['Plane'].location[0] = 0
    bpy.data.objects['Plane'].location[1] = 0
    bpy.data.objects['Plane'].location[2] = -bpy.context.object.dimensions.z * 0.5
```

이후 모델을 불러와 중심을 지오메트리 기준으로 중앙으로 맞춘 뒤 위치 xyz값을 조정해 가운데에 놓고, Plane이 모델 바로 밑 바닥에 놓여있도록 위치 값과 크기 값을 조절한다.

```
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
```
이어서 Plane 모델을 선택해 매테리얼을 가져온다. 이상이 없을 경우 미리 준비된 Shadow 이미지 노드를 선택해 해당 노드에 위에서 만들었던 새로운 이미지 파일을 할당한다.

```
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.bake_type = 'SHADOW'
    bpy.context.scene.render.bake.margin = 0
    bpy.context.view_layer.objects.active = bpy.context.active_object
    bpy.ops.object.bake(type='SHADOW', save_mode='EXTERNAL')

    bpy.context.scene.node_tree.nodes['Image'].image = img
    bpy.context.scene.node_tree.nodes['File Output'].base_path = file_loc_export
    bpy.ops.render.render(write_still = 1)
    bpy.data.images['Viewer Node'].save_render(file_loc_export + modelName + '_shadow.png')
```

그 다음 Plane에 그림자를 Bake하고, Compositing 탭의 이미지 노드에 그림자가 Bake된 이미지를 할당한 뒤 렌더링을 시작한다. 렌더링이 완료된 이후 Viewer 노드에 보여지는 투명 처리가 된 그림자 이미지를 출력 경로에 .png 확장자로 저장한다.

```
    if mat:
        shadow_node.image = bpy.data.images.load(file_loc_export + modelName + '_shadow.png')
        l1 = mat.node_tree.links.new(shadow_node.outputs['Color'], base_node.inputs['Base Color'])
        l2 = mat.node_tree.links.new(shadow_node.outputs['Alpha'], base_node.inputs['Alpha'])

    bpy.ops.export_scene.gltf(filepath=file_loc_export+modelName+'.glb', export_materials='EXPORT', export_format='GLB')

    if mat:
        mat.node_tree.links.remove(l1)
        mat.node_tree.links.remove(l2)

    bpy.data.objects.remove(imported_object)
```

마지막으로 투명 처리 그림자 이미지를 다시 이미지 노드에 불러와 베이스 노드에 연결한 후, .glb 확장자로 저장한 다음 노드 링크와 오브젝트를 제거하면 한 모델에 대한 작업이 완료된다. 이런 식으로 모든 모델에 대해 자동화 작업을 진행한다. 