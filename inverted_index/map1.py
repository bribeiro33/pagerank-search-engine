#!/usr/bin/env python3
"""Map 1."""
import re
import csv
import sys

# Stop words: list of stop words in inverted_index/stopwords.txt
with open('stopwords.txt') as infile:
    # strip and casefold redundant, as no extra whitspace or capitals
    stop_words = set(infile.read().split('\n').strip().casefold())

# 1. Data clean
# 2. Organize terms to find all docs that contain a term in reduce
csv.field_size_limit(sys.maxsize)
for line in csv.reader(sys.stdin):
    doc_id, doc_title, doc_body = line
    # Combine both document title and document body by concatenating them, 
    # separated by a space.
    doc_text = doc_title + " " + doc_body
    # Remove non-alphanumeric characters (that also aren’t spaces)
    text = re.sub(r"[^a-zA-Z0-9 ]+", "", doc_text)
    # Case insensitive. 
    # Convert upper case characters to lower case using casefold().
    text = text.casefold()
    # Split the text into whitespace-delimited terms.
    text_list = text.split()
    # Remove stop words.
    text_list = [word for word in text_list if word not in stop_words]
    # If term, post_cleaning, is in doc --> <term, doc_id>
    for term in text_list:
        val_dict = {"doc_id": doc_id, "count": 1, "doc_text": text_list}
        print(f"{term}\t{val_dict}")