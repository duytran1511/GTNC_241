import os
import re
import unicodedata

def getDir(file_name):
    full_path = os.path.realpath(__file__)
    path, filename = os.path.split(full_path)
    dir = os.path.join(path, file_name)
    print(dir)
    return dir

def sanitize(text: str):
    return remove_stopwords_from_address(text)

# List of stopwords like Phường, Xã, Huyện, Tỉnh, etc.

# Note 1: The length of each word must be ordered from longest to shortest
# Note 2: We will not take 1-letter words into account
stopwords = ['thành phố', 'thị trấn', 'phường', 'huyện', 'tỉnh', 'quận', 't.p', 'Tp.', 'tt.', 'tx.', 't.x', 'xã', 'h.', 'x.', 't.', 'q.', 'tx', 'x2']

# Function to remove stopwords from the address
def remove_stopwords_from_address(address: str):
    chunks = address.split(",")
    clear_chunks = []

    for chunk in chunks:
        words:str = chunk.split(" ")
        stopword_clear_words = []
        for word in words:
            for stopword in stopwords:
                if stopword is word:
                    break
                elif word.lower().startswith(stopword):
                    word = word[len(stopword):]
                elif word.lower().endswith(stopword):
                    word = word[:len(word) - len(stopword)]
            striped_word = re.sub(r'\W+', '', word.strip())
            if len(striped_word) > 1:
                stopword_clear_words.append(striped_word)
        clear_chunks.append("_".join(stopword_clear_words))
        # TODO: Remove First Letter of Stopword (X, T, H) that follows with a Conso
    return clear_chunks



# text_file = 'text_test.txt'
text_file = 'text.txt'
text_data = open(getDir(text_file), encoding='utf8')
results = []
for row in text_data:
    print("*" + row + " -> " + str(sanitize(row)))