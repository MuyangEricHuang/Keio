#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DE   RecName: Full=thr operon leader peptide {ECO:0000255|HAMAP-Rule:MF_01907};
DR   GO; GO:0005886; C:plasma membrane; IEA:UniProtKB-SubCell.
DR   GO; GO:0009242; P:colanic acid biosynthetic process; IMP:EcoCyc.
DR   eggNOG; COG1869; LUCA.
"""

from goatools.obo_parser import GODag
godag = GODag("data/raw/go-basic.obo")

#P00561  AK1H_ECOLI      820     thrAthrA1;thrA2
def main():
    cog_id_class_dict = classify_cog_class()
    print_list = []

    #>sp|P0A7V8|RS4_ECOLI|30S_ribosomal_protein_S4|83333|GN=rpsD
    in_file = "data/tmp/uniprot4000over.faa"
    with open(in_file, "r") as file_handle:
        for row in file_handle:
            row = row.rstrip()
            if not row.startswith(">"):
                continue
            col = row[4:].split("|")
            up_id = col[0]
            if up_id=="P46121":
                continue
            up_info = get_up_info(up_id, cog_id_class_dict)

            up_id2 = up_info["id"]
            if col[1]==up_id2:
                up_id2 = "SAME_ID"
            up_name = up_info["name"].replace(" ", "_")
            if col[2] in up_name:
                up_name = "SAME_NAME"

            print_str = ["\t".join([col[-1]] + col[:-1]), 
                        up_id2,
                        up_name,
                        "|".join(up_info["go"]), 
                        "|".join(up_info["cog"])
                        ]
            print_list.append("\t".join(print_str))

    out_file = "data/tmp/uniprot4000over_with_gocog.txt"
    with open(out_file, "w") as file_handle:
        for one in print_list:
            print(one, file=file_handle)

def get_up_info(up_id, cog_id_class_dict):
    cog_list = []
    go_set = set([])
    bnumber = None
    name = None

    #ID   TRHO_ECOLI              Reviewed;         350 AA.
    #GN   Name=rpsL; Synonyms=strA; OrderedLocusNames=b3342, JW3304;
    up_file = f"data/raw/uniprot4000over/{up_id}.txt"
    with open(up_file, "r") as file_handle:
        for row in file_handle:
            row = row.rstrip()
            if row[:5]=="ID   ":
                id_in_txt = row.split("ID   ")[1].split(" ")[0]
            if row[:12]=="DE   RecName":
                name = row.split("Full=")[1].split("{")[0]
            if row[:16]=="DR   eggNOG; COG":
                cog_id = row.split("eggNOG; ")[1].split(";")[0]

                cog_info = "{0};{1}".format(cog_id, cog_id_class_dict[cog_id])
                cog_list.append(cog_info)

            if row[:8]=="DR   GO;":
                go_id = row.split("GO; ")[1].split(";")[0]
                go_parent_list = get_all_parent_go(go_id)
                for go_info in go_parent_list:
                    go_set.add(go_info)

            if "OrderedLocusNames=" in row:
                bnumber = row.split("OrderedLocusNames=")[1].split(";")[0]

    go_list = sorted(list(go_set), key=lambda x: x.split("GO:")[1].split(";")[0])

    up_info = {"id": id_in_txt, "name": name, "cog": cog_list, "go": list(go_set), "bnumber": bnumber}
    return up_info

#COG0001 H       Glutamate-1-semialdehyde aminotransferase       HemL    Heme biosynthesis               2CFB
def classify_cog_class():
    cog_id_class_dict = {}
    in_file = "data/tmp/edited_cog20.def.tab"
    with open(in_file, "r") as file_handle:
        for row in file_handle:
            row = row.rstrip()
            if row[0]=="#":
                continue
            cog_id = row.split("\t")[0]
            cog_class = row.split("\t")[1].replace(" ", "")
            cog_id_class_dict.update({cog_id: cog_class})
    return cog_id_class_dict

def get_all_parent_go(go_id):
    top_3go_dict = {"GO:0005575": "cellular component", "GO:0008150": "biological process", "GO:0003674": "molecular function"}
    go_parent_list = []

    if go_id not in godag.keys():
        return go_parent_list

    go_name = godag[go_id].name
    go_dict = {go_id: go_name}
    while go_id not in top_3go_dict.keys():
        for one in godag[go_id]._parents:
            go_id = one
            go_dict.update({go_id: godag[go_id].name})

            go_info = "{0};{1}".format(go_id, godag[go_id].name)
            go_parent_list.insert(0, go_info)

    out_file = "data/tmp/all_go_parent.txt"
    with open(out_file, "a") as file_handle:
        print("\t".join(go_parent_list), file=file_handle)

    return go_parent_list

if __name__=="__main__":
    main()
