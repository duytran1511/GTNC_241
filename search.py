import json
from extract import getDir, saveToTxt

indent = '  '

class TrieNode:
    count = 0
    # constructor
    def __init__(self, string = '', letter = ''):
        self.string = string
        self.letter = letter
        self.children = []
        # end of legit word
        self.terminal = False
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
def insert_word(root, word, current_str = ''):
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
    current_node.terminal = True
    #print(current_str)
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
root_ward.printCount()

# logs to check trie structures
saveToTxt(root_district.log(), 'root_district.txt')
saveToTxt(root_province.log(), 'root_province.txt')
saveToTxt(root_ward.log(), 'root_ward.txt')

print(search_word(root_ward, 'Xuân Lâm'))
print(search_word(root_ward, 'Xn Lâm'))
#root_district.printCount()