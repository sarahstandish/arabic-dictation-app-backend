import csv

"""
Diacritics:
U+0650 kesra
U+064F damma
U+064E kesra
U+0651 shadda
U+0652 sukuun
U+0670 superscript alif
"""

diacritics = [f"\u0650", f"\u064F", f"\u064E", f"\u0651", f"\u0652", f"\u0670"]

source_file = 'text-processing/byu-corpus.csv'
destination_content = []
destination_file = 'text-processing/voweled-and-unvoweled-words.csv'

with open(source_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row["Exclude"].lower() != 'yes':
            voweled_word = row["Word"].strip()
            unvoweled_word = ""
            for char in voweled_word:
                if char not in diacritics:
                    unvoweled_word += char
            destination_content.append({"voweled_word": voweled_word, "unvoweled_word": unvoweled_word})
            
with open(destination_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames=['voweled_word', 'unvoweled_word']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(destination_content)