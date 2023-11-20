#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict

def main():
    pro_gene_id_vals = make_protein_vals()
    tra_gene_id_vals = make_mrna_vals()
    common_id_list = list(set(pro_gene_id_vals) & set(tra_gene_id_vals))

    header_line = "\t".join(["#gene_id"] + [f"H{i}" for i in range(1,12)])

    out_file = "data/tmp/peca/common_id_proteome.txt"
    with open(out_file, "w") as file_handle:
        print(header_line, file=file_handle)
        for gene_id in common_id_list:
            vals = pro_gene_id_vals[gene_id]
            print(gene_id, "\t".join(vals), sep="\t", file=file_handle)

    out_file = "data/tmp/peca/common_id_transcriptome.txt"
    with open(out_file, "w") as file_handle:
        print(header_line, file=file_handle)
        for gene_id in common_id_list:
            vals = tra_gene_id_vals[gene_id]
            print(gene_id, "\t".join(vals), sep="\t", file=file_handle)

def get_id_conversion_table():
    tra_conversion_table = {}
    pro_conversion_table = {}
    ##gene_name      type    Levenshtein.ratio       gtf_query       uniprot_entry   count
    #thrL    NAME    0.977   thrL-1_190_255_fwd_thrL_AIN30539_protein-coding sp|P0AD86|LPT_ECOLI|thr_operon_leader_peptide|83333|GN=thrL     1
    in_file = "data/tmp/gtf_query_uniprot_conversion.txt"
    with open(in_file, "r") as file_handle:
        for row in file_handle:
            row = row.rstrip()
            if row.startswith("#"):
                continue
            col = row.split("\t")
            gene_id = col[0]
            hit_type = col[1]
            if ("_PSEUDO" in hit_type) or (hit_type=="NOHIT"):
                continue

            tra_id = col[3].split("_")[5]
            pro_id = col[4].split("|")[1]
            tra_conversion_table[tra_id] = gene_id
            pro_conversion_table[pro_id] = gene_id
    return tra_conversion_table, pro_conversion_table

def make_protein_vals():
    tra_conversion_table, pro_conversion_table = get_id_conversion_table()

    #A5A614  YCIZ_ECOLI      UPF0509 protein YciZ    #yciZ   N       1.241   1.003   0.961   1.003   0.881   0.929   0.843   1.548   0.97    1.2     1.362   1.418   1.13    1.199   1.31    1.009   0.924   0.902
    gene_id_vals = {}
    in_file = "data/tmp/proteome_expression.txt"
    with open(in_file, "r") as file_handle:
        for row in file_handle:
            row = row.rstrip()
            col = row.split("\t")
            pro_id = col[0]
            vals = col[12:]

            if pro_id not in pro_conversion_table.keys():
                continue
            if "---" in vals:
                continue
            gene_id = pro_conversion_table[pro_id]
            gene_id_vals[gene_id] = vals

    return gene_id_vals

def make_mrna_vals():
    tra_conversion_table, pro_conversion_table = get_id_conversion_table()

    #gene_id transcript_id(s)    length  effective_length    expected_count  TPM FPKM
    #BW25113_0001_thrL   AIN30539_thrL-1 66.00   0.00    0.00    0.00    0.00
    gene_id_tpm_dict = defaultdict(lambda: [])
    for index in range(1, 12):
        input_file = f"../all/data/tmp/rsem/{index}_expression.genes.results"
        with open(input_file, "r") as file_handle:
            for row in file_handle:
                row = row.rstrip()
                if row.startswith("gene_id"):
                    continue
                col = row.split("\t")
                tpm = col[5]

                tra_id = col[1].split("_")[0]
                if tra_id not in tra_conversion_table.keys():
                    continue
                gene_id = tra_conversion_table[tra_id]
                gene_id_tpm_dict[gene_id].append(tpm)

    gene_id_vals = {}
    for gene_id, tpm_list in gene_id_tpm_dict.items():
        tpm_set = set(tpm_list)
        #if len(tpm_set)==1 and tpm_list[0]=="0.00":
        #    continue
        if "0.00" in tpm_set:
            continue
        gene_id_vals[gene_id] = tpm_list
    return gene_id_vals

if __name__=="__main__":
    main()
