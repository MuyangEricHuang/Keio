#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last update: 09/02/2021

from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import DivergingNorm
import pandas as pd
import seaborn as sns; sns.set(color_codes=True, style="ticks", font_scale=.25)
import scipy.stats as sp
import json

def main():
    input_file1 = "proteome_expression_median.txt"
    protein_ids = defaultdict()
    protein_values = {}
    protein_values_with_npnan = {}
    uniprot_ac = []
    with open(input_file1, "r") as file_handle1:
        for row_num1, row1 in enumerate(file_handle1):
            row1 = row1.rstrip()
            col1 = row1.split("\t")
            if row_num1 == 0:
                continue
            else:
                pro_uniprot_ac = col1[3].split("#")[1]
                if "---" in row1:
                    missing_flag = False
                    for i in range(14, 21):
                        if not col1[i] == "---":
                            break
                        if i == 20:
                            missing_flag = True
                    if missing_flag:
                        continue

                uniprot_ac.append([col1[0], col1[1], col1[2], col1[3], col1[4], col1[5], col1[6]])
                protein_ids[pro_uniprot_ac] = [col1[0], col1[1], col1[2], col1[3], col1[4], col1[5], col1[6]]

                protein_not_missing_value = []
                mask_position = []
                values_zscore = []
                not_missing_values_number = 0
                # for index, one in enumerate(col1[14:]):
                for index, one in enumerate(col1[14:21]):
                    if one != "---":
                        protein_not_missing_value.append(float(one))
                    else:
                        mask_position.append(index)
                if protein_not_missing_value:
                    if len(protein_not_missing_value) == 1:
                        # for one in col1[14:]:
                        for one in col1[14:21]: 
                            if one != "---":
                                values_zscore.append(0)
                                # not_missing_values_number += 1
                            else:
                                values_zscore.append(-2)
                    else:
                        zscore_not_missing_values = sp.stats.zscore(protein_not_missing_value)
                        # for one in col1[14:]:
                        for one in col1[14:21]:
                            if one != "---":
                                values_zscore.append(zscore_not_missing_values[not_missing_values_number])
                                not_missing_values_number += 1
                            else:
                                values_zscore.append(-2)

                    values_with_npnan = []
                    for index, one in enumerate(values_zscore):
                        if index in mask_position:
                            values_with_npnan.append(np.nan)
                        else:
                            values_with_npnan.append(values_zscore[index])

                    protein_values.update({pro_uniprot_ac: values_zscore})
                    protein_values_with_npnan.update({pro_uniprot_ac: values_with_npnan})


    input_file2 = "transcriptome_expression_-f2changed.txt"
    RNA_ids = defaultdict()
    RNA_values = {}
    RNA_garbages = {}
    with open(input_file2, "r") as file_handle2:
        for row_num2, row2 in enumerate(file_handle2):
            row2 = row2.rstrip()
            col2 = row2.split("\t")
            if row_num2 == 0:
                continue
            else:
                garbages = []
                tra_uniprot_ac = col2[0].split("_")[-1].split("-")[0]
                RNA_ids[tra_uniprot_ac] = [col2[0], col2[1]]
                changing_flag = False
                if "0.00" in row2:
                    for index, oneData in enumerate(col2[2:9]):
                        if not oneData == "0.00":
                            break
                        if index == 6:
                            changing_flag = True
                if changing_flag:
                    for j in range(2, 9):
                        garbages.append(float(col2[j]))
                    RNA_garbages.update({tra_uniprot_ac: garbages})
                    continue

                RNA_value = []
                RNA_not_missing_value = []
                values_zscore = []
                for index, one in enumerate(col2[2:9]):
                    if one != "0.00":
                        RNA_not_missing_value.append(float(one))
                        RNA_value.append(float(one))
                    else:
                        RNA_value.append(float(one))
                if RNA_not_missing_value:
                    if len(RNA_not_missing_value) == 1:
                        for one in col2[2:13]:
                            if one != "0.00":
                                values_zscore.append(0)
                            else:
                                values_zscore.append(-2)
                    else:
                        values_zscore = sp.stats.zscore(RNA_value)
                    RNA_values.update({tra_uniprot_ac: values_zscore})


    input_file3 = "511145_v2020_sRDB18-13_dsRNA_regNetwork.json"
    file_list = ["rpoD_cluster_1_tr", "rpoD_cluster_2_tr", "rpoD_cluster_3_tr", "rpoH_cluster_1_tr", "rpoH_cluster_2_tr", "rpoE_cluster_1_tr", "rpoE_cluster_2_tr", "rpoE_cluster_3_tr", "rpoE_cluster_4_tr", "rpoS_cluster_1_tr", "rpoS_cluster_2_tr", "rpoN_cluster_1_tr", "rpoN_cluster_2_tr"]
    # Upstream_Table = []
    for afile_list in file_list:
        input_file2 = "../{}.txt".format(afile_list)
        upstream_expression= {}
        group_genes = []
        with open(input_file2, "r") as file_handle2:
            for a_group_num_gene in file_handle2:
                a_group_num_gene = a_group_num_gene.rstrip()
                group_genes.append(a_group_num_gene)
        # JSONファイルからテキストストリームを生成．
        with open(input_file3, mode='rt', encoding='utf-8') as file:
            # 辞書オブジェクト(dictionary)を取得．
            data = json.load(file)
            for a_group_gene in group_genes:
            # upstream_tabel = [False, False, False]
                source = []
                for adata in data["elements"]["edges"]:
                    if a_group_gene in adata["data"]["target"]:
                        source.append(adata["data"]["source"])
                        if adata["data"]["source"] in protein_values.keys() and adata["data"]["source"] not in upstream_expression.keys():
                            upstream_expression.update({adata["data"]["source"]: protein_values[adata["data"]["source"]]})

                with open("{}_upstream_genes.txt".format(afile_list), "a") as f:
                    print(a_group_gene + "\t" + str(len(source)) + "\t" + str(source), file=f)

        h2 = plt.figure(figsize=[36, 36])
        df = pd.DataFrame.from_dict(upstream_expression)
        df.index = ["H{}".format(i+1) for i in range(7)]
        # df.T.to_csv("H(7)_transcriptome_df.txt", sep="\t")
        my_cmap = sns.diverging_palette(h_neg=268, h_pos=54, s=100, l=54, as_cmap=True)
        divnorm = DivergingNorm(vmin=-2, vcenter=0, vmax=2)
        h2 = sns.clustermap(df.T, method="ward", metric="euclidean", col_cluster=False, cmap="bwr", norm=divnorm, cbar_kws={"ticks":[-2,-1,+0,+1,+2]})
        plt.setp(h2.ax_heatmap.xaxis.get_majorticklabels(), rotation=90)
        # plt.setp(h2.ax_heatmap, facecolor="black")
        plt.setp(h2.ax_heatmap.yaxis.get_majorticklines(), color="white", linewidth=0.001)
        plt.title("{} upstream of {} {} {}".format(len(upstream_expression), afile_list.split("_")[0], afile_list.split("_")[1], afile_list.split("_")[2]), loc='left')
        output_fig = "{}_other_upstream.pdf".format(afile_list)
        # output_pickle = "H(7)_other_upstream_clustermap.pickle"
        h2.savefig(output_fig)
        # with open(output_pickle, "wb") as file_handle:
        #     pickle.dump(h2, file_handle)

if __name__=="__main__":
    main()
