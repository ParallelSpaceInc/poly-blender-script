# .ply to textured .glb in Blender
****

Blender는 3D 모델을 가공할 수 있는 오픈소스 그래픽 소프트웨어이다. Blender에는  파이썬 코드를 통해 기능을 제어할 수 있는 bpy 모듈을 지원하는데, 이를 잘 활용하면  반복적인 작업을 사용자가 편리하게끔 자동화할 수 있다.

이 README 파일은 Blender와 파이썬 스크립트를 통해 .ply 확장자의 3D 모델들을 텍스쳐가 포함된 .glb 확장자 형식으로 변환하는 방법을 설명한다.

****

## 1. 프로그램 설치

먼저 Blender와 Python이 설치되어있어야 한다. 각각 [https://www.blender.org/download/](https://www.blender.org/download/) 와 [https://www.python.org/downloads/](https://www.python.org/downloads/) 에서 최신 버전을 다운로드 받을 수 있다. 리눅스 환경이라면 아래의 명령어를 터미널 창에 입력하는 것으로도 파이썬을 설치할 수 있다.

```
sudo apt-get install python3
```

그 다음 스크립트 실행에 필요한 파이썬 모듈을 설치하기 위해 터미널을 연다. 윈도우 환경에서 터미널은 검색 창이나 폴더의 주소창에서 cmd를 입력하면 열 수 있다. 

터미널 창에서 해당 명령어를 입력해 zipfile 모듈을 설치한다. zipfile 모듈은 파이썬에서 ZIP 압축 파일을 다루기 위해 필요한 라이브러리이며, 자동화 스크립트로 변환한 파일들을 압축시킬 때에 사용된다.

```
pip install zipfile
```

설치가 성공적으로 완료되었으면 이제 자동화 스크립트를 실행할 수 있다.


****

## 2. 스크립트 실행

자동화 스크립트를 사용하기 위해선 한 폴더 안에 다음 항목들을 모두 집어넣어야 한다.

1. 변환할 .ply 모델 파일들
2. 자동화 스크립트 파일 `BlednerCLI.py`
3. 배치 파일 `script.bat` (Windows) / 쉘 파일 `script.sh` (Linux)

가급적이면 디렉토리 경로 상에 한글이 섞이지 않은 편이 좋다.

### 2-1. 윈도우 환경 버전 체크

윈도우 환경일 경우 우선 Blender의 버전을 확인한다. 버전은 `C:\Program Files\Blender Foundation` 경로에 존재하는 폴더의 이름을 통해 확인할 수 있다. `script.bat` 파일에 작성된 Blender 버전은 3.3으로 설정되어 있으므로 만약 다르다면 이를 변경해주어야 한다.

script.bat 파일을 메모장으로 열고 다음과 같은 라인을 찾는다.

```
"C:/Program Files/Blender Foundation/Blender 3.3/blender.exe" -b -P %1
```

여기서 Blender 버전에 따라 `Blender 3.3` 부분을 바꾸고 다시 저장한다.

### 2-2. 터미널 실행

준비가 끝났으면 파일들이 있는 디렉토리 경로에 터미널 창을 연다. 윈도우에선 폴더의 주소창에 cmd를 입력하여 바로 띄울 수 있다.

해당 터미널 창에 다음의 명령어를 입력한다.

```
script.bat BlednerCLI.py
```

그러면 스크립트가 실행되며 .ply 파일의 변환이 시작된다.

해당 폴더에 순차적으로 매핑된 텍스쳐 파일 `scene.png` 와 변환된 모델 `scene.glb` 파일이 생성되며 이를 원본 모델의 이름으로 zip 으로 압축되어 저장한다. 모든 모델에 대한 처리가 끝나면 터미널 창에서 `Blender quit` 이라는 메시지와 함께 종료된다.

****

## 3. 스크립트 설명

### 3-1. script.bat / script.sh 

먼저 script.bat 파일의 내용을 살펴보면 다음과 같다.

```
ECHO OFF

IF "%1"=="" GOTO USAGE

"C:/Program Files/Blender Foundation/Blender 3.3/blender.exe" -b -P %1
GOTO END

:USAGE
ECHO script.bat [filename]

:END
```

`ECHO OFF` 명령어는 실행한 명령에 대한 결과만을 보여줌으로써 터미널 화면을 간결하게 만들기 위한 명령어다.

`IF "%1"=="" GOTO USAGE` 는 만약 터미널에서 배치 파일을 실행할 때 인자 없이 그냥 `script.bat` 만 실행했을 경우 정확한 사용법을 알려주는 명령어다. 배치 파일을 실행할 때에는 항상 인자로 파이썬 스크립트 파일을 추가해 주어야 한다.

`"C:/Program Files/Blender Foundation/Blender 3.3/blender.exe" -b -P %1` 는 해당 경로의 `blender.exe` 파일을 통해 터미널 상에서 블렌더의 파이썬 스크립트를 실행할 수 있도록 해주는 명령어이다. `%1` 부분에선 배치 파일과 함께 입력했던 첫 번째 인자인 .py 파일이 들어간다.

Linux에서 사용되는 script.sh 파일의 내용은 비교적 간단하다.

```
#!/bin/bash
if [ "$#" = 1 ]
then
	blender -b -P "$1"
else
	echo 2gltf2.sh [SCRIPT.py]
fi
```

터미널 상에서 쉘 파일과 함께 입력받는 인자가 1개일 경우 `blender -b -P [SCRIPT.py]` 로 해당 파이썬 스크립트를 실행한다. 그렇지 않을 경우 파일의 정확한 사용법을 알려준다.

Linux 환경에서는 경로에 상관없이 터미널 상에서 바로 Blender 프로그램을 실행할 수 있다.

### 3-2. BlenderCLI.py

`BlenderCLI.py` 는 Blender로 .ply 파일의 텍스쳐를 추출하여 .glb 파일로 내보내는 과정을 자동화한 스크립트이다.

```
import os
import bpy
import zipfile

from os.path import basename

file_loc_export = os.getcwd() + '//'
file_loc_import = os.getcwd() + '//'
fileEx = r'.ply'
fileList = [file for file in os.listdir(file_loc_import) if file.endswith(fileEx)]

scene = bpy.context.scene

#using bat
bpy.ops.object.delete()

```

처음엔 스크립트 작동에 필요한 모듈을 import하고 파일 변환 입출력 경로를 설정한다. 텍스쳐를 추출할 .ply 모델이 있는 곳은 `file_loc_import`에, .glb 파일로 내보낼 위치는 `file_loc_export`에 각각 할당한다. 지금은 현재 파일 경로로 설정되어 있으나 사용자가 임의로 수정할 수 있다.

모델들을 import할 경로에서 .ply 파일만 찾아 `fileList`로 만든다. 그리고 Blender 프로그램을 처음 시작하면 기본적으로 Cube 오브젝트를 만들어두는데, 이를 삭제하기 위해 `bpy.ops.object.delete` 함수를 실행한다.

```

for model in fileList:
    imported_object = bpy.ops.import_mesh.ply(filepath=file_loc_import+model)

    image_name = bpy.context.active_object.name + '_tex'
    img = bpy.data.images.new(image_name,2048,2048)

    mat = bpy.data.materials.get("Material")
    
    if len(bpy.context.active_object.data.materials) == 0:
        bpy.context.active_object.data.materials.append(bpy.data.materials['Material'])
    else:
        bpy.context.active_object.data.materials[0] = bpy.data.materials['Material']

```

`fileList` 의 각 .ply 모델들을 불러와 차례대로 처리를 시작한다. 먼저 텍스쳐를 추출할 이미지 `img`를 생성하고 모델에 할당할 매테리얼 정보를 `mat` 에 지정한다. 만약 매테리얼 정보가 없다면 새로 생성한다.

```

    if mat:
        mat.node_tree.nodes.new("ShaderNodeVertexColor")
        base_node = mat.node_tree.nodes[1]
        mat.node_tree.links.new(mat.node_tree.nodes[2].outputs['Color'], mat.node_tree.nodes[1].inputs['Base Color'])

        mat.use_nodes = True
        texture_node =mat.node_tree.nodes.new('ShaderNodeTexImage')
        texture_node.name = 'Bake_node'
        texture_node.select = True
        mat.node_tree.nodes.active = texture_node
        texture_node.image = img #Assign the image to the node
```

매테리얼에서 모델의 표면 색상을 반영하는 정점 색상 노드를 생성하고, 렌더러에 반영되는 베이스 노드에 연결한다. 그 후 모델의 텍스쳐를 Bake하기 위해 이미지 노드를 생성해 준 다음 선택하여 활성화시킨다. 또한 위에서 생성했던 이미지 `img`를 노드에 할당해 준다.

```
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=1.55334)
    bpy.ops.object.editmode_toggle()

    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.bake_type = 'DIFFUSE'
    bpy.context.scene.render.bake.use_pass_direct = False
    bpy.context.scene.render.bake.use_pass_indirect = False
    bpy.context.scene.render.bake.margin = 0

    bpy.context.view_layer.objects.active = bpy.context.active_object
    bpy.ops.object.bake(type='DIFFUSE', save_mode='EXTERNAL')

    img.save_render(file_loc_export+'scene.png')
```

UV 매핑을 위해 불러온 모델의 모든 정점을 선택해 준 다음 `bpy.ops.uv.smart_project` 함수를 시행한다. `angle_limit` 인자는 매핑 시 최대 각도를 설정하며 최대값은 89도 = 1.55334 이다.

이후 Blender의 렌더링 엔진을 Cycles로 변경한 다음 Bake 타입을 Diffuse(확산), 직접광과 간접광 반영 여부를 각각 False로 설정해준다. 이후 오브젝트를 Bake하고 이미지를 저장하면 출력 경로에 모델이 매핑된 `scene.png` 파일이 생성된다.

```
    if mat:
        mat.node_tree.links.new(texture_node.outputs['Color'], base_node.inputs['Base Color'])

    zip_file = zipfile.ZipFile(file_loc_export+os.path.splitext(model)[0]+'.zip', "w")
    zip_file.write(file_loc_export + 'scene.png', basename(file_loc_export + 'scene.png'), compress_type=zipfile.ZIP_DEFLATED)

    bpy.ops.export_scene.gltf(filepath=file_loc_export+'scene.glb', export_materials='EXPORT', export_format='GLB')
    zip_file.write(file_loc_export + 'scene.glb', basename(file_loc_export + 'scene.glb'), compress_type=zipfile.ZIP_DEFLATED)

    for mat in bpy.context.active_object.data.materials:
        for n in mat.node_tree.nodes:
            if n.name == 'Bake_node':
                mat.node_tree.nodes.remove(n)

    bpy.ops.object.delete()
    zip_file.close()
```

그 다음 생성한 텍스쳐 파일을 모델에 반영하기 위해 베이스 노드와 이미지 노드를 연결하고, Zip 파일을 생성해 기존에 만든 `scene.png` 파일과 출력한 모델 파일 `scene.glb`를 함께 압축시킨다. 마지막으로 매테리얼의 텍스쳐 노드와 오브젝트를 지우면 모델 하나에 대한 작업이 종료된다. 이 과정을 모든 모델에 반복한다.
