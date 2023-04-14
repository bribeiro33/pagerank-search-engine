#!/usr/bin/env python3
"""Reduce 3.
Calc idfk = log(n/nk)
input: 
key: t1 val: {"N": N, "nk": n1, 
              "docs": [doc_id_i, tfik]}
key: t2 val: {"N": N, "nk": n2, "docs": [doc_id_j, tfjk]}

output: 
key: t1 val: {"idfk": idfk, "nk": n1, 
              "docs": [doc_id_i, tfik]}
key: t2 val: {"idfk": idfk, "nk": n2,
              "docs": [doc_id_j, tfjk]}

e.g. of INPUT (i think? from reducer 2 and map3 passthrough?)
d3js	{"N": 3, "nk": 1, "docs": ["1", 1]}
document	{"N": 3, "nk": 4, "docs": ["1", 2]}
document	{"N": 3, "nk": 4, "docs": ["2", 1]}
document	{"N": 3, "nk": 4, "docs": ["3", 1]}

e.g. of OUTPUT
d3js	{"idfk": log(3/1), "nk": 1, "docs": ["1", 1]}
//this next part i dont get, is this "docs" but expanded? but like its not.
document	{"idfk": log(3/1), "nk": 4, "docs": ["1", 2]}
document	{"idfk": log(3/1), "nk": 4, "docs": ["2", 1]}
document	{"idfk": log(3/1), "nk": 4, "docs": ["3", 1]}
"""

import sys
import itertools
import json
import re
import math

# Calculate tfik

def reduce_one_group(key, group):
    """Reduce one group."""

    # TODO: mlorp fix me
    # Each line is a term, then the file info
    # The number of lines in the group = the number of times 
    # the term appears in the doc
    # log(a,Base)
    file_count = 0
    with open("total_document_count.txt", "r") as file:
        file_count = float(file.readline())

    # so copy over all the stuff
    # not changing anything, but also calcing tfik
    for line in sys.stdin:
        doc = line.strip()
        doc = line.split()
        term = doc[0].strip()
        nk = doc[1].strip()
        docid = doc[2].strip()
        tfik = doc[3].strip()
        # length of sys.stdin list is # docs thatre containing the term
        # cause each list item is for a doc that contains the term
        idfk = math.log(file_count / len(list(sys.stdin)), 10)
        sys.stdout.write(f"{term}\t{idfk} {nk} {docid} {tfik}\n")
        # shld i be doing some value dict-y thing w json?



def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.split("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
