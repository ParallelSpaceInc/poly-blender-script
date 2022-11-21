# Remesh in Blender
****

Blender는 3D 모델을 가공할 수 있는 오픈소스 그래픽 소프트웨어이다. Blender에는  파이썬 코드를 통해 기능을 제어할 수 있는 bpy 모듈을 지원하는데, 이를 잘 활용하면  반복적인 작업을 사용자가 편리하게끔 자동화할 수 있다.

이 README 파일은 Blender와 파이썬 스크립트를 통해 모델을 자동으로 가공하는 스크립트들을 설명한다. 아래의 스크립트들은 Lab1의 예시처럼 콘솔 창을 통해 사용할 수도 있고, Blender 프로그램의 Script 탭에서 직접 입력하여 사용할 수도 있다. Blender와 Python 설치는 Lab1의 **1.프로그램 설치** 를 참고한다. 

****

## 1. RemeshScript.py

RemeshScript.py 는 모델의 크기와 용량을 축소하고, 썸네일 이미지와 함께 압축 파일로 내보내는 스크립트이다.

```
import os
import zipfile
```

먼저 `os` 모듈과 `zipfile` 모듈을 추가한다. os 모듈은 파일 입출력 경로를 참조하기 위해 필요하고, zipfile 모듈은 압축 파일을 생성하기 위해 필요하다. 만약 해당 모듈이 파이썬에 설치되어 있지 않다면 명령 프롬프트 창을 열고 `pip install os (또는 zipfile)` 을 입력하여 해당 패키지를 설치하면 된다.

```
file_loc_export = 'C:\\Users\\82109\\Downloads\\RemeshedObj\\'
file_loc_import = 'C:\\Users\\82109\\Downloads\\BlenderUVs\\'
fileEx = r'.ply'
fileList = [file for file in os.listdir(file_loc_import) if file.endswith(fileEx)]
```

이후 파일을 입출력할 경로가 할당된 변수와, 작업을 처리할 모델의 확장자가 할당된 변수를 미리 선언한다. 그리고 임포트할 폴더 경로 내부에 존재하는, 해당 확장자를 가진 파일들을 불러와 `fileList` 변수에 할당해준다. 만약 불러올 모델의 경로나 확장자를 바꾸고 싶다면 이 변수들의 값만 수정해 준다면 쉽게 변경할 수 있다.

```
scene = bpy.context.scene
scene.render.resolution_y = 1024
scene.render.resolution_x = 1024
scene.render.film_transparent = True
scene.render.filepath = file_loc_export + 'thumbnail.png'
```

그 다음 썸네일 이미지를 추출하기 위해 `scene` 변수에 `bpy.context.scene` 을 캐싱해준다. `scene`의 멤버들로 하여금 추출된 이미지의 크기나 이름, 확장자 등을 자유롭게 변경할 수 있다.

`film_transparent`은 렌더된 이미지를 추출할 때 배경을 투명하게 할 지를 결정하는 속성이다. 이 경우 투명도 값이 손실되지 않기 위해 이미지 파일의 확장자를 .png로 설정해야 한다.

```
for model in fileList:
    imported_object = bpy.ops.import_mesh.ply(filepath=file_loc_import+model)

    bpy.context.object.scale[0] = 0.010
    bpy.context.object.scale[1] = 0.010
    bpy.context.object.scale[2] = 0.010
    bpy.context.object.rotation_euler[0] = 1.5708
```

for문을 사용해 `fileList` 에 존재하는 모델 파일들을 각각 작업한다. 먼저 `bpy.ops.import_mesh.ply(filepath)` 함수로 모델을 불러와 임시적으로 캐싱한다.

모델의 크기를 원하는 수치만큼 조정한다. `scale` 배열의 각 원소들은 모델의 x, y, z축 스케일 값이다. 각각 0.01로 설정하면 모델의 크기가 그만큼 축소되게 된다.

그리고 `rotation_euler`의 원소값을 수정하여 누워있는 모델을 회전시킨다. [0]번째 원소는 x축이고, 1.5708 이라는 수치는 오일러 변환된 각도값으로 90도 만큼 반시계 방향으로 회전한다는 것을 의미한다.

