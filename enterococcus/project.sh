#!/bin/bash
# Last update: 12/30/2021
set -eu pipefail

mkdir 2021_gew
cd 2021_gew/
cp /home/gaou/gew/2021/BC11.fastq.gz .
cp /home/gaou/gew/2021/report_FAP20986_20211022_1525_282fadcf-BC08-10.pdf .
mkdir Illumina
cd Illumina/
cp /home/gaou/gew/2021/illumina/GEW-BC11_S5_merged_R1.fq.gz .
cd ..
mkdir NanoPlot
cd NanoPlot/
cp -r /home/gaou/gew/2021/NanoPlot/BC11/ .
cp /home/gaou/gew/2021/NanoPlot/BC12NanoPlot_20211026_1109.log .
cd ..

gunzip BC11.fastq.gz

# リードのフィルタリング．

/home/gaou/kumamushi/software_smith/bbmap/stats.sh BC11.fastq
# A       C       G       T       N       IUPAC   Other   GC      GC_stdev
# 0.3097  0.1886  0.1921  0.3096  0.0000  0.0000  0.0000  0.3807  0.0508

# Main genome scaffold total:             70022
# Main genome contig total:               70022
# Main genome scaffold sequence total:    297.995 MB
# Main genome contig sequence total:      297.995 MB      0.000% gap
# Main genome scaffold N/L50:             10118/8.417 KB
# Main genome contig N/L50:               10118/8.417 KB
# Main genome scaffold N/L90:             35530/2.471 KB
# Main genome contig N/L90:               35530/2.471 KB
# Max scaffold length:                    201.273 KB
# Max contig length:                      201.273 KB
# Number of scaffolds > 50 KB:            36
# % main genome in scaffolds > 50 KB:     0.80%


# Minimum         Number          Number          Total           Total           Scaffold
# Scaffold        of              of              Scaffold        Contig          Contig
# Length          Scaffolds       Contigs         Length          Length          Coverage
# --------        --------------  --------------  --------------  --------------  --------
#     All                 70,022          70,022     297,994,916     297,994,916   100.00%
#      50                 67,120          67,120     297,891,233     297,891,233   100.00%
#     100                 61,668          61,668     297,515,439     297,515,439   100.00%
#     250                 58,312          58,312     296,968,871     296,968,871   100.00%
#     500                 55,050          55,050     295,761,781     295,761,781   100.00%
#    1 KB                 49,179          49,179     291,412,781     291,412,781   100.00%
#  2.5 KB                 35,275          35,275     267,572,629     267,572,629   100.00%
#    5 KB                 19,265          19,265     208,580,101     208,580,101   100.00%
#   10 KB                  7,682           7,682     126,660,297     126,660,297   100.00%
#   25 KB                    756             756      25,373,452      25,373,452   100.00%
#   50 KB                     36              36       2,373,125       2,373,125   100.00%
#  100 KB                      1               1         201,273         201,273   100.00%

# ==========
# Scaffold totalで70022本のリードを読めていることが分かる．
# Scaffold sequence totalで実際に297.995 MB塩基読まれていることが分かる．
# Max scaffold lengthで最長の配列は201.273 KBで，Illumina等と比べると大分違うことが分かる．
# N50は8.417 KB.
# 10 KBは約40×.
# ==========

scp -r t18301mh@cs0.bioinfo.ttck.keio.ac.jp:/home/t18301mh/2021_gew/NanoPlot/BC11 ~/Downloads/.
open ~/Downloads/BC11

# ==========
# Histogram of read lengths:
#  リードの長さとその分布．
# Read length vs Average read quality plot:
#  クオリティーの分布．
#  Q10は97~99%.
# ==========
# ==========
# NCBIでenterococcus faecalisのgenomeを検索:
#  https://www.ncbi.nlm.nih.gov/genome/?term=enterococcus%20faecalis
#  Enterococcus faecalis EnGen0336
#  Statistics:	 median total length (Mb): 2.97338
#  写メではReference genomeはEnterococcus faecalis EnGen0336で2.87
#  50×の場合:
#   2.97 ×50 ~ 2.87 ×50
#   148.669 ~ 143.5 M 
#  結果から見ると，10KBは126,660,297あるので，これはおよそ40×
#  基本20× ~ 50×にあれば良いので十分．
# ==========

