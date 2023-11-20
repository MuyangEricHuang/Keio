#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file: "data/tmp/ecoli_from_uniprot_reviesd.txt"
P0AD86  LPT_ECOLI       21      thrL

file:
DE   RecName: Full=thr operon leader peptide {ECO:0000255|HAMAP-Rule:MF_01907};
DR   GO; GO:0005886; C:plasma membrane; IEA:UniProtKB-SubCell.
DR   GO; GO:0009242; P:colanic acid biosynthetic process; IMP:EcoCyc.
DR   eggNOG; COG1869; LUCA.
"""

import os
from goatools.obo_parser import GODag
godag = GODag("data/raw/go-basic.obo")

def main():
    print_list = []
    input_file = "data/tmp/ecoli_from_uniprot_reviesd.txt"
    with open(input_file, "r") as ecoli_file_handle:
        for row in ecoli_file_handle:
            row = row.rstrip()
            col = row.split("\t")
            up_id = col[0]
            up_name, go_list = get_go_list(up_id)

            print_str = "{0}\t{1}\t{2}".format(row, up_name, "|".join(go_list))
            print_list.append(print_str)

    output_file = "data/tmp/ecoli_from_uniprot_reviesd_withGO.txt"
    with open(output_file, "w") as file_handle:
        for one in print_list:
            print(one, file=file_handle)

def get_go_list(uniprot_id):
    up_file = "data/raw/uniprot/{}.txt".format(uniprot_id)
    go_list = []
    with open(up_file, "r") as up_file_handle:
        for row in up_file_handle:
            row = row.rstrip()
            if row[:12]=="DE   RecName":
                name = row.split("Full=")[1].split("{")[0]
            if row[:8]=="DR   GO;":
                go_id = row.split("GO; ")[1].split(";")[0]
                get_all_parent_go(go_id)
                go_info = "{0};{1}".format(go_id, godag[go_id].name)
                go_list.append(go_info)
    return name, go_list

def get_all_parent_go(go_id):
    top_3go_dict = {"GO:0005575": "cellular component", "GO:0008150": "biological process", "GO:0003674": "molecular function"}

    go_parent_list = []
    go_dict = {go_id: godag[go_id].name}
    while go_id not in top_3go_dict.keys():
        for one in godag[go_id]._parents:
            go_id = one
            go_dict.update({go_id: godag[go_id].name})

            go_info = "{0};{1}".format(go_id, godag[go_id].name)
            go_parent_list.insert(0, go_info)

    output_file = "data/tmp/all_go_parent.txt"
    with open(output_file, "a") as file_handle:
        print("\t".join(go_parent_list), file=file_handle)

    return go_dict

if __name__=="__main__":
    main()
