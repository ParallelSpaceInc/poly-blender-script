# File Editing with Python
****

Lab2의 RemeshScript.py 로 출력된 zip 파일의 데이터들을 파이썬 스크립트를 통해 한꺼번에 수정, 갱신할 수 있다.

****

## 1. ReGlbScript.py

ReGlbScript.py 는 Remesh 스크립트로 내보내진 zip 파일들 내부의 `scene.gltf` 파일의 정보를 읽어온다. 

```
import os
import zipfile

file_loc_import = 'C:\\Users\\USER\\Downloads\\Remesh\\Old\\RemeshedObj\\'
fileEx = r'.gltf'
fileZipEx = r'.zip'
fileList = [file for file in os.listdir(file_loc_import) if file.endswith(fileZipEx)]

for zipFile in fileList:
    archive = zipfile.ZipFile(file_loc_import+zipFile, 'r')
    sceneData = archive.read('scene.gltf')
    print(sceneData)
```

`file_loc_import` 는 .zip 파일을 불러올 경로다. `fileList` 를 사용하여 해당 폴더에 존재하는 zip 파일을 불러와 내부의 `scene.gltf` 를 불러오고 출력한다.

***

## 2. RenameScript.py

RenameScript.py 는 파일의 제목 중 불필요한 텍스트를 `replace` 메소드를 사용해 지우는 스크립트이다. 파일을 불러오는 부분은 ReGlbScript.py 와 동일하며, `fileEx` 변수를 수정함으로써 불러올 파일의 확장자를 결정할 수 있다.

```
for model in fileList:
    tmpstr = model
    file_oldname = os.path.join(file_loc, tmpstr)

    tmpstr_new = tmpstr.replace('_서비스_3D모델링', '').replace('_전체','')
    file_newname = os.path.join(file_loc, tmpstr_new)

    os.rename(file_oldname, file_newname)
```

본 스크립트는 파일 제목의 '_서비스_3D모델링' 이나 '_전체' 등 실제 모델을 서비스할 때 불필요한 부분을 제거하였다.

***

## 3. RetextScript.py

RetextScript.py 는 기존의 txt 파일에 새 문구를 추가하는 파일이다.

```
for textfile in fileList:
    with open(file_loc+textfile, "a", encoding='utf-8') as f:
        f.write("\n\n\n• 자료 출처 : 문화재청")
        f.write("\n• 본 저작물은 문화재청에서 작성하여 공공누리 제0유형으로 개방한 3D 문화유산 데이터를 이용하였으며, 해당 저작물은 문화재청, 공공데이터포털에서 무료로 다운받을 수 있습니다.")
        f.close
```

`open` 함수로 경로의 문화재 설명 txt 파일들을 차례대로 연 후, 문화재 저작권 관련 문구를 추가하였다.

***

## 4. RezipScript.py

RezipScript.py 는 다른 폴더에 존재하는 문화재 설명 파일을 읽어와 zip 파일 내부에 추가하는 스크립트이다. `os` 모듈 이외에도 `zipfile` 과 `shutil` 모듈을 임포트해야한다.

```
for zips in fileList:
    fileName = os.path.splitext(zips)[0]
    zip_file = zipfile.ZipFile(file_loc_zip+fileName+'.zip', "a")

    if(os.path.isfile(file_loc_txt+fileName+'.txt')):
        shutil.copy(file_loc_txt+fileName+'.txt',file_loc_txt+'description.txt')
        zip_file.write(file_loc_txt+'description.txt', basename(file_loc_txt+'description.txt'), compress_type=zipfile.ZIP_DEFLATED)

    zip_file.close()
```

`shutil.copy` 함수로 문화재 설명 텍스트 파일들이 저장된 폴더에서 해당 문화재를 매칭해 설명 파일을 불러온 다음, zip 파일 내부에 재압축하고 저장한다. `file_loc_zip` 에는 zip 파일들이, `file_loc_txt` 는 문화재 설명 파일들이 저장된 경로를 미리 지정해둔다.