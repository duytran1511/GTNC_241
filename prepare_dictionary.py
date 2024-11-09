import os

# Define file paths
district_file = 'data/district.txt'
province_file = 'data/province.txt'
ward_file = 'data/ward.txt'
output_file = 'data/vietnamese_dictionary.txt'

# Set to store unique words
unique_words = set()

# Function to load entries from a file and split into individual words
def load_unique_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Split line into words and add to the set (removes duplicates automatically)
            words = line.strip().split()
            unique_words.update(words)

# Load words from each file
load_unique_words(district_file)
load_unique_words(province_file)
load_unique_words(ward_file)

# Convert set to sorted list (optional, for better readability)
sorted_unique_words = sorted(unique_words)

# Check if the output file exists, create or replace it
if os.path.exists(output_file):
    os.remove(output_file)  # Remove the file if it exists

# Write the unique words to the new or replaced dictionary file
with open(output_file, 'w', encoding='utf-8') as dict_file:
    for word in sorted_unique_words:
        dict_file.write(word + '\n')

print("Unique Vietnamese words dictionary created successfully.")
