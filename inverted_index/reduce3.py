#!/usr/bin/env python3
"""Reduce 3.
Calc idfk = log(n/nk)
input: 
key: t1 val: {"N": N, "nk": n1, 
              "docs": [doc_id_i, tfik]}
key: t2 val: {"N": N, "nk": n2, "docs": [doc_id_j, tfjk]}

output: 
key: t1 val: {"nk": n1, 
              "docs": [[doc_id_i, tfik]], "idfk": idfk}
key: t2 val: {"nk": n2,
              "docs": [[doc_id_i, tfik], [doc_id_j, tfjk]], "idfk": idfk}

e.g. of INPUT 
d3js	{"N": 3, "nk": 1, "docs": ["1", 1]}
document	{"N": 3, "nk": 4, "docs": ["1", 2]}
document	{"N": 3, "nk": 4, "docs": ["2", 1]}
document	{"N": 3, "nk": 4, "docs": ["3", 1]}

e.g. of OUTPUT
d3js	{"nk": 1, "docs": [["1", 1]], "idfk": 0.47712125471966244}
document	{"nk": 4, "docs": [["1", 2], ["2", 1], ["3", 1]], "idfk": 0.0}
"""

import sys
import itertools
import json
import math

# Calculate idfk

def reduce_one_group(key, group):
    """Reduce one group."""
    group = list(group)
    #print(group)
    # TODO: mlorp fix me
    # Each line is a term, then the file info
    # The number of lines in the group = the number of times 
    # the term appears in the doc
    # log(a,Base)
    
    # Don't do this, we aren't allowed to read in from a separate file
    # past map 0 and 1. N is stored in the value dict
    # file_count = 0
    # with open("total_document_count.txt", "r") as file:
    #     file_count = float(file.readline())
    val_dict = {} # need to globalize?
    nk = 0
    docs = []
    # so copy over all the stuff
    # not changing anything, but also calcing tfik
    for line in group:
        # doc = line.strip()
        # doc = line.split()
        # term = doc[0].strip()
        # nk = doc[1].strip()
        # docid = doc[2].strip()
        # tfik = doc[3].strip()
        # easier way, not as much stripping and if we change the order of 
        # the vars in earlier files, we won't have to change the indexes here: 

        value = line.split("\t")[1]
        val_dict = json.loads(value)
        # increment nk as the number of docs with tk = num of lines in group
        nk += 1
        # append this line's docs to docs to bring all tk's docs back together
        docs.append(val_dict['docs'])

    # Update docs in the dict with the new, complete doc list 
    val_dict['docs'] = docs
    # length of group list is # docs thatre containing the term 
    # cause each list item is for a doc that contains the term
    idfk = math.log((val_dict['N'] / len(val_dict['docs'])), 10)
    val_dict['idfk'] = idfk
    # delete N from dict as we no longer need it 
    del val_dict['N']
    sys.stdout.write(f"{key}\t{json.dumps(val_dict)}\n")
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
