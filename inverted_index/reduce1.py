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
              "docs": [[doc_id_a, doc_text_a], [doc_id_b, doc_text_b]]}
key: t2 val: {"N": N, "nk": n2, "docs": [(doc_id_a, doc_text_b)]}
"""
import sys
import itertools
import json


# Find all docs that contain ti for all i
# sorted docs by id
def reduce_one_group(key, group):
    """Reduce one group."""
    group = list(group)
    nk = 0
    docs = []
    N = 0
    for line in group:
        # increase nk by count
        key, value = line.split("\t")
        # Split at the space to separate N from the dict
        output_parts = value.strip().split(' ', 1)
        N = int(output_parts[0])
        val_dic = output_parts[1]

        value_dict = json.loads(val_dic)  # converts to dict

        # Add value to total_count (sould increment by one)
        nk += value_dict['count']
        # add doc_id and doc_text to docs
        doc_ids = value_dict['doc_id']
        docs.append(doc_ids)

    val_dict = {"N": N, "nk": nk, "docs": docs}
    sys.stdout.write(f"{key}\t{json.dumps(val_dict)}\n")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.split()[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
