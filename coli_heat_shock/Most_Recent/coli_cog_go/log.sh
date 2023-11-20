#!/usr/bin/bash

#GOATOOLS: https://www.nature.com/articles/s41598-018-28948-z

# prepare ecoli uniprot data
wget -O data/raw/ecoli_from_uniprot.txd https://www.uniprot.org/docs/ecoli.txt
less data/raw/ecoli_from_uniprot.txd | tail -n +48 | head -n 4407 | cut -c36- | sed -E -e $'s/\; /\;/g' -e $'s/\s+/\t/g' | awk -F"\t" '{print $2"\t"$1"\t"$3"\t"$4}' | less > data/tmp/ecoli_from_uniprot_reviesd.txt
mkdir data/raw/uniprot
time nohup bash -c 'for uniprot_id in $(less data/tmp/ecoli_from_uniprot_reviesd.txt | cut -f1 | less); do wget -O data/raw/uniprot/${uniprot_id}.txt https://www.uniprot.org/uniprot/${uniprot_id}.txt; done' &
#real    57m21.035s

# get GO annotation
wget -O data/raw/go-basic.obo http://geneontology.org/ontology/go-basic.obo
#time python scripts/annotate_go_to_ecoli_uniprot.py & 
#real    0m32.175s

# extract gene related our study (not good)
less ../data/ecoli_heat_proteome.txt | tail -n+47 | cut -f2-4,7,12-25 | cut -f1 | tail -n+2 | grep -v REV > data/tmp/our_proteome_uniprot_ids.txt
#python scripts/extract_gene_with_specific_go.py

# get COG annotation
wget -O data/raw/genomes2003-2014.tab ftp://ftp.ncbi.nih.gov/pub/COG/COG2014/data/genomes2003-2014.tab
wget -O data/raw/cog2003-2014.csv ftp://ftp.ncbi.nih.gov/pub/COG/COG2014/data/cog2003-2014.csv
wget -O data/raw/cognames2003-2014.tab ftp://ftp.ncbi.nih.gov/pub/COG/COG2014/data/cognames2003-2014.tab

# edit COG file
cat data/raw/cognames2003-2014.tab | LANG=C grep -n -v '^[[:cntrl:][:print:]]*$'
cp data/raw/cognames2003-2014.tab data/tmp/edited_cognames2003-2014.tab
vim data/tmp/edited_cognames2003-2014.tab 

python scripts/annotate_cog_go_to_ecoli_uniprot.py
for id in $(less data/tmp/our_proteome_uniprot_ids.txt); do grep ${id} data/tmp/ecoli_from_uniprot_reviesd_with_gocog.txt >> data/tmp/our_proteome_with_gocog.txt; done
python scripts/pair_uniprot_bnumber.py 
