#!/usr/bin/env python3
"""Reduce 4.

Calc |di| e.i. norm factor.
input:
key: docid_1 val: t_k t_f(1)k idfk
key: docid_2 val: t_k t_f(2)k idfk
key: docid_2 val: t_l t_f(2)k idfl

output:
key: term_k val: idf_k docid_i t_f_ki norm_fac_i
key: term_l val: idf_l docid_j t_f_lj norm_fac_j

e.g. of INPUT
2	document 1 0.0
3	document 1 0.0
3	fine 1 0.47712125471966244

e.g. of OUTPUT
cool	0.47712125471966244 1 1 1.138223458526325
d3js	0.47712125471966244 1 1 1.138223458526325
document	0.0 1 2 1.138223458526325
...
document	0.0 2 1 1.593512841936855
"""
import sys
import itertools


# Calculate norm factor
# 1) For each term, perform (t_f * idf)^2
# 2) Add up all those values
# 3) don't perform sqrt for inverted index
def reduce_one_group(group):
    """Reduce one group."""
    group = list(group)  # required, as have to iterate trhough twice
    norm_fac = 0
    # the group is all the terms in the doc
    # each line is a term
    for line in group:
        # docid, term, t_f, idf
        _, _, t_f, idf = line.split()
        norm_fac += (float(t_f) * float(idf)) ** 2

    for line in group:
        docid, term, t_f, idf = line.split()
        sys.stdout.write(f"{term}\t{idf} {docid} {t_f} {norm_fac}\n")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.split("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for _, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(group)


if __name__ == "__main__":
    main()
