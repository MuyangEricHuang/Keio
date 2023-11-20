#!/bin/bash
# Last update: 2019
set -eu pipefail

makeblastdb -in mt-L.fasta -out MTLDB -dbtype nucl -parse_seqids

time blastn -db MTLDB -query xxx.fasta -out result1.txt -evalue 1e-05 -max_target_seqs 10000 -matrix BLOSUM65 -outfmt 6

time blastn -db MTLDB -query xxx.fasta -out result2.txt -evalue 1e-15 -max_target_seqs 10000 -matrix BLOSUM90 -outfmt 6

makeblastdb -in mt-R.fasta -out MTRDB -dbtype nucl -parse_seqids

time blastn -db MTRDB -query xxx.fasta -out result3.txt -evalue 1e-05 -max_target_seqs 10000 -matrix BLOSUM65 -outfmt 6
time blastn -db MTRDB -query xxx.fasta -out result4.txt -evalue 1e-15 -max_target_seqs 10000 -matrix BLOSUM90 -outfmt 7 
