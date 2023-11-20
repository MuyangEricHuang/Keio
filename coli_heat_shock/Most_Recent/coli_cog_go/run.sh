#!/usr/bin/bash

mkdir -p data/raw data/tmp scripts log tmp
mkdir data/raw/uniprot
mkdir scripts/disposable

time nohup bash -c 'for uniprot_id in $(less data/tmp/proteome_expression.txt | cut -f1); do wget -O data/raw/uniprot/${uniprot_id}.txt https://www.uniprot.org/uniprot/${uniprot_id}.txt; done' &
time nohup bash -c 'for uniprot_id in $(less data/tmp/proteome_expression.txt | cut -f1); do wget -O data/raw/uniprot/${uniprot_id}.fasta https://www.uniprot.org/uniprot/${uniprot_id}.fasta; done' &
python scripts/check_uniprot_donwload.py 
python scripts/make_fasta_from_db.py
for upid in $(less data/tmp/proteome_expression.txt | cut -f1); do less data/raw/uniprot/${upid}.fasta >> data/tmp/uniprot.faa; done

mkdir data/tmp/db data/tmp/blast
makeblastdb -hash_index -in data/tmp/gtf.fna -dbtype nucl -out data/tmp/db/gtf >> data/tmp/db/log_makeblastdb.txt
makeblastdb -hash_index -in data/tmp/pec_essential.faa -dbtype prot -out data/tmp/db/pec_essential >> data/tmp/db/log_makeblastdb.txt
makeblastdb -hash_index -in data/tmp/regulondb.fna -dbtype nucl -out data/tmp/db/regulondb >> data/tmp/db/log_makeblastdb.txt
makeblastdb -hash_index -in data/tmp/uniprot.faa -dbtype prot -out data/tmp/db/uniprot >> data/tmp/db/log_makeblastdb.txt
makeblastdb -hash_index -in data/tmp/uniprot4000over.faa -dbtype prot -out data/tmp/db/uniprot4000over >> data/tmp/db/log_makeblastdb.txt

qsub scripts/do_blast.pbs

mkdir data/tmp/blast
qsub scripts/do_blast.pbs

python scripts/pair_sequences_from_db.py > data/tmp/gtf_query_uniprot_conversion.txt 



mkdir data/raw/uniprot4000over
time nohup bash -c 'for upid in $(less data/tmp/uniprot4000over.faa | grep ">" | cut -d"|" -f2); do wget -O data/raw/uniprot4000over/${upid}.txt https://www.uniprot.org/uniprot/${upid}.txt; done' &

# get GO and COG annotation
wget -O data/raw/go-basic.obo http://geneontology.org/ontology/go-basic.obo
wget -O data/raw/cog20.def.tab https://ftp.ncbi.nih.gov/pub/COG/COG2020/data/cog-20.def.tab
cat data/raw/cog20.def.tab | LANG=C grep -n -v '^[[:cntrl:][:print:]]*$'
cp data/raw/cog20.def.tab data/tmp/edited_cog20.def.tab
vim data/tmp/edited_cog20.def.tab # remove multibyte characters

python scripts/annotate_cog_go_to_ecoli_uniprot.py
less data/tmp/uniprot4000over_with_gocog.txt | grep -e "GO:0009451" -e "GO:0006400" -e "GO:0000154" | grep -v alaS | grep -v alkB | grep -v cmoA | grep -v rimO | grep -v thiI | grep -v yfjP | grep -v ykfA | less > data/tmp/trna_rrna_modification_enzyme.txt


# PECAplus
cd scripts
git clone https://github.com/PECAplus/PECAplus_cmd_line.git
make -j 8
cd ../

mkdir data/tmp/peca
python scripts/prepare_peca.py
cd data/tmp/peca/
./scripts/PECAplus_cmd_line/peca_core/peca_core_bin data/tmp/peca/input_params.txt
python scripts/PECAplus_cmd_line/peca_core/peca_core.py 
for one in $(less data/tmp/peca/output_file_names.txt); do mv ${one} data/tmp/peca/ ;done
