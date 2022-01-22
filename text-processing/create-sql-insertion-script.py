import csv

"""
Take vocabular words from a CSV file 
and write them to a SQL file to load into a database
"""

source_file = "text-processing/voweled-and-unvoweled-words.csv"
destination_file = "text-processing/load_arabic_words.sql"

def create_sql_insertion_script(source_file, destination_file):

    f = open(destination_file, "a", encoding="UTF-8")

    table_name = "words"
    column1 = "voweled_word"
    column2 = "unvoweled_word"

    with open(source_file, newline='', encoding='UTF-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            value1 = row[f"\ufeff{column1}"]
            value2 = row[f"{column2}"]
            f.write(f"INSERT INTO {table_name} ({column1}, {column2}) VALUES ('{value1}', '{value2}');\n")

    f.close()

create_sql_insertion_script(source_file, destination_file)