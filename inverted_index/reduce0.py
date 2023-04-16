#!/usr/bin/env python3
"""Reduce 0."""
import sys
import itertools
# Reduce computes
# The output should be a single integer.


def reduce_one_group(group):
    """Reduce one group."""
    total_count = 0
    group = list(group)  # not sure if necessary
    for line in group:
        # Get the value of the line
        value = int(line.split("\t")[1])
        # Add value to total_count (sould be one)
        total_count += value
    sys.stdout.write(f"{total_count}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for _, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(group)


if __name__ == "__main__":
    main()
