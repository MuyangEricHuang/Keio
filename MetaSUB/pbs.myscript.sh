#!/usr/bin/bash
# Last update: 03/30/2023
#PBS -q blast
#PBS -l mem=96GB
#PBS -N pbs.myscript.sh
set -eu pipefail

cd 

mkdir gCSD_Tsuruoka
cd gCSD_Tsuruoka
mkdir raw script analyses
cd raw
# wget ~

gpg --print-md md5 DNBSEQ_203_Read1.fq.gz
gpg --print-md md5 DNBSEQ_203_Read2.fq.gz
cat *.md5
cd ..

#クオリティ管理にはFASTQC, アダプタートリミングにはCutadapt, リードのプルーニングとフィルター処理にはTrimmomaticを使用するのが典型的な組み合わせ．
#レポートのAdaptersのセクションのother adapter sequencesの行が見つかる．

# fastp -i raw/DNBSEQ_203_Read1.fq -I raw/DNBSEQ_203_Read2.fq -o analyses/203_R1_qc.fq.gz -O analyses/203_R2_qc.fq.gz -h analyses/203.report.html -j analyses/203.report.json -q 20 -t 1 -T 1 -l 20 -w $(getconf _NPROCESSORS_ONLN)
fastp -i raw/DNBSEQ_203_Read1.fq -I raw/DNBSEQ_203_Read2.fq -o analyses/203_R1_qc_dafp.fq.gz -O analyses/203_R2_qc_dafp.fq.gz -h analyses/203_dafp.report.html -j analyses/203_dafp.report.json -q 20 -t 1 -T 1 -l 20 --detect_adapter_for_pe -w $(getconf _NPROCESSORS_ONLN)
multiqc .

# mv analyses/203_R1_qc.fq.gz analyses/203_R1_qc.fq.gz.Z
# mv analyses/203_R2_qc.fq.gz analyses/203_R2_qc.fq.gz.Z
# zcat analyses/203_R1_qc.fq.gz > analyses/203.fq
# zcat analyses/203_R2_qc.fq.gz >> analyses/203.fq

mv analyses/203_R1_qc_dafp.fq.gz analyses/203_R1_qc_dafp.fq.gz.Z
mv analyses/203_R2_qc_dafp.fq.gz analyses/203_R2_qc_dafp.fq.gz.Z
zcat analyses/203_R1_qc_dafp.fq.gz > analyses/203_dafp.fq
zcat analyses/203_R2_qc_dafp.fq.gz >> analyses/203_dafp.fq

mkdir database
metaphlan --install --bowtie2db database

# metaphlan analyses/203.fq --input_type fastq --bowtie2db database --nproc $(getconf _NPROCESSORS_ONLN) > analyses/203_profile.txt
metaphlan analyses/203_dafp.fq --input_type fastq --bowtie2db database --nproc $(getconf _NPROCESSORS_ONLN) > analyses/203_dafp_profile_1.txt
metaphlan analyses/203_dafp.fq --input_type fastq --bowtie2db database/mpa_v30_CHOCOPhlAn_201901 --nproc $(getconf _NPROCESSORS_ONLN) > analyses/203_dafp_profile_2.txt

merge_metaphlan_tables.py analyses/203_dafp_profile_1.txt > analyses/merged_abundance_table_1.txt
merge_metaphlan_tables.py analyses/203_dafp_profile_2.txt > analyses/merged_abundance_table_2.txt

grep -E "s__|clade" analyses/merged_abundance_table_1.txt | sed 's/^.*s__//g' | cut -f1,3-8 | sed -e 's/clade_name/body_site/g' > analyses/merged_abundance_table_species_1.txt
grep -E "s__|clade" analyses/merged_abundance_table_2.txt | sed 's/^.*s__//g' | cut -f1,3-8 | sed -e 's/clade_name/body_site/g' > analyses/merged_abundance_table_species_2.txt

hclust2.py -i analyses/merged_abundance_table_species_1.txt -o analyses/abundance_heatmap_species_1.png --f_dist_f braycurtis --s_dist_f braycurtis --cell_aspect_ratio 0.5 -l --flabel_size 10 --slabel_size 10 --max_flabel_len 100 --max_slabel_len 100 --minv 0.1 --dpi 300
hclust2.py -i analyses/merged_abundance_table_species_2.txt -o analyses/abundance_heatmap_species_2.png --f_dist_f braycurtis --s_dist_f braycurtis --cell_aspect_ratio 0.5 -l --flabel_size 10 --slabel_size 10 --max_flabel_len 100 --max_slabel_len 100 --minv 0.1 --dpi 300
