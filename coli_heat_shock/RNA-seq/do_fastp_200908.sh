#!/usr/bin/sh
#PBS -j oe
#PBS -o ./data/tmp/trimmed_fq_fastp/log
#PBS -q all.q
#PBS -t 1-11%6
#PBS -l nodes=1:ppn=16

cd $PBS_O_WORKDIR

index=${PBS_ARRAYID}
in_dir="../data/200903_mRNA/Sequence/Ec_H${index}"
out_dir="data/tmp/trimmed_fq_fastp"

fastp -i ${in_dir}/Ec_H${index}_1.fq.gz -I ${in_dir}/Ec_H${index}_2.fq.gz\
 -o ${out_dir}/mrna_H${index}_1.fq -O ${out_dir}/mrna_H${index}_2.fq\
 -h ${out_dir}/report_H${index}.html -j ${out_dir}/report_H${index}.json\
 --detect_adapter_for_pe -5 -3 -q 15 -n 10 -l 20 -w 16

echo ${index} >> ${out_dir}/time.txt
date >> ${out_dir}/time.txt
