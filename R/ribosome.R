#' ---
#' title: "Assignment 11 - My Draft Report"
#' author: '@Mokuyo_Koh(71843014)'
#' date: "`r Sys.Date()`"
#' output:
#'    html_document:
#'      toc: true
#' ---

#' # [Compiling Reports from R Scripts](https://rmarkdown.rstudio.com/articles_report_from_r_script.html)

#' # Assignment 11 - My Draft Report
#' - Integrate and modify your previous assignments (e.g. results of analyzing DNA/protein sequences of interest) in order to produce a draft report, and submit it as a PDF/HTML document.
#' - これまでの課題（興味あるDNA/タンパク質の配列を解析した結果等）を統合・修正してレポートのドラフトを作成し，PDF/HTML形式ファイルで提出する．
#' 
#' # リボソームタンパク質の部分的機能変異と分子進化
#' 
#' ## 1. リボソーム複合体の一部であるリボソームタンパク質(s)
#' ![リボソーム複合体の一部であるリボソームタンパク質(s).](/Users/huang/Desktop/Keio/2020_Spring/Tues./Period3_Data_Science_for_Genome_Dynamics_[DS2]/11th_Jul.14th/1.png)
#' 
#' ## 2. 背景
#' - ### ○リボソームとは:
#'   - #### アミノ酸を重合させてタンパク質を合成
#'   - #### 生物の細胞中に普遍的に存在
#' - ### ○リボソームタンパク質とは:
#'   - #### 50Sと30Sの大小各1個ずつのサブユニットから構成

#' - ### ○S7について:
#'   - #### 16S rRNAとではなくtRNAとの相互作用
#'   ![完全に溶媒領域にさらされたフレキシブルなβアームとα6](/Users/huang/Desktop/Keio/2020_Spring/Tues./Period3_Data_Science_for_Genome_Dynamics_[DS2]/11th_Jul.14th/S7のβアームとα6.png)
#'   完全に溶媒領域にさらされたフレキシブルなβアームとα6 .
#' - ### ○L2について:
#'   - #### 2つの核酸結合モチーフを持つ
#'   - #### 核酸結合タンパク質の間での分子進化を示唆
#'   ![*Bacillus*由来のL2と*Metanococcus*由来EIF-5Aとの構造，C末はSH3-like barrel,N末はOB-foldと類似](/Users/huang/Desktop/Keio/2020_Spring/Tues./Period3_Data_Science_for_Genome_Dynamics_[DS2]/11th_Jul.14th/L2の2つの核酸結合モチーフ.png)
#'   *Bacillus*由来のL2と*Metanococcus*由来EIF-5Aとの構造，C末はSH3-like barrel,N末はOB-foldと類似．
#' - ### ○L5について:
#'   - #### RRM (RNA Recognition Motif) を持つ
#'   ![L5と類似のモチーフRRM (RNA認識に関わる) を持つタンパク質](/Users/huang/Desktop/Keio/2020_Spring/Tues./Period3_Data_Science_for_Genome_Dynamics_[DS2]/11th_Jul.14th/L5のRRMモチーフ.png)
#'   L5と類似のモチーフRRM (RNA認識に関わる) を持つタンパク質．
#' 
#' ## 3. 対象と手法
#' ### 対象生物:
#' - バクテリア:
#'   - モデル生物:
#'     - 大腸菌（*Escherichia coli*）
#'     - 枯草菌（*Bacillus subtilis*）
#'     - シアノバクテリア（*Cyanobacteria*）
#'     - サーマス・サーモフィルス（*Thermus thermophilus*）
#'   - 非モデル生物:
#'     - ゲオバチルス・ステアロサーモフィルス（*Bacillus stearothermophilus*）
#' - 古細菌:
#'   - ハロアーキュラ・マリスモルツイ（*Haloarcula marismortui*）
#'   - メタノカルドコックス・ヤンナスキイ（*Metanococcus jannaschii*）
#'   
#' ### 手法:
#' - NCBIより対象生物のタンパク質アミノ酸配列のダウンロード
#' - アミノ酸配列に対するマルチプルアライメント解析
#' - 系統樹の描画
#' - PDBによるタンパク質の立体構造の確認
#' - Chimeraで変異が起きたアミノ酸のマッピング
#' - 変異がもたらすタンパク質の機能変化の考察
#' - 分子進化について議論
#' 
#' ## 環境:
#' ```
#' huang@MuyangnoMBP ~ % uname -a
#' Darwin MuyangnoMBP 19.4.0 Darwin Kernel Version 19.4.0: Wed Mar  4 22:28:40 PST 2020; root:xnu-6153.101.6~15/RELEASE_X86_64 x86_64
#' 
#' huang@MuyangnoMBP ~ % sw_vers
#' ProductName:	Mac OS X
#' ProductVersion:	10.15.4
#' BuildVersion:	19E287
#' 
#' R version 4.0.0 (2020-04-24) -- "Arbor Day"
#' Copyright (C) 2020 The R Foundation for Statistical Computing
#' Platform: x86_64-apple-darwin17.0 (64-bit)
#' [R.app GUI 1.71 (7827) x86_64-apple-darwin17.0]
#' R.app GUI 1.71 (7827 Catalina build), S. Urbanek & H.-J. Bibiko, © R Foundation for Statistical Computing, 2016
#' RStudio 1.2.5042, © 2009-2020 RStudio, Inc.
#' 
#' Chimera-1.14-mac64, Nov. 13, 2019,  © 2019 Regents of the University of California.  All Rights Reserved.
#' ```

#' # Chunk options
#' 
#' - https://r4ds.had.co.nz/r-markdown.html#chunk-options
#' 
#' ### [Retrieving genome sequence data using SeqinR](http://a-little-book-of-r-for-bioinformatics.readthedocs.io/en/latest/src/chapter1.html#retrieving-genome-sequence-data-using-seqinr).
#' 
#' **RパッケージSeqinRを用いて、アミノ酸配列データを取得する.**
#' 
#' `seqinr`等のパッケージの呼び出し:
# load the R package.
#+ results = "hide"
#+ warning = FALSE
#+ message = FALSE
library(seqinr)
library(Biostrings)
library(msa)
library(ape)

#+ echo = FALSE
#' ## ○S7について:
#' Answer the following questions. For each question, please record your answer, and what you typed into R to get this answer.
#' 
#' Q1. Calculate the genetic distances between > 3 protein sequences of interest. Which are the most closely related proteins, based on the genetic distances?

#+ warning = FALSE
#+ message = FALSE
#+ include = FALSE
seqnames_S7 <- c("P02359", "P21469", "P17291", "P22744", "P32552", "P54063") # Make a vector containing the names of the sequences
# retrieve several sequences from UniProt
retrieve_seqs_uniprot_S7 <- function(ACCESSION) read.fasta(file=paste0("http://www.uniprot.org/uniprot/",ACCESSION,".fasta"), seqtype="AA", strip.desc=TRUE)[[1]]
seqs_S7 <- lapply(seqnames_S7,  retrieve_seqs_uniprot_S7) # Retrieve the sequences and store them in list variable "seqs"
#' write out the sequences to a FASTA file
write.fasta(seqs_S7, seqnames_S7, file="myseq_Assignment_S7.fasta")
#' Read an XStringSet object from a file
mySequences_S7 <- readAAStringSet(file = "myseq_Assignment_S7.fasta")

#+ warning = FALSE
#+ message = FALSE
#+ include = TRUE
#+ echo = FALSE
#' Multiple Sequence Alignment using ClustalW
myAlignment_S7 <- msa(mySequences_S7, "ClustalW")
print(myAlignment_S7, show="complete")

#+ warning = FALSE
#+ message = FALSE
#+ include = FALSE
#' ![S7のConsensus配列](/Users/huang/Desktop/Keio/2020_Spring/Tues./Period3_Data_Science_for_Genome_Dynamics_[DS2]/11th_Jul.14th/S7.png)
#' Chimeraを用いて可視化したS7のConsensus配列．
#' 
#' write an XStringSet object to a file
writeXStringSet(unmasked(myAlignment_S7), file = "myaln_Assignment_S7.fasta")
#' read the FASTA-format alignment into R
myaln_S7 <- read.alignment(file = "myaln_Assignment_S7.fasta", format = "fasta")

#+ warning = FALSE
#+ message = FALSE
#+ include = TRUE
#+ echo = FALSE
#' calculate the genetic distances between the protein sequences
mydist_S7 <- dist.alignment(myaln_S7)
mydist_S7
#' get sequence annotations
unlist(getAnnot(seqs_S7))
#' **Bacillus subtilis(P21469) and Geobacillus stearothermophilus(P22744) are the most closely related proteins, based on the genetic distances.**
#' 
#' Q2. Build an unrooted phylogenetic tree of the proteins, using the neighbour-joining algorithm. Which are the most closely related proteins, based on the tree?
# construct a phylogenetic tree with the neighbor joining algorithm
mytree_S7 <- nj(mydist_S7)
plot.phylo(mytree_S7, type="unrooted")
#' **Bacillus subtilis(P21469) and Geobacillus stearothermophilus(P22744) are the most closely related proteins, based on the tree.**
#' 
#' Q3. Build a rooted phylogenetic tree of the proteins, using an outgroup. Which are the most closely related proteins, based on the tree? What extra information does this tree tell you, compared to the unrooted tree in Q2?
mytree_S7 <- root(mytree_S7, outgroup = "P54063", resolve.root = TRUE)
plot.phylo(mytree_S7, main = "Phylogenetic Tree")
#' **Bacillus subtilis(P21469) and Geobacillus stearothermophilus(P22744) are the most closely related proteins, based on the tree.**
#' **Escherichia coli(P02359) is more closely related to Bacillus subtilis(P21469) and Geobacillus stearothermophilus(P22744) rather than Thermus thermophilus(P17291).**
#' 
#' ## ○L2について:
#' Answer the following questions. For each question, please record your answer, and what you typed into R to get this answer.
#' 
#' Q1. Calculate the genetic distances between > 3 protein sequences of interest. Which are the most closely related proteins, based on the genetic distances?

#+ warning = FALSE
#+ message = FALSE
#+ include = FALSE
seqnames_L2 <- c("P60422", "P42919", "P60405", "P04257", "P20276", "P54017") # Make a vector containing the names of the sequences
# retrieve several sequences from UniProt
retrieve_seqs_uniprot_L2 <- function(ACCESSION) read.fasta(file=paste0("http://www.uniprot.org/uniprot/",ACCESSION,".fasta"), seqtype="AA", strip.desc=TRUE)[[1]]
seqs_L2 <- lapply(seqnames_L2,  retrieve_seqs_uniprot_L2) # Retrieve the sequences and store them in list variable "seqs"
#' write out the sequences to a FASTA file
write.fasta(seqs_L2, seqnames_L2, file="myseq_Assignment_L2.fasta")
#' Read an XStringSet object from a file
mySequences_L2 <- readAAStringSet(file = "myseq_Assignment_L2.fasta")

#+ warning = FALSE
#+ message = FALSE
#+ include = TRUE
#+ echo = FALSE
#' Multiple Sequence Alignment using ClustalW
myAlignment_L2 <- msa(mySequences_L2, "ClustalW")
print(myAlignment_L2, show="complete")

#+ warning = FALSE
#+ message = FALSE
#+ include = FALSE
#' ![L2のConsensus配列](/Users/huang/Desktop/Keio/2020_Spring/Tues./Period3_Data_Science_for_Genome_Dynamics_[DS2]/11th_Jul.14th/L2.png)
#' Chimeraを用いて可視化したL2のConsensus配列．
#' 
#' write an XStringSet object to a file
writeXStringSet(unmasked(myAlignment_L2), file = "myaln_Assignment_L2.fasta")
#' read the FASTA-format alignment into R
myaln_L2 <- read.alignment(file = "myaln_Assignment_L2.fasta", format = "fasta")

#+ warning = FALSE
#+ message = FALSE
#+ include = TRUE
#+ echo = FALSE
#' calculate the genetic distances between the protein sequences
mydist_L2 <- dist.alignment(myaln_L2)
mydist_L2
#' get sequence annotations
unlist(getAnnot(seqs_L2))
#' **Bacillus subtilis(P42919) and Geobacillus stearothermophilus(P04257) are the most closely related proteins, based on the genetic distances.**
#' 
#' Q2. Build an unrooted phylogenetic tree of the proteins, using the neighbour-joining algorithm. Which are the most closely related proteins, based on the tree?
# construct a phylogenetic tree with the neighbor joining algorithm
mytree_L2 <- nj(mydist_L2)
plot.phylo(mytree_L2, type="unrooted")
#' **Bacillus subtilis(P42919) and Geobacillus stearothermophilus(P04257) are the most closely related proteins, based on the tree.**
#' 
#' Q3. Build a rooted phylogenetic tree of the proteins, using an outgroup. Which are the most closely related proteins, based on the tree? What extra information does this tree tell you, compared to the unrooted tree in Q2?
mytree_L2 <- root(mytree_L2, outgroup = "P54017", resolve.root = TRUE)
plot.phylo(mytree_L2, main = "Phylogenetic Tree")
#' **Bacillus subtilis(P42919) and Geobacillus stearothermophilus(P04257) are the most closely related proteins, based on the tree.**
#' **Thermus thermophilus(P60405) is more closely related to Bacillus subtilis(P42919) and Geobacillus stearothermophilus(P04257) rather than Escherichia coli(P60422).**
#' 
#' ## ○L5について:
#' Answer the following questions. For each question, please record your answer, and what you typed into R to get this answer.
#' 
#' Q1. Calculate the genetic distances between > 3 protein sequences of interest. Which are the most closely related proteins, based on the genetic distances?

#+ warning = FALSE
#+ message = FALSE
#+ include = FALSE
seqnames_L5 <- c("P62399", "P12877", "P41201", "P08895", "P14124", "P54040") # Make a vector containing the names of the sequences
# retrieve several sequences from UniProt
retrieve_seqs_uniprot_L5 <- function(ACCESSION) read.fasta(file=paste0("http://www.uniprot.org/uniprot/",ACCESSION,".fasta"), seqtype="AA", strip.desc=TRUE)[[1]]
seqs_L5 <- lapply(seqnames_L5,  retrieve_seqs_uniprot_L5) # Retrieve the sequences and store them in list variable "seqs"
#' write out the sequences to a FASTA file
write.fasta(seqs_L5, seqnames_L5, file="myseq_Assignment_L5.fasta")
#' Read an XStringSet object from a file
mySequences_L5 <- readAAStringSet(file = "myseq_Assignment_L5.fasta")

#+ warning = FALSE
#+ message = FALSE
#+ include = TRUE
#+ echo = FALSE
#' Multiple Sequence Alignment using ClustalW
myAlignment_L5 <- msa(mySequences_L5, "ClustalW")
print(myAlignment_L5, show="complete")

#+ warning = FALSE
#+ message = FALSE
#+ include = FALSE
#' ![L5のConsensus配列](/Users/huang/Desktop/Keio/2020_Spring/Tues./Period3_Data_Science_for_Genome_Dynamics_[DS2]/11th_Jul.14th/L5.png)
#' Chimeraを用いて可視化したL5のConsensus配列．
#' 
#' write an XStringSet object to a file
writeXStringSet(unmasked(myAlignment_L5), file = "myaln_Assignment_L5.fasta")
#' read the FASTA-format alignment into R
myaln_L5 <- read.alignment(file = "myaln_Assignment_L5.fasta", format = "fasta")

#+ warning = FALSE
#+ message = FALSE
#+ include = TRUE
#+ echo = FALSE
#' calculate the genetic distances between the protein sequences
mydist_L5 <- dist.alignment(myaln_L5)
mydist_L5
#' get sequence annotations
unlist(getAnnot(seqs_L5))
#' **Bacillus subtilis(P12877) and Geobacillus stearothermophilus(P08895) are the most closely related proteins, based on the genetic distances.**
#' 
#' Q2. Build an unrooted phylogenetic tree of the proteins, using the neighbour-joining algorithm. Which are the most closely related proteins, based on the tree?
# construct a phylogenetic tree with the neighbor joining algorithm
mytree_L5 <- nj(mydist_L5)
plot.phylo(mytree_L5, type="unrooted")
#' **Bacillus subtilis(P12877) and Geobacillus stearothermophilus(P08895) are the most closely related proteins, based on the tree.**
#' 
#' Q3. Build a rooted phylogenetic tree of the proteins, using an outgroup. Which are the most closely related proteins, based on the tree? What extra information does this tree tell you, compared to the unrooted tree in Q2?
mytree_L5 <- root(mytree_L5, outgroup = "P54040", resolve.root = TRUE)
plot.phylo(mytree_L5, main = "Phylogenetic Tree")
#' **Bacillus subtilis(P12877) and Geobacillus stearothermophilus(P08895) are the most closely related proteins, based on the tree.**
#' **Escherichia coli(P62399) is more closely related to Bacillus subtilis(P12877) and Geobacillus stearothermophilus(P08895) rather than Thermus thermophilus(P41201).**
#' 
#' # References
#' - [保坂 晴美，中島 崇，姚 閔，田中 勲，リボソームタンパク質の構造・機能・分子進化，構造生物 Vol.7 No.1(2001)](http://www.sbsp.jp/sbsp/Sb/sb71.html)

sessionInfo()
