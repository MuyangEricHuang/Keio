#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Levenshtein
from Bio.Seq import Seq

def main():
    #pair_gtf_uniprot()
    pair_gtf_pec_essential()
    #pair_gtf_regulondb()

def pair_gtf_uniprot():
    print_list = [["#gene_name", "type", "Levenshtein.ratio", "gtf_query", "uniprot_entry", "count"]]
    #print("\t".join(["#gene_name", "type", "Levenshtein.ratio", "gtf_query", "uniprot_entry", "count"]))

    gtf_gene_name_entry_dict = {}
    gtf_gene_name_seq_dict = {}
    in_file = "data/tmp/gtf.fna"
    #>thrL-1_190_255_fwd_thrL_AIN30539_protein-coding
    with open(in_file, "r") as file_handle:
        for row in file_handle:
            row = row.rstrip()
            if row.startswith(">"):
                entry = row[1:]
                gene_name = row.split("_")[4]
            else:
                seq = str(Seq(row).translate())
                gtf_gene_name_seq_dict[gene_name] = seq
                gtf_gene_name_entry_dict[gene_name] = entry

    uniprot_gene_name_entry_dict = {}
    uniprot_gene_name_seq_dict = {}
    in_file = "data/tmp/uniprot4000over.faa"
    #>sp|P0A7V8|RS4_ECOLI|30S_ribosomal_protein_S4|83333|GN=rpsD
    with open(in_file, "r") as file_handle:
        for row in file_handle:
            row = row.rstrip()
            if row.startswith(">"):
                gene_name = row.split("|")[1]
                if "|GN=" in row:
                    gene_name = row.split("|GN=")[1]
                entry = row[1:]
            else:
                seq = row
                uniprot_gene_name_seq_dict[gene_name] = seq
                uniprot_gene_name_entry_dict[gene_name] = entry

    gene_name_not_found = set([])
    for gene_name, seq in gtf_gene_name_seq_dict.items():
        if gene_name in uniprot_gene_name_seq_dict.keys():
            uniprot_seq = uniprot_gene_name_seq_dict[gene_name]
            query = gtf_gene_name_entry_dict[gene_name]
            entry = uniprot_gene_name_entry_dict[gene_name]
            ratio = Levenshtein.ratio(seq, uniprot_seq)
            if query.endswith("_pseudogene"):
                print_list.append([gene_name, "NAME_PSEUDO", f"{ratio:.3f}", query, entry, "1"])
                #print(gene_name, "NAME_PSEUDO", f"{ratio:.3f}", query, entry, 1, sep="\t")
            elif 0.9<=ratio:
                print_list.append([gene_name, "NAME", f"{ratio:.3f}", query, entry, "1"])
                #print(gene_name, "NAME", f"{ratio:.3f}", query, entry, 1, sep="\t")
            else:
                gene_name_not_found.add(gene_name)
        else:
            gene_name_not_found.add(gene_name)

    for gene_name in gene_name_not_found:
        query = gtf_gene_name_entry_dict[gene_name]
        transcript_id = query.split("_")[5]
        uniprot_blast_file = f"data/tmp/blast/{transcript_id}_uniprot4000over.txt"
        with open(uniprot_blast_file, "r") as file_handle:
            count = 0
            for row in file_handle:
                row = row.rstrip()
                if row.startswith("# Query: "):
                    top_hit = True

                if row.startswith("#"):
                    continue

                col = row.split("\t")
                entry = col[1]
                entry_gene_name = entry.split("|")[1]
                if "|GN=" in row:
                    entry_gene_name = entry.split("|GN=")[1]
                uniprot_seq = uniprot_gene_name_seq_dict[entry_gene_name]
                gtf_seq = gtf_gene_name_seq_dict[gene_name]
                ratio = Levenshtein.ratio(gtf_seq, uniprot_seq)

                if top_hit and 0.9<=ratio:
                    mode = "TOP"
                    if "pseudogene" in query:
                        mode = "TOP_PSEUDO"
                else:
                    continue

                count+=1
                top_hit = False
                print_list.append([gene_name, mode, f"{ratio:.3f}", query, entry, str(count)])
                #print(gene_name, mode, f"{ratio:.3f}", query, entry, count, sep="\t")

            if count==0:
                mode = "NOHIT"
                print_list.append([gene_name, mode, "NOMATCH", query, str(None), str(count)])
                #print(gene_name, mode, "NOMATCH", query, None, count, sep="\t")

    out_file = "data/tmp/gtf_query_uniprot_conversion.txt"
    with open(out_file, "w") as file_handle:
        for one in print_list:
            print("\t".join(one), file=file_handle)

