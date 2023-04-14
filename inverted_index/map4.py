#!/usr/bin/env python3
"""Map 4.
Make key doc_i, find  di [norm factor] in reduce.
input: 
key: t1 val: {"docs": [[doc_id_i, tfik]], "idfk": idfk, "tk": t1}
key: t2 val: {"docs": [[doc_id_i, tfik], [doc_id_j, tfjk]], "idfk": idfk,
              "tk": t2}

e.g. of INPUT
d3js	{"docs": [["1", 1]], "idfk": 0.47712125471966244, "tk": "d3js"}
document	{"docs": [["1", 2], ["2", 1], ["3", 1]], "idfk": 0.0, 
            "tk": "document"}

# this might be incredibly inefficient but we'll see
# ugly but it works
output: 
key: doc1 val: [{"docs": [[doc_id_1, tfik], [doc_id_j, tfjk]], "idfk": idfk,
                 "tk": t2}], [{"nk": n1, "docs": [[doc_id_1, tfik]], 
                 "idfk": idfk, "tk": t1}]

key: doc3 val: [{"docs": [[doc_id_1, tfik], [doc_id_j, tfjk]], "idfk": idfk,
                 "tk": t2}]

e.g. of OUTPUT
3	[{"docs": [["1", 2], ["2", 1], ["3", 1]], "idfk": 0.0, "tk": "document"}, 
     {"docs": [["3", 1]], "idfk": 0.47712125471966244, "tk": "fine"}, 
     {"docs": [["3", 1]], "idfk": 0.47712125471966244, "tk": "forgetting"}, 
     {"docs": [["3", 1]], "idfk": 0.47712125471966244, "tk": "hear"}, 
     {"docs": [["3", 1]], "idfk": 0.47712125471966244, "tk": "heard"}, 
     {"docs": [["3", 1]], "idfk": 0.47712125471966244, "tk": "laurence"}, 
     {"docs": [["3", 1]], "idfk": 0.47712125471966244, "tk": "originality"}, 
     {"docs": [["3", 1]], "idfk": 0.47712125471966244, "tk": "peter"}, 
     {"docs": [["3", 1]], "idfk": 0.47712125471966244, "tk": "remembering"}]

"""
import sys 
import json

# all the doc ids 
documents = {}
# each line is a different term
for line in sys.stdin: 
    key, value = line.split("\t")
    value_dict = json.loads(value) 

    # loop over each doc in docs 
    for doc in value_dict['docs']:
        docid = doc[0]
        if docid in documents: 
            documents[docid].append(value_dict)
        else: 
            documents[docid] = []

for docid, doc_content in documents.items(): 
    sys.stdout.write(f"{docid}\t{json.dumps(doc_content)}\n")
