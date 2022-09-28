import os


file_loc = 'C:\\Users\\82109\\Downloads\\Models67\\'
fileEx = r'.ply'

fileList = [file for file in os.listdir(file_loc) if file.endswith(fileEx)]

for model in fileList:
    tmpstr = model
    file_oldname = os.path.join(file_loc, tmpstr)

    tmpstr_new = tmpstr.replace('_서비스_3D모델링', '').replace('_전체','')
    file_newname = os.path.join(file_loc, tmpstr_new)

    os.rename(file_oldname, file_newname)