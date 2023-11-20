#!/bin/bash
# Last update: 2019
set -eu pipefail

cp /home/gaou/gew/2019/BC06.fq .
awk 'BEGIN {OFS = "\n"} {header = $0 ; getline seq ; getline qheader ; getline qseq ; if (length(seq) >= 40000 ) {print header, seq, qheader, qseq}}' < input.fq > filtered-40000.fastq
/home/gaou/kumamushi/software/bbmap/reformat.sh in=BC06.fq out=BC06-filter40k.fq minlength=40000 qin=34
/home/gaou/kumamushi/software/bbmap/stats.sh BC06-filter40k.fq
/home/gaou/kumamushi/software/canu-1.8/Linux-amd64/bin/canu -nanopore-raw BC06-filter40k.fq -d BC06 -p BC06 -fast useGrid=false genomeSize=4m maxThreads=64
/home/gaou/kumamushi/software/canu-1.8/Linux-amd64/bin/canu -nanopore-raw BC06-filter40k.fq -d BC06_nofast -p BC06_nofast useGrid=false genomeSize=4m maxThreads=32

cd BC06
/home/gaou/kumamushi/software/bbmap/stats.sh BC06.contigs.fasta

cd ../BC06_nofast
/home/gaou/kumamushi/software/bbmap/stats.sh BC06_nofast/BC06_nofast.contigs.fasta
grep ">" BC06_nofast.contigs.fasta

# "TGATGGCGTTAGTGGTGG"配列でマッチ．

# gVolante

/home/gaou/kumamushi/software/bwa-0.7.11/bwa index BC06_nofast_circular.contigs.fasta
/home/gaou/kumamushi/software/bwa-0.7.11/bwa mem -t 32 BC06_nofast_circular.contigs.fasta ../../../gaou/gew/2019/Illumina/BC06_S6_merged_R1.fq | /home/gaou/kumamushi/software/samtools-1.9/samtools view -@ 4 -b -o aln.bam -
/home/gaou/kumamushi/software/samtools-1.9/samtools sort -T sort.tmp -o aln.sorted.bam -@ 4 aln.bam
/home/gaou/kumamushi/software/samtools-1.9/samtools index aln.sorted.bam
java -Xms8g -jar /home/gaou/kumamushi/software/pilon-1.23.jar --genome BC06_nofast_circular.contigs.fasta --bam aln.sorted.bam --threads 32 --output pilon1

cd ..
mkdir Pilon_1
cd Pilon_1
cp ../BC06_nofast/pilon1.fasta .
/home/gaou/kumamushi/software/bwa-0.7.11/bwa index pilon1.fasta
/home/gaou/kumamushi/software/bwa-0.7.11/bwa mem -t 64 pilon1.fasta ../../../gaou/gew/2019/Illumina/BC06_S6_merged_R1.fq | /home/gaou/kumamushi/software/samtools-1.9/samtools view -@ 4 -b -o aln.bam -
/home/gaou/kumamushi/software/samtools-1.9/samtools sort -T sort.tmp -o aln.sorted.bam -@ 32 aln.bam
/home/gaou/kumamushi/software/samtools-1.9/samtools index aln.sorted.bam
java -Xms8g -jar /home/gaou/kumamushi/software/pilon-1.23.jar --genome pilon1.fasta --bam aln.sorted.bam --threads 64 --output pilon2

cd ..
mkdir Pilon_2
cd Pilon_2
cp ../Pilon_1/pilon2.fasta .
/home/gaou/kumamushi/software/bwa-0.7.11/bwa index pilon2.fasta
/home/gaou/kumamushi/software/bwa-0.7.11/bwa mem -t 64 pilon2.fasta ../../../gaou/gew/2019/Illumina/BC06_S6_merged_R1.fq | /home/gaou/kumamushi/software/samtools-1.9/samtools view -@ 32 -b -o aln.bam -
/home/gaou/kumamushi/software/samtools-1.9/samtools sort -T sort.tmp -o aln.sorted.bam -@ 64 aln.bam
/home/gaou/kumamushi/software/samtools-1.9/samtools index aln.sorted.bam
java -Xms8g -jar /home/gaou/kumamushi/software/pilon-1.23.jar --genome pilon2.fasta --bam aln.sorted.bam --threads 64 --output pilon3

