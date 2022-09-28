import os
import zipfile
import shutil

from os.path import basename


file_loc_zip = 'C:\\Users\\USER\\Downloads\\Remesh\\Obaek\\'
file_loc_txt = 'C:\\Users\\USER\\Downloads\\Remesh\\Old\\Texts\\'
fileEx = r'.zip'

fileList = [file for file in os.listdir(file_loc_zip) if file.endswith(fileEx)]

for zips in fileList:
    fileName = os.path.splitext(zips)[0]
    zip_file = zipfile.ZipFile(file_loc_zip+fileName+'.zip', "a")

    if(os.path.isfile(file_loc_txt+fileName+'.txt')):
        shutil.copy(file_loc_txt+fileName+'.txt',file_loc_txt+'description.txt')
        zip_file.write(file_loc_txt+'description.txt', basename(file_loc_txt+'description.txt'), compress_type=zipfile.ZIP_DEFLATED)

    zip_file.close()