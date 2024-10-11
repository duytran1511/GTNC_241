# Python program to convert JSON to Python
import json
import os

def getDir(file_name):
    full_path = os.path.realpath(__file__)
    path, filename = os.path.split(full_path)
    dir = os.path.join(path, file_name)
    print(dir)
    return dir

def saveToTxt(data, name):
    dir = getDir(name)
    with open(dir, 'w', encoding='utf8') as f:
        for line in data:
            #print(line)
            f.write("%s\n" % line)
    return
    
def extractData(data):
    text = set([])
    district = set([])
    ward = set([])
    province = set([])
    for i in data:
        text.add(i['text'])
        district.add(i['result']['district'])
        ward.add(i['result']['ward'])
        province.add(i['result']['province'])
    
    saveToTxt(text, 'text.txt')
    saveToTxt(district, 'district.txt')
    saveToTxt(ward, 'ward.txt')
    saveToTxt(province, 'province.txt')
    return


dir = getDir('public.json')
json_file = open(dir, encoding='utf8')
data = json.load(json_file)
extractData(data)
