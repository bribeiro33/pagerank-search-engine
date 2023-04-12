#!/usr/bin/env python3
"""Map 1.
Pass through, find tfik in reduce.
input: 
key: t1 val: {"N": N, "nk": n1, 
              "docs": [(doc_id_a, doc_text_a), (doc_id_b, doc_text_b)]}
key: t2 val: {"N": N, "nk": n2, "docs": [(doc_id_a, doc_text_b)]}

output: 
key: t1 val: {"N": N, "nk": n1, 
              "docs": [(doc_id_a, doc_text_a), (doc_id_b, doc_text_b)]}
key: t2 val: {"N": N, "nk": n2, "docs": [(doc_id_a, doc_text_b)]}

"""
import sys 
import json

for line in sys.stdin: 
    print(f"{line}\n")
