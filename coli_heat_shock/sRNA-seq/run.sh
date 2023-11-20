#!/usr/bin/bash
# Last update: 02/24/2022

mkdir -p data/log scripts

wget -O data/bw25113.fna.gz ftp://ftp.ensemblgenomes.org/pub/bacteria/release-48/fasta/bacteria_87_collection/escherichia_coli_bw25113/dna/Escherichia_coli_bw25113.ASM75055v1.dna.toplevel.fa.gz
wget -O data/bw25113.gtf.gz ftp://ftp.ensemblgenomes.org/pub/bacteria/release-48/gtf/bacteria_87_collection/escherichia_coli_bw25113/Escherichia_coli_bw25113.ASM75055v1.48.gtf.gz
gunzip data/bw25113.fna.gz
gunzip data/bw25113.gtf.gz

bowtie2-build --threads 4 -f data/bw25113.fna data/bw25113 # 3 sec.
echo -e "Chromosome\t4631469" > data/bw25113_chrom.sizes
cp ~/opt/tools/millefy/tutorial/bamtools_*.json data/

mkdir data/fastp_220224 data/sam_220224 data/fwdrev_220224
sh scripts/merge_fastq_220224.sh
qsub scripts/do_paired_fastp_bowtie2_samtools_220224.pbs

