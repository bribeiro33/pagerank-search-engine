#!/usr/bin/env python3
"""Reduce 2.

Calculate tfik (# times a termk appears in doci)
input:
key: t1 val: {"N": N, "nk": n1,
              "docs": [doc_id_a, doc_id_b]}
key: t2 val: {"N": N, "nk": n2, "docs": [doc_id_a]}

output:
key: t1 val: {"N": N, "nk": n1,
              "docs": [doc_id_i, tfik]}
key: t2 val: {"N": N, "nk": n2, "docs": [doc_id_j, tfjk]}

e.g.
d3js	{"N": 3, "nk": 1, "docs": ["1", 1]}
document	{"N": 3, "nk": 4, "docs": ["1", 2]}
document	{"N": 3, "nk": 4, "docs": ["2", 1]}
document	{"N": 3, "nk": 4, "docs": ["3", 1]}
"""
import sys
import itertools
import json
import re
# Calculate tfik


def reduce_one_group(key, group):
    """Reduce one group."""
    # Each line is a term, file id pairing
    # The number of lines in the group = the number of times
    # the term appears in the doc
    key_correct = re.sub(r"[^a-zA-Z0-9 ]+", "", key)
    term, doc_id = key_correct.split()
    freq_count = 0
    for line in group:
        freq_count += 1

        # Just to keep curr info, pass on
        value = line.split("\t")[1]
        value_dict = json.loads(value)
    # Edit docs to be a list of doc_id and term_freq
    value_dict['docs'] = [doc_id, freq_count]
    sys.stdout.write(f"{term}\t{json.dumps(value_dict)}\n")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.split("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
