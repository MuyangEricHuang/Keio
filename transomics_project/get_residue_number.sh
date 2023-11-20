#!/usr/bin/bash
# Last update: 11/14/2018
set -euo pipefail

cut -f2,8 phosphoproteome_rme.txt > ipi.raw_resnum.txt

awk -F"\t" '{ if($2 ~ /^\"/){ n=split($2, aRes, ", ") ; for(i=1;i<=n;i++){ print $1"\t"aRes[i] } } else { print } }' ipi.raw_resnum.txt > ipi.raw_resnum_tmp.txt

tr -d \" < ipi.raw_resnum_tmp.txt | sort | uniq > ipi.resnum.txt
# sed -e s/\"//g | sort | uniq > ipi.resnum.txt
