import json
from extract import getDir, saveToTxt
import time  

indent = '  '

class TrieNode:
    count = 0
    count = 0
    # constructor
    def __init__(self, string = '', letter = ''):
        self.string = string
        self.letter = letter
        self.children = []
        # end of legit word
        self.terminal = False
        self.fragment = False
        # increase static counter
        TrieNode.count += 1
        
    # log number of nodes
    def printCount(self):
        print(TrieNode.count)
    
    # log current letter
    def logLetter(self, line_break = ''):
        #print(line_break + self.letter)
        return line_break + self.letter

    # log current string
    def logString(self, line_break = ''):
        #print(line_break + self.string)
        return line_break + self.string

    # log string recursively (find children nodes to log)
    def log(self, line_break = '\n',):
        log = ''
        log += self.logString(line_break)
        for child in self.children:
            log += child.log(line_break + indent)
        return log

    # log string recursively IF current node is terminal
    def logTerminal(self, line_break = '\n'):
        log = ''
        if self.terminal:
            log += self.logString(line_break)
        for child in self.children:
            log += child.logTerminal(line_break + indent)
        return log
            
    # log string recursively IF current node is terminal
    def logFragment(self, line_break = '\n'):
        log = ''
        if self.fragment:
            log += self.logString(line_break)
        for child in self.children:
            log += child.logFragment(line_break + indent)
        return log

# basic insert
def insert_word(root, word, current_str = '', type = 'terminal'):
    current_node = root
    # iter through input word
    for letter in word:
        current_str += letter
        found = False
        # iter though child node
        for child in current_node.children:
            if letter == child.letter:
                # switch node
                current_node = child
                found = True
                break
        if (not found):
            current_node.children.append(TrieNode(current_str, letter))
            current_node = current_node.children[-1]
    if type == 'terminal':
        current_node.terminal = True
    elif type == 'fragment':
        current_node.fragment = True
    #print(current_str)
    return
    return

# basic search (Needs to enhance for auto correct)
def search_word(root, word):
    current_node = root
    # iter through input word
    for letter in word:
        found = False
        # iter though child node
        for child in current_node.children:
            #print(child.letter)
            #print(child.terminal)
            if letter == child.letter:
                # switch node
                current_node = child
                found = True
                break
        if (not found):
            pass
    return current_node.string, current_node.terminal

# insert both the word and the ending fragments for each word into trie 
def insert_word_frag(root, word):
    #print('============================')
    # insert the full word with type terminal
    insert_word(root, word)
    # insert the fragments
    for i in range(1, len(word)):
        prefix = word[:i]
        frag = word[i:]
        #print(prefix)
        #print(frag)
        insert_word(root, frag, prefix, type = 'fragment')
    return

# def search_children_closest(letter, current_node):
#     found = False
#     # iter though child node
#     for child in current_node.children:
#         #print(child.letter)
#         #print(child.terminal)
#         if letter == child.letter:
#             # switch node
#             current_node = child
#             found = True
#             break
#     if (not found):
#         for child in current_node.children:
#             current_node = search_children_closest(letter, child)
#         #error_num += 1
#         pass
#     return current_node

def search_word_error(root, word):
    error_lim = 0.2 * len(word)
    error_num = 0
    match_num = 0
    current_node = root
    # iter through input word
    for letter in range(len(word)):
        found = False
        # iter though child node
        for child in current_node.children:
            #print(child.letter)
            #print(child.terminal)
            if word[letter] == child.letter:
                match_num += 1
                # switch node
                current_node = child
                found = True
                break
        if (not found):
            error_num += 1
            for child in current_node.children:        
                result = search_word_error(child, word[letter:])
                if result != None:
                    error_num += result[-2]
                    match_num += result[-1]
                    return result
            pass
    return current_node.string, current_node.terminal, current_node.fragment, error_num, match_num

def search_address(ward, province, district, address, time_limit = 0.099999000):
    check_time = 0
    start_time = time.time()
    result = []
    start_idx = 0
    for i in range(0, len(address)):
        slice = address[:i]
        result_ward = search_word_error(ward, slice)
        result_province = search_word_error(province, slice)
        result_district = search_word_error(district, slice)
        # this result is garbage since all searches are called from beginning to end (illogical)
        # we only do this to test the speed of the search algorithm
        # since the real search_address won't call this many search functions
        result = [result_district, result_province, result_ward]
        check_time = time.time()
        #print(slice)
        #print(check_time)
        if time_limit < (check_time - start_time):
            print('timeout on input:')
            print(address)
            return address, result
    final_time = check_time - start_time
    print(f'runtime: {final_time} s')
    return address, result

district_file = 'district.txt'
district_data = open(getDir(district_file), encoding='utf8')

province_file = 'province.txt'
province_data = open(getDir(province_file), encoding='utf8')

ward_file = 'ward.txt'
ward_data = open(getDir(ward_file), encoding='utf8')

root_district = TrieNode()
root_province = TrieNode()
root_ward = TrieNode()

for i in district_data:
    insert_word(root_district, i.replace('\n', '')) # remove linebreak from input file's line
root_district.printCount()

for i in province_data:
    insert_word(root_province, i.replace('\n', ''))
root_province.printCount()

for i in ward_data:
    insert_word(root_ward, i.replace('\n', ''))

#==================================================
# logging
saveToTxt(root_district.log(), 'root_district.txt')
saveToTxt(root_province.log(), 'root_province.txt')
saveToTxt(root_ward.log(), 'root_ward.txt')

print(search_word_error(root_ward, 'Xuân Lâm'))
print(search_word_error(root_ward, 'Xn Lâm'))
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
dir = getDir('public.json')
json_file = open(dir, encoding='utf8')
data = json.load(json_file)
for i in data:
    i = json.dumps(i, sort_keys=True)
sorted_data = sorted(data, key=lambda x: x['text'])
#data = json.dumps(data, sort_keys=True)
#print(sorted_data)

#==================================================
# print comparison result
passed = 0
for i in range(len(results)):
    if results[i][1][0][0] == sorted_data[i]['result']['district'] and results[i][1][1][0] == sorted_data[i]['result']['province'] and results[i][1][2][0] == sorted_data[i]['result']['ward']:
        print(results[i][1])
        print(json.dumps(sorted_data[i]['result'], sort_keys=True, ensure_ascii=False))
        passed += 1
        pass
print(passed / len(results))

#==================================================
# performance test: random string with fixed length
import string
import random
length = 300
rand_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
print(rand_str)
search_address(root_ward, root_province, root_district, rand_str)