#!/usr/bin/sh
#PBS -j oe
#PBS -o ./data/tmp/rsem_200908/log
#PBS -q all.q
#PBS -t 1-11%11
#PBS -l nodes=1:ppn=32

cd $PBS_O_WORKDIR

index=${PBS_ARRAYID}
in_dir="data/tmp/trimmed_fq_fastp"
out_dir="data/tmp/rsem_200908"

rsem-calculate-expression \
 --num-threads 32 --paired-end --bowtie2 --bowtie2-path ~/opt/ --estimate-rspd --append-names\
 --output-genome-bam ${in_dir}/mrna_H${index}_1.fq ${in_dir}/mrna_H${index}_2.fq\
 ${out_dir}/ec_rsem_ref ${out_dir}/${index}_expression 2> ${out_dir}/${index}_log.txt

echo ${index} >> ${out_dir}/time.txt
date >> ${out_dir}/time.txt
