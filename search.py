import json
from extract import getDir

fine_name = 'district.txt'
dir = getDir(fine_name)
data = open(dir, encoding='utf8')

for i in data:
    print(i)
    pass