def pair_gtf_pec_essential():
    print_list = [["#gene_name", "type", "Levenshtein.ratio", "gtf_query", "pec_entry", "count"]]
    #print("\t".join(["#gene_name", "type", "Levenshtein.ratio", "gtf_query", "pec_entry", "count"]))

    gtf_gene_name_entry_dict = {}
    gtf_gene_name_seq_dict = {}
    in_file = "data/tmp/gtf.fna"
    #>thrL-1_190_255_fwd_thrL_AIN30539_protein-coding
    with open(in_file, "r") as file_handle:
        for row in file_handle:
            row = row.rstrip()
            if row.startswith(">"):
                entry = row[1:]
                gene_name = row.split("_")[4]
            else:
                seq = str(Seq(row).translate())
                gtf_gene_name_seq_dict[gene_name] = seq
                gtf_gene_name_entry_dict[gene_name] = entry

    pec_gene_name_entry_dict = {}
    pec_gene_name_seq_dict = {}
    in_file = "data/tmp/pec_essential.faa"
    #>ribF_21407_22348_fwd_b0025,ECK0026,JW0023,o312,yaaC_bifunctional-riboflavin-kinase/FAD-synthetase
    with open(in_file, "r") as file_handle:
        for row in file_handle:
            row = row.rstrip()
            if row.startswith(">"):
                gene_name = row[1:].split("_")[0]
                entry = row[1:]
            else:
                seq = row
                pec_gene_name_seq_dict[gene_name] = seq
                pec_gene_name_entry_dict[gene_name] = entry

    gene_name_not_found = set([])
    for gene_name, seq in gtf_gene_name_seq_dict.items():
        if gene_name in pec_gene_name_seq_dict.keys():
            pec_seq = pec_gene_name_seq_dict[gene_name]
            query = gtf_gene_name_entry_dict[gene_name]
            entry = pec_gene_name_entry_dict[gene_name]
            ratio = Levenshtein.ratio(seq, pec_seq)
            print(gene_name, f"{ratio:.3f}", query, entry, sep="\t")
            continue

            if query.endswith("_pseudogene"):
                print_list.append([gene_name, "NAME_PSEUDO", f"{ratio:.3f}", query, entry, "1"])
                #print(gene_name, "NAME_PSEUDO", f"{ratio:.3f}", query, entry, 1, sep="\t")
            elif 0.9<=ratio:
                print_list.append([gene_name, "NAME", f"{ratio:.3f}", query, entry, "1"])
                #print(gene_name, "NAME", f"{ratio:.3f}", query, entry, 1, sep="\t")
            else:
                gene_name_not_found.add(gene_name)
        else:
            gene_name_not_found.add(gene_name)

    for gene_name in gene_name_not_found:
        query = gtf_gene_name_entry_dict[gene_name]
        transcript_id = query.split("_")[5]
        pec_blast_file = f"data/tmp/blast/{transcript_id}_pec_essential.txt"
        with open(pec_blast_file, "r") as file_handle:
            count = 0
            for row in file_handle:
                row = row.rstrip()
                if row.startswith("# Query: "):
                    top_hit = True

                if row.startswith("#"):
                    continue

                col = row.split("\t")
                entry = col[1]
                entry_gene_name = entry.split("_")[0]
                pec_seq = pec_gene_name_seq_dict[entry_gene_name]
                gtf_seq = gtf_gene_name_seq_dict[gene_name]
                ratio = Levenshtein.ratio(gtf_seq, pec_seq)

                if top_hit and 0.9<=ratio:
                    mode = "TOP"
                    if "pseudogene" in query:
                        mode = "TOP_PSEUDO"
                else:
                    continue

                count+=1
                top_hit = False
                print_list.append([gene_name, mode, f"{ratio:.3f}", query, entry, str(count)])
                #print(gene_name, mode, f"{ratio:.3f}", query, entry, count, sep="\t")

            if count==0:
                mode = "NOHIT"
                print_list.append([gene_name, mode, "NOMATCH", query, str(None), str(count)])
                #print(gene_name, mode, "NOMATCH", query, None, count, sep="\t")

    out_file = "data/tmp/gtf_query_pec_essential_conversion.txt"
    with open(out_file, "w") as file_handle:
        for one in print_list:
            print("\t".join(one), file=file_handle)

