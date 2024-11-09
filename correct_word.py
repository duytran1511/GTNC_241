import re
import editdistance
import unicodedata
import json
import pandas as pd
import time

# Define file paths
province_file = 'data/province.txt'
district_file = 'data/district.txt'
ward_file = 'data/ward.txt'
test_case_file = 'data/public.json'
output_pass_file = 'output_pass.txt'
output_fail_file = 'output_fail.txt'

# Load province, district, and ward data
provinces, districts, wards = set(), set(), set()
province_abbr, district_abbr, ward_abbr = {}, {}, {}
district_ward_mapping = {}

def load_names(file_path, container, abbr_mapping):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            name = line.strip()
            container.add(name)
            parts = name.split()
            if len(parts) > 1:
                abbr = ''.join(part[0].upper() for part in parts)  # E.g., "Vĩnh Long" -> "VL"
                abbr_mapping[abbr] = name
                type1_abbr = '.'.join(part[0] for part in parts[:-1]) + '.' + parts[-1]
                abbr_mapping[type1_abbr] = name
                type2_abbr = ''.join(part[0] for part in parts[:-1]) + parts[-1]
                abbr_mapping[type2_abbr] = name

def load_ward_mapping(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            ward_name = line.strip()
            district_name = ward_name.split(",")[-1].strip()  # Extract district from ward
            if district_name not in district_ward_mapping:
                district_ward_mapping[district_name] = []
            district_ward_mapping[district_name].append(ward_name)

# Load data and abbreviations
load_names(province_file, provinces, province_abbr)
load_names(district_file, districts, district_abbr)
load_names(ward_file, wards, ward_abbr)
load_ward_mapping(ward_file)

# Prefix replacements
prefix_replacements = {
    "Ap": "Ấp",
    "F ": "Phường ",
    "F.": "Phường",
    "H ": "Huyện",
    "H. ": "Huyện",
    "H.C.M": "Hồ Chí Minh",
    "HCM": "Hồ Chí Minh",
    "Muyện": "Huyện",
    "Q.": "Quận",
    "T ": "Tỉnh",
    "T.P": "Thành phố",
    "T.Phố": "Thành phố",
    "T.p": "Thành phố",
    "T.X.": "Thị xã",
    "Thx": "Thị xã",
    "TP ": "Thành phố ",
    "TPHCM": "Thành phố Hồ Chí Minh",
    "TT ": "Thị trấn",
    "Thi trấ ": "Thị trấn ",
    "x2": "Xã",
    "X.": "Xã",
    ",H.": "Huyện"
}

stop_word_province = {
    "Tỉnh", "T ", "T. ", ",T.", ", T.", "Thành phố", "T.P", "T.P", "T.Phố", "T.p", "TP ", "TP"
}

stop_word_district = {
    "Quận", "Q.", "Q. ", "Huyện", "Muyện", "H ", "H. ", "Thị xã", "T.X.", "Thx", "TX.", ",TX", ", TX", "TX ", " TX", "Thành phố"
}

stop_word_ward = {
    "Phường", "F ", "F. ", "F.", "P. ", "P.", "P ", "Xã", "X.", "X ", ", X", "Thị trấn", "Thi trấ ", "TT ", "TT. "
}

def replace_prefixes(text):
    for prefix, replacement in prefix_replacements.items():
        text = text.replace(prefix, replacement)
        
    # Regex pattern for districts with numbers like "Q.10" or "P10"
    text = re.sub(r'\b(Q|q)\.?\s*(\d+)', r'Quận \2', text)  # Ensure "Quận 10"
    text = re.sub(r'\b(P|p|F|f)\.?\s*(\d+)', r'Phường \2', text)  # Ensure "Phường 10"
    
    return text

def remove_stop_words(text, stop_words):
    for word in stop_words:
        text = text.replace(word, "")
    return text.strip()

def normalize(text, retain_diacritics=True):
    # Replace commas and periods with spaces within the text
    text = re.sub(r"[.,]", " ", text)
    
    # Remove any trailing comma or period at the end of the text
    text = re.sub(r"[.,\s]+$", "", text)
    
    if retain_diacritics:
        # Lowercase and strip leading/trailing whitespace
        text = text.lower().strip()
    else:
        # Remove diacritics if retain_diacritics is False
        text = ''.join(
            c for c in unicodedata.normalize('NFD', text)
            if unicodedata.category(c) != 'Mn'
        )
        text = text.lower().strip()
        
    return text

def split_words(text):
    text = re.sub(r'\bT\d+\b', '', text)
    text = re.sub(r'(?<=[a-zà-ỹ])(?=[A-Z])', ' ', text)
    return text.split()

def find_best_match(text, dictionary, abbr_mapping):
    # Step 1: Replace prefixes and abbreviations
    text = replace_prefixes(text)
    words = split_words(text)
    normalized_text = normalize(' '.join(words), retain_diacritics=True)
    best_match, lowest_distance = None, float('inf')

    # Check for abbreviation matches first
    for abbr, full_name in abbr_mapping.items():
        if abbr in normalized_text:
            return full_name, 0

    # Step 2: Special Handling for Districts with Numbers (i.e., Quận 1, Quận 10, etc.)
    # Match 'Quận 10', 'Quận 1' etc. directly in the text to ensure exact match
    district_number_pattern = r"(Quận\s?\d+)"  # Match 'Quận 10', 'Quận 1', etc.
    
    # Check for numeric districts explicitly (with the exact match of both district and number)
    for district in dictionary:
        if re.search(district_number_pattern, district):  # Match district like "Quận 10"
            # Extract numeric part of the district (e.g., "10" from "Quận 10")
            district_number = re.search(r"\d+", district).group(0)
            # If the text contains the same district number, we make sure it's a direct match
            if district_number in normalized_text:
                # Check if we have an exact match between the district name and the number
                if normalized_text == district:
                    return district, 0
    
    # Step 3: Regular Levenshtein Distance Matching (for non-numeric cases)
    for start in range(len(words) - 1, -1, -1):
        for count in range(2, min(5, len(words) - start + 1)):
            phrase = ' '.join(words[start:start + count])
            normalized_phrase = normalize(phrase, retain_diacritics=True)
            for entry in sorted(dictionary):
                normalized_entry = normalize(entry, retain_diacritics=True)
                if normalized_phrase in normalized_entry or normalized_entry in normalized_phrase:
                    return entry, 0
                distance = editdistance.eval(normalized_phrase, normalized_entry)
                if distance < lowest_distance or (
                    distance == lowest_distance and len(normalized_entry) < len(best_match or '')
                ):
                    best_match = entry
                    lowest_distance = distance
    return best_match, lowest_distance


def replace_abbreviations(text, abbr_mappings):
    """Replace abbreviations in the text based on the provided abbreviation mappings."""
    for abbr, full_name in abbr_mappings.items():
        text = re.sub(r'\b' + re.escape(abbr) + r'\b', full_name, text)
    return text

# Modify the extract_address_components function to include generalized abbreviation replacement
def extract_address_components(text):
    # Step 2: Normalize prefixes (expand any common prefixes like 'Q.' and 'P.')
    normalized_text = replace_prefixes(text)
    
    # Step 1: Replace all abbreviations in the text using mappings
    text = replace_abbreviations(text, province_abbr)
    text = replace_abbreviations(text, district_abbr)
    text = replace_abbreviations(text, ward_abbr)
    
    # Step 3: Remove stop words for each component level to clean the text
    province_text = remove_stop_words(normalized_text, stop_word_province)
    district_text = remove_stop_words(normalized_text, stop_word_district)
    ward_text = remove_stop_words(normalized_text, stop_word_ward)
    
    # Step 4: Identify the province
    province, province_distance = find_best_match(province_text, sorted(provinces), province_abbr)
    if province_distance > 1:
        province = ""

    # Step 5: Identify the district, ensuring it's not confused with the province
    district_abbr_filtered = {k: v for k, v in district_abbr.items() if v != province}
    district, district_distance = find_best_match(
        district_text, sorted(districts - {province} if province else districts), district_abbr_filtered
    )
    if district_distance > 1:
        district = ""

    # Step 6: Identify the ward, ensuring it's not confused with the province or district
    ward_abbr_filtered = {k: v for k, v in ward_abbr.items() if v != province and v != district}
    ward, ward_distance = find_best_match(
        ward_text, sorted(wards - {province, district} if province or district else wards), ward_abbr_filtered
    )
    if ward_distance > 1:
        ward = ""

    # Step 7: Default to the first known ward in the district if both province and district are present but ward is missing
    if province and district and not ward:
        known_wards = district_ward_mapping.get(district, [])
        if known_wards:
            ward = known_wards[0]  # Take the first known ward as default

    # Print final extracted components
    extracted_components = {"province": province or "", "district": district or "", "ward": ward or ""}
    
    return extracted_components

# Load test cases
with open(test_case_file, 'r', encoding='utf-8') as f:
    test_cases = json.load(f)

# Run tests and store results
pass_results, fail_results = [], []
pass_count, fail_count = 0, 0

for case in test_cases:
    start_time = time.time()
    extracted = extract_address_components(case["text"])
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    expected = {
        "province": case["result"]["province"],
        "district": case["result"]["district"],
        "ward": case["result"]["ward"]
    }
    pass_fail = "Pass" if extracted == expected else "Fail"
    
    result_entry = {
        "Text": case["text"],
        "Extracted (province, district, ward)": f"{extracted['province']}, {extracted['district']}, {extracted['ward']}",
        "Expected (province, district, ward)": f"{expected['province']}, {expected['district']}, {expected['ward']}",
        "Result": pass_fail,
        "Time (s)": round(elapsed_time, 6)
    }
    
    if pass_fail == "Pass":
        pass_results.append(result_entry)
        pass_count += 1
    else:
        fail_results.append(result_entry)
        fail_count += 1

# Convert results to DataFrame for formatting
df_pass = pd.DataFrame(pass_results)
df_fail = pd.DataFrame(fail_results)

# Save results to respective files
with open(output_pass_file, 'w', encoding='utf-8') as f:
    f.write(df_pass.to_string(index=False))
    f.write(f"\n\nTotal Pass: {pass_count}")

with open(output_fail_file, 'w', encoding='utf-8') as f:
    f.write(df_fail.to_string(index=False))
    f.write(f"\n\nTotal Fail: {fail_count}")

print(f"Total Pass: {pass_count}")
print(f"Total Fail: {fail_count}")
