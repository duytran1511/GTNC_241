import json
import os

def getDir(file_name):
    if file_name == 'data/public.json':
        return file_name  # public.json is expected in the root folder
    
    # Get the absolute path of the current script
    full_path = os.path.realpath(__file__)
    path, _ = os.path.split(full_path)
    
    # Join path with the 'data' folder for all other files
    dir = os.path.join(path, 'data', file_name)
    return dir


def saveToTxt(data, name):
    dir = getDir(name)
    # Create the data folder if it doesn't exist
    os.makedirs(os.path.dirname(dir), exist_ok=True)
    
    with open(dir, 'w', encoding='utf8') as f:
        for line in data:
            f.write(line)
    return


def extractData(data):
    text = set()
    district = set()
    ward = set()
    province = set()
    
    for i in data:
        text.add(i['text'] + '\n')
        district.add(i['result']['district'] + '\n')
        ward.add(i['result']['ward'] + '\n')
        province.add(i['result']['province'] + '\n')
    
    # Sort and save each set to the "data" folder
    saveToTxt(sorted(text), 'text.txt')
    saveToTxt(sorted(district), 'district.txt')
    saveToTxt(sorted(ward), 'ward.txt')
    saveToTxt(sorted(province), 'province.txt')

# Load the JSON data from 'public.json' in the root directory
json_path = 'data/public.json'  # Adjust path if needed
with open(json_path, encoding='utf8') as json_file:
    data = json.load(json_file)

# Extract and save data into text files in the "data" folder
extractData(data)
print("Data extraction complete.")