def pair_gtf_regulondb():
    print_list = [["#gene_name", "type", "Levenshtein.ratio", "gtf_query", "regulondb_entry", "count"]]
    #print("\t".join(["#gene_name", "type", "Levenshtein.ratio", "gtf_query", "regulondb_entry", "count"]))

    gtf_gene_name_entry_dict = {}
    gtf_gene_name_seq_dict = {}
    in_file = "data/tmp/gtf.fna"
    #>thrL-1_190_255_fwd_thrL_AIN30539_protein-coding
    with open(in_file, "r") as file_handle:
        for row in file_handle:
            row = row.rstrip()
            if row.startswith(">"):
                entry = row[1:]
                gene_name = row.split("_")[4]
            else:
                #seq = str(Seq(row).translate())
                seq = row
                gtf_gene_name_seq_dict[gene_name] = seq
                gtf_gene_name_entry_dict[gene_name] = entry

    regulondb_gene_name_entry_dict = {}
    regulondb_gene_name_seq_dict = {}
    in_file = "data/tmp/regulondb.fna"
    #>ECK120001251-thrL(b0001)-190-255-fwd-ECK0001,EG11277,b0001-ECK120005727-EG11277_MONOMER-NP_414542-P0AD86-<i>thr</i>_operon_leader_peptide
    with open(in_file, "r") as file_handle:
        for row in file_handle:
            row = row.rstrip()
            if row.startswith(">"):
                gene_name = row[1:].split("-")[1].split("(")[0]
                if gene_name=="Phantom_Gene":
                    gene_naeme = row[1:].split("-")[1].split("(")[1].split(")")[0]
                entry = row[1:]
            else:
                seq = row
                regulondb_gene_name_seq_dict[gene_name] = seq
                regulondb_gene_name_entry_dict[gene_name] = entry

    gene_name_not_found = set([])
    for gene_name, seq in gtf_gene_name_seq_dict.items():
        if gene_name in regulondb_gene_name_seq_dict.keys():
            regulondb_seq = regulondb_gene_name_seq_dict[gene_name]
            query = gtf_gene_name_entry_dict[gene_name]
            entry = regulondb_gene_name_entry_dict[gene_name]
            ratio = Levenshtein.ratio(seq, regulondb_seq)
            if query.endswith("_pseudogene"):
                print_list.append([gene_name, "NAME_PSEUDO", f"{ratio:.3f}", query, entry, "1"])
                #print(gene_name, "NAME_PSEUDO", f"{ratio:.3f}", query, entry, 1, sep="\t")
            elif 0.9<=ratio:
                print_list.append([gene_name, "NAME", f"{ratio:.3f}", query, entry, "1"])
                #print(gene_name, "NAME", f"{ratio:.3f}", query, entry, 1, sep="\t")
            else:
                gene_name_not_found.add(gene_name)
        else:
            gene_name_not_found.add(gene_name)

    for gene_name in gene_name_not_found:
        query = gtf_gene_name_entry_dict[gene_name]
        transcript_id = query.split("_")[5]
        regulondb_blast_file = f"data/tmp/blast/{transcript_id}_regulondb.txt"
        with open(regulondb_blast_file, "r", encoding="utf-8") as file_handle:
            count = 0
            for row in file_handle:
                row = row.rstrip()
                if row.startswith("# Query: "):
                    top_hit = True

                if row.startswith("#"):
                    continue

                col = row.split("\t")
                entry = col[1]
                entry_gene_name = entry.split("-")[1].split("(")[0]
                regulondb_seq = regulondb_gene_name_seq_dict[entry_gene_name]
                gtf_seq = gtf_gene_name_seq_dict[gene_name]
                ratio = Levenshtein.ratio(gtf_seq, regulondb_seq)

                if top_hit and 0.9<=ratio:
                    mode = "TOP"
                    if "pseudogene" in query:
                        mode = "TOP_PSEUDO"
                else:
                    continue

                count+=1
                top_hit = False
                print_list.append([gene_name, mode, f"{ratio:.3f}", query, entry, str(count)])
                #print(gene_name, mode, f"{ratio:.3f}", query, entry, count, sep="\t")

            if count==0:
                mode = "NOHIT"
                print_list.append([gene_name, mode, "NOMATCH", query, str(None), str(count)])
                #print(gene_name, mode, "NOMATCH", query, None, count, sep="\t")

    out_file = "data/tmp/gtf_query_regulondb_conversion.txt"
    with open(out_file, "w", encoding="utf-8") as file_handle:
        for one in print_list:
            print("\t".join(one), file=file_handle)

if __name__=="__main__":
    main()
