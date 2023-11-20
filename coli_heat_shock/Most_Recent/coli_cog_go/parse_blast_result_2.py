#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob

def main():
    query_gtf_conversion = {}
    query_type = {}

    name_list = []
    in_file = "data/tmp/gtf.fna"
    with open(in_file, "r") as file_handle:
        for row in file_handle:
            row = row.rstrip()
            if not row.startswith(">"):
                continue
            name = row.split("_")[5]
            name_list.append(name)

    for name in name_list:
        uniprot_file = f"data/tmp/blast/{name}_uniprot4000over.txt"
        pec_file = f"data/tmp/blast/{name}_pec_essential.txt"
        regulondb_file = f"data/tmp/blast/{name}_regulondb.txt"

        #if name!="P77173":
        #if name!="P76349":
        #if name!="P46889":
        #if name!="P36930":
        #    continue

    # Fields: query acc.ver, subject acc.ver, % identity, alignment length, mismatches, gap opens, q. start, q. end, s. start, s. end, evalue, bit score, identical, query length, subject length, query seq, subject seq
    #hofB-1_112201_113586_rev_hofB_AIN30637_protein-coding   sp|P36645|HOFB_ECOLI|Protein_transport_protein_HofB_homolog|83333|GN=hofB       100.000 461     0       0       1       1383    1       461     0.0     937     461     1386    461    MNIPQLTALCL   MNIPQLTALCLRYHGVLLDAS
        with open(uniprot_file, "r") as file_handle:
            count = 0
            for row in file_handle:
                row = row.rstrip()
                if row.startswith("# Query: "):
                    query = row.split("# Query: ")[1]
                    gene_name = row.split("_")[4]
                    top_hit = True

                if row.startswith("#"):
                    continue

                col = row.split("\t")
                entry = col[1]
                identity = float(col[2])
                evalue = col[10]
                bit_score = float(col[11])

                qstart, qend, qlength = int(col[6]), int(col[7]), int(col[13])
                qstart_coverage = qstart / qlength
                qend_coverage = qend / qlength
                qcoverage = qend_coverage - qstart_coverage
                sstart, send, slength = int(col[8]), int(col[9]), int(col[14])
                sstart_coverage = sstart / slength
                send_coverage = send / slength
                scoverage = send_coverage - sstart_coverage

                over_th_coverage = (0.65<=qcoverage) and (0.65<=scoverage)
                if entry.endswith(f"|GN={gene_name}") and (97<=identity):
                    mode = "NAME"
                    if "torI" in entry:
                        print(entry)
                    if "pseudogene" in query:
                        mode = "NAME_PSEUDO"
                elif top_hit and (98<=identity) and (over_th_coverage):
                    mode = "TOP"
                    if "pseudogene" in query:
                        mode = "TOP_PSEUDO"
                else:
                    continue

                count+=1
                top_hit = False
                query_gtf_conversion[query] = entry
                query_type[query] = mode
                print(gene_name, mode, count, query, entry, f"{identity:.2f}", evalue, f"{bit_score:.2f}", \
                    f"{qstart_coverage:.2f}", f"{qend_coverage:.2f}", f"{qcoverage:.2f}", qlength, \
                    f"{sstart_coverage:.2f}", f"{send_coverage:.2f}", f"{scoverage:.2f}", f"{slength}*3={slength*3}", \
                sep="\t")

            if count==0:
                mode = "NOHIT"
                query_gtf_conversion[query] = None
                query_type[query] = mode
                print(gene_name, mode, count, query, sep="\t")

            if ("INSE1_ECOLI" in query) or ("INSI1_ECOLI" in query) or ("EFTU1_ECOLI" in query):
                query_type[query]= "MULTICOPY"

    out_file = "test.txt"
    with open(out_file, "w") as file_handle:
        print("#uniprot_query", "gtf_info", "type", sep="\t", file=file_handle)
        for query, gtf_info in query_gtf_conversion.items():
            print(query, gtf_info, query_type[query], sep="\t", file=file_handle)

if __name__=="__main__":
    main()
