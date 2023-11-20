#!/usr/bin/bash
# Last update: 11/05/2020
set -eu pipefail

# E.coli data
wget -O data/raw/ec.fa.gz ftp://ftp.ensemblgenomes.org/pub/bacteria/release-48/fasta/bacteria_87_collection/escherichia_coli_bw25113/dna/Escherichia_coli_bw25113.ASM75055v1.dna.toplevel.fa.gz
wget -O data/raw/ec.gtf.gz ftp://ftp.ensemblgenomes.org/pub/bacteria/release-48/gtf/bacteria_87_collection/escherichia_coli_bw25113/Escherichia_coli_bw25113.ASM75055v1.48.gtf.gz
gunzip data/raw/ec.fa.gz
gunzip data/raw/ec.gtf.gz
cat data/raw/ec.gtf | awk '{OFS = "\t"} {print $1,$4,$5,$3,$6,$7}' > data/raw/ec.bed

# mRNA-seq
mkdir -p data/tmp/trimmed_fq_fastp
mkdir -p data/tmp/rsem_200908
qsub scripts/do_fastp_200908.sh
rsem-prepare-reference --num-threads 32 --gtf data/raw/ec.gtf data/raw/ec.fa --bowtie2 --bowtie2-path ~/opt/ data/tmp/rsem_200908/ec_rsem_ref
qsub scripts/do_rsem_200908.sh 
python scripts/shape_mrna_amount_200909.py

mkdir -p data/tmp/bed_201105
for one in $(less data/tmp/transcriptome_ex_missing_val.txt | cut -f1); do echo -e ${one} $(grep ${one} ../19-08-24_ecoli_cog_go/data/tmp/ecoli_from_uniprot_reviesd.txt); done > data/tmp/ecoli_from_uniprot_reviesd_with_transcript_name.txt