/home/gaou/kumamushi/software_smith/bbmap/reformat.sh in=BC11.fastq out=BC11-
# filter10k.fq minlength=10000 qin=33
# Input is being processed as unpaired
# Input:                          70022 reads             297994916 bases
# Short Read Discards:            62340 reads (89.03%)    171334619 bases (57.50%)
# Output:                         7682 reads (10.97%)     126660297 bases (42.50%)

# Time:                           1.899 seconds.
# Reads Processed:       70022    36.86k reads/sec
# Bases Processed:        297m    156.88m bases/sec

/home/gaou/kumamushi/software_smith/bbmap/stats.sh BC11-filter10k.fq
# A       C       G       T       N       IUPAC   Other   GC      GC_stdev
# 0.3093  0.1883  0.1920  0.3104  0.0000  0.0000  0.0000  0.3802  0.0244

# Main genome scaffold total:             7682
# Main genome contig total:               7682
# Main genome scaffold sequence total:    126.660 MB
# Main genome contig sequence total:      126.660 MB      0.000% gap
# Main genome scaffold N/L50:             2675/16.482 KB
# Main genome contig N/L50:               2675/16.482 KB
# Main genome scaffold N/L90:             6476/11.02 KB
# Main genome contig N/L90:               6476/11.02 KB
# Max scaffold length:                    201.273 KB
# Max contig length:                      201.273 KB
# Number of scaffolds > 50 KB:            36
# % main genome in scaffolds > 50 KB:     1.87%


# Minimum         Number          Number          Total           Total           Scaffold
# Scaffold        of              of              Scaffold        Contig          Contig
# Length          Scaffolds       Contigs         Length          Length          Coverage
# --------        --------------  --------------  --------------  --------------  --------
#     All                  7,682           7,682     126,660,297     126,660,297   100.00%
#    5 KB                  7,682           7,682     126,660,297     126,660,297   100.00%
#   10 KB                  7,682           7,682     126,660,297     126,660,297   100.00%
#   25 KB                    756             756      25,373,452      25,373,452   100.00%
#   50 KB                     36              36       2,373,125       2,373,125   100.00%
#  100 KB                      1               1         201,273         201,273   100.00%

# Canuでのアセンブリー．

qsub -I -l nodes=1:ppn=32
# qsub -I -l nodes=k03:ppn=32

/home/gaou/kumamushi/software_smith/canu-2.2/bin/canu -nanopore-raw BC11-filter10k.fq -d BC11_1 -p BC11_1 -fast useGrid=false genomeSize=3m maxThreads=32
/home/gaou/kumamushi/software_smith/bbmap/stats.sh BC11_1/BC11_1.contigs.fasta
# A       C       G       T       N       IUPAC   Other   GC      GC_stdev
# 0.3103  0.1878  0.1866  0.3154  0.0000  0.0000  0.0000  0.3744  0.0135

# Main genome scaffold total:             2
# Main genome contig total:               2
# Main genome scaffold sequence total:    2.975 MB
# Main genome contig sequence total:      2.975 MB        0.000% gap
# Main genome scaffold N/L50:             1/2.885 MB
# Main genome contig N/L50:               1/2.885 MB
# Main genome scaffold N/L90:             1/2.885 MB
# Main genome contig N/L90:               1/2.885 MB
# Max scaffold length:                    2.885 MB
# Max contig length:                      2.885 MB
# Number of scaffolds > 50 KB:            2
# % main genome in scaffolds > 50 KB:     100.00%


