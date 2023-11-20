#!/bin/bash
set -eu pipefail

mkdir fastqc_reports_01--nogroup
fastqc -t 32 --nogroup -o ./fastqc_reports_01--nogroup *.fastq
cd fastqc_reports_01--nogroup/
multiqc .
cd .. 

# trimmomaticに使うfaファイルを作り，fastqc_reports_01--nogroupのディレクトリ内に置く．

mkdir trimmomatic_01
java -jar ~/opt/tools/Trimmomatic-0.39/trimmomatic-0.39.jar SE -threads 32 -phred33 -trimlog trimmomatic_01/log.txt DRR000605.fastq trimmomatic_01/DRR000605_trimmomatic01.fq ILLUMINACLIP:fastqc_reports_01--nogroup/adapters.fa:2:30:10

fastx_clipper -Q33 -a NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN -i trimmomatic_01/DRR000605_trimmomatic01.fq -o trimmomatic_01/DRR000605_trimmomatic01_fastx01.fq

mkdir fastqc_reports_02--nogroup
cd trimmomatic_01/
fastqc -t 32 --nogroup -o ../fastqc_reports_02--nogroup *.fq
cd ../fastqc_reports_02--nogroup
multiqc .
cd ..

mkdir trimmomatic_02
java -jar ~/opt/tools/Trimmomatic-0.39/trimmomatic-0.39.jar SE -threads 32 -phred33 -trimlog trimmomatic_02/log.txt trimmomatic_01/DRR000605_trimmomatic01_fastx01.fq trimmomatic_02/DRR000605_trimmomatic02_fastx01.fq ILLUMINACLIP:fastqc_reports_02--nogroup/adapters.fa:2:30:10

fastx_clipper -Q33 -a NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN -i trimmomatic_02/DRR000605_trimmomatic02_fastx01.fq -o trimmomatic_02/DRR000605_trimmomatic02_fastx02.fq

mkdir fastqc_reports_03--nogroup
cd trimmomatic_02/
fastqc -t 32 --nogroup -o ../fastqc_reports_03--nogroup *.fq
cd ../fastqc_reports_03--nogroup
multiqc .
cd ..

mkdir Mapping
# toplevel.faファイルをコピー（追記: 恐らくMappingとtrimmomatic_real01のディレクトリにコピー．）

# 各ディレクトリにEscherichia_coli_bw25113.ASM75055v1.dna.toplevel.fa.fai (index) を作成する．
samtools faidx trimmomatic_01/Escherichia_coli_bw25113.ASM75055v1.dna.toplevel.fa
samtools faidx trimmomatic_01/sequence.fasta
samtools faidx trimmomatic_02/Escherichia_coli_bw25113.ASM75055v1.dna.toplevel.fa
samtools faidx trimmomatic_02/sequence.fasta

bowtie2-build -f trimmomatic_01/Escherichia_coli_bw25113.ASM75055v1.dna.toplevel.fa trimmomatic_01/INDEX_top
bowtie2-build -f trimmomatic_01/sequence.fasta trimmomatic_01/INDEX_seq
bowtie2-build -f trimmomatic_02/Escherichia_coli_bw25113.ASM75055v1.dna.toplevel.fa trimmomatic_02/INDEX_top
bowtie2-build -f trimmomatic_02/sequence.fasta trimmomatic_02/INDEX_seq

mkdir sam_t1f0
bowtie2 -p 32 -x trimmomatic_01/INDEX_top -U trimmomatic_01/DRR000605_trimmomatic01.fq -S sam_t1f0/DRR000605_trimmomatic01_top.sam
grep -v "XS:" sam_t1f0/DRR000605_trimmomatic01_top.sam > sam_t1f0/DRR000605_trimmomatic01_top.unique.sam
bowtie2 -p 32 -x trimmomatic_01/INDEX_seq -U trimmomatic_01/DRR000605_trimmomatic01.fq -S sam_t1f0/DRR000605_trimmomatic01_seq.sam
grep -v "XS:" sam_t1f0/DRR000605_trimmomatic01_seq.sam > sam_t1f0/DRR000605_trimmomatic01_seq.unique.sam

mkdir sam_t1f1
bowtie2 -p 32 -x trimmomatic_01/INDEX_top -U trimmomatic_01/DRR000605_trimmomatic01_fastx01.fq -S sam_t1f1/DRR000605_trimmomatic01_fastx01_top.sam
grep -v "XS:" sam_t1f1/DRR000605_trimmomatic01_fastx01_top.sam > sam_t1f1/DRR000605_trimmomatic01_fastx01_top.unique.sam
bowtie2 -p 32 -x trimmomatic_01/INDEX_seq -U trimmomatic_01/DRR000605_trimmomatic01_fastx01.fq -S sam_t1f1/DRR000605_trimmomatic01_fastx01_seq.sam
grep -v "XS:" sam_t1f1/DRR000605_trimmomatic01_fastx01_seq.sam > sam_t1f1/DRR000605_trimmomatic01_fastx01_seq.unique.sam

mkdir sam_t2f1
bowtie2 -p 32 -x trimmomatic_02/INDEX_top -U trimmomatic_02/DRR000605_trimmomatic02_fastx01.fq -S sam_t2f1/DRR000605_trimmomatic02_fastx01_top.sam
grep -v "XS:" sam_t2f1/DRR000605_trimmomatic02_fastx01_top.sam > sam_t2f1/DRR000605_trimmomatic02_fastx01_top.unique.sam
bowtie2 -p 32 -x trimmomatic_02/INDEX_seq -U trimmomatic_02/DRR000605_trimmomatic02_fastx01.fq -S sam_t2f1/DRR000605_trimmomatic02_fastx01_seq.sam
grep -v "XS:" sam_t2f1/DRR000605_trimmomatic02_fastx01_seq.sam > sam_t2f1/DRR000605_trimmomatic02_fastx01_seq.unique.sam

mkdir sam_t2f2
bowtie2 -p 32 -x trimmomatic_02/INDEX_top -U trimmomatic_02/DRR000605_trimmomatic02_fastx02.fq -S sam_t2f2/DRR000605_trimmomatic02_fastx02_top.sam
grep -v "XS:" sam_t2f2/DRR000605_trimmomatic02_fastx02_top.sam > sam_t2f2/DRR000605_trimmomatic02_fastx02_top.unique.sam
bowtie2 -p 32 -x trimmomatic_02/INDEX_seq -U trimmomatic_02/DRR000605_trimmomatic02_fastx02.fq -S sam_t2f2/DRR000605_trimmomatic02_fastx02_seq.sam
grep -v "XS:" sam_t2f2/DRR000605_trimmomatic02_fastx02_seq.sam > sam_t2f2/DRR000605_trimmomatic02_fastx02_seq.unique.sam

samtools sort -@ 32 -O bam -o sam_t1f0/DRR000605_trimmomatic01_top.unique.sort.bam sam_t1f0/DRR000605_trimmomatic01_top.unique.sam
samtools index sam_t1f0/DRR000605_trimmomatic01_top.unique.sort.bam
samtools sort -@ 32 -O bam -o sam_t1f0/DRR000605_trimmomatic01_seq.unique.sort.bam sam_t1f0/DRR000605_trimmomatic01_seq.unique.sam
samtools index sam_t1f0/DRR000605_trimmomatic01_seq.unique.sort.bam 

samtools sort -@ 32 -O bam -o sam_t1f1/DRR000605_trimmomatic01_fastx01_top.unique.sort.bam sam_t1f1/DRR000605_trimmomatic01_fastx01_top.unique.sam
samtools index sam_t1f1/DRR000605_trimmomatic01_fastx01_top.unique.sort.bam
samtools sort -@ 32 -O bam -o sam_t1f1/DRR000605_trimmomatic01_fastx01_seq.unique.sort.bam sam_t1f1/DRR000605_trimmomatic01_fastx01_seq.unique.sam
samtools index sam_t1f1/DRR000605_trimmomatic01_fastx01_seq.unique.sort.bam

samtools sort -@ 32 -O bam -o sam_t2f1/DRR000605_trimmomatic02_fastx01_top.unique.sort.bam sam_t2f1/DRR000605_trimmomatic02_fastx01_top.unique.sam
samtools index sam_t2f1/DRR000605_trimmomatic02_fastx01_top.unique.sort.bam
samtools sort -@ 32 -O bam -o sam_t2f1/DRR000605_trimmomatic02_fastx01_seq.unique.sort.bam sam_t2f1/DRR000605_trimmomatic02_fastx01_seq.unique.sam
samtools index sam_t2f1/DRR000605_trimmomatic02_fastx01_seq.unique.sort.bam

samtools sort -@ 32 -O bam -o sam_t2f2/DRR000605_trimmomatic02_fastx02_top.unique.sort.bam sam_t2f2/DRR000605_trimmomatic02_fastx02_top.unique.sam
samtools index sam_t2f2/DRR000605_trimmomatic02_fastx02_top.unique.sort.bam
samtools sort -@ 32 -O bam -o sam_t2f2/DRR000605_trimmomatic02_fastx02_seq.unique.sort.bam sam_t2f2/DRR000605_trimmomatic02_fastx02_seq.unique.sam
samtools index sam_t2f2/DRR000605_trimmomatic02_fastx02_seq.unique.sort.bam

# アノテーションファイル（GFFまたはGTF, gff3）をtrimmomatic_01と02にコピー

rsem-refseq-extract-primary-assembly trimmomatic_01/Escherichia_coli_bw25113.ASM75055v1.dna.toplevel.fa trimmomatic_01/Escherichia_coli_bw25113.ASM75055v1.dna.toplevel.primary_assembly.fa
rsem-prepare-reference --gtf trimmomatic_01/Escherichia_coli_bw25113.ASM75055v1.44.gtf --bowtie2 --bowtie2-path ~/.linuxbrew/bin trimmomatic_01/Escherichia_coli_bw25113.ASM75055v1.dna.toplevel.fa trimmomatic_01/INDEX-top
rsem-refseq-extract-primary-assembly trimmomatic_01/sequence.fasta trimmomatic_01/sequence.primary_assembly.fa
rsem-prepare-reference --gff3 trimmomatic_01/sequence.gff3 -p 32 --bowtie2 --bowtie2-path ~/.linuxbrew/bin trimmomatic_01/sequence.fasta trimmomatic_01/INDEX-seq

rsem-refseq-extract-primary-assembly trimmomatic_02/Escherichia_coli_bw25113.ASM75055v1.dna.toplevel.fa trimmomatic_02/Escherichia_coli_bw25113.ASM75055v1.dna.toplevel.primary_assembly.fa
rsem-prepare-reference --gtf trimmomatic_02/Escherichia_coli_bw25113.ASM75055v1.44.gtf --bowtie2 --bowtie2-path ~/.linuxbrew/bin trimmomatic_02/Escherichia_coli_bw25113.ASM75055v1.dna.toplevel.fa trimmomatic_02/INDEX-top
rsem-refseq-extract-primary-assembly trimmomatic_02/sequence.fasta trimmomatic_02/sequence.primary_assembly.fa
rsem-prepare-reference --gff3 trimmomatic_02/sequence.gff3 -p 32 --bowtie2 --bowtie2-path ~/.linuxbrew/bin trimmomatic_02/sequence.fasta trimmomatic_02/INDEX-seq

mkdir RSEM

mkdir RSEM/t1f0_exp_rsem
result_dir_01=RSEM/t1f0_exp_rsem
rsem-calculate-expression -p 32 --bowtie2 --bowtie2-path ~/.linuxbrew/bin --estimate-rspd --append-names --output-genome-bam trimmomatic_01/DRR000605_trimmomatic01.fq trimmomatic_01/INDEX-top ${result_dir_01}
mkdir RSEM/t1f1_exp_rsem
result_dir_02=RSEM/t1f1_exp_rsem
rsem-calculate-expression -p 32 --bowtie2 --bowtie2-path ~/.linuxbrew/bin --estimate-rspd --append-names --output-genome-bam trimmomatic_01/DRR000605_trimmomatic01_fastx01.fq  trimmomatic_01/INDEX-top ${result_dir_02}

mkdir RSEM/t1f2_exp_rsem
mkdir RSEM_PE/Ec-H${seqlib}_paired_nofastx_exp_rsem
for seqlib in ${SEQLIBS[@]}; do
    result_dir_01=RSEM_PE/Ec-H${seqlib}_paired_nofastx_exp_rsem
    rsem-calculate-expression -p 32 --paired-end --bowtie2 --bowtie2-path ~/.linuxbrew/bin --estimate-rspd --append-names --output-genome-bam trimmomatic_PE01/paired_Ec-H${seqlib}_R1_trimmomatic01.fq trimmomatic_PE01/paired_Ec-H${seqlib}_R2_trimmomatic01.fq trimmomatic_PE01/INDEX ${result_dir_01}
    mkdir RSEM_PE/Ec-H${seqlib}_paired_fastx_exp_rsem
    result_dir_02=RSEM_PE/Ec-H${seqlib}_paired_fastx_exp_rsem
    rsem-calculate-expression -p 32 --paired-end --bowtie2 --bowtie2-path ~/.linuxbrew/bin --estimate-rspd --append-names --output-genome-bam trimmomatic_PE01/paired_Ec-H${seqlib}_R1_trimmomatic01_fastx01.fq trimmomatic_PE01/paired_Ec-H${seqlib}_R2_trimmomatic01_fastx01.fq trimmomatic_PE01/INDEX ${result_dir_02}
    mkdir RSEM_PE/Ec-H${seqlib}_unpaired_nofastx_exp_rsem
    result_dir_03=RSEM_PE/Ec-H${seqlib}_unpaired_nofastx_exp_rsem
    rsem-calculate-expression -p 32 --paired-end --bowtie2 --bowtie2-path ~/.linuxbrew/bin --estimate-rspd --append-names --output-genome-bam trimmomatic_PE01/unpaired_Ec-H${seqlib}_R1_trimmomatic01.fq trimmomatic_PE01/unpaired_Ec-H${seqlib}_R2_trimmomatic01.fq trimmomatic_PE01/INDEX ${result_dir_03}
    mkdir RSEM_PE/Ec-H${seqlib}_unpaired_fastx_exp_rsem
    result_dir_04=RSEM_PE/Ec-H${seqlib}_unpaired_fastx_exp_rsem
    rsem-calculate-expression -p 32 --paired-end --bowtie2 --bowtie2-path ~/.linuxbrew/bin --estimate-rspd --append-names --output-genome-bam trimmomatic_PE01/unpaired_Ec-H${seqlib}_R1_trimmomatic01_fastx01.fq trimmomatic_PE01/unpaired_Ec-H${seqlib}_R2_trimmomatic01_fastx01.fq trimmomatic_PE01/INDEX ${result_dir_04}
done

mkdir RSEM_PE_parameter
for seqlib in ${SEQLIBS[@]}; do
    mkdir RSEM_PE_parameter/Ec-H${seqlib}_paired_nofastx_exp_rsem
    result_dir_01=RSEM_PE_parameter/Ec-H${seqlib}_paired_nofastx_exp_rsem
    rsem-calculate-expression -p 32 --paired-end --bowtie2 --bowtie2-path ~/.linuxbrew/bin --estimate-rspd --append-names --output-genome-bam trimmomatic_PE_parameter01/paired_Ec-H${seqlib}_R1_trimmomatic01.fq trimmomatic_PE_parameter01/paired_Ec-H${seqlib}_R2_trimmomatic01.fq trimmomatic_PE_parameter01/INDEX ${result_dir_01}
    mkdir RSEM_PE_parameter/Ec-H${seqlib}_paired_fastx_exp_rsem
    result_dir_02=RSEM_PE_parameter/Ec-H${seqlib}_paired_fastx_exp_rsem
    rsem-calculate-expression -p 32 --paired-end --bowtie2 --bowtie2-path ~/.linuxbrew/bin --estimate-rspd --append-names --output-genome-bam trimmomatic_PE_parameter01/paired_Ec-H${seqlib}_R1_trimmomatic01_fastx01.fq trimmomatic_PE_parameter01/paired_Ec-H${seqlib}_R2_trimmomatic01_fastx01.fq trimmomatic_PE_parameter01/INDEX ${result_dir_02}
    mkdir RSEM_PE_parameter/Ec-H${seqlib}_unpaired_nofastx_exp_rsem
    result_dir_03=RSEM_PE_parameter/Ec-H${seqlib}_unpaired_nofastx_exp_rsem
    rsem-calculate-expression -p 32 --paired-end --bowtie2 --bowtie2-path ~/.linuxbrew/bin --estimate-rspd --append-names --output-genome-bam trimmomatic_PE_parameter01/unpaired_Ec-H${seqlib}_R1_trimmomatic01.fq trimmomatic_PE_parameter01/unpaired_Ec-H${seqlib}_R2_trimmomatic01.fq trimmomatic_PE_parameter01/INDEX ${result_dir_03}
    mkdir RSEM_PE_parameter/Ec-H${seqlib}_unpaired_fastx_exp_rsem
    result_dir_04=RSEM_PE_parameter/Ec-H${seqlib}_unpaired_fastx_exp_rsem
    rsem-calculate-expression -p 32 --paired-end --bowtie2 --bowtie2-path ~/.linuxbrew/bin --estimate-rspd --append-names --output-genome-bam trimmomatic_PE_parameter01/unpaired_Ec-H${seqlib}_R1_trimmomatic01_fastx01.fq trimmomatic_PE_parameter01/unpaired_Ec-H${seqlib}_R2_trimmomatic01_fastx01.fq trimmomatic_PE_parameter01/INDEX ${result_dir_04}
done

# RSEM_PE/Ec-H4_unpaired_nofastx_exp_rsem欠.genes.results, .genome.bam, .isoforms.results, .transcript.bam, 1つ.tempというファイルが多い．
# RSEM_PE_parameter内，H1はpaired_fastx, unpaired_nofastx, H2はpaired_fastx, unpaired_fastx, unpaired_nofastx, H3はpaired_fastx, unpaired_nofastx, H4は，paired_fastx, unpaired_fastx, unpaired_nofastxが上行4ファイル欠けて1ファイル増え，通常は1TPにpaired, unpaired, fastx, nofastxの4種の組み合わせがある．

# for seqlib in ${SEQLIBS[@]}; do
#     rsem-plot-model RSEM_noqc/Ec-H${seqlib}_exp_rsem RSEM_noqc/Ec-H${seqlib}_diagnostic.pdf
##     rsem-plot-transcript-wiggles --gene-list --show-unique RSEM_noqc/Ec-H${seqlib}_exp_rsem gene_ids.txt RSEM_noqc/Ec-H${seqlib}_transcript_wiggle.pdf
#     rsem-bam2wig RSEM_noqc/Ec-H${seqlib}_exp_rsem.genome.bam RSEM_noqc/Ec-H${seqlib}.wig Mapping/INDEX
#     samtools sort -@ 32 RSEM_noqc/Ec-H${seqlib}_exp_rsem.genome.bam > RSEM_noqc/Ec-H${seqlib}_exp_rsem.genome.sorted.bam
#     samtools index RSEM_noqc/Ec-H${seqlib}_exp_rsem.genome.sorted.bam -@ 32
# done
for seqlib in ${SEQLIBS[@]}; do
    rsem-plot-model RSEM/Ec-H${seqlib}_exp_rsem RSEM/Ec-H${seqlib}_diagnostic.pdf
    rsem-plot-transcript-wiggles --gene-list --show-unique RSEM/Ec-H${seqlib}_exp_rsem gene_ids.txt RSEM/Ec-H${seqlib}_transcript_wiggle.pdf
    rsem-bam2wig RSEM/Ec-H${seqlib}_exp_rsem.genome.bam RSEM/Ec-H${seqlib}.wig trimmomatic_real01/INDEX
    samtools sort -@ 32 RSEM/Ec-H${seqlib}_exp_rsem.genome.bam > RSEM/Ec-H${seqlib}_exp_rsem.genome.sorted.bam
    samtools index RSEM/Ec-H${seqlib}_exp_rsem.genome.sorted.bam -@ 32
done

# mkdir htseq_noqc
# for seqlib in ${SEQLIBS[@]}; do
#     htseq-count -f bam -r pos sam_noqc/Ec-H${seqlib}.unique.sort.bam Mapping/Escherichia_coli_bw25113.ASM75055v1.44.gtf > htseq_noqc/Ec-H${seqlib}_count_data.txt
# done
mkdir htseq
for seqlib in ${SEQLIBS[@]}; do
    htseq-count -f bam -r pos sam/Ec-H${seqlib}_trimmomatic01_fastx01.unique.sort.bam trimmomatic_real01/Escherichia_coli_bw25213.ASM75055v1.44.gtf > htseq/Ec-H${seqlib}_trimmomatic01_fastx01_count_data.txt
done
