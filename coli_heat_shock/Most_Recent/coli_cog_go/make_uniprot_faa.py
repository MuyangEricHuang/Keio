#!/usr/bin/env python
# -*- coding: utf-8 -*-

def main():
    entry_seq_dict = {}
    is_uniprot_id_list = []
    is_keyword_list = ["Insertion element IS", "Transposase Ins", "Putative transposase", "transposase ins", "insertion element IS", "Prophage integrase Int"]
    in_file = "data/tmp/revised_uniprot_fasta_seq_list.txt"
    with open(in_file, "r") as file_handle:
        for row in file_handle:
            row = row.rstrip()
            if row.startswith("File#") or row.startswith("1"):
                continue
            col = row.split("\t")
            entry = col[3]
            up_id = col[4]
            seq = col[8]
            redundant_num = int(col[9])
            redundant_ids = col[10]

            is_flag = False
            for one in is_keyword_list:
                if one in entry:
                    is_flag = True
            if is_flag:
                is_uniprot_id_list.append(up_id)
                continue

            if entry[0]=='"':
                entry = entry[1:]
            if entry[-1]=='"':
                entry = entry[:-1]

            first = entry.split(" OS=")[0]
            first = first.split(" ")[0] + "|"  + "_".join(first.split(" ")[1:])
            second = entry.split(" OX=")[1].split(" PE=")[0].replace(" ", "|")
            gene_name = up_id
            if "GN=" in second:
                gene_name = second.split("GN=")[1]
            entry = first + "|" + second

            entry_seq_dict[entry] = seq

    print(f"{len(is_uniprot_id_list)} uniprot id are excluded: {is_uniprot_id_list}")

    out_file = "data/tmp/uniprot4000over.faa"
    with open(out_file, "w") as file_handle:
        for entry, seq in entry_seq_dict.items():
            print(f"{entry}\n{seq}", file=file_handle)

if __name__=="__main__":
    main()
