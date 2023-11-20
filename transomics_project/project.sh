#!/usr/bin/bash
# Last update: 01/17/2019
set -euo pipefail

cd ..
mkdir Transomics
cd Transomics
# wget ~
wget ftp://ftp.ebi.ac.uk/pub/databases/IPI/last_release/current/ipi.RAT.xrefs.gz
wget ftp://ftp.ebi.ac.uk/pub/databases/IPI/last_release/current/ipi.RAT.fasta.gz
gzip -d ipi.RAT.xrefs.gz
gzip -d ipi.RAT.fasta.gz

tr \\r \\n < metabolome_mac.txt > metabolome.txt
tr \\r \\n < phosphoproteome_mac.txt > phosphoproteome.txt
tr \\r \\n < rpk_mac.txt > rpk.txt
tr \\r \\n < posterior_mac.txt > posterior.txt

grep CoA metabolome.txt > metabolome_CoA.txt
awk -F"\t" '($80 != "N.D.") && ($80 != "") {print}' metabolome.txt |tail -n +2 > measured_metabolite.txt
awk -F"\t" '($4 != "-"){print}' measured_metabolite.txt > mappable_metabolite.txt
awk -F"\t" '($80 > 1){print}' mappable_metabolite.txt | cut -f 4 |awk -F"\t" '{ print $1 "\t" "red" }' > metabolite_mapping.txt
awk -F"\t" '($80 < -1){print}' mappable_metabolite.txt | cut -f 4 | grep "C" | awk -F"\t" '{ print $1 "\t" "blue" }' >> metabolite_mapping.txt
awk -F"\t" '($80 > -1) && ($80 < 1) {print}' mappable_metabolite.txt | cut -f 4 | grep "C" | awk -F"\t" '{ print $1 "\t" "green" }' >> metabolite_mapping.txt

open metabolite_mapping.txt

# KEGG Mapper (http://www.genome.jp/kegg/tool/map_pathway2.html) を開き、以下の手順で代謝経路図を表示
# 1. metabolite_mapping.txt の内容を KEGG Mapper の入力フォームにコピー&ペースト
# 2. KEGG Mapper にて、Search against 欄に Rattus novegicus を意味する 'rno' を入力 (∵ Fao 細胞はラット肝がん由来)
# 3. Use uncolored diagram をチェックして Exec ボタンを押す
# 4. 'rno01100 Metabolic pathways - Rattus norvegicus (rat)' をクリックする

