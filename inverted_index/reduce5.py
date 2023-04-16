#!/usr/bin/env python3
"""Reduce 5.

Sort and output inverted index according to spec.

input:
key: docid % 3 val: term docid idf t_f norm_fac

e.g. of INPUT
1	d3js 1 0.47712125471966244 1 1.138223458526325
1	document 1 0.0 2 1.138223458526325
...
2	document 2 0.0 1 1.593512841936855
...
0	document 3 0.0 1 2.048802225347385
"""
import sys
import itertools
# 0	art 3 0.47712125471966244 1 2.048802225347385
# 0	document 3 0.0 1 2.048802225347385
# 0	fine 3 0.47712125471966244 1 2.048802225347385
# 0	forgetting 3 0.47712125471966244 1 2.048802225347385
# 0	hear 3 0.47712125471966244 1 2.048802225347385
# 0	heard 3 0.47712125471966244 1 2.048802225347385
# 0	laurence 3 0.47712125471966244 1 2.048802225347385
# 0	originality 3 0.47712125471966244 1 2.048802225347385
# 0	peter 3 0.47712125471966244 1 2.048802225347385
# 0	remembering 3 0.47712125471966244 1 2.048802225347385
# 1	bostock 1 0.47712125471966244 1 1.138223458526325
# 1	cool 1 0.47712125471966244 1 1.138223458526325
# 1	d3js 1 0.47712125471966244 1 1.138223458526325
# 1	document 1 0.0 2 1.138223458526325
# 1	made 1 0.47712125471966244 1 1.138223458526325
# 1	mike 1 0.47712125471966244 1 1.138223458526325
# 2	build 2 0.47712125471966244 1 1.593512841936855
# 2	character 2 0.47712125471966244 1 1.593512841936855
# 2	document 2 0.0 1 1.593512841936855
# 2	flaw 2 0.47712125471966244 1 1.593512841936855
# 2	human 2 0.47712125471966244 1 1.593512841936855
# 2	kurt 2 0.47712125471966244 1 1.593512841936855
# 2	maintenance 2 0.47712125471966244 1 1.593512841936855
# 2	vonnegut 2 0.47712125471966244 1 1.593512841936855


def reduce_one_group(group):
    """Reduce one group."""
    docs = {}
    group = list(group)

    for line in group:
        trimmed_input = [word.strip() for word in line.split()]
        _, term, docid, idf, t_f, norm_fac = trimmed_input
        # adds all the vals to
        if (term, idf) in docs:
            docs[(term, idf)].extend([docid, t_f, norm_fac])
        else:
            docs[(term, idf)] = [docid, t_f, norm_fac]

    for term, idf in docs:
        final_docs = " ".join(docs[(term, idf)])
        sys.stdout.write(f"{term} {idf} {final_docs}\n")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.split("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for _, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(group)


if __name__ == "__main__":
    main()
