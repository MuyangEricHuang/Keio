#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last update: 03/11/2022

from collections import defaultdict

def main():
    #gene_id transcript_id(s)    length  effective_length    expected_count  TPM FPKM
    #BW25113_0001_thrL   AIN30539_thrL-1 66.00   0.00    0.00    0.00    0.00

    gene_id_tpm_dict = defaultdict(lambda: [])
    for index in range(1, 12):
        input_file = "data/tmp/rsem_200908/{}_expression.genes.results".format(index)
        with open(input_file, "r") as file_handle:
            for row in file_handle:
                row = row.rstrip()
                if row.startswith("gene_id"):
                    continue
                col = row.split("\t")
                gene_id = col[0]
                gene_id_short = gene_id.split("_")[-1]
                if "ins" in gene_id_short:
                    # insertion sequence
                    continue
                tpm = col[5]
                gene_id_tpm_dict[gene_id_short].append(tpm)

    output_file = "data/tmp/transcriptome_ex_missing_val.txt"
    with open(output_file, "w") as file_handle:
        for gene_id, tpm_list in gene_id_tpm_dict.items():
            tpm_set = set(tpm_list)
            if len(tpm_set)==1 and tpm_list[0]=="0.00":
                continue
            print(gene_id, "\t".join(tpm_list), sep="\t", file=file_handle)

if __name__=="__main__":
    main()
