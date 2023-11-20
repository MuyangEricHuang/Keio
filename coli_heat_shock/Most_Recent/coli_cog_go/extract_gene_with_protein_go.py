#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""
ecoli_from_uniprot_reviesd_withGO.txt
P0AD86  LPT_ECOLI       21      thrL    thr operon leader peptide       GO:0009088;threonine biosynthetic process|GO:0031555;transcriptional attenuation|GO:0031556;transcriptional attenuation by ribosome
"""
from collections import defaultdict

def main():
    our_up_ids = get_our_up_ids() #set
    selcted_go_dict = get_selected_go_dict() #dict
    selected_go_parent_info = get_selected_go_parent_info(selcted_go_dict)

    print_list = []
    input_file = "data/tmp/ecoli_from_uniprot_reviesd_with_gocog.txt"
    for one in selected_go_parent_info.keys():
        go_id = one.split("\t")[-1].split(";")[0]

        with open(input_file, "r") as file_handle:
            for row in file_handle:
                row = row.rstrip()
                up_id = row.split("\t")[0]
                if up_id not in our_up_ids:
                    continue
                if go_id in row:
                    division = "|".join(list(set(selected_go_parent_info[one])))
                    go_ids = "|".join(one.split("\t"))
                    print_str = "{0}\t{1}\t{2}".format(row, division, go_ids)
                    print_list.append(print_str)

    output_file = "data/tmp/ecoli_from_uniprot_reviesd_with_protein_gocog.txt"
    with open(output_file, "w") as file_handle:
        for one in print_list:
            print(one, file=file_handle)

def get_our_up_ids():
    input_file = "data/tmp/our_proteome_uniprot_ids.txt"
    with open(input_file, "r") as file_handle:
        our_up_ids = set(file_handle.read().split("\n"))
    return our_up_ids

def get_selected_go_dict():
#    selected_go_dict = {}
#    input_file = "data/tmp/selected_go_list.txt"
#    with open(input_file, "r") as file_handle:
#        for row in file_handle:
#            row = row.rstrip()
#            col = row.split(";")
#            go_id = col[1]
#            division = col[0]
#            selected_go_dict.update({go_id: division})
    selected_go_dict = {"GO:0006508": "proteolysis", "GO:0015031": "protein transport"}
    return selected_go_dict

def get_selected_go_parent_info(selected_go_dict):
    selected_go_parent_info = defaultdict(lambda: [])
    input_file = "data/tmp/all_go_parent.txt"
    with open(input_file, "r") as file_handle:
        for row in file_handle:
            row = row.rstrip()
            for go_id in selected_go_dict.keys():
                if go_id in row:
                    selected_go_parent_info[row].append(selected_go_dict[go_id])
    return selected_go_parent_info

if __name__=="__main__":
    main()
