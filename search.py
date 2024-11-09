import json
from extract import getDir, saveToTxt
from trie import TrieNode, Trie
import time
from tabulate import tabulate
import json


def getBest(preds):
    result = None
    for pred in preds:
        if result == None:
            result = pred
            continue
        if result[0] == pred[0]:
            result[4] += pred[4]
        elif (result[4] - result[3]) < (pred[4] - pred[3]):
            result = pred
    return result

def search_address(ward, province, district, address, time_limit = 0.099999000):
    check_time = 0
    start_time = time.time()
    result = []
    result_ward = []
    result_province = []
    result_district = []
    start_idx = 0
    for i in range(0, len(address)):
        slice1 = address[i:ward.max_length]
        slice2 = address[i:province.max_length]
        slice3 = address[i:district.max_length]
        result_ward += [ward.search_word_error(slice1)]
        result_province += [province.search_word_error(slice2)]
        result_district += [district.search_word_error(slice3)]
        # this result is garbage since all searches are called from beginning to end (illogical)
        # we only do this to test the speed of the search algorithm
        # since the real search_address won't call this many search functions
        check_time = time.time()
        #print(slice)
        #print(check_time)
        timer = check_time - start_time
        if time_limit < timer:
            result = [getBest(result_district), getBest(result_province), getBest(result_ward)]
            print('timeout on input: ', timer)
            print(address)
            return address, result
    result = [getBest(result_district), getBest(result_province), getBest(result_ward)]
    final_time = check_time - start_time
    #print(f'runtime: {final_time} s')
    return address, result

district_file = 'district.txt'
district_data = open(getDir(district_file), encoding='utf8')

province_file = 'province.txt'
province_data = open(getDir(province_file), encoding='utf8')

ward_file = 'ward.txt'
ward_data = open(getDir(ward_file), encoding='utf8')

root_district = Trie()
root_province = Trie()
root_ward = Trie()

for i in district_data:
    root_district.insert_word(i.replace('\n', '')) # remove linebreak from input file's line
root_district.printCount()

for i in province_data:
    root_province.insert_word(i.replace('\n', ''))
root_province.printCount()

for i in ward_data:
    root_ward.insert_word(i.replace('\n', ''))

#==================================================
# logging
saveToTxt(root_district.log(), 'root_district.txt')
saveToTxt(root_province.log(), 'root_province.txt')
saveToTxt(root_ward.log(), 'root_ward.txt')

print(root_ward.search_word_error('Xuân Lâm'))
print(root_ward.search_word_error('Xn Lâm'))
#root_district.printCount()

#==================================================
# get results from search address (sorted by input)
text_file = 'text.txt'
text_data = open(getDir(text_file), encoding='utf8')
results = []
for i in text_data:
    results.append(search_address(root_ward, root_province, root_district, i))
#print(results)

#==================================================
# get output data to compare (sorted by input)
dir = getDir('data/public.json')
json_file = open(dir, encoding='utf8')
data = json.load(json_file)
for i in data:
    i = json.dumps(i, sort_keys=True)
sorted_data = sorted(data, key=lambda x: x['text'])
#data = json.dumps(data, sort_keys=True)
#print(sorted_data)

#==================================================
# Initialize variables to track results
passed = 0
total = len(results)
output_table = []

# Process each result and store formatted data in output_table
for i in range(total):
    address = results[i][0].strip()
    actual = results[i][1]
    expected = sorted_data[i]['result']
    
    # Check each component for match
    ward_match = actual[2][0] == expected['ward']
    province_match = actual[1][0] == expected['province']
    district_match = actual[0][0] == expected['district']
    
    # Determine pass/fail status
    if ward_match and province_match and district_match:
        status = "Pass"
        passed += 1
    else:
        status = "Fail"
    
    # Format expected and actual results as strings
    expected_result_str = json.dumps(expected, ensure_ascii=False)
    actual_result_str = {
        'district': actual[0][0] if actual[0] else "None",
        'province': actual[1][0] if actual[1] else "None",
        'ward': actual[2][0] if actual[2] else "None"
    }
    actual_result_str = json.dumps(actual_result_str, ensure_ascii=False)
    runtime = results[i][2] if len(results[i]) > 2 else "N/A"
    
    # Append row data to output_table
    output_table.append([
        address,
        expected_result_str,
        actual_result_str,
        status,
        f"{runtime:.4f}" if isinstance(runtime, float) else "N/A"
    ])

# Save the table to output.txt
headers = ["Address", "Expected Result", "Actual Result", "Status", "Runtime (s)"]
output_text = tabulate(output_table, headers=headers, tablefmt="grid")

# Write the table and summary to output.txt
with open("output.txt", "w", encoding="utf-8") as f:
    f.write(output_text)
    f.write("\n\nSummary:\n")
    f.write(f"Total Cases: {total}\n")
    f.write(f"Passed Cases: {passed}\n")
    f.write(f"Failed Cases: {total - passed}\n")
    f.write(f"Pass Rate: {passed / total * 100:.2f}%\n")

print("Results have been saved to output.txt")

