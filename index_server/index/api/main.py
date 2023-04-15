"""Index Server main code."""
import math
import pathlib
import re
from flask import jsonify, request
import index

# Globals: stopwords (set), pagerank (dict), inverted_index (dict)
# Might need to 
def load_index():
    """Load inverted index, pagerank, and stopwords into memory."""
    index_dir = pathlib.Path(__file__).parent.parent
    load_stopwords(index_dir)
    load_pagerank(index_dir)
    load_inverted_index(index_dir)


def load_stopwords(index_dir):
    """Load the stopwords.txt file into stopwords."""
    # Create global var to be accessed in calc funcs later
    global stopwords
    stopwords = set()
    # Get correct path: /index/stopwords.txt
    stopwords_file = index_dir / "stopwords.txt"
    with open(str(stopwords_file), 'r', encoding='utf-8') as infile:
        for line in infile:
            # incase there's extra whitespace, strip
            new_word = line.strip()
            stopwords.add(new_word)


def load_pagerank(index_dir):
    """Load the pagerank.out file into pagerank."""
    # Create global var to be accessed in calc funcs later
    global pagerank
    pagerank = {}
    # Get correct path: /index/pagerank.out
    pagerank_file = index_dir / "pagerank.out"
    with open(str(pagerank_file), 'r', encoding='utf-8') as infile:
        for line in infile:
            line = line.strip()
            # create a data structure that maps doc ID to PageRank score
            #e.g. 
            # 3434750,0.0193215
            # 20381,0.0104298
            docid, score = line.split(",")
            pagerank[docid] = float(score)


def load_inverted_index(index_dir):
    """Read the inverted_index.txt file, based on the configured envvar."""
    global inverted_index
    inverted_index = {}
    
    # which index_path was set is the index file of inverted index to read from 
    # e.g. inverted_index_0.txt
    index_file_config = index.app.config["INDEX_PATH"]
    # /index/inverted_index/inverted_index_0|1|2.txt
    inverted_index_file = index_dir / "inverted_index" / index_file_config
    with open(str(inverted_index_file), 'r', encoding='utf-8') as infile:
        for line in infile:
            # Each item is separated by a space
            index_list = line.strip().split()
            term_name = index_list[0]
            idf = index_list[1]
            # doc specific info starts at [2] and contains 3 items for each doc
            counter = 2
            # keep track of all doc triples for the term
            # docs is a list of dicts 
            docs = []
            while counter < len(index_list):
                curr_doc_triple = {
                    "docid": index_list[counter],
                    "tf": int(index_list[counter + 1]),
                    "norm_fac": float(index_list[counter + 2])
                }
                docs.append(curr_doc_triple)
                counter += 3
            term_value = {
                "idf": idf,
                "docs": docs
            }
            inverted_index[term_name] = term_value