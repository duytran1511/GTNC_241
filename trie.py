class TrieNode:
    count = 0
    indent = '  '
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
            log += child.log(line_break + TrieNode.indent)
        return log

    # log string recursively IF current node is terminal
    def logTerminal(self, line_break = '\n'):
        log = ''
        if self.terminal:
            log += self.logString(line_break)
        for child in self.children:
            log += child.logTerminal(line_break + TrieNode.indent)
        return log
            
    # log string recursively IF current node is terminal
    def logFragment(self, line_break = '\n'):
        log = ''
        if self.fragment:
            log += self.logString(line_break)
        for child in self.children:
            log += child.logFragment(line_break + TrieNode.indent)
        return log


class Trie:
    # constructor
    def __init__(self):
        self.root = TrieNode()
        self.max_length = 0
        
    # log number of nodes
    def printCount(self):
        return self.root.printCount()
    
    # log current letter
    def logLetter(self, line_break = ''):
        return self.root.logLetter(line_break = line_break)

    # log current string
    def logString(self, line_break = ''):
        return self.root.logString(line_break = line_break)

    # log string recursively (find children nodes to log)
    def log(self, line_break = '\n',):
        return self.root.log(line_break = line_break)

    # log string recursively IF current node is terminal
    def logTerminal(self, line_break = '\n'):
        return self.root.logTerminal(line_break = line_break)
            
    # log string recursively IF current node is terminal
    def logFragment(self, line_break = '\n'):
        return self.root.logFragment(line_break = line_break)

    # basic insert
    def insert_word(self, word, current_str = '', type = 'terminal'):
        self.max_length = max(self.max_length, len(word))
        current_node = self.root
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

    # basic search (Needs to enhance for auto correct)
    def search_word(self, word):
        current_node = self.root
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
    def insert_word_frag(self, word):
        #print('============================')
        # insert the full word with type terminal
        self.insert_word(word)
        # insert the fragments
        for i in range(1, len(word)):
            prefix = word[:i]
            frag = word[i:]
            #print(prefix)
            #print(frag)
            self.insert_word(frag, prefix, type = 'fragment')
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

    def search_word_error(self, word, node=None):
        error_lim = 0.2 * len(word)
        error_num = 0
        match_num = 0
        if not node:
            current_node = self.root
        else:
            current_node = node
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
                    result = self.search_word_error(word[letter:], child)
                    if result != None:
                        error_num += result[-2]
                        match_num += result[-1]
                        return result
                pass
        return [current_node.string, current_node.terminal, current_node.fragment, error_num, match_num]