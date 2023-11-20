#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob

def main():
    files = glob.glob("data/raw/uniprot/*.txt")
    for afile in files:
        count = 0
        with open(afile, "r") as file_handle:
            for row in file_handle:
                row = row.rstrip()
                if row=="//":
                    count+=1
        if 1<count:
            print(f"{count} entries in {afile}")

if __name__=="__main__":
    main()
