#!/usr/bin/bash
# Last update: 11/13/2018
set -euo pipefail

tail -n+3 phosphoproteome.txt | ggrep -wf rme.txt > phosphoproteome_rme.txt

cut -f2 phosphoproteome_rme.txt | sort | uniq > phospho_rme.ipi.txt

awk '{if ($1 ~ /^>/){ ipi=substr($1,6,11); printf "\n"ipi"\t";} else printf $1}' ipi.RAT.fasta | tail -n +2 > ipi.fasta.xrefs
# 1列目の行頭が>で始まる場合、変数名ipiに一個目の第6文字目から第11文字目の文字列という特定の文字を渡すし、「改行」ipi「Tab」というようにprintする。
# 1列目の行頭が>で始まらない場合、一個目をそのままプリントする（fasta）。

ggrep -wf phospho_rme.ipi.txt ipi.fasta.xrefs > ipi.fasta.phospho_rme.xrefs

awk -F"\t" '{ print ">"$1 ; print $2 }' ipi.fasta.phospho_rme.xrefs > phospho_rme.fasta
