#!/usr/bin/env python3.11

import sys
import difflib
import itertools

def find_common_parts(files):
    file_contents = [open(file, "r").read().splitlines() for file in files]

    common_parts = set(file_contents[0])

    for i, j in itertools.combinations(file_contents, 2):
        sequence_matcher = difflib.SequenceMatcher(None, i, j)

        matches = sequence_matcher.get_matching_blocks()
        matches = filter(lambda x: x.size > 0, matches)
        matches = map(lambda x: i[x.a:x.a + x.size], matches)
        matches = [x for xs in matches for x in xs]

        common_parts = common_parts.intersection(matches)

    return common_parts

if __name__ == "__main__":
    files = sys.argv[1:]
    common_parts = find_common_parts(files)
    for line in common_parts:
        print(line)
