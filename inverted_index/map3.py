#!/usr/bin/env python3
"""Map 1.
Pass through, Calc idfk and log(n/nk) in reduce
input: 
key: t1 val: {"N": N, "nk": n1, 
              "docs": [doc_id_i, tfik]}
key: t2 val: {"N": N, "nk": n2, "docs": [doc_id_j, tfjk]}

output: 
key: t1 val: {"N": N, "nk": n1, 
              "docs": [doc_id_i, tfik]}
key: t2 val: {"N": N, "nk": n2, "docs": [doc_id_j, tfjk]}

"""
import sys 
import json

for line in sys.stdin: 
    """ key, value = line.split("\t")
    value_dict = json.loads(value) 
    for doc_id in value_dict['docs']: 
        sys.stdout.write(f"{(key, doc_id)}\t{json.dumps(value_dict)}\n") """
    sys.stdout.write(line)
