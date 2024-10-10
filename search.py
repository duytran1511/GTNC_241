# Python program to convert JSON to Python
import json
import os

file_name = 'public.json'
full_path = os.path.realpath(__file__)
path, filename = os.path.split(full_path)
dir = os.path.join(path, file_name)
print(dir)

json_file = open(dir, encoding="utf8")
data = json.load(json_file)
for i in data:
    print(i)