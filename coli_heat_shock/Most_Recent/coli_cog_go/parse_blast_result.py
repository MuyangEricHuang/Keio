#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob

def main():
    query_gtf_conversion = {}
    query_type = {}
    files = glob.glob("data/raw/uniprot/*.txt")
    for afile in files:
        name = afile.split("/")[-1].split(".")[0]
        gtf_file = f"data/tmp/blast/{name}_gtf.txt"
        pec_file = f"data/tmp/blast/{name}_pec_essential.txt"
        regulondb_file = f"data/tmp/blast/{name}_regulondb.txt"

        #if name!="P77173":
        #if name!="P76349":
        #if name!="P46889":
        #if name!="P36930":
        #    continue

        ## Fields: query acc.ver, subject acc.ver, % identity, alignment length, mismatches, gap opens, q. start, q. end, s. start, s. end, evalue, bit score, identical, query length, subject length, query seq, subject seq
        #sp|P27431|ROXA_ECOLI 50S ribosomal protein L16 3-hydroxylase OS=Escherichia coli (strain K12) OX=83333 GN=roxA PE=1 SV=2
        with open(gtf_file, "r") as file_handle:
            count = 0
            for row in file_handle:
                row = row.rstrip()
                if row.startswith("# Query: "):
                    query = row.split("Query: ")[1]
                    first = query.split(" OS=")[0]
                    first = first.split(" ")[0] + "|"  + "_".join(first.split(" ")[1:])
                    second = query.split(" OX=")[1].split(" PE=")[0].replace(" ", "|")
                    gene_name = second.split("GN=")[1]
                    query = first + "|" + second
                    top_hit = True

                if row.startswith("#"):
                    continue
                if "BIPA_ECO27" in query:
                    continue
                if "gndA" in query:
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

                if (f"_{gene_name}_" in entry) and (98<=identity):
                    mode = "NAME"
                    if "pseudogene" in entry:
                        mode = "NAME_PSEUDO"
                elif top_hit and (98<=identity):
                    mode = "TOP"
                    if "pseudogene" in entry:
                        mode = "TOP_PSEUDO"
                else:
                    continue

                count+=1
                top_hit = False
                query_gtf_conversion[query] = entry
                query_type[query] = mode
                #print(gene_name, mode, count, query, entry, f"{identity:.2f}", evalue, f"{bit_score:.2f}", \
                #    f"{qstart_coverage:.2f}", f"{qend_coverage:.2f}", f"{qcoverage:.2f}", f"{qlength}*3={qlength*3}", \
                #    f"{sstart_coverage:.2f}", f"{send_coverage:.2f}", f"{scoverage:.2f}", slength, \
                #sep="\t")

            if count==0:
                mode = "NOHIT"
                query_gtf_conversion[query] = None
                query_type[query] = mode
                #print(gene_name, mode, count, query, sep="\t")

            if ("INSE1_ECOLI" in query) or ("INSI1_ECOLI" in query) or ("EFTU1_ECOLI" in query):
                query_type[query]= "MULTICOPY"

    out_file = "data/tmp/uniprot_query_gtf_conversion.txt"
    with open(out_file, "w") as file_handle:
        print("#uniprot_query", "gtf_info", "type", sep="\t", file=file_handle)
        for query, gtf_info in query_gtf_conversion.items():
            print(query, gtf_info, query_type[query], sep="\t", file=file_handle)

if __name__=="__main__":
    main()
