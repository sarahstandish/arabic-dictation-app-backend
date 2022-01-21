import csv
from distutils.command.check import check
from pydoc import source_synopsis

source_file = 'text-processing/byu-corpus.csv'
destination_file = 'text-processing/voweled-and-unvoweled-words.csv'

def remove_diacritics(source_file):

    """
    Diacritics:
    U+0650 kesra
    U+064F damma
    U+064E kesra
    U+0651 shadda
    U+0652 sukuun
    U+0670 superscript alif
    U+064B tanween fatha
    """

    diacritics = ["\u0650", "\u064F", "\u064E", "\u0651", "\u0652", "\u0670", "\u064B"]
    destination_content = []

    with open(source_file, newline='', encoding='UTF-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["Exclude"].lower() != 'yes':
                voweled_word = row["Word"].strip()
                unvoweled_word = ""
                for char in voweled_word:
                    if char not in diacritics:
                        unvoweled_word += char
                voweled_word = remove_final_tanween_fatha(voweled_word)
                # wow! apparently Excel can't interpret unicode utf-8 without a byte-order mark at the beginning
                # so it's necessary to add U+FEFF at the beginning of the file
                # otherwise it will be interpreted as ascii
                destination_content.append({"\ufeffvoweled_word": voweled_word, "unvoweled_word": unvoweled_word})

    return destination_content

def check_for_latin_chars(row, voweled_word, char):
    """
    check for any remaining latin characters
    """
    if ord(char) < 127:
        print("Latin letters found in", voweled_word)
        print(row["\ufeffID"])
    input()

def check_for_short_words(row, word):
    """
    Check for presence of single-character words
    """
    if len(word) <= 2:

        print(f"Short word {word} found in row", row["\ufeffID"])
        input()

def remove_final_tanween_fatha(word):
    """
    remove final tanween fatha from words ending in alif maqsuura
    """
    alif_maqsuura_tanween_fatha = "\u0649\u064B"
    if word[-2:] == alif_maqsuura_tanween_fatha:
        word = word[:-1]
    return word

def write_destination_content_to_file(destination_content, destination_file):

    with open(destination_file, 'w', newline='') as csvfile:
        fieldnames=['\ufeffvoweled_word', 'unvoweled_word']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(destination_content)

def extract_plurals(source_file):
    """
    Extract plurals from the corpus.
    Plurals are found in the Notes column
    If there is a plural, the Notes text would start with "pl. "
    And the following character would be non-ascii
    """
    destination_file = "text-processing/plurals.csv"
    destination_content = []

    with open(source_file, newline='', encoding='UTF-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["Exclude"].lower() != 'yes':
                if row["Notes"][:3] == "pl." and ord(row["Notes"][4]) > 127:
                    split = row["Notes"].split()
                    plural = split[1].strip()
                    # remove commas from the end of words
                    if plural[-1] == ",":
                        plural = plural[:-1]
                    # exclude words ending in tanween kesra
                    tanween_kesra = "\u064D"
                    if plural[-1] != tanween_kesra:
                        destination_content.append({"\ufeffplural": plural})

        with open(destination_file, 'w', newline='') as csvfile:
            fieldnames=['\ufeffplural']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(destination_content)

destination_content = remove_diacritics(source_file)

write_destination_content_to_file(destination_content, destination_file)