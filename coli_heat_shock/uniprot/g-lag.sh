#!/bin/bash
# Last update: 03/07/2022
set -eu pipefail

# array=$(echo "CH" "H")
# for i in ${array} ; do
# for j in $(seq 6) ; do
# mkdir ./${i}${j}_master
# for aUP in $(cut -f 2 ${i}${j}_uniprot.txt | grep -v "REV") ; do
## mkdir ./${i}${j}_master
## curl http://link.g-language.org/$aUP > test.txt
# wget -O ./${i}${j}_master/${aUP} http://link.g-language.org/${aUP} ;
## less test.txt | grep '^# GO_*' > ./CH1/$aUP
## sleep 1
# done
# done
# done

array=$(echo "CH" "H")
for i in ${array} ; do
for j in $(seq 6) ; do
mkdir -p ./${i}${j}
for aUP in $(ls ${i}${j}_master) ; do
# echo ${i} ${j} ${array} ${aUP} >> test.txt
grep '^# GOslim_process' ./${i}${j}_master/${aUP} | cut -f 2- | sort > ./${i}${j}/${aUP}.txt ;
grep '^# GOslim_function' ./${i}${j}_master/${aUP} | cut -f 2- | sort >> ./${i}${j}/${aUP}.txt ;
done
done
done