```
    mod = bpy.context.object.modifiers.new(name='decimate', type='DECIMATE')
    mod.ratio = 0.1
    bpy.ops.object.modifier_apply(modifier='decimate')
```

폴리곤 수를 압축하기 위해 decimate 모디파이어를 모델에 추가해준다. mod 변수에 캐싱한 다음 ratio 멤버를 0.1로 조정해주면 텍스쳐가 좀 뭉개지는 대신 모델의 폴리곤 수가 10분의 1로 줄어든다. `modifier_apply` 함수를 실행하지 않으면 변경 사항이 적용되지 않으니 주의한다.

```
    mat = bpy.data.materials.get("Material")
  
    if len(bpy.context.active_object.data.materials) == 0:
          bpy.context.active_object.data.materials.append(bpy.data.materials['Material'])
    else:
        bpy.context.active_object.data.materials[0] = bpy.data.materials['Material']

    if mat:
        mat.node_tree.nodes.new("ShaderNodeVertexColor")
        mat.node_tree.links.new(mat.node_tree.nodes[2].outputs['Color'], mat.node_tree.nodes[1].inputs['Base Color'])
```

다음은 모델의 정점 색상을 출력하기 위해 매테리얼을 추가하는 과정이다. 이 과정이 없으면 추출된 모델이 아무런 색 없이 하얗게만 보이게 된다.

매테리얼 데이터를 가져와 mat 변수에 할당하고, 만약 모델에 매테리얼 정보가 없다면 새로 생성한다. 이후 쉐이더의 노드 트리에 Vertex Color라는 노드를 새로 생성한 뒤 모델의 Base Color에 연결시킨다. 이러면 모델의 정점 색상이 기본적으로 할당되어 렌더링 후 추출할 때에도 제대로 보이게 된다.

```
    zip_file = zipfile.ZipFile(file_loc_export+os.path.splitext(model)[0]+'.zip', "w")
    bpy.ops.render.render(write_still = 1)
    zip_file.write(scene.render.filepath, basename(scene.render.filepath), compress_type=zipfile.ZIP_DEFLATED)
```

이렇게 만들어진 모델을 압축 파일로 만들기 위해 `zip_file` 변수를 선언한다. 파일 경로는 추출할 경로로 설정하고, 현재 작업 중인 모델 파일 이름에 .zip 확장자를 붙인 뒤 읽기 전용으로 만든다.

`bpy.ops.render.render` 함수를 실행하면 렌더링 작업이 시작되고, write_still 파라미터를 True로 설정하면 지정해둔 경로에 방금 설정했던 썸네일 png 파일이 생성된다. 이후 만든 이미지를 .zip 파일 안에 들어가게끔 압축시킨다.

```
from os.path import basename
```

이 때 `basename` 파라미터를 삽입해야 압축 파일 내부에 경로 폴더가 생성되지 않고 파일만 압축된다. 이를 위해 코드 상단에 미리 `basename`을 임포트해둔다.

```
    bpy.ops.export_scene.gltf(filepath=file_loc_export+'scene.gltf', export_materials='EXPORT', export_format='GLTF_EMBEDDED')
    bpy.ops.object.delete()
    zip_file.write(file_loc_export + 'scene.gltf', basename(file_loc_export + 'scene.gltf'), compress_type=zipfile.ZIP_DEFLATED)
    zip_file.close()
```

이제 `export_scene.gltf` 메소드를 통해 gltf 형식으로 모델 파일을 추출한다. 함수를 변경하면 .obj나 .ply 등의 다른 확장자로도 추출할 수 있으며, export_format 파라미터의 값을 변경하면 .glb 확장자로도 추출이 가능하다.

반복문의 다음 작업에 방해되지 않기 위해 `delete` 함수로 작업한 모델을 삭제한다. 그리고 추출한 모델 파일을 아까 전의 .zip 파일에 같이 압축시키면 일련의 작업이 완료된다. 


***

## 2. AutoUnitSize.py

AutoUnitSize.py 는 1x1x1 박스 안에 들어가게끔 모델 크기를 자동 가공하는 기능을 추가한 스크립트이다. 전체적인 작업 플로우는 기존의 RemeshScript.py 를 기반으로 하나, 일부 코드를 수정하였다.