# Minimum         Number          Number          Total           Total           Scaffold
# Scaffold        of              of              Scaffold        Contig          Contig
# Length          Scaffolds       Contigs         Length          Length          Coverage
# --------        --------------  --------------  --------------  --------------  --------
#     All                      2               2       2,974,837       2,974,837   100.00%
#   50 KB                      2               2       2,974,837       2,974,837   100.00%
#  100 KB                      1               1       2,884,939       2,884,939   100.00%
#  250 KB                      1               1       2,884,939       2,884,939   100.00%
#  500 KB                      1               1       2,884,939       2,884,939   100.00%
#    1 MB                      1               1       2,884,939       2,884,939   100.00%
#  2.5 MB                      1               1       2,884,939       2,884,939   100.00%

/home/gaou/kumamushi/software_smith/canu-2.2/bin/canu -nanopore-raw BC11-filter10k.fq -d BC11_1 -p BC11_2 useGrid=false genomeSize=3m maxThreads=32
/home/gaou/kumamushi/software_smith/bbmap/stats.sh BC11_2/BC11_2.contigs.fasta
# A       C       G       T       N       IUPAC   Other   GC      GC_stdev
# 0.3103  0.1878  0.1866  0.3154  0.0000  0.0000  0.0000  0.3744  0.0135

# Main genome scaffold total:             2
# Main genome contig total:               2
# Main genome scaffold sequence total:    2.975 MB
# Main genome contig sequence total:      2.975 MB        0.000% gap
# Main genome scaffold N/L50:             1/2.885 MB
# Main genome contig N/L50:               1/2.885 MB
# Main genome scaffold N/L90:             1/2.885 MB
# Main genome contig N/L90:               1/2.885 MB
# Max scaffold length:                    2.885 MB
# Max contig length:                      2.885 MB
# Number of scaffolds > 50 KB:            2
# % main genome in scaffolds > 50 KB:     100.00%


# Minimum         Number          Number          Total           Total           Scaffold
# Scaffold        of              of              Scaffold        Contig          Contig
# Length          Scaffolds       Contigs         Length          Length          Coverage
# --------        --------------  --------------  --------------  --------------  --------
#     All                      2               2       2,974,947       2,974,947   100.00%
#   50 KB                      2               2       2,974,947       2,974,947   100.00%
#  100 KB                      1               1       2,884,967       2,884,967   100.00%
#  250 KB                      1               1       2,884,967       2,884,967   100.00%
#  500 KB                      1               1       2,884,967       2,884,967   100.00%
#    1 MB                      1               1       2,884,967       2,884,967   100.00%
#  2.5 MB                      1               1       2,884,967       2,884,967   100.00%

# 末端処理．

grep ">" BC11_2.contigs.fasta
# >tig00000001 len=2884967 reads=7034 class=contig suggestRepeat=no suggestBubble=no suggestCircular=yes trim=7174-2864934
# >tig00000002 len=89980 reads=138 class=contig suggestRepeat=no suggestBubble=no suggestCircular=yes trim=10444-77950

# 12/28追記==========

# 上が染色体で下がプラスミドの可能性がある．

# 末端部位の検索:
# 1. AAGTCGCCATTAACACTTTATCCAGGTACATCTAATAGTGTCCAAT
# 2. GCCCACCTAAAACTATGACCACAAAAAGTCCACCAATGCTTAAAAACAGTCGTATTTTTCGTTTGTCTTGCATACTTTACTCTCCTTTTACATA

# アセンブリークオリティの検証．

# Job Title: 01st-gVolante:
# ----------------------------------------------------------------------
# gVolante Analysis: ver.2.0.0

# Summary of the submitted job:
# JOB_ID: 202112290053-MUFDD3U2A91DL1UL
# PROJECT_NAME: 01st-gVolante
# FASTA_FILE: BC11-2.contigs-removed.fasta
# MIN_LENGTH_OF_SEQ_STATS: 1
# ASSEMBLY_TYPE: genome
# PROGRAM: BUSCO_v1
# SELECTED_REFERENCE_GENE_SET: Bacteria
# ----------------------------------------------------------------------
# Result: Core gene set = 39 (97.50%)
# https://gvolante.riken.jp/script/detail.cgi?202112290053-MUFDD3U2A91DL1UL
# Detected as Missing: COG0184
# COG0184: RpsO 
# Ribosomal protein S15P/S13E [Translation, ribosomal structure and biogenesis]
# COG0184 is a member of the superfamily cl00349.


