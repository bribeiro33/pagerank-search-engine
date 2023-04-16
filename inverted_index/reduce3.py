#!/usr/bin/env python3
"""Reduce 3.

Calc idfk = log(n/n_k)
input:
key: t1 val: {"N": N, "n_k": n1,
              "docs": [doc_id_i, tfik]}
key: t2 val: {"N": N, "n_k": n2, "docs": [doc_id_j, tfjk]}

output:
key: t1 val: {"docs": [doc_id_i, tfik], "idfk": idfk}
key: t2 val: {"docs": [doc_id_i, tfik],
key: t2 val: {"docs": [doc_id_j, tfjk], "idfk": idfk}

e.g. of INPUT
d3js	{"N": 3, "n_k": 1, "docs": ["1", 1]}
document	{"N": 3, "n_k": 4, "docs": ["1", 2]}
document	{"N": 3, "n_k": 4, "docs": ["2", 1]}
document	{"N": 3, "n_k": 4, "docs": ["3", 1]}

e.g. of OUTPUT
d3js	{"docs": ["1", 1], "idfk": 0.47712125471966244}
document	{"docs": ["1", 2], "idfk": 0.0}
document	{"docs": ["2", 1], "idfk": 0.0}
document	{"docs": ["3", 1], "idfk": 0.0}
"""

import sys
import itertools
import json
import math


# Calculate idfk
def reduce_one_group(key, group):
    """Reduce one group."""
    group = list(group)
    # print(group)
    # Each line is a term, then the file info
    # The number of lines in the group = the number of times
    # the term appears in the doc
    # log(a,Base)

    # Don't do this, we aren't allowed to read in from a separate file
    # past map 0 and 1. N is stored in the value dict
    # file_count = 0
    # with open("total_document_count.txt", "r") as file:
    #     file_count = float(file.readline())
    val_dict = {}  # need to globalize?
    n_k = 0
    docs = []
    # so copy over all the stuff
    # not changing anything, but also calcing tfik
    for line in group:
        # doc = line.strip()
        # doc = line.split()
        # term = doc[0].strip()
        # n_k = doc[1].strip()
        # docid = doc[2].strip()
        # tfik = doc[3].strip()
        # easier way, not as much stripping and if we change the order of
        # the vars in earlier files, we won't have to change the indexes here:

        value = line.split("\t")[1]
        val_dict = json.loads(value)
        # increment n_k as the number of docs with tk = num of lines in group
        n_k += 1
        # append this line's docs to docs to bring all tk's docs back together
        docs.append(val_dict['docs'])

    # length of group list is # docs thatre containing the term
    # cause each list item is for a doc that contains the term
    idfk = math.log((val_dict['N'] / len(docs)), 10)
    val_dict['idfk'] = idfk
    # delete N and n_k from dict as we no longer need it
    del val_dict['N']
    del val_dict['n_k']

    for doc in docs:
        val_dict['docs'] = doc
        sys.stdout.write(f"{key}\t{json.dumps(val_dict)}\n")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.split("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