cd ..
mkdir Pilon_3
cd Pilon_3
cp ../Pilon_2/pilon3.fasta .
/home/gaou/kumamushi/software/bwa-0.7.11/bwa index pilon3.fasta
/home/gaou/kumamushi/software/bwa-0.7.11/bwa mem -t 64 pilon3.fasta ../../../gaou/gew/2019_Illumina/BC06_S6_merged_R1.fq | /home/gaou/kumamushi/software/samtools-1.9/samtools view -@ 64 -b -o aln.bam -
/home/gaou/kumamushi/software/samtools-1.9/samtools sort -T sort.tmp -o aln.sorted.bam -@ 64 aln.bam
/home/gaou/kumamushi/software/samtools-1.9/samtools index aln.sorted.bam
java -Xms8g -jar /home/gaou/kumamushi/software/pilon-1.23.jar --genome pilon3.fasta --bam aln.sorted.bam --threads 64 --output pilon4

cd ..
mkdir Pilon_4
cd Pilon_4
cp ../Pilon_3/pilon4.fasta .
/home/gaou/kumamushi/software/bwa-0.7.11/bwa index pilon4.fasta
/home/gaou/kumamushi/software/bwa-0.7.11/bwa mem -t 64 pilon4.fasta ../../../gaou/gew/2019/Illumina/BC06_S6_merged_R1.fq | /home/gaou/kumamushi/software/samtools-1.9/samtools view -@ 64 -b -o aln.bam -
/home/gaou/kumamushi/software/samtools-1.9/samtools sort -T sort.tmp -o aln.sorted.bam -@ 64 aln.bam
/home/gaou/kumamushi/software/samtools-1.9/samtools index aln.sorted.bam
java -Xms8g -jar /home/gaou/kumamushi/software/pilon-1.23.jar --genome pilon4.fasta --bam aln.sorted.bam --threads 64 --output pilon5

cd ..
mkdir Pilon_5
cd Pilon_5
cp ../Pilon_4/pilon5.fasta .

# 一番高精度なやり方．

cd ..
/home/gaou/kumamushi/software/canu-1.8/Linux-amd64/bin/canu -nanopore-raw BC06.fq -d BC06_best -p BC06_best useGrid=false genomeSize=4m maxThreads=64

cd BC06_best
/home/gaou/kumamushi/software/bbmap/stats.sh BC06_best.contigs.fasta
grep ">" BC06_best.contigs.fasta

# "TGTTAGCCAGCAGGCACGTGTCATTT"配列でマッチ．

# gVolante

/home/gaou/kumamushi/software/bwa-0.7.11/bwa index BC06_best_circular.contigs.fasta
/home/gaou/kumamushi/software/bwa-0.7.11/bwa mem -t 64 BC06_best_circular.contigs.fasta ../../../gaou/gew/2019/Illumina/BC06_S6_merged_R1.fq | /home/gaou/kumamushi/software/samtools-1.9/samtools view -@ 64 -b -o aln.bam -
/home/gaou/kumamushi/software/samtools-1.9/samtools sort -T sort.tmp -o aln.sorted.bam -@ 8 aln.bam
/home/gaou/kumamushi/software/samtools-1.9/samtools index aln.sorted.bam
java -Xms8g -jar /home/gaou/kumamushi/software/pilon-1.23.jar --genome BC06_best_circular.contigs.fasta --bam aln.sorted.bam --threads 64 --output pilon1

