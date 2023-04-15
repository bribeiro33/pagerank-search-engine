"""Index Server main code."""
import math
import pathlib
import re
from flask import jsonify, request
import index


STOPWORDS_SET = set()
PAGERANK_DICT = {}
INVERTEDINDEX_DICT = {}

def load_index():
    """Load inverted index, pagerank, and stopwords into memory."""
    index_dir = pathlib.Path(__file__).parent.parent
    read_stopwords(index_dir)
    read_pagerank(index_dir)
    read_inverted_index(index_dir)


def read_stopwords(index_dir):
    """Read the stopwords.txt file."""
    stopwords_file = index_dir / "stopwords.txt"
    with open(str(stopwords_file), 'r', encoding='utf-8') as stopfile:
        for line in stopfile:
            STOPWORDS_SET.add(line.strip())


def read_pagerank(index_dir):
    """Read the pagerank.out file."""
    pagerank_file = index_dir / "pagerank.out"
    with open(str(pagerank_file), 'r', encoding='utf-8') as pagerankfile:
        for line in pagerankfile:
            line = line.strip()
            doc_id, score = line.split(",")
            PAGERANK_DICT[doc_id] = float(score)


def read_inverted_index(index_dir):
    """Read the inverted_index.txt file, based on the configured envvar."""
    index_file_config = index.app.config["INDEX_PATH"]
    inverted_index_file = index_dir / "inverted_index" / index_file_config
    with open(str(inverted_index_file), 'r', encoding='utf-8') as indexfile:
        for line in indexfile:
            term_info_list = line.strip().split()
            term_name = term_info_list[0]
            idf_k = term_info_list[1]
            counter = 2
            term_appears = []
            while counter < len(term_info_list):
                curr_appear = {
                    "doc_id": term_info_list[counter],
                    "tf_ik": int(term_info_list[counter + 1]),
                    "norm": float(term_info_list[counter + 2])
                }
                term_appears.append(curr_appear)
                counter += 3
            term_context = {
                "idf_k": idf_k,
                "term_info_appear": term_appears
            }
            INVERTEDINDEX_DICT[term_name] = term_context