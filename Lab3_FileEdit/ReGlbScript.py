import os
import zipfile

file_loc_import = 'C:\\Users\\USER\\Downloads\\Remesh\\Old\\RemeshedObj\\'
fileZipEx = r'.zip'
fileList = [file for file in os.listdir(file_loc_import) if file.endswith(fileZipEx)]

for zipFile in fileList:
    archive = zipfile.ZipFile(file_loc_import+zipFile, 'r')
    sceneData = archive.read('scene.gltf')
    print(sceneData)
