# Excel with Python
****

Lab2에서 가공한 모델들의 정보를 파이썬의 Excel 관련 라이브러리를 통해 자동적으로 문서화할 수 있다.

***

## 1. ExcelScript.py

ExcelScript.py 는 가공한 모델 파일들의 전체적 통계를 구하기 위해 작성된 스크립트이다. 사용하기 위해선 먼저 `openpyxl` 모듈을 설치해야 한다. 

```
import os
import zipfile

from genericpath import isfile
from openpyxl import Workbook
from openpyxl.styles import Alignment

wb = Workbook()

ws = wb.create_sheet('Models')
ws = wb.active

align = Alignment(horizontal='center', vertical='center')
```

먼저 필요한 모듈들을 임포트하고 `Workbook` 클래스의 인스턴스를 `wb`라는 이름으로 생성한다. 또한 해당 `wb` 에서 Models 라는 이름으로 워크시트를 하나 생성해준다.

`align`은 엑셀 시트의 정렬 인자다. 읽어들인 데이터를 엑셀에 기입할 때 셀 내부 내용이 가로 세로 각각 중앙으로 정렬되도록 맞추기 위해 필요하다.

```
path_origin = "C:/Users/USER/Downloads/Remesh/Old/Origins/"
path_s100_r10_gltf = "C:/Users/USER/Downloads/Remesh/models_gltf_s100_r10_0902/"
path_s100_r10_glb = "C:/Users/USER/Downloads/Remesh/models_glb_s100_r10_0906/"
path_s500_r10_glb = "C:/Users/USER/Downloads/Remesh/models_glb_s500_r10_0919/"

size_origin = []
size_s100_r10_gltf = []
size_s100_r10_glb = []
size_s500_r10_glb = []
```

비교할 데이터가 있는 모델들의 경로를 각각 지정한다. 이 스크립트에서는 원본 모델, 1/100 크기와 1/10 용량으로 gltf와 glb로 변환한 모델, 그리고 1/500 크기로 변환한 모델들이 있는 폴더를 지정하였다. 또한 각 경로마다 읽어들인 데이터를 저장할 리스트가 필요하다.

```
ws.append(["순번", "이름", "원본 PLY 용량(KB)", "s100_r10_gltf(KB)", "s100_r10_glb(KB)", "s500_r10_glb(KB)"])
ws.column_dimensions['B'].width = 55
ws.column_dimensions['C'].width = 18
ws.column_dimensions['D'].width = 18
ws.column_dimensions['E'].width = 18
ws.column_dimensions['F'].width = 18

file_list = os.listdir(path_s500_r10_glb)
```

엑셀 파일의 맨 위 첫줄에 표의 구분 항목을 차례대로 입력한다. 그 다음 2번째 열부터 6번째 열 까지의 가로 너비를 읽기 편하도록 적절히 맞춘다. 그리고 `file_list` 에 엑셀에 기입할 파일 이름들을 할당한다.

```
for model in file_list:
    modelpath = path_origin+os.path.splitext(model)[0]+'.ply'
    if os.path.isfile(modelpath):
        sizekb = os.path.getsize(modelpath) // 1024
        size_origin.append(sizekb)

    modelpath = path_s100_r10_gltf+model
    if os.path.isfile(modelpath):
        ziptmp = zipfile.ZipFile(modelpath)
        sizekb = ziptmp.getinfo(ziptmp.namelist()[1]).file_size // 1024
        size_s100_r10_gltf.append(sizekb)

    modelpath = path_s100_r10_glb+model
    if os.path.isfile(modelpath):
        ziptmp = zipfile.ZipFile(modelpath)
        sizekb = ziptmp.getinfo(ziptmp.namelist()[1]).file_size // 1024
        size_s100_r10_glb.append(sizekb)

    modelpath = path_s500_r10_glb+model
    if os.path.isfile(modelpath):
        ziptmp = zipfile.ZipFile(modelpath)
        sizekb = ziptmp.getinfo(ziptmp.namelist()[1]).file_size // 1024
        size_s500_r10_glb.append(sizekb)
```

`file_list` 를 차례대로 읽어와 각 path에 있는 모델들을 탐색한다. 해당 모델이 존재할 경우 사이즈를 읽어와 각 리스트에 추가한다. 이 때 읽어오는 사이즈는 바이트 단위이기 때문에 킬로바이트(KB)로 변환하기 위해서 1024 만큼 나누어 주어야 한다.

```
for x in range(2, (len(file_list)+1)):
    ws.cell(x, 2, os.path.splitext(file_list[x-2])[0])
    ws.cell(x, 3, size_origin[x-2])
    ws.cell(x, 4, size_s100_r10_gltf[x-2])
    ws.cell(x, 5, size_s100_r10_glb[x-2])
    ws.cell(x, 6, size_s500_r10_glb[x-2])

for row in ws.rows:
    for col in row[0:]:
        col.alignment = align

wb.save("C:/Users/USER/Downloads/Remesh/Excel/ModelTable.xlsx")
```

모든 모델에 대한 리스트 삽입이 완료되었으면 이제 시트에 데이터를 기입한다. 1번째 행은 구분 항목이고 1번째 열은 파일의 인덱스이므로, 2번째 행부터 차례대로 이름, 원본 사이즈, 1/100 gltf, 1/100 glb, 1/500 glb 데이터를 차례대로 기입한다.