# Job Title: 01st-DFAST:
# Rank: species; Taxon: Enterococcus faecalis (20 genomes, 298 marker sets).
# Result: Completeness: 98.41%; Contamination: 0.14%.


# エラーコレクション．

mkdir error_correction_1
/home/gaou/kumamushi/software_smith/bwa-0.7.11/bwa index BC11-2.contigs-removed.fasta
# [bwa_index] Pack FASTA... 0.04 sec
# [bwa_index] Construct BWT for the packed sequence...
# [bwa_index] 0.77 seconds elapse.
# [bwa_index] Update BWT... 0.03 sec
# [bwa_index] Pack forward-only FASTA... 0.03 sec
# [bwa_index] Construct SA from BWT and Occ... 0.28 sec
# [main] Version: 0.7.11-r1034
# [main] CMD: /home/gaou/kumamushi/software_smith/bwa-0.7.11/bwa index BC11-2.contigs-removed.fasta
# [main] Real time: 1.238 sec; CPU: 1.160 sec
gunzip Illumina/GEW-BC11_S5_merged_R1.fq.gz
/home/gaou/kumamushi/software_smith/bwa-0.7.11/bwa mem -t 32 BC11-2.contigs-removed.fasta Illumina/GEW-BC11_S5_merged_R1.fq | /home/gaou/kumamushi/software_smith/samtools-1.9/samtools view -@ 32 -b -o error_correction_1/aln.bam -
# [M::bwa_idx_load_from_disk] read 0 ALT contigs
# [M::process] read 4267406 sequences (320000053 bp)...
# [M::mem_process_seqs] Processed 4267406 reads in 197.896 CPU sec, 11.828 real sec
# [M::process] read 4267886 sequences (320000013 bp)...
# [M::mem_process_seqs] Processed 4267886 reads in 172.051 CPU sec, 5.880 real sec
# [M::process] read 4267162 sequences (320000101 bp)...
# [M::mem_process_seqs] Processed 4267162 reads in 186.243 CPU sec, 6.062 real sec
# [M::process] read 4267700 sequences (320000058 bp)...
# [M::mem_process_seqs] Processed 4267700 reads in 162.162 CPU sec, 5.517 real sec
# [M::process] read 4267440 sequences (320000027 bp)...
# [M::mem_process_seqs] Processed 4267440 reads in 170.300 CPU sec, 5.569 real sec
# [M::process] read 4267756 sequences (320000064 bp)...
# [M::mem_process_seqs] Processed 4267756 reads in 166.643 CPU sec, 5.739 real sec
# [M::process] read 4267658 sequences (320000013 bp)...
# [M::process] read 2254447 sequences (169011728 bp)...
# [M::mem_process_seqs] Processed 4267658 reads in 153.991 CPU sec, 5.151 real sec
# [M::mem_process_seqs] Processed 2254447 reads in 90.172 CPU sec, 3.728 real sec
# [main] Version: 0.7.11-r1034
# [main] CMD: /home/gaou/kumamushi/software_smith/bwa-0.7.11/bwa mem -t 32 BC11-2.contigs-removed.fasta Illumina/GEW-BC11_S5_merged_R1.fq
# [main] Real time: 81.399 sec; CPU: 1342.168 sec
/home/gaou/kumamushi/software_smith/samtools-1.9/samtools sort -T sort.tmp -o error_correction_1/aln.sorted.bam -@ 32 error_correction_1/aln.bam
# [bam_sort_core] merging from 0 files and 16 in-memory blocks...
/home/gaou/kumamushi/software_smith/samtools-1.9/samtools index error_correction_1/aln.sorted.bam

