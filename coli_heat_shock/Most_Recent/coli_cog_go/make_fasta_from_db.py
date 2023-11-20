#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from Bio import SeqIO
from Bio.Seq import Seq

def main():
    #make_gtf_fna()
    #make_regulondb_fna()
    make_pec_faa()
    #make_uniprot_faa()

def make_gtf_fna():
    in_file = "data/raw/Escherichia_coli_bw25113.ASM75055v1.dna.toplevel.fa"
    with open(in_file, "rU") as file_handle:
        for seq_record in SeqIO.parse(file_handle, "fasta"):
            genome_seq = seq_record.seq

    entry_seq_dict = {}
    #Chromosome      ena     transcript      190     255     .       +       .       gene_id "BW25113_0001"; transcript_id "AIN30539"; gene_name "thrL"; gene_source "ena"; gene_biotype "protein_coding"; transcript_name "thrL-1"; transcript_source "ena"; transcript_biotype "protein_coding";
    in_file = "data/raw/Escherichia_coli_bw25113.ASM75055v1.44.gtf"
    with open(in_file, "r") as file_handle:
        for row in file_handle:
            row = row.rstrip()
            if row.startswith("#"):
                continue
            col = row.split("\t")
            feature_type = col[2]
            if feature_type!="transcript":
                continue
            start, end = int(col[3]), int(col[4])
            strand = col[6]
            if strand=="+":
                strand = "fwd"
                seq = str(genome_seq[start-1:end])
            else:
                strand = "rev"
                seq = str(genome_seq[start-1:end].complement())[::-1]

            ids = col[8]
            id_symbols = ["transcript_id", "gene_name", "transcript_name", "transcript_biotype"]
            additional_ids = {id_symbol: None for id_symbol in id_symbols}
            for id_symbol in id_symbols:
                if id_symbol in ids:
                    additional_ids[id_symbol] = ids.split(f'{id_symbol} "')[1].split('";')[0]

            gene_name = additional_ids["gene_name"]
            transcript_id = additional_ids["transcript_id"].replace("_", "-")
            transcript_name = additional_ids["transcript_name"].replace("_", "-")
            transcript_biotype = additional_ids["transcript_biotype"].replace("_", "-")
            
            entry = f"{transcript_name}_{start}_{end}_{strand}_{gene_name}_{transcript_id}_{transcript_biotype}"
            entry_seq_dict[entry] = seq

    out_file = "data/tmp/gtf.fna"
    with open(out_file, "w") as file_handle:
        for entry, seq in entry_seq_dict.items():
            print(f">{entry}\n{seq}", file=file_handle)

