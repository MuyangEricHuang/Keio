#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last update: 04/29/2021

from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns; sns.set(color_codes=True, style="ticks", font_scale=3.25)
import pandas as pd
import numpy as np
import scipy.stats as sp
import scipy.cluster.hierarchy as hierarchy
# from sklearn.preprocessing import Imputer
import pickle
import pprint
from ipywidgets import interact, FloatSlider
# import fastcluster

def main():
    plot_dict = {}
    input_file1 = "TFs_Group_1_tr.txt"
    group_1 = []
    with open(input_file1, "r") as file_handle1:
        for a_group_1_gene in file_handle1:
            a_group_1_gene = a_group_1_gene.rstrip()
            group_1.append(a_group_1_gene)
    
    input_file2 = "TFs_Group_2_tr.txt"
    group_2 = []
    with open(input_file2, "r") as file_handle2:
        for a_group_2_gene in file_handle2:
            a_group_2_gene = a_group_2_gene.rstrip()
            group_2.append(a_group_2_gene)
    
    input_file3 = "TFs_Group_3_tr.txt"
    group_3 = []
    with open(input_file3, "r") as file_handle3:
        for a_group_3_gene in file_handle3:
            a_group_3_gene = a_group_3_gene.rstrip()
            group_3.append(a_group_3_gene)
    
    input_file4 = "TFs_Group_4_tr.txt"
    group_4 = []
    with open(input_file4, "r") as file_handle4:
        for a_group_4_gene in file_handle4:
            a_group_4_gene = a_group_4_gene.rstrip()
            group_4.append(a_group_4_gene)
    
    input_file5 = "TFs_Group_5_tr.txt"
    group_5 = []
    with open(input_file5, "r") as file_handle5:
        for a_group_5_gene in file_handle5:
            a_group_5_gene = a_group_5_gene.rstrip()
            group_5.append(a_group_5_gene)

    input_file6 = "transcriptome_expression_-f2changed.txt"
    RNA_ids = defaultdict()
    RNA_values = {}
    RNA_garbages = {}

    with open(input_file6, "r") as file_handle6:
        for row_num2, row2 in enumerate(file_handle6):
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
                    for index, oneData in enumerate(col2[2:13]):
                        if not oneData == "0.00":
                            break
                        if index == 10:
                            changing_flag = True
                if changing_flag:
                    for j in range(2, 13):
                        garbages.append(float(col2[j]))
                    RNA_garbages.update({tra_uniprot_ac: garbages})
                    continue

                RNA_value = []
                RNA_not_missing_value = []
                values_zscore = []
                for index, one in enumerate(col2[2:]):
                    if one != "0.00":
                        RNA_not_missing_value.append(float(one))
                        RNA_value.append(float(one))
                    else:
                        RNA_value.append(float(one))
                if RNA_not_missing_value:
                    if len(RNA_not_missing_value) == 1:
                        for one in col2[2:]: 
                            if one != "0.00":
                                values_zscore.append(0)
                            else:
                                values_zscore.append(-2)
                    else:
                        zscore_not_missing_values = sp.stats.zscore(RNA_value)
                        for one in range(11):
                            values_zscore.append(zscore_not_missing_values[one])

                    RNA_values.update({tra_uniprot_ac: values_zscore})
    
    # # #
    for a_TRG in group_5:
        plot_dict.update({a_TRG: RNA_values["{}".format(a_TRG)]})

    # make DataFrame
    df = pd.DataFrame.from_dict(plot_dict)
    df.index = ["TP{}".format(i+1) for i in range(11)]
    df.T.to_csv("H(11)_TFs_group_5_df.txt", sep="\t")

    # seaborn clustermap
    # mask = df_with_npnan.T.isnull() # define missing value position
    # cmap = sns.diverging_palette(240, 10, s=90, l=50, n=5, center="light", as_cmap=True) # color map https://qiita.com/SaitoTsutomu/items/c79c9973a92e1e2c77a7
    # g1 = sns.clustermap(df.T, method="ward", metric="euclidean", figsize=(61.805, 100), col_cluster=False, cmap='coolwarm', mask=mask) # 以前まではfigsize=(80, 270)．
    g1 = sns.clustermap(df.T, method="ward", metric="euclidean", figsize=(22.25, 36), col_cluster=False, cmap='bwr', vmin=-2, vmax=2, cbar_kws={"ticks":[-2,-1,0,1,2]})
    # we want to change color bar location, however it is difficult (https://github.com/mwaskom/seaborn/issues/589)
    plt.setp(g1.ax_heatmap, facecolor="black")
    plt.setp(g1.ax_heatmap.yaxis.get_majorticklines(), color="white", linewidth=0.001)
    plt.title("            HCA of Transcription Related Genes' mRNA in Group 5 of Heat Shock Samples TP1~11", loc='left')
    # plt.setp(g1.ax_heatmap.yaxis.get_majorticklabels(), rotation=0) # rotate protein-id-label # 三浦さんの方だと，これがないとラベルは縦に表示される．

    # save fig and pickle
    output_fig = "H(11)_TFs_group_5_clustermap.pdf"
    output_pickle = "H(11)_TFs_group_5_clustermap.pickle"
    g1.savefig(output_fig)
    with open(output_pickle, "wb") as file_handle:
        pickle.dump(g1, file_handle)

if __name__=="__main__":
    main()
