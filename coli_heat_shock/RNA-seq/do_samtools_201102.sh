#!/usr/bin/bash

input_dir="data/tmp/rsem_200908"
#samtools view -@ 32 -bS ${input_dir}/0.sam > ${input_dir}/0.bam &
#wait
#samtools sort -@ 32 -o ${input_dir}/1_expression.genome.sorted.bam ${input_dir}/1_expression.genome.bam &
#wait
#samtools index ${input_dir}/1_expression.genome.sorted.bam
#samtools view -@ 32 ${input_dir}/1_expression.genome.sorted.bam > ${input_dir}/1_expression.genome.sorted.sam

samtools sort -@ 32  ${input_dir}/1_expression.genome.bam > ${input_dir}/1_expression.genome.sorted2.bam &
wait
samtools index ${input_dir}/1_expression.genome.sorted2.bam
samtools view -@ 32 ${input_dir}/1_expression.genome.sorted2.bam > ${input_dir}/1_expression.genome.sorted2.sam