def make_regulondb_fna():
    gene_id_others_dict = defaultdict(lambda: "NoOtherID")
    #ECK120001251    thrL    190     255     forward ECK0001,EG11277,b0001   STRING:511145.b0001, ASAP:ABE-0000006, ECHOBASE:EB1255, OU-MICROARRAY:b0001, REGULONDB:b0001, ECOLIHUB:thrL,    ECK120005727    <i>thr</i> operon leader peptide        ThrL    ECOCYC:EG11277-MONOMER, INTERPRO:IPR011720, REFSEQ:NP_414542, PRIDE:P0AD86, UNIPROT:P0AD86, PFAM:PF08254, ECOLIWIKI:b0001,
    in_file = "data/raw/GeneProductAllIdentifiersSet.txt"
    with open(in_file, "r") as file_handle:
        for row in file_handle:
            row = row.rstrip()
            if row.startswith("#"):
                continue
            col = row.split("\t")
            gene_id = col[0]
            synonyms = col[5]
            product_id = col[7]
            product_name = col[9]

            product_db_ids = col[10]
            id_symbols = ["ECOCYC", "REFSEQ", "UNIPROT"]
            additional_ids = {id_symbol: None for id_symbol in id_symbols}
            for id_symbol in id_symbols:
                if f"{id_symbol}:" in product_db_ids:
                    additional_ids[id_symbol] = product_db_ids.split(f"{id_symbol}:")[1].split(",")[0].replace("-", "_")

            others = f"{synonyms}-{product_id}-" + "-".join([str(additional_ids[id_symbol]) for id_symbol in id_symbols])
            gene_id_others_dict[gene_id] = others


    entry_seq_dict = {}
    #ECK120001251    thrL(b0001)     190     255     forward -       <i>thr</i> operon leader peptide        ATG     TGA     ATGAAACGCATTAGCACCACCATTACCACCACCATCACCATTACCACAGGTAACGGTGCGGGCTGA      b0001 
    in_file = "data/raw/Gene_sequence.txt"
    with open(in_file, "r") as file_handle:
        for row in file_handle:
            row = row.rstrip()
            if row.startswith("#"):
                continue
            col = row.split("\t")
            gene_id = col[0]
            others = gene_id_others_dict[gene_id]

            product = None
            if 6<len(col):
                product = col[6]
                if product:
                    product = product.replace("-", "_").replace(" ", "_")
                else:
                    product = None
            entry = "-".join(col[:5]).replace("forward", "fwd").replace("reverse", "rev") + f"-{others}-{product}"
            entry = entry.replace(" ", "_")
            if 8<len(col):
                seq = col[9]
                entry_seq_dict[entry] = seq
            else:
                print(f"{col} is not included in fasta.")

    out_file = "data/tmp/regulondb.fna"
    with open(out_file, "w") as file_handle:
        for entry, seq in entry_seq_dict.items():
            print(f">{entry}\n{seq}", file=file_handle)

def make_pec_faa():
    entry_conversion_dict = {}
    #Orf ID  Feature Type(1:gene 2:rRNA 3:tRNA 4:ncRNA 7:tmRNA 8:sRNA)       Orf     Alternative name        MapPosition     Start(BP)       End(BP) Length(BP)      Direction(0:+ 1:-)      Class(1:essential 2:noessential 3:unknown)      PID     Product PMID
    #1       1       thrL    b0001,ECK0001,JW4367    0.004095110110938549    190     255     66      0       2       1786182 thr operon leader peptide 
    in_file = "data/raw/PECData.data"
    with open(in_file, "r") as file_handle:
        for row in file_handle:
            row = row.rstrip()
            if row.startswith("Orf ID"):
                continue
            col = row.split("\t")

            feature_type = int(col[1])
            essential_class = int(col[9])
            if feature_type!=1 or essential_class!=1:
                continue

            orf = col[2]
            alt_name = col[3].replace("_", "-")
            start = int(col[5])
            end = int(col[6])
            strand = "fwd"
            if col[8]=="1":
                strand = "rev"
            product = col[11].replace("_", "-").replace(" ", "-")
            #entry = f"{orf}-{start}-{end}"
            entry = f"{start}-{end}"
            entry2 = "_".join([orf, str(start), str(end), strand, alt_name, product])
            entry_conversion_dict[entry] = entry2
           
    entry_seq_dict = {}
    #>thrL(Gene,190...255,non_essential)
    #MKRISTTITTTITITTGNGAG
    in_file = "data/raw/pecv4_gene_aa.fas"
    with open(in_file, "r") as file_handle:
        entry_flag = False
        for row in file_handle:
            row = row.rstrip()
            if row.startswith(">"):
                entry = row[1:]
                orf = entry.split("(")[0]
                start = entry.split("...")[0].split(",")[1]
                end = entry.split("...")[1].split(",")[0]
                #entry = f"{orf}-{start}-{end}"
                entry = f"{start}-{end}"
                if entry in entry_conversion_dict.keys():
                    entry_flag = True
                    entry = entry_conversion_dict[entry]
            elif entry_flag:
                seq = row
                entry_seq_dict[entry] = seq
                entry_flag = False

    out_file = "data/tmp/pec_essential.faa"
    with open(out_file, "w") as file_handle:
        for entry, seq in entry_seq_dict.items():
            print(f">{entry}\n{seq}", file=file_handle)

def make_uniprot_faa():
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