마지막으로 모든 행렬을 미리 정해둔 인자로 정렬해준 다음 원하는 경로에 저장하면, 해당 폴더에 데이터가 기입된 엑셀 파일이 생성된다.

***

## 2. MeasureSize.py

MeasureSize.py 는 모델을 둘러싼 Bounding Box의 크기를 재어 엑셀 파일에 저장하는 함수이다. bpy 모듈이 필요하기 때문에 Blender 프로그램을 경유하여 사용해야 한다.

```
import os
import bpy

from genericpath import isfile
from openpyxl import Workbook
from openpyxl.styles import Alignment
from bpy import context

wb = Workbook()

ws = wb.create_sheet('Models')
ws = wb.active

align = Alignment(horizontal='center', vertical='center')

path_origin = "C:/Users/USER/Downloads/Remesh/Old/Origins/"

sizeX = []
sizeY = []
sizeZ = []

ws.append(["순번", "이름","sizeX", "sizeY", "sizeZ"])
ws.column_dimensions['B'].width = 55
ws.column_dimensions['C'].width = 10
ws.column_dimensions['D'].width = 10
ws.column_dimensions['E'].width = 10

file_list = os.listdir(path_origin)
```

먼저 관련 모듈들을 임포트한 뒤 ExcelScript.py 처럼 워크북과 워크시트를 생성한다. 그리고 크기를 잴 파일 경로를 설정한 뒤 각 모델의 x, y, z 너비를 저장할 리스트 3개를 생성한다. 엑셀 시트 맨 위에는 구분 항목을 정해주고 지정된 경로에서 모델 목록을 불러와 `file_list` 에 저장한다.

```
for model in file_list:
    modelpath = path_origin+os.path.splitext(model)[0]+'.ply'
    if os.path.isfile(modelpath):
        imported_object = bpy.ops.import_mesh.ply(filepath=modelpath)
        sizeX.append(bpy.context.object.dimensions.x)
        sizeY.append(bpy.context.object.dimensions.y)
        sizeZ.append(bpy.context.object.dimensions.z)
        bpy.ops.object.delete()
```

이후 Blender 상에서 해당 경로의 모델들을 차례대로 불러와 x, y, z 너비를 측정하여 시트에 추가한다. 모델을 지우고 새로 불러오는 작업을 계속 반복한다.

```
for x in range(2, (len(file_list)+1)):
    ws.cell(x, 2, os.path.splitext(file_list[x-2])[0])
    ws.cell(x, 3, sizeX[x-2])
    ws.cell(x, 4, sizeY[x-2])
    ws.cell(x, 5, sizeZ[x-2])
    
for row in ws.rows:
    for col in row[0:]:
        col.alignment = align
        
wb.save("C:/Users/USER/Downloads/Remesh/Excel/ModelSize.xlsx")
```

마지막으로 엑셀 파일에 모델 이름과 측정한 값을 기입한 뒤, 정렬하고 지정된 경로에 저장하면 엑셀 파일이 생성되고 작업이 완료된다.

***

## 3. ExcelRename.py

ExcelRename.py 는 기존의 엑셀 파일을 불러와 내용물을 수정한다. 여기서는 기존에 기입되어 있던 모델의 이름에 필요없는 접두사를 제거하는 과정을 진행하였다. 

```
import os
import zipfile
import openpyxl

from genericpath import isfile
from openpyxl import Workbook
from openpyxl.styles import Alignment

file_loc_zip = "C:\\Users\\USER\\Downloads\\Remesh\\Renames\\"
file_loc_excel = 'C:\\Users\\USER\\Downloads\\Remesh\\Excel\\'

wb = openpyxl.load_workbook(file_loc_excel + "ReadTable.xlsx")

ws = wb.create_sheet('Models')
ws = wb.active

align = Alignment(horizontal='center', vertical='center')

size_model = []
name_model = []
```

먼저 필요한 모듈들을 임포트하고 워크북을 설정한다. 이때 지정된 `file_loc_excel` 경로에 존재하는 엑셀 파일을 불러온다. 그러면 해당 워크북에 존재하는 시트를 접근할 수 있다. 이후 모델의 크기값과 이름이 각각 저장될 리스트를 생성해둔다.

```
file_list = os.listdir(file_loc_zip)

for model in file_list:
    name_model.append(os.path.splitext(model)[0].split('_', 1)[1])
    modelpath = file_loc_zip+model
    if os.path.isfile(modelpath):
        ziptmp = zipfile.ZipFile(modelpath)
        sizekb = ziptmp.getinfo(ziptmp.namelist()[1]).file_size // 1024
        size_model.append(sizekb)
```

그 다음 `file_list` 에 파일 목록을 할당하고 경로에 있는 모델의 이름과 크기값을 차례대로 불러와 리스트에 기입한다.

```
for x in range(2, (len(file_list)+2)):
    ws.cell(x, 3, name_model[x-2])
    ws.cell(x, 9, size_model[x-2])

for row in ws.rows:
    for col in row[0:]:
        col.alignment = align

wb.save("C:/Users/USER/Downloads/Remesh/Excel/ModelTable3.xlsx")
```

마지막으로 원래 엑셀 파일의 이름과 크기가 기입되어 있던 부분에 새로 받은 리스트의 데이터로 덮어씌운 후, 정렬한 뒤 지정한 경로에 저장하면 작업이 종료된다.