cd ..
mkdir Pilon_best_1
cd Pilon_best_1
cp ../BC06_best/pilon1.fasta .
/home/gaou/kumamushi/software/bwa-0.7.11/bwa index pilon1.fasta
/home/gaou/kumamushi/software/bwa-0.7.11/bwa mem -t 64 pilon1.fasta ../../../gaou/gew/2019/Illumina/BC06_S6_merged_R1.fq | /home/gaou/kumamushi/software/samtools-1.9/samtools view -@ 64 -b -o aln.bam -
/home/gaou/kumamushi/software/samtools-1.9/samtools sort -T sort.tmp -o aln.sorted.bam -@ 8 aln.bam
/home/gaou/kumamushi/software/samtools-1.9/samtools index aln.sorted.bam
java -Xms8g -jar /home/gaou/kumamushi/software/pilon-1.23.jar --genome pilon1.fasta --bam aln.sorted.bam --threads 64 --output pilon2

cd ..
mkdir Pilon_best_2
cd Pilon_best_2
cp ../Pilon_best_1/pilon2.fasta .
/home/gaou/kumamushi/software/bwa-0.7.11/bwa index pilon2.fasta
/home/gaou/kumamushi/software/bwa-0.7.11/bwa mem -t 64 pilon2.fasta ../../../gaou/gew/2019/Illumina/BC06_S6_merged_R1.fq | /home/gaou/kumamushi/software/samtools-1.9/samtools view -@ 64 -b -o aln.bam -
/home/gaou/kumamushi/software/samtools-1.9/samtools sort -T sort.tmp -o aln.sorted.bam -@ 8 aln.bam
/home/gaou/kumamushi/software/samtools-1.9/samtools index aln.sorted.bam
java -Xms8g -jar /home/gaou/kumamushi/software/pilon-1.23.jar --genome pilon2.fasta --bam aln.sorted.bam --threads 64 --output pilon3

cd ..
mkdir Pilon_best_3
cd Pilon_best_3
cp ../Pilon_best_2/pilon3.fasta .
/home/gaou/kumamushi/software/bwa-0.7.11/bwa index pilon3.fasta
/home/gaou/kumamushi/software/bwa-0.7.11/bwa mem -t 64 pilon3.fasta ../../../gaou/gew/2019/Illumina/BC06_S6_merged_R1.fq | /home/gaou/kumamushi/software/samtools-1.9/samtools view -@ 64 -b -o aln.bam -
/home/gaou/kumamushi/software/samtools-1.9/samtools sort -T sort.tmp -o aln.sorted.bam -@ 8 aln.bam
/home/gaou/kumamushi/software/samtools-1.9/samtools index aln.sorted.bam 
java -Xms8g -jar /home/gaou/kumamushi/software/pilon-1.23.jar --genome pilon3.fasta --bam aln.sorted.bam --threads 64 --output pilon4

cd ..
mkdir Pilon_best_4
cd Pilon_best_4
cp ../Pilon_best_3/pilon4.fasta .
/home/gaou/kumamushi/software/bwa-0.7.11/bwa index pilon4.fasta
/home/gaou/kumamushi/software/bwa-0.7.11/bwa mem -t 64 pilon4.fasta ../../../gaou/gew/2019/Illumina/BC06_S6_merged_R1.fq | /home/gaou/kumamushi/software/samtools-1.9/samtools view -@ 64 -b -o aln.bam -
/home/gaou/kumamushi/software/samtools-1.9/samtools sort -T sort.tmp -o aln.sorted.bam -@ 8 aln.bam
/home/gaou/kumamushi/software/samtools-1.9/samtools index aln.sorted.bam
java -Xms8g -jar /home/gaou/kumamushi/software/pilon-1.23.jar --genome pilon4.fasta --bam aln.sorted.bam --threads 64 --output pilon5

cd ..
mkdir Pilon_best_5
cd Pilon_best_5
cp ../Pilon_best_4/pilon5.fasta .

