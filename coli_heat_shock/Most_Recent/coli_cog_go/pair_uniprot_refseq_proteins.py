#!/usr/bin/env python
# -*- coding: utf-8 -*-

#P00561  AK1H_ECOLI      820     thrAthrA1;thrA2
def main():
    uniprot_refseq_id_dict = {}
    input_file = "data/tmp/ecoli_from_uniprot_reviesd_with_gocog.txt"
    with open(input_file, "r") as ecoli_file_handle:
        #P0AD86  LPT_ECOLI       21      thrL    thr operon leader peptide               GO:0009088;threonine biosynthetic process|GO:
        for row in ecoli_file_handle:
            row = row.rstrip()
            col = row.split("\t")
            up_id = col[0]
            refseq_id = get_uniprot_refseq_id(up_id)
            uniprot_refseq_id_dict.update({up_id: refseq_id})

    output_file = "data/tmp/ecoli_uniprot_refseq_id.txt"
    with open(output_file, "w") as file_handle:
        for up_id, refseq_id in uniprot_refseq_id_dict.items():
            print(up_id, refseq_id, sep="\t", file=file_handle)

def get_uniprot_refseq_id(uniprot_id):
    up_file = f"data/raw/uniprot/{uniprot_id}.txt"
    refseq_id = None
    with open(up_file, "r") as up_file_handle:
        #GN   Name=rpsL; Synonyms=strA; OrderedLocusNames=b3342, JW3304;
        #DR   RefSeq; NP_416621.1; NC_000913.3.
        #DR   RefSeq; WP_000356817.1; NZ_LN832404.1.
        for row in up_file_handle:
            row = row.rstrip()
            if ("DR   RefSeq;" in row) and ("WP_" in row):
                for one in row.split("DR   RefSeq;")[1].split("; "):
                    if "WP_" in one:
                        refseq_id = one
                break
    return refseq_id

if __name__=="__main__":
    main()
