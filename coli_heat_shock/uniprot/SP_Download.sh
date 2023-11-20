#!/bin/bash
# Last update: 03/07/2022
set -eu pipefail

mkdir SP
cd SP

while read line
do
    wget https://www.uniprot.org/uniprot/${line}.txt
# done <  ../SP.txt
# done < ../4401_nai_SPID.txt
done < ../mainUP_left_duplicate_right_cutf1.txt

# while read line
# do
#     echo ${line}
# done < cut -f 1 ../mainUP_left_duplicate_right.txt

cd ..

