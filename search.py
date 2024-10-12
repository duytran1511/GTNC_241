import json
from extract import getDir, saveToTxt

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
    current_node = root
    # iter through input word
    for letter in range(len(word)):
        found = False
        # iter though child node
        for child in current_node.children:
            #print(child.letter)
            #print(child.terminal)
            if word[letter] == child.letter:
                # switch node
                current_node = child
                found = True
                break
        if (not found):
            error_num += 1
            for child in current_node.children:        
                return search_word_error(child, word[letter:])
            pass
    return current_node.string, current_node.terminal, current_node.fragment

def search_address(district, province, ward, address, time_limit):
    for i in range(len(address)):
        
        pass
    return

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

#print('districts:')
#print(root_district.log())
saveToTxt(root_district.log(), 'root_district.txt')
#print('provices:')
#root_province.printTerminal()
#print('wards:')
#root_ward.printTerminal()
#
#root_district.printFragment()
#print(search_word(root_ward, 'Xuân Lâm'))
print(search_word_error(root_ward, 'Xân Lâm'))
#root_district.printCount()