```
    dimX = bpy.context.object.dimensions.x
    dimY = bpy.context.object.dimensions.y
    dimZ = bpy.context.object.dimensions.z

    dimMax = dimX if dimX > dimY else dimY
    dimMax = dimZ if dimZ > dimMax else dimMax

    bpy.context.object.scale[0] = 1 / dimMax
    bpy.context.object.scale[1] = 1 / dimMax
    bpy.context.object.scale[2] = 1 / dimMax
    bpy.context.object.rotation_euler[0] = 1.5708
    
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')
    bpy.context.object.location[0] = 0
    bpy.context.object.location[1] = 0
    bpy.context.object.location[2] = 0
```

 해당 코드는 불러온 모델의 크기를 자동으로 가공하는 부분이다. `bpy.context.object.dimension`을 통해 모델을 둘러싼 Bounding Box의 xyz 값을 추출하고, 개중 가장 큰 값인 `dimMax` 값으로 모델의 스케일을 같은 비율로 나눈다. 각 스케일 값에 동일하게 `1 / dimMax` 를 곱했기 때문에 모델은 기존 비율을 유지하면서 썸네일 렌더링의 기준이 되는 1x1x1 박스 안에 들어갈 수 있을 정도로 축소된다.

 또한 `bpy.ops.object.origin_set` 함수를 사용하여 모델의 피벗 기준점을 볼륨 가중치에 따라 중앙으로 변경한 뒤, 위치를 다시 원점으로 보정한다. 이러면 모델과 기준점의 위치가 매칭되지 않는 문제를 방지할 수 있다.

***

## 3. RespectRemesh.py

RespectRemesh.py 는 모델 주변 8방향으로 썸네일을 렌더링해 압축하는 스크립트이다. 역시 하단 부분을 제외하곤 기존의 스크립트와 유사하다.

```
    zip_file = zipfile.ZipFile(file_loc_export+os.path.splitext(model)[0]+'.zip', "w")

    for i in range(0, 8):
        scene.render.filepath = file_loc_export + 'thumbnail'+str(i)+'.png'
        bpy.data.objects['Empty'].rotation_euler[2] = math.radians(i*45)
        bpy.ops.render.render(write_still = 1) 

        impath = scene.render.filepath
        im = Image.open(impath)
        nim = Image.new(mode = "RGBA", size = im.size, color = (221, 221, 221))
        nim.paste(im, (0, 0), im)
        nim.save(impath)
        zip_file.write(impath, basename(impath), compress_type=zipfile.ZIP_DEFLATED)
```

해당 코드는 원점의 모델을 중심으로 카메라를 45도 각도로 회전시켜 총 8장의 썸네일을 렌더링해 출력하는 부분이다. 번호가 매겨진 thumnail png 파일을 생성한 뒤, 서로 다른 카메라 각도로 렌더링한 모델을 각 png파일에 그려서 임의로 생성한 zip 파일에 압축시켜 넣는 작업을 수행한다. 

***

## 4. RemeshWhite.py

RemeshWhite.py 는 기존의 RemeshScript.py 에서 모델의 밝기를 단계적으로 조절하는 기능을 추가한 스크립트이다.

```
    for i in range(1, 11):
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = i
        bpy.ops.render.render(write_still = 1)
        zip_file = zipfile.ZipFile(file_loc_export+os.path.splitext(model)[0]+str(i).zfill(2)+'.zip', "w")
        zip_file.write(scene.render.filepath, basename(scene.render.filepath), compress_type=zipfile.ZIP_DEFLATED)
        zip_file.write(file_loc_export + 'scene.glb', basename(file_loc_export + 'scene.glb'), compress_type=zipfile.ZIP_DEFLATED)
        zip_file.close()
```

for문의 첫 번째 줄은 blender 프로그램 상 World의 백그라운드 노드를 가져와서 그중 두 번째 인자인 Ambient 밝기를 단계에 따라 조절하는 기능이다.

해당 함수로 렌더링 시 모델의 전체적 밝기를 조절하고, 이후 기존의 방식대로 렌더링해 썸네일 png 파일을 생성한 뒤 압축 파일에 glb와 이미지 파일을 각각 저장한다.