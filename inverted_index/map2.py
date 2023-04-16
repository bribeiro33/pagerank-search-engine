#!/usr/bin/env python3
"""Map 1.

Make key term and doc_id tuple, find tfik in reduce.
input:
key: t1 val: {"N": N, "nk": n1,
              "docs": [doc_id_a, doc_id_b]}
key: t2 val: {"N": N, "nk": n2, "docs": [doc_id_a]}

output:
key: (t1, doc_id_a) val: {"N": N, "nk": n1,
              "docs": [[doc_id_a, doc_text_a], [doc_id_b, doc_text_b]]}
key: (t1, doc_id_b) val: {"N": N, "nk": n2, "docs": [[doc_id_a, doc_text_b]]}

"""
import sys
import json

for line in sys.stdin:
    key, value = line.split("\t")
    value_dict = json.loads(value)
    for doc_id in value_dict['docs']:
        sys.stdout.write(f"{(key, doc_id)}\t{json.dumps(value_dict)}\n")
