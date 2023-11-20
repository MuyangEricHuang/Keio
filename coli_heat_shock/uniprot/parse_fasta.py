#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last update: 03/07/2022
import glob

def main():
    entry = {}
    input_file1 = "mainUP_left_duplicate_right.txt"
    with open(input_file1, "r") as file_handle1:
        for row1 in file_handle1:
            row1 = row1.rstrip()
            col1 = row1.split("\t")
            if col1[0] not in entry.keys():
                # entry.update({col1[0]: row1})
                entry.update({col1[0]: [col1[0], "_", col1[1]]})
            else:
                # all_entry = entry[col1[0]]
                # entry.update({col1[0]: "{}_{}".format(all_entry, col1[1])})
                entry[col1[0]].append(col1[1])
    
    # files = glob.glob("uniprot/*")
    fasta = []
    files = glob.glob("SP/*")
    for afile in files:
        # print(afile.split("/")[-1].split(".")[0])
        #up_id = None
        flag = False
        aline = ""
        with open(afile, "r") as file_handle:
            for row in file_handle:
                row = row.rstrip()
                if flag:
                    # print(row)
                    aline+=row[5:]
                if row.startswith("SQ   "):
                    flag = True
                    # print(True)
                    continue
                if row.startswith("//"):
                    flag = False
                    fasta.append(">" + "_".join(entry[afile.split("/")[-1].split(".")[0]]))
                    fasta.append(aline.replace(" ", ""))

    with open("duplicate.fasta", "w") as f:
        for aline in fasta:
            print(aline, file=f)

if __name__=="__main__":
    main()
