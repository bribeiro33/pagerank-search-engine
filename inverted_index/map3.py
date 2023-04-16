#!/usr/bin/env python3
"""Map 1.
Pass through, Calc idfk e.i.log(n/nk) in reduce
input:
key: t1 val: {"N": N, "nk": n1,
              "docs": [doc_id_i, tfik]}
key: t2 val: {"N": N, "nk": n2, "docs": [doc_id_j, tfjk]}

e.g.
d3js	{"N": 3, "nk": 1, "docs": ["1", 1]}
document	{"N": 3, "nk": 4, "docs": ["1", 2]}
document	{"N": 3, "nk": 4, "docs": ["2", 1]}
document	{"N": 3, "nk": 4, "docs": ["3", 1]}

output:
key: t1 val: {"N": N, "nk": n1,
              "docs": [doc_id_i, tfik]}
key: t2 val: {"N": N, "nk": n2, "docs": [doc_id_j, tfjk]}


"""
import sys
import json

# Pass through, no need for json load and dump
for line in sys.stdin:
    sys.stdout.write(line)


# for line in sys.stdin:
#     key, value = line.split("\t")
#     value_dict = json.loads(value)


#     sys.stdout.write(f"{(key, doc_id)}\t{json.dumps(value_dict)}\n")
