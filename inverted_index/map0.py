#!/usr/bin/env python3
"""Map 0."""
import csv
import sys
# Map transforms

# Each map output line contains
# One key-value pair separated by a TAB character.
# Count the total number of documents in the collection (N)
csv.field_size_limit(sys.maxsize)
# Read input from the "/input" directory
for line in csv.reader(sys.stdin):
    sys.stdout.write("file\t1\n")
