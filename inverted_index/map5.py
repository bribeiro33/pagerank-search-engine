#!/usr/bin/env python3
"""Map 5.

Format info to print out correctly into 3 segments in reduce.

input:
key: term_k val: idf_k docid_i tf_ki norm_fac_i
key: term_l val: idf_l docid_j tf_lj norm_fac_j

output:
key: docid % 3 val: term docid idf tf norm_fac

e.g. of INPUT
cool	0.47712125471966244 1 1 1.138223458526325
d3js	0.47712125471966244 1 1 1.138223458526325
document	0.0 1 2 1.138223458526325
...
document	0.0 2 1 1.593512841936855

e.g. of OUTPUT
1	d3js 1 0.47712125471966244 1 1.138223458526325
1	document 1 0.0 2 1.138223458526325
...
2	document 2 0.0 1 1.593512841936855
...
0	document 3 0.0 1 2.048802225347385
"""
import sys

# doc_id % 3 as the mapper output key in the last job
for line in sys.stdin:
    trimmed_input = [word.strip() for word in line.split()]
    term, idf, docid, tf, norm_fac = trimmed_input
    new_key = int(docid) % 3
    sys.stdout.write(f"{new_key}\t {term} {docid} {idf} {tf} {norm_fac}\n")
