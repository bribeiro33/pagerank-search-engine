#!/usr/bin/env python3
"""Map 4.

Make key doc_i, find  di [norm factor] in reduce.

input:
key: t1 val: {"docs": [doc_id_i, tfik], "idfk": idfk}
key: t2 val: {"docs": [doc_id_i, tfik], "idfk": idfk}
key: t2 val: {"docs": [doc_id_j, tfjk], "idfk": idfk}

e.g. of INPUT
d3js	{"docs": ["1", 1], "idfk": 0.47712125471966244}
document	{"docs": ["1", 2], "idfk": 0.0}
document	{"docs": ["2", 1], "idfk": 0.0}
document	{"docs": ["3", 1], "idfk": 0.0}

output:
key: docid_1 val: t_k tf(1)k idfk
key: docid_2 val: t_k tf(2)k idfk
key: docid_2 val: t_l tf(2)k idfl

e.g. of OUTPUT
2	document 1 0.0
3	document 1 0.0
3	fine 1 0.47712125471966244
"""
import sys
import json

for line in sys.stdin:
    key, value = line.split("\t")
    value_dict = json.loads(value)
    # the new key is the doc id
    docid = value_dict['docs'][0]
    # We're going to have to print out with just spaces b/w,
    # so now ur strat is better
    term = key
    t_f = value_dict['docs'][1]
    idf = value_dict['idfk']
    sys.stdout.write(f"{docid}\t{term} {t_f} {idf}\n")