java -Xms8g -jar /home/gaou/kumamushi/software_smith/pilon-1.23.jar --genome BC11-2.contigs-removed.fasta --bam error_correction_1/aln.sorted.bam --threads 16 --output pilon1
# Pilon version 1.23 Mon Nov 26 16:04:05 2018 -0500
# Genome: BC11-2.contigs-removed.fasta
# Fixing snps, indels, gaps, local
# Input genome size: 2925260
# Scanning BAMs
# aln.sorted.bam: 32230986 reads, 0 filtered, 31390418 mapped, 0 proper, 0 stray, Unpaired 100% 75+/-4, max 86 unpaired
# Processing tig00000002:1-67506
# Processing tig00000001:1-2857754
# tig00000002:1-67506 log:
# unpaired aln.sorted.bam: coverage 638
# Total Reads: 786779, Coverage: 638, minDepth: 64
# Confirmed 67432 of 67506 bases (99.89%)
# Corrected 1 snps; 0 ambiguous bases; corrected 51 small insertions totaling 64 bases, 2 small deletions totaling 2 bases
# # Attempting to fix local continuity breaks
# fix break: tig00000002:22971-22991 22980 -7 +12 BreakFix
# # fix break: tig00000002:38000-38045 0 -0 +0 NoSolution
# # fix break: tig00000002:38606-38624 0 -0 +0 NoSolution
# # fix break: tig00000002:48397-48633 0 -0 +0 NoSolution
# Finished processing tig00000002:1-67506
# tig00000001:1-2857754 log:
# unpaired aln.sorted.bam: coverage 588
# Total Reads: 30603639, Coverage: 588, minDepth: 59
# Confirmed 2856516 of 2857754 bases (99.96%)
# Corrected 5 snps; 0 ambiguous bases; corrected 1156 small insertions totaling 1406 bases, 4 small deletions totaling 4 bases
# Large collapsed region: tig00000001:2799301-2838323 size 39023
# # Attempting to fix local continuity breaks
# fix break: tig00000001:14927-14931 14927 -30 +34 BreakFix
# fix break: tig00000001:496246 496319 -11 +14 BreakFix
# # fix break: tig00000001:1287986-1288034 0 -0 +0 NoSolution
# # fix break: tig00000001:1310793-1310801 0 -0 +0 NoSolution
# # fix break: tig00000001:1361621 0 -0 +0 NoSolution
# # fix break: tig00000001:2188198-2188219 0 -0 +0 NoSolution
# # fix break: tig00000001:2254232-2254277 0 -0 +0 NoSolution
# Finished processing tig00000001:1-2857754
# Writing updated tig00000001_pilon to pilon1.fasta
# Writing updated tig00000002_pilon to pilon1.fasta
# Mean unpaired coverage: 589
# Mean total coverage: 589

# 2回目．

mkdir error_correction_2
/home/gaou/kumamushi/software_smith/bwa-0.7.11/bwa index pilon1.fasta
# [bwa_index] Pack FASTA... 0.05 sec
# [bwa_index] Construct BWT for the packed sequence...
# [bwa_index] 0.81 seconds elapse.
# [bwa_index] Update BWT... 0.03 sec
# [bwa_index] Pack forward-only FASTA... 0.02 sec
# [bwa_index] Construct SA from BWT and Occ... 0.26 sec
# [main] Version: 0.7.11-r1034
# [main] CMD: /home/gaou/kumamushi/software_smith/bwa-0.7.11/bwa index pilon1.fasta
# [main] Real time: 1.232 sec; CPU: 1.186 sec
/home/gaou/kumamushi/software_smith/bwa-0.7.11/bwa mem -t 32 pilon1.fasta Illumina/GEW-BC11_S5_merged_R1.fq | /home/gaou/kumamushi/software_smith/samtools-1.9/samtools view -@ 32 -b -o error_correction_2/aln.bam -
# [M::bwa_idx_load_from_disk] read 0 ALT contigs
# [M::process] read 4267406 sequences (320000053 bp)...
# [M::mem_process_seqs] Processed 4267406 reads in 185.212 CPU sec, 11.269 real sec
# [M::process] read 4267886 sequences (320000013 bp)...
# [M::mem_process_seqs] Processed 4267886 reads in 184.892 CPU sec, 9.736 real sec
# [M::process] read 4267162 sequences (320000101 bp)...
# [M::process] read 4267700 sequences (320000058 bp)...
# [M::mem_process_seqs] Processed 4267162 reads in 142.942 CPU sec, 4.781 real sec
# [M::mem_process_seqs] Processed 4267700 reads in 193.344 CPU sec, 10.418 real sec
# [M::process] read 4267440 sequences (320000027 bp)...
# [M::process] read 4267756 sequences (320000064 bp)...
# [M::mem_process_seqs] Processed 4267440 reads in 140.470 CPU sec, 4.620 real sec
# [M::mem_process_seqs] Processed 4267756 reads in 197.813 CPU sec, 10.372 real sec
# [M::process] read 4267658 sequences (320000013 bp)...
# [M::process] read 2254447 sequences (169011728 bp)...
# [M::mem_process_seqs] Processed 4267658 reads in 143.899 CPU sec, 4.856 real sec
# [M::mem_process_seqs] Processed 2254447 reads in 89.071 CPU sec, 4.079 real sec
# [main] Version: 0.7.11-r1034
# [main] CMD: /home/gaou/kumamushi/software_smith/bwa-0.7.11/bwa mem -t 32 pilon1.fasta Illumina/GEW-BC11_S5_merged_R1.fq
# [main] Real time: 98.571 sec; CPU: 1327.346 sec
/home/gaou/kumamushi/software_smith/samtools-1.9/samtools sort -T sort.tmp -o error_correction_2/aln.sorted.bam -@ 32 error_correction_2/aln.bam
# [bam_sort_core] merging from 0 files and 32 in-memory blocks...
/home/gaou/kumamushi/software_smith/samtools-1.9/samtools index error_correction_2/aln.sorted.bam

java -Xms8g -jar /home/gaou/kumamushi/software_smith/pilon-1.23.jar --genome pilon1.fasta --bam error_correction_2/aln.sorted.bam --threads 32 --output pilon2
# Pilon version 1.23 Mon Nov 26 16:04:05 2018 -0500
# Genome: pilon1.fasta
# Fixing snps, indels, gaps, local
# Input genome size: 2926729
# Scanning BAMs
# error_correction_2/aln.sorted.bam: 32231856 reads, 0 filtered, 31393952 mapped, 0 proper, 0 stray, Unpaired 100% 75+/-4, max 86 unpaired
# Processing tig00000001_pilon:1-2859161
# Processing tig00000002_pilon:1-67568
# tig00000002_pilon:1-67568 log:
# unpaired error_correction_2/aln.sorted.bam: coverage 639
# Total Reads: 789524, Coverage: 639, minDepth: 64
# Confirmed 67548 of 67568 bases (99.97%)
# Corrected 0 snps; 0 ambiguous bases; corrected 0 small insertions totaling 0 bases, 0 small deletions totaling 0 bases
# # Attempting to fix local continuity breaks
# # fix break: tig00000002_pilon:38040-38085 0 -0 +0 NoSolution
# Finished processing tig00000002_pilon:1-67568
# tig00000001_pilon:1-2859161 log:
# unpaired error_correction_2/aln.sorted.bam: coverage 588
# Total Reads: 30604428, Coverage: 588, minDepth: 59
# Confirmed 2859092 of 2859161 bases (100.00%)
# Corrected 3 snps; 0 ambiguous bases; corrected 0 small insertions totaling 0 bases, 4 small deletions totaling 5 bases
# Large collapsed region: tig00000001_pilon:2800691-2839722 size 39032
# # Attempting to fix local continuity breaks
# fix break: tig00000001_pilon:496465-496552 496539 -14 +11 BreakFix
# # fix break: tig00000001_pilon:1288612-1288660 0 -0 +0 NoSolution
# # fix break: tig00000001_pilon:2255360-2255405 0 -0 +0 NoSolution
# Finished processing tig00000001_pilon:1-2859161
# Writing updated tig00000001_pilon_pilon to pilon2.fasta
# Writing updated tig00000002_pilon_pilon to pilon2.fasta
# Mean unpaired coverage: 589
# Mean total coverage: 589
