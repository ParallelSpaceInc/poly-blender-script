import os
import bpy
import zipfile

from os.path import basename
from bpy import context
from PIL import Image

file_loc_export = 'C:\\Users\\USER\\Downloads\\Remesh\\Old\\RemeshedGlb\\'
file_loc_import = 'C:\\Users\\USER\\Downloads\\Remesh\\Old\\RemeshedObj\\'
fileEx = r'.gltf'
fileZipEx = r'.zip'
fileList = [file for file in os.listdir(file_loc_import) if file.endswith(fileZipEx)]


for zipFile in fileList:
    archive = zipfile.ZipFile(file_loc_import+zipFile, 'r')
    sceneData = archive.read('scene.gltf')
    print(sceneData)
