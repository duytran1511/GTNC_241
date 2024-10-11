import json
from extract import getDir

class TrieNode:
    # constructor
    def __init__(self, string = '', letter = ''):
        self.string = string
        self.letter = letter
        self.children = []
        # end of legit word
        self.terminal = False

    # print current letter
    def printLetter(self):
        print(self.letter)

    # print current string
    def printString(self):
        print(self.string)

    # print string recursively (find children nodes to print)
    def print(self):
        self.printString()
        for child in self.children:
            child.print()

    # print string recursively IF current node is terminal
    def printTerminal(self):
        if self.terminal:
            self.printString()
        for child in self.children:
            child.printTerminal()

# basic insert
def insert_word(root, word):
    current_node = root
    current_str = ''
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
    return current_node.terminal


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
for i in province_data:
    insert_word(root_province, i.replace('\n', ''))
for i in ward_data:
    insert_word(root_ward, i.replace('\n', ''))

print('districts:')
root_district.printTerminal()
print('provices:')
root_province.printTerminal()
print('wards:')
root_ward.printTerminal()

print(search_word(root_ward, 'Xuân Lâm'))