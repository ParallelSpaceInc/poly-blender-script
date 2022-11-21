import os


file_loc = 'C:\\Users\\USER\\Downloads\\Remesh\\Big\\'
fileEx = r'.txt'

fileList = [file for file in os.listdir(file_loc) if file.endswith(fileEx)]

for textfile in fileList:
    with open(file_loc+textfile, "a", encoding='utf-8') as f:
        f.write("\n\n\n• 자료 출처 : 문화재청")
        f.write("\n• 본 저작물은 문화재청에서 작성하여 공공누리 제0유형으로 개방한 3D 문화유산 데이터를 이용하였으며, 해당 저작물은 문화재청, 공공데이터포털에서 무료로 다운받을 수 있습니다.")
        f.close