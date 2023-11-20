#!/usr/bin/bash
# Last update: 02/23/2022
set -eu pipefail

mkdir -p data/log scripts

wget -O data/bw25113.fna.gz ftp://ftp.ensemblgenomes.org/pub/bacteria/release-48/fasta/bacteria_87_collection/escherichia_coli_bw25113/dna/Escherichia_coli_bw25113.ASM75055v1.dna.toplevel.fa.gz
wget -O data/bw25113.gtf.gz ftp://ftp.ensemblgenomes.org/pub/bacteria/release-48/gtf/bacteria_87_collection/escherichia_coli_bw25113/Escherichia_coli_bw25113.ASM75055v1.48.gtf.gz
gunzip data/bw25113.fna.gz
gunzip data/bw25113.gtf.gz

bowtie2-build --threads 4 -f data/bw25113.fna data/bw25113 # 3 sec.
echo -e "Chromosome\t4631469" > data/bw25113_chrom.sizes

mkdir data/fastp_211018 data/sam_211018 data/fwdrev_211018

#ROUND 1 (2021-10-18)
qsub scripts/do_paired_fastp_bowtie2_samtools_211018.pbs

# ROUND 2 (2022-02-23)
cp ~/opt/tools/millefy/tutorial/bamtools_*.json data/
mkdir data/fwdrev_220223
qsub scripts/do_paired_fastp_bowtie2_samtools_220223.pbs
