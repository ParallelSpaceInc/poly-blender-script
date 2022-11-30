# poly-blender-script

Blender의 파이썬 라이브러리인 bpy 모듈을 사용하여 다수의 모델 가공을 자동화하는 데 사용되는 스크립트들이다. 사용 방식과 종류에 따라 각 Lab으로 구성되어 있다.

## Lab1. ply to textured glb in Blender

.ply 확장자의 3D 모델들을 텍스쳐가 포함된 .glb 파일로 변환하는 스크립트 BlenderCLI.py 와, 이를 콘솔 창에서 자동적으로 실행할 수 있도록 도와주는 배치/쉘 파일이 존재한다.

## Lab2. Remesh in Blender

Blender의 Decimate 기능을 통해 모델의 Vertex 수를 줄여 용량을 축소화하는 스크립트 RemeshScript.py 와 그것의 파생으로 모델의 크기를 일정 기준으로 조절하는 AutoSize.py, 모델 주변 8방향으로 썸네일을 생성하는 RespectRemesh.py, 그리고 모델의 밝기 단계를 조절하여 썸네일을 생성하는 RemeshWhite.py 스크립트가 존재한다.

## Lab3. File Editing with Python

Lab2의 스크립트로 출력되어 모델+썸네일이 압축된 zip 파일들을 가공하는 스크립트들이 존재한다. zip 파일 내부의 모델을 불러와 정보를 출력하는 ReGlbScript.py, 이름의 불필요한 부분을 제거하는 RenameScript.py, 기존 텍스트 파일에 새 문구를 추가하는 RetextScript.py, 그리고 다른 폴더의 텍스트 파일을 zip 내부에 추가하는 RezipScript.py 가 존재한다.

## Lab4. Excel with Python

기존의 파이썬 스크립트들에 엑셀 관련 라이브러리를 연동한 스크립트들이 존재한다. 가공한 파일들의 통계를 구하는 데 사용되는 ExcelScript.py, 모델의 스케일 크기를 측정하여 기록하는 MeasureSize.py, 기존의 엑셀 파일을 불러와 내용물을 수정하는 ExcelRename.py 스크립트가 존재한다.

## Lab5. Export Model with Shadow

모델에 그림자 텍스쳐를 붙여 같이 출력하기 위해 작성된 스크립트 AutoShadow.py 가 존재한다. 

## Hanpac

각 파이썬 스크립트들의 주요 기능들을 모듈화하여 정리한 패키지 파일이다. 해당 패키지의 자세한 사용법은 [이 문서](https://parallelspaces.atlassian.net/l/cp/G0R29FMw) 를 참조하면 좋다.