curl http://rest.kegg.jp/get/cpd:C00158 | awk '$1 ~ /^ENZYME/','$1 ~ /^[A-Z]/ && $1 !~ /^ENZYME/' | sed '$d' > C00158.txt
for aCPD in $(grep "red\|blue" metabolite_mapping.txt | cut -f1) ; do for anEC in $(curl http://rest.kegg.jp/get/cpd:${aCPD} | awk '$1 ~ /^ENZYME/','$1~/^[A-Z]/ && $1!~/^ENZYME/' | sed '$d') ; do echo "ec:$anEC" ; done ; done | sort | uniq | grep -v ENZYME > rme.txt
for anEC in $(cat rme.txt) ; do echo -e $anEC"\tblack" ; done > rme_mapping.txt

cut -f 1 phosphoproteome_ec.txt | tail -n +3 | ggrep -wf rme.txt | sort | uniq > phospho_rme_ec.txt
for anEC in $(cat phospho_rme_ec.txt ); do echo -e "$anEC\tblack"; done

# http://netphorest.info/
open -a TextEdit phospho_rme_sample.fasta
# 配列相同度が最も高いタンパク質を選択し、[Next]を押す
# "Loadsitesfromfile" にて、ipi.resnum_sample.txt を選択する(ipi.resnum_sample.txtは、 タンパク質の ID と当該タンパク質において実際にリン酸化が確認された残基の位置が記述されている)。最後に[Start prediction]ボタンをクリックする
# 今回はキナーゼによるリン酸化のみ使うので、8つあるチェックボックス “KIN”, “SH2”, “PTP”, “PTB”, “14-3-3”, “BRCT”, “WW” ,”WD40” のうち ”KIN” のみチェックする。
# [Save] → Full dataset を選択し、キナーゼの予測結果を networkin_predictions_sample.tsv に保存する。

# sh get_phospho_rme_fasta.sh

for anEC in $( cut -f 1 phosphoproteome.txt | tail -n +3 | grep "ec") ; do echo -e $anEC"\tblack" ; done > ipi.phosphoproteome1.txt
# awk -F"\t" '{print $1"\tblack" }' phosphoproteome.txt | tail -n +3 | grep "ec" > ipi.phosphoproteome2.txt

# sh get_residue_number.sh

open -e phospho_rme.fasta | open  ipi.resnum.txt
open -en phospho_rme.fasta ipi.resnum.txt 
open -n -a TextEdit phospho_rme.fasta ipi.resnum.txt
# リン酸化された責任代謝酵素の FASTA 形式ファイル phospho_rme.fasta およびリン酸化部位ファイル ipi.resnum.txt を NetPhorest に入力し、キナーゼの予測結果を networkin_predictions.tsv に保存

awk -F"\t" '{ print $1"\t"$2"\t"$6"\t"$7 }' networkin_predictions.tsv > ipi.kinase.txt

grep "PKA_group\|PKB_group\|PKC_group\|p70S6K_group\|GSK3_group" ipi.kinase.txt > ipi.insulin_kinase.txt
grep -wf <(cut -f1 ipi.insulin_kinase.txt | sort | uniq) phosphoproteome.txt > phosphoproteome_insulin_kinase.txt
# ggrep -wf <(cut -f1 ipi.insulin_kinase.txt) phosphoproteome.txt > phosphoproteome_insulin_kinase.txt
# ggrep -wf <(cut -f1 ipi.insulin_kinase.txt | sort | uniq) phosphoproteome.txt > phosphoproteome_insulin_kinase.txt

curl http://rest.kegg.jp/link/ec/map00010 > glycolysis_ec.txt && curl http://rest.kegg.jp/link/ec/map00020 > tca_ec.txt && curl http://rest.kegg.jp/link/ec/map00030 > ppp_ec.txt
cat glycolysis_ec.txt tca_ec.txt ppp_ec.txt | cut -f 2 | sort | uniq > ccm_ec.txt
ggrep -wf <(cat ccm_ec.txt) phosphoproteome_insulin_kinase.txt > phosphoproteome_insulin_ccm.txt
# ggrep -wf ccm_ec.txt phosphoproteome_insulin_kinase.txt > phosphoproteome_insulin_ccm.txt
ggrep -wf <(cut -f 2 phosphoproteome_insulin_ccm.txt) ipi.insulin_kinase.txt > ipi.insulin_kinase.ccm.txt

# wget ~
mkdir -p ~/Library/Java/Extensions
cd ~/Library/Java/Extensions
wget https://jogamp.org/deployment/java3d/1.6.0-pre12/jogamp-java3d.7z --no-check-certificate
wget https://jogamp.org/deployment/jogamp-current/archive/jogamp-fat-all.7z --no-check-certificate
7z x jogamp-java3d.7z
7z x jogamp-fat-all.7z
mv jogamp-fat/jogamp-fat.jar .

# HIVE with VANTED をデスクトップにダウンロードし、起動
# https://immersive-analytics.infotech.monash.edu/hive/
# “File” “Open” より、central_carbon_metabolism.gml と insulin_signaling.gml をそれぞれ開き
# “File” “New” より、新しいファイルを開き、insulin_trans_omic.gml という名前で保存
# central_carbon_metabolism.gml 所収の全ネットワークを新しいファイルにコピー (central_carbon_metabolism.gml のウィンドウにて ”Edit” ”Select All”, “Copy”、 新しいファイルのウィンドウにて”Edit” ”Paste”)
# insulin_trans_omic.gml の全ネットワークを選択し、“Cluster” ”Enter Cluster ID” ”Enter and set cluster ID” を選択し、Cluster ID に ’metabolism’ と入力
# insulin_signaling.gml の全ネットワークを insulin_trans_omic.gml にコピー。central_carbon_metabolism.gml のネットワークの隣に置く
# insulin_trans_omic.gml にて、インスリンシグナル伝達ネットワークを選択し、Cluster ID に ’signaling’ と入力
# insulin_trans_omic.gml を保存
# 同定した責任キナーゼと代謝酵素の間のネットワークに基づき、 insulin_trans_omic.gml の中の対応するノード同士をエッジで結ぶ
# 2D 表示ウィンドウにて、“Edit” ”Selection” ”Select Cluster” で metabolism または signaling を選ぶと、代謝層またはシグナル層を選択できる。一方の層を選択し、両者が上下にくるように位置を調整。2D 表示ウィンドウで位置を調整してファイルを保存すると、3D 表示ウィンドウに反映される
