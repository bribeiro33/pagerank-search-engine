#!/usr/bin/env python3
"""Reduce 1.
Find all docs that contain tk for all k
and calc nk (num of docs containing tk)
input: 
grouped: by ti
key: t1 val: {"doc_id": doc_id_a, "count": 1, "doc_text": doc_text_a}
key: t1 val: {"doc_id": doc_id_b, "count": 1, "doc_text": doc_text_b}
key: t2 val: {"doc_id": doc_id_a, "count": 1, "doc_text": doc_text_a}
output:
key: t1 val: {"N": N, "nk": n1, 
              "docs": [(doc_id_a, doc_text_a), (doc_id_b, doc_text_b)]}
key: t2 val: {"N": N, "nk": n2, "docs": [(doc_id_a, doc_text_b)]}
"""
import sys
import itertools
import json

# Find all docs that contain ti for all i 
# sorted docs by id

with open("total_document_count.txt") as infile:
    N = int(infile.read())


def reduce_one_group(key, group):
    """Reduce one group."""
    group = list(group) #needed?
    nk = 0
    docs = []
    for line in group:
        # increase nk by count
        value = line.split("\t")[1]
        value_dict = json.loads(value) #  converts to dict
        # Add value to total_count (sould increment by one)
        nk += value_dict['count']
        # add doc_id and doc_text to docs
        doc_tuple = (value_dict['doc_id'], value_dict['doc_text'])
        docs.append(doc_tuple)

    val_dict = {"N": N, "nk": nk, "docs": docs}
    sys.stdout.write(f"{key}\t{val_dict}\n")



def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.split()[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()