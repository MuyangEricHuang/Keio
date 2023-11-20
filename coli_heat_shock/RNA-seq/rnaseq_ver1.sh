#!/bin/bash
set -eu pipefail

mkdir fastqc_reports_01--nogroup
fastqc -t 32 --nogroup -o ./fastqc_reports_01--nogroup *.fq
cd fastqc_reports_01--nogroup/
multiqc .
cd .. 

# trimmomaticに使うfaファイルを作り，fastqc_reports_01--nogroupのディレクトリ内に置く．
# 今回のデータはNo Hitが続き，2020年度春学期と夏プロの試みにより，trimmomaticによるparameterとfastxによるN配列の除去が必要ないということで，直接mappingに移行する．
# 尚，No Hitを取り除いたり，各種パラメータで試すことは可，その場合，fastqc_reports_01--nogroupディレクトリにadapters.faと，重複を削除したadapters_fin.faが存在する．
# 考えられるパターンとして，[01] adapters.faなし，SE, parameter [02] adapters.faなし，SE, fastx [03] adapters.faなし，SE, parameter. fastx [04] adapters.faなし，PE, parameter [05] adapters.faなし，PE, fastx [06] adapters.faなし，PE, parameter. fastx [07] adapters.fa, SE, parameter [08] adapters.fa, SE, fastx [09] adapters.fa, SE, parameter. fastx [10] adapters.fa, PE, parameter [11] adapters.fa, PE, fastx [12] adapters.fa, PE, parameter. fastx

mkdir trimmomatic_real01
PAIREDS=(1 2)
# SEQLIBS=(1 2 3 4)
SEQLIBS=(1 2 3 4 5 6 7 8 9 10 11)
for paired in ${PAIREDS[@]}; do
    for seqlib in ${SEQLIBS[@]}; do
        java -jar ~/opt/tools/Trimmomatic-0.39/trimmomatic-0.39.jar SE -threads 32 -phred33 -trimlog trimmomatic_real01/log_H${seqlib}_R${paired}.txt Ec-H${seqlib}_R${paired}_001.fastq trimmomatic_real01/Ec-H${seqlib}_R${paired}_trimmomatic01.fq ILLUMINACLIP:fastqc_reports_01--nogroup/adapters_fin.fa:2:30:10
    done
done

mkdir trimmomatic_PE01
for seqlib in ${SEQLIBS[@]}; do
    java -jar ~/opt/tools/Trimmomatic-0.39/trimmomatic-0.39.jar PE -threads 32 -phred33 -trimlog trimmomatic_PE01/log_H${seqlib}.txt Ec_H${seqlib}_1.fq Ec_H${seqlib}_2.fq trimmomatic_PE01/paired_Ec_H${seqlib}_1_trimmomatic01.fq trimmomatic_PE01/unpaired_Ec_H${seqlib}_1_trimmomatic01.fq trimmomatic_PE01/paired_Ec_H${seqlib}_2_trimmomatic01.fq trimmomatic_PE01/unpaired_Ec_H${seqlib}_2_trimmomatic01.fq ILLUMINACLIP:fastqc_reports_01--nogroup/adapters_fin.fa:2:30:10
done
# mkdir trimmomatic_PE_parameter01
# for seqlib in ${SEQLIBS[@]}; do
#     java -jar ~/opt/tools/Trimmomatic-0.39/trimmomatic-0.39.jar PE -threads 32 -phred33 -trimlog trimmomatic_PE_parameter01/log_H${seqlib}.txt Ec-H${seqlib}_R1_001.fastq Ec-H${seqlib}_R2_001.fastq trimmomatic_PE_parameter01/paired_Ec-H${seqlib}_R1_trimmomatic01.fq trimmomatic_PE_parameter01/unpaired_Ec-H${seqlib}_R1_trimmomatic01.fq trimmomatic_PE_parameter01/paired_Ec-H${seqlib}_R2_trimmomatic01.fq trimmomatic_PE_parameter01/unpaired_Ec-H${seqlib}_R2_trimmomatic01.fq ILLUMINACLIP:fastqc_reports_01--nogroup/adapters_fin.fa:2:30:10 LEADING:20 TRAILING:20 SLIDINGWINDOW:4:15 MINLEN:36
# done

MODE=(unpaired paired)
for paired in ${PAIREDS[@]}; do
    for seqlib in ${SEQLIBS[@]}; do
        fastx_clipper -Q33 -a NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN -i trimmomatic_real01/Ec-H${seqlib}_R${paired}_trimmomatic01.fq -o trimmomatic_real01/Ec-H${seqlib}_R${paired}_trimmomatic01_fastx01.fq
    done
done

# for mode in ${MODE[@]}; do
#     for paired in ${PAIREDS[@]}; do
#         for seqlib in ${SEQLIBS[@]}; do
#             fastx_clipper -Q33 -a NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN -i trimmomatic_PE01/${mode}_Ec-H${seqlib}_R${paired}_trimmomatic01.fq -o trimmomatic_PE01/${mode}_Ec-H${seqlib}_R${paired}_trimmomatic01_fastx01.fq
#         done
#     done
# done
# for mode in ${MODE[@]}; do
#     for paired in ${PAIREDS[@]}; do
#         for seqlib in ${SEQLIBS[@]}; do
#             fastx_clipper -Q33 -a NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN -i trimmomatic_PE_parameter01/${mode}_Ec-H${seqlib}_R${paired}_trimmomatic01.fq -o trimmomatic_PE_parameter01/${mode}_Ec-H${seqlib}_R${paired}_trimmomatic01_fastx01.fq
#         done
#     done
# done

mkdir fastqc_reports_02--nogroup
cd trimmomatic_real01/
fastqc -t 32 --nogroup -o ../fastqc_reports_02--nogroup *.fq
cd ../fastqc_reports_02--nogroup
multiqc .
cd ..

mkdir fastqc_reports_02_PE
cd trimmomatic_PE01/
fastqc -t 32 --nogroup -o ../fastqc_reports_02_PE *.fq
cd ../fastqc_reports_02_PE
multiqc .
cd ..
# mkdir fastqc_reports_02_PE_parameter
# cd trimmomatic_PE_parameter01/
# fastqc -t 32 --nogroup -o ../fastqc_reports_02_PE_parameter *.fq
# cd ../fastqc_reports_02_PE_parameter
# multiqc .
# cd ..

mkdir Mapping
# toplevel.faファイルをコピー（追記: 恐らくMappingとtrimmomatic_real01のディレクトリにコピー．）
# （2021/04/12追記: Paired-EndのmRNAの場合，trimmomatic_real01ではなくtrimmomatic_PE01の気がする）


# 各ディレクトリにEscherichia_coli_bw25113.ASM75055v1.dna.toplevel.fa.fai (index) を作成する．
samtools faidx Mapping/Escherichia_coli_bw25113.ASM75055v1.dna.toplevel.fa
# samtools faidx trimmomatic_real01/Escherichia_coli_bw25113.ASM75055v1.dna.toplevel.fa
samtools faidx trimmomatic_PE01/Escherichia_coli_bw25113.ASM75055v1.dna.toplevel.fa
# samtools faidx trimmomatic_PE_parameter01/Escherichia_coli_bw25113.ASM75055v1.dna.toplevel.fa

bowtie2-build -f Mapping/Escherichia_coli_bw25113.ASM75055v1.dna.toplevel.fa Mapping/INDEX
# bowtie2-build -f trimmomatic_real01/Escherichia_coli_bw25113.ASM75055v1.dna.toplevel.fa trimmomatic_real01/INDEX
bowtie2-build -f trimmomatic_PE01/Escherichia_coli_bw25113.ASM75055v1.dna.toplevel.fa trimmomatic_PE01/INDEX
# bowtie2-build -f trimmomatic_PE_parameter01/Escherichia_coli_bw25113.ASM75055v1.dna.toplevel.fa trimmomatic_PE_parameter01/INDEX

mkdir sam_noqc
for seqlib in ${SEQLIBS[@]}; do
    bowtie2 -p 32 -x Mapping/INDEX -1 Ec_H${seqlib}_1.fq -2 Ec_H${seqlib}_2.fq -S sam_noqc/Ec_H${seqlib}.sam
    grep -v "XS:" sam_noqc/Ec_H${seqlib}.sam > sam_noqc/Ec_H${seqlib}.unique.sam
done
# mkdir sam_nofastx
# for seqlib in ${SEQLIBS[@]}; do
#     bowtie2 -p 32 -x trimmomatic_real01/INDEX -1 trimmomatic_real01/Ec-H${seqlib}_R1_trimmomatic01.fq -2 trimmomatic_real01/Ec-H${seqlib}_R2_trimmomatic01.fq -S sam_nofastx/Ec-H${seqlib}_trimmomatic01.sam
#     grep -v "XS:" sam_nofastx/Ec-H${seqlib}_trimmomatic01.sam > sam_nofastx/Ec-H${seqlib}_trimmomatic01.unique.sam
# done
# mkdir sam_fastx
# for seqlib in ${SEQLIBS[@]}; do
#     bowtie2 -p 32 -x trimmomatic_real01/INDEX -1 trimmomatic_real01/Ec-H${seqlib}_R1_trimmomatic01_fastx01.fq -2 trimmomatic_real01/Ec-H${seqlib}_R2_trimmomatic01_fastx01.fq -S sam_fastx/Ec-H${seqlib}_trimmomatic01_fastx01.sam
#     grep -v "XS:" sam_fastx/Ec-H${seqlib}_trimmomatic01_fastx01.sam > sam_fastx/Ec-H${seqlib}_trimmomatic01_fastx01.unique.sam
# done

mkdir sam_PE_nofastx
for seqlib in ${SEQLIBS[@]}; do
    bowtie2 -p 32 -x trimmomatic_PE01/INDEX -1 trimmomatic_PE01/paired_Ec_H${seqlib}_1_trimmomatic01.fq -2 trimmomatic_PE01/paired_Ec_H${seqlib}_2_trimmomatic01.fq -S sam_PE_nofastx/paired_Ec_H${seqlib}_trimmomatic01.sam
    grep -v "XS:" sam_PE_nofastx/paired_Ec_H${seqlib}_trimmomatic01.sam > sam_PE_nofastx/paired_Ec_H${seqlib}_trimmomatic01.unique.sam
done
# mkdir sam_PE_fastx
# for mode in ${MODE[@]}; do
#     for seqlib in ${SEQLIBS[@]}; do
#         bowtie2 -p 32 -x trimmomatic_PE01/INDEX -1 trimmomatic_PE01/${mode}_Ec-H${seqlib}_R1_trimmomatic01_fastx01.fq -2 trimmomatic_PE01/${mode}_Ec-H${seqlib}_R2_trimmomatic01_fastx01.fq -S sam_PE_fastx/${mode}_Ec-H${seqlib}_trimmomatic01_fastx01.sam
#         grep -v "XS:" sam_PE_fastx/${mode}_Ec-H${seqlib}_trimmomatic01_fastx01.sam > sam_PE_fastx/${mode}_Ec-H${seqlib}_trimmomatic01_fastx01.unique.sam
#     done
# done
# mkdir sam_PE_parameter_nofastx
# for mode in ${MODE[@]}; do
#     for seqlib in ${SEQLIBS[@]}; do
#         bowtie2 -p 32 -x trimmomatic_PE_parameter01/INDEX -1 trimmomatic_PE_parameter01/${mode}_Ec-H${seqlib}_R1_trimmomatic01.fq -2 trimmomatic_PE_parameter01/${mode}_Ec-H${seqlib}_R2_trimmomatic01.fq -S sam_PE_parameter_nofastx/${mode}_Ec-H${seqlib}_trimmomatic01.sam
#         grep -v "XS:" sam_PE_parameter_nofastx/${mode}_Ec-H${seqlib}_trimmomatic01.sam > sam_PE_parameter_nofastx/${mode}_Ec-H${seqlib}_trimmomatic01.unique.sam
#     done
# done
# mkdir sam_PE_parameter_fastx
# for mode in ${MODE[@]}; do
#     for seqlib in ${SEQLIBS[@]}; do
#         bowtie2 -p 32 -x trimmomatic_PE_parameter01/INDEX -1 trimmomatic_PE_parameter01/${mode}_Ec-H${seqlib}_R1_trimmomatic01_fastx01.fq -2 trimmomatic_PE_parameter01/${mode}_Ec-H${seqlib}_R2_trimmomatic01_fastx01.fq -S sam_PE_parameter_fastx/${mode}_Ec-H${seqlib}_trimmomatic01_fastx01.sam
#         grep -v "XS:" sam_PE_parameter_fastx/${mode}_Ec-H${seqlib}_trimmomatic01_fastx01.sam > sam_PE_parameter_fastx/${mode}_Ec-H${seqlib}_trimmomatic01_fastx01.unique.sam
#     done
# done

for seqlib in ${SEQLIBS[@]}; do
    samtools sort -@ 32 -O bam -o sam_noqc/Ec_H${seqlib}.unique.sort.bam sam_noqc/Ec_H${seqlib}.unique.sam
    samtools index sam_noqc/Ec_H${seqlib}.unique.sort.bam
done
# for seqlib in ${SEQLIBS[@]}; do
#     samtools sort -@ 32 -O bam -o sam_nofastx/Ec-H${seqlib}_trimmomatic01.unique.sort.bam sam_nofastx/Ec-H${seqlib}_trimmomatic01.unique.sam
#     samtools index sam_nofastx/Ec-H${seqlib}_trimmomatic01.unique.sort.bam
# done
# for seqlib in ${SEQLIBS[@]}; do
#     samtools sort -@ 32 -O bam -o sam_fastx/Ec-H${seqlib}_trimmomatic01_fastx01.unique.sort.bam sam_fastx/Ec-H${seqlib}_trimmomatic01_fastx01.unique.sam
#     samtools index sam_fastx/Ec-H${seqlib}_trimmomatic01_fastx01.unique.sort.bam
# done

for seqlib in ${SEQLIBS[@]}; do
    samtools sort -@ 32 -O bam -o sam_PE_nofastx/paired_Ec_H${seqlib}_trimmomatic01.unique.sort.bam sam_PE_nofastx/paired_Ec_H${seqlib}_trimmomatic01.unique.sam
    samtools index sam_PE_nofastx/paired_Ec_H${seqlib}_trimmomatic01.unique.sort.bam
done
# for mode in ${MODE[@]}; do
#     for seqlib in ${SEQLIBS[@]}; do
#         samtools sort -@ 32 -O bam -o sam_PE_fastx/${mode}_Ec-H${seqlib}_trimmomatic01_fastx01.unique.sort.bam sam_PE_fastx/${mode}_Ec-H${seqlib}_trimmomatic01_fastx01.unique.sam
#         samtools index sam_PE_fastx/${mode}_Ec-H${seqlib}_trimmomatic01_fastx01.unique.sort.bam
#     done
# done
# for mode in ${MODE[@]}; do
#     for seqlib in ${SEQLIBS[@]}; do
#         samtools sort -@ 32 -O bam -o sam_PE_parameter_nofastx/${mode}_Ec-H${seqlib}_trimmomatic01.unique.sort.bam sam_PE_parameter_nofastx/${mode}_Ec-H${seqlib}_trimmomatic01.unique.sam
#         samtools index sam_PE_parameter_nofastx/${mode}_Ec-H${seqlib}_trimmomatic01.unique.sort.bam
#     done
# done
# for mode in ${MODE[@]}; do
#     for seqlib in ${SEQLIBS[@]}; do
#         samtools sort -@ 32 -O bam -o sam_PE_parameter_fastx/${mode}_Ec-H${seqlib}_trimmomatic01_fastx01.unique.sort.bam sam_PE_parameter_fastx/${mode}_Ec-H${seqlib}_trimmomatic01_fastx01.unique.sam
#         samtools index sam_PE_parameter_fastx/${mode}_Ec-H${seqlib}_trimmomatic01_fastx01.unique.sort.bam
#     done
# done

# アノテーションファイル（GFFまたはGTF）をMapppingとtrimmomatic_real01にコピー
# （2021/04/12追記: Paired-EndのmRNAの場合，trimmomatic_real01ではなくtrimmomatic_PE01の気がする）

rsem-refseq-extract-primary-assembly Mapping/Escherichia_coli_bw25113.ASM75055v1.dna.toplevel.fa Mapping/Escherichia_coli_bw25113.ASM75055v1.dna.toplevel.primary_assembly.fa
rsem-prepare-reference --gtf Mapping/Escherichia_coli_bw25113.ASM75055v1.44.gtf --bowtie2 --bowtie2-path ~/.linuxbrew/bin Mapping/Escherichia_coli_bw25113.ASM75055v1.dna.toplevel.fa Mapping/INDEX
# rsem-refseq-extract-primary-assembly trimmomatic_real01/Escherichia_coli_bw25113.ASM75055v1.dna.toplevel.fa trimmomatic_real01/Escherichia_coli_bw25113.ASM75055v1.dna.toplevel.primary_assembly.fa
# rsem-prepare-reference --gtf trimmomatic_real01/Escherichia_coli_bw25113.ASM75055v1.44.gtf --bowtie2 --bowtie2-path ~/.linuxbrew/bin trimmomatic_real01/Escherichia_coli_bw25113.ASM75055v1.dna.toplevel.fa trimmomatic_real01/INDEX

rsem-refseq-extract-primary-assembly trimmomatic_PE01/Escherichia_coli_bw25113.ASM75055v1.dna.toplevel.fa trimmomatic_PE01/Escherichia_coli_bw25113.ASM75055v1.dna.toplevel.primary_assembly.fa
rsem-prepare-reference --gtf trimmomatic_PE01/Escherichia_coli_bw25113.ASM75055v1.44.gtf --bowtie2 --bowtie2-path ~/.linuxbrew/bin trimmomatic_PE01/Escherichia_coli_bw25113.ASM75055v1.dna.toplevel.fa trimmomatic_PE01/INDEX
# rsem-refseq-extract-primary-assembly trimmomatic_PE_parameter01/Escherichia_coli_bw25113.ASM75055v1.dna.toplevel.fa trimmomatic_PE_parameter01/Escherichia_coli_bw25113.ASM75055v1.dna.toplevel.primary_assembly.fa
# rsem-prepare-reference --gtf trimmomatic_PE_parameter01/Escherichia_coli_bw25113.ASM75055v1.44.gtf --bowtie2 --bowtie2-path ~/.linuxbrew/bin trimmomatic_PE_parameter01/Escherichia_coli_bw25113.ASM75055v1.dna.toplevel.fa trimmomatic_PE_parameter01/INDEX

mkdir RSEM_noqc
for seqlib in ${SEQLIBS[@]}; do
    mkdir RSEM_noqc/Ec_H${seqlib}_exp_rsem
    result_dir=RSEM_noqc/Ec_H${seqlib}_exp_rsem
    rsem-calculate-expression -p 32 --paired-end --bowtie2 --bowtie2-path ~/.linuxbrew/bin --estimate-rspd --append-names --output-genome-bam Ec_H${seqlib}_1.fq Ec_H${seqlib}_2.fq Mapping/INDEX ${result_dir}
done
# mkdir RSEM_SE
# for seqlib in ${SEQLIBS[@]}; do
#     mkdir RSEM_SE/Ec-H${seqlib}_exp_rsem
#     result_dir_01=RSEM_SE/Ec-H${seqlib}_exp_rsem
#     rsem-calculate-expression -p 32 --paired-end --bowtie2 --bowtie2-path ~/.linuxbrew/bin --estimate-rspd --append-names --output-genome-bam trimmomatic_real01/Ec-H${seqlib}_R1_trimmomatic01.fq trimmomatic_real01/Ec-H${seqlib}_R2_trimmomatic01.fq trimmomatic_real01/INDEX ${result_dir_01}
#     mkdir RSEM_SE/Ec-H${seqlib}_fastx_exp_rsem
#     result_dir_02=RSEM_SE/Ec-H${seqlib}_fastx_exp_rsem
#     rsem-calculate-expression -p 32 --paired-end --bowtie2 --bowtie2-path ~/.linuxbrew/bin --estimate-rspd --append-names --output-genome-bam trimmomatic_real01/Ec-H${seqlib}_R1_trimmomatic01_fastx01.fq trimmomatic_real01/Ec-H${seqlib}_R2_trimmomatic01_fastx01.fq trimmomatic_real01/INDEX ${result_dir_02}
# done

mkdir RSEM_PE
for seqlib in ${SEQLIBS[@]}; do
    mkdir RSEM_PE/Ec_H${seqlib}_paired_nofastx_exp_rsem
    result_dir_01=RSEM_PE/Ec_H${seqlib}_paired_nofastx_exp_rsem
    rsem-calculate-expression -p 32 --paired-end --bowtie2 --bowtie2-path ~/.linuxbrew/bin --estimate-rspd --append-names --output-genome-bam trimmomatic_PE01/paired_Ec_H${seqlib}_1_trimmomatic01.fq trimmomatic_PE01/paired_Ec_H${seqlib}_2_trimmomatic01.fq trimmomatic_PE01/INDEX ${result_dir_01}
done

# mkdir RSEM_PE_parameter
# for seqlib in ${SEQLIBS[@]}; do
#     mkdir RSEM_PE_parameter/Ec-H${seqlib}_paired_nofastx_exp_rsem
#     result_dir_01=RSEM_PE_parameter/Ec-H${seqlib}_paired_nofastx_exp_rsem
#     rsem-calculate-expression -p 32 --paired-end --bowtie2 --bowtie2-path ~/.linuxbrew/bin --estimate-rspd --append-names --output-genome-bam trimmomatic_PE_parameter01/paired_Ec-H${seqlib}_R1_trimmomatic01.fq trimmomatic_PE_parameter01/paired_Ec-H${seqlib}_R2_trimmomatic01.fq trimmomatic_PE_parameter01/INDEX ${result_dir_01}
#     mkdir RSEM_PE_parameter/Ec-H${seqlib}_paired_fastx_exp_rsem
#     result_dir_02=RSEM_PE_parameter/Ec-H${seqlib}_paired_fastx_exp_rsem
#     rsem-calculate-expression -p 32 --paired-end --bowtie2 --bowtie2-path ~/.linuxbrew/bin --estimate-rspd --append-names --output-genome-bam trimmomatic_PE_parameter01/paired_Ec-H${seqlib}_R1_trimmomatic01_fastx01.fq trimmomatic_PE_parameter01/paired_Ec-H${seqlib}_R2_trimmomatic01_fastx01.fq trimmomatic_PE_parameter01/INDEX ${result_dir_02}
#     mkdir RSEM_PE_parameter/Ec-H${seqlib}_unpaired_nofastx_exp_rsem
#     result_dir_03=RSEM_PE_parameter/Ec-H${seqlib}_unpaired_nofastx_exp_rsem
#     rsem-calculate-expression -p 32 --paired-end --bowtie2 --bowtie2-path ~/.linuxbrew/bin --estimate-rspd --append-names --output-genome-bam trimmomatic_PE_parameter01/unpaired_Ec-H${seqlib}_R1_trimmomatic01.fq trimmomatic_PE_parameter01/unpaired_Ec-H${seqlib}_R2_trimmomatic01.fq trimmomatic_PE_parameter01/INDEX ${result_dir_03}
#     mkdir RSEM_PE_parameter/Ec-H${seqlib}_unpaired_fastx_exp_rsem
#     result_dir_04=RSEM_PE_parameter/Ec-H${seqlib}_unpaired_fastx_exp_rsem
#     rsem-calculate-expression -p 32 --paired-end --bowtie2 --bowtie2-path ~/.linuxbrew/bin --estimate-rspd --append-names --output-genome-bam trimmomatic_PE_parameter01/unpaired_Ec-H${seqlib}_R1_trimmomatic01_fastx01.fq trimmomatic_PE_parameter01/unpaired_Ec-H${seqlib}_R2_trimmomatic01_fastx01.fq trimmomatic_PE_parameter01/INDEX ${result_dir_04}
# done

# RSEM_PE/Ec-H4_unpaired_nofastx_exp_rsem欠.genes.results, .genome.bam, .isoforms.results, .transcript.bam, 1つ.tempというファイルが多い．
# RSEM_PE_parameter内，H1はpaired_fastx, unpaired_nofastx, H2はpaired_fastx, unpaired_fastx, unpaired_nofastx, H3はpaired_fastx, unpaired_nofastx, H4は，paired_fastx, unpaired_fastx, unpaired_nofastxが上行4ファイル欠けて1ファイル増え，通常は1TPにpaired, unpaired, fastx, nofastxの4種の組み合わせがある．

for seqlib in ${SEQLIBS[@]}; do
    rsem-plot-model RSEM_noqc/Ec_H${seqlib}_exp_rsem RSEM_noqc/Ec_H${seqlib}_diagnostic.pdf
    rsem-plot-transcript-wiggles --gene-list --show-unique RSEM_noqc/Ec_H${seqlib}_exp_rsem gene_ids.txt RSEM_noqc/Ec_H${seqlib}_transcript_wiggle.pdf
    rsem-bam2wig RSEM_noqc/Ec_H${seqlib}_exp_rsem.genome.bam RSEM_noqc/Ec_H${seqlib}.wig Mapping/INDEX
    samtools sort -@ 32 RSEM_noqc/Ec_H${seqlib}_exp_rsem.genome.bam > RSEM_noqc/Ec_H${seqlib}_exp_rsem.genome.sorted.bam
    samtools index RSEM_noqc/Ec_H${seqlib}_exp_rsem.genome.sorted.bam -@ 32
done
for seqlib in ${SEQLIBS[@]}; do
    rsem-plot-model RSEM_PE/Ec_H${seqlib}_paired_nofastx_exp_rsem RSEM_PE/Ec_H${seqlib}_diagnostic.pdf
    rsem-plot-transcript-wiggles --gene-list --show-unique RSEM_PE/Ec_H${seqlib}_paired_nofastx_exp_rsem gene_ids.txt RSEM_PE/Ec_H${seqlib}_transcript_wiggle.pdf
    rsem-bam2wig RSEM_PE/Ec_H${seqlib}_paired_nofastx_exp_rsem.genome.bam RSEM_PE/Ec_H${seqlib}.wig trimmomatic_PE01/INDEX
    samtools sort -@ 32 RSEM_PE/Ec_H${seqlib}_paired_nofastx_exp_rsem.genome.bam > RSEM_PE/Ec_H${seqlib}_exp_rsem.genome.sorted.bam
    samtools index RSEM_PE/Ec_H${seqlib}_exp_rsem.genome.sorted.bam -@ 32
done

mkdir htseq_noqc
for seqlib in ${SEQLIBS[@]}; do
    htseq-count -f bam -r pos sam_noqc/Ec_H${seqlib}.unique.sort.bam Mapping/Escherichia_coli_bw25113.ASM75055v1.44.gtf > htseq_noqc/Ec_H${seqlib}_count_data.txt
done
mkdir htseq_PE
for seqlib in ${SEQLIBS[@]}; do
    htseq-count -f bam -r pos sam_PE_nofastx/paired_Ec_H${seqlib}_trimmomatic01.unique.sort.bam trimmomatic_PE01/Escherichia_coli_bw25113.ASM75055v1.44.gtf > htseq_PE/Ec_H${seqlib}_trimmomatic01_count_data.txt
done
