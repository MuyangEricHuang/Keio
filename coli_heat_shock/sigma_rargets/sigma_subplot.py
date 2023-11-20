#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last update: 09/02/2021

from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
# import matplotlib.cm as cm
from matplotlib.colors import DivergingNorm
import pandas as pd
# import seaborn as sns; sns.set(color_codes=True, style="ticks", font_scale=1.3)
# import seaborn as sns; sns.set(color_codes=True, style="ticks", font_scale=3)
# import seaborn as sns; sns.set(color_codes=True, style="ticks", font_scale=.8)
import seaborn as sns; sns.set(color_codes=True, style="ticks", font_scale=1)
# import math
# import scipy.stats as stats
import scipy.stats as sp
# from sklearn.preprocessing import Imputer
# from sklearn import preprocessing
# import pickle
# import pprint
# from ipywidgets import interact, FloatSlider
import json

def main():
    input_file1 = "transcript_sort_uniq.txt"
    tf_data = []
    tf_data = ["rpoD", "rpoH", "rpoE", "rpoS", "rpoN"]
    histogram = []
    Thesis_Table = []
    TFs_proteins = {}
    TFs_proteins_with_npnan = {}
    TFs_mRNAs = {}
    with open(input_file1, "r") as file_handle1:
        for oneLine in file_handle1:
            oneLine = oneLine.rstrip()
            onetf = oneLine.split("\t")
            tf_data.append(onetf[0])

    extra_data = []
    input_extrafile = "TRGs.txt"
    with open(input_extrafile, "r") as extrafile_handle:
        for extraLine in extrafile_handle:
            extraLine = extraLine.rstrip()
            oneextra = extraLine.split("\t")
            extra_data.append(oneextra[0])

    input_file2 = "proteome_expression_median.txt"
    protein_ids = defaultdict()
    protein_values = {}
    protein_values_with_npnan = {}
    uniprot_ac = []

    with open(input_file2, "r") as file_handle2:
        for row_num1, row1 in enumerate(file_handle2):
            row1 = row1.rstrip()
            col1 = row1.split("\t")
            if row_num1 == 0:
                continue
            else:
                pro_uniprot_ac = col1[3].split("#")[1]
                if "---" in row1:
                    missing_flag = False
                    # for i in range(14, 25):
                    for i in range(14, 21):
                        if not col1[i] == "---":
                            break
                        # if i == 24:
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
                                not_missing_values_number += 1
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

    

    input_file3 = "transcriptome_expression_-f2changed.txt"
    RNA_ids = defaultdict()
    RNA_values = {}
    RNA_garbages = {}

    with open(input_file3, "r") as file_handle3:
        for row_num2, row2 in enumerate(file_handle3):
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
                    # for index, oneData in enumerate(col2[2:13]):
                    for index, oneData in enumerate(col2[2:9]):
                        if not oneData == "0.00":
                            break
                        # if index == 10:
                        if index == 6:
                            changing_flag = True
                if changing_flag:
                    # for j in range(2, 13):
                    for j in range(2, 9):
                        garbages.append(float(col2[j]))
                    RNA_garbages.update({tra_uniprot_ac: garbages})
                    continue

                RNA_value = []
                RNA_not_missing_value = []
                values_zscore = []
                # for index, one in enumerate(col2[2:]):
                for index, one in enumerate(col2[2:9]):
                    if one != "0.00":
                        RNA_not_missing_value.append(float(one))
                        RNA_value.append(float(one))
                    else:
                        RNA_value.append(float(one))
                if RNA_not_missing_value:
                    if len(RNA_not_missing_value) == 1:
                        # for one in col2[2:]:
                        for one in col2[2:9]:
                            if one != "0.00":
                                values_zscore.append(0)
                            else:
                                values_zscore.append(-2)
                    else:
                        values_zscore = sp.stats.zscore(RNA_value)
                        # zscore_not_missing_values = sp.stats.zscore(RNA_value)
                        # # for one in range(11):
                        # for one in range(7):
                        #     values_zscore.append(zscore_not_missing_values[one])
                    RNA_values.update({tra_uniprot_ac: values_zscore})



    input_file4 = "511145_v2020_sRDB18-13_dsRNA_regNetwork.json"
    # JSONファイルからテキストストリームを生成．
    with open(input_file4, mode='rt', encoding='utf-8') as file:
        notmatch = []
        no_protein = []
        no_RNA = []
        # left = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
        left = np.array([1, 2, 3, 4, 5, 6, 7])
        none = np.array([0, 0, 0, 0, 0, 0, 0])
        # 辞書オブジェクト(dictionary)を取得．
        data = json.load(file)
        for atf in tf_data:
            thesis_table = [atf, False, False, False, False]
            # h = plt.figure(figsize=[8, 8])
            target = []
            # JSONデータから必要な箇所を出力．
            for adata in data["elements"]["edges"]:
                if atf in adata["data"]["source"]:
                   target.append(adata["data"]["target"])
                else:
                    continue
            if len(target) == 0:
                notmatch.append(atf)
                thesis_table[3] = 0
            else:
                thesis_table[3] = len(target)
            
            

            # 下部．
            cluster_values = {}
            # plt.subplot(2, 1, 2)
            target_RNA_num = 0
            for ii in target:
                if ii in RNA_values.keys():
                    target_RNA_num += 1
                    target_RNA = RNA_values["{}".format(ii)]
                    # plt.plot(left, target_RNA, c='blue', marker='s', linestyle="solid")

                    cluster_values.update({ii: RNA_values["{}".format(ii)]})

            if target_RNA_num != 0:
                thesis_table[4] = target_RNA_num
            else:
                # plt.plot(left, none, linewidth=1, c='black', marker=False, linestyle="dashed")
                thesis_table[4] = 0



            # plt.grid(False)
            # plt.gca().spines['right'].set_visible(False)
            # plt.gca().spines['top'].set_visible(False)
            # plt.xlabel("Time Points")
            # plt.ylabel("Target RNA")
            histogram.append([atf, len(target), target_RNA_num])

            # 上部．
            # plt.subplot(2, 1, 1)
            if atf in protein_values.keys():
                protein = protein_values["{}".format(atf)]
                # p1 = plt.plot(left, protein, c='red', marker='o', linestyle="solid")
                thesis_table[2] = "Measured"
            else:
                no_protein.append(atf)
                thesis_table[2] = "-"
            if atf in RNA_values.keys():
                RNA = RNA_values["{}".format(atf)]
                # p2 = plt.plot(left, RNA, c='blue', marker='s', linestyle="solid")
                thesis_table[1] = "Measured"
            else:
                no_RNA.append(atf)
                thesis_table[1] = "-"
            
            Thesis_Table.append("\t".join(map(str, thesis_table)))
            
            # plt.grid(False)
            # plt.gca().spines['right'].set_visible(False)
            # plt.gca().spines['top'].set_visible(False)
            # plt.xlabel("Time Points")
            # plt.ylabel("Transcription Related Gene")
            # plt.legend((p1[0], p2[0]), ("Protein", "RNA"))
            # plt.title("{} ({}/{}; Observed/DB)".format(atf, target_RNA_num, len(target)), loc='left')
            # judge = ["H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H10", "H11"]
            judge = ["H1", "H2", "H3", "H4", "H5", "H6", "H7"]

            # h.savefig("{}.pdf".format(atf))
            # h = plt.show()

            if target_RNA_num > 1:
                if atf in protein_values.keys():
                    if atf in RNA_values.keys():
                        # TFs_proteins.append(protein_values["{}".format(atf)])
                        TFs_proteins.update({atf: protein_values["{}".format(atf)]})
                        TFs_proteins_with_npnan.update({atf: protein_values_with_npnan["{}".format(atf)]})

                h2 = plt.figure(figsize=[36, 36])
                df = pd.DataFrame.from_dict(cluster_values)
                # df.index = ["TP{}".format(i+1) for i in range(11)]
                df.index = ["H{}".format(i+1) for i in range(7)]
                # df.T.to_csv("H(7)_transcriptome_df.txt", sep="\t")
                # my_cmap = sns.diverging_palette(240, 10, s=90, l=50, n=5, center="light", as_cmap=True) # color map https://qiita.com/SaitoTsutomu/items/c79c9973a92e1e2c77a7
                my_cmap = sns.diverging_palette(h_neg=268, h_pos=54, s=100, l=54, as_cmap=True)
                # my_cmap = sns.diverging_palette(h_neg=268, h_pos=54, s=81, l=68, center="dark", as_cmap=True)
                divnorm = DivergingNorm(vmin=-2, vcenter=0, vmax=2)
                # h2 = sns.clustermap(df.T, method="ward", metric="euclidean", figsize=(36, 36), col_cluster=False, cmap='PuOr_r', norm=divnorm, cbar=False)
                # rdgn = sns.diverging_palette(h_neg=130, h_pos=10, s=99, l=55, sep=3)

                h2 = sns.clustermap(df.T, method="ward", metric="euclidean", figsize=(61.805, 100), col_cluster=False, cmap="bwr", norm=divnorm, cbar_kws={"ticks":[-2,-1,+0,+1,+2]})
                # h2 = sns.clustermap(df.T, method="ward", metric="euclidean", col_cluster=False, cmap=my_cmap, norm=divnorm, cbar=False)
                # cbar.ax.set_yticklabels(['<-2', '-1', '0', '1', '>2'])
                plt.setp(h2.ax_heatmap.xaxis.get_majorticklabels(), rotation=90)

                # ####
                # h2.ax_heatmap.set_xticklabels(h2.ax_heatmap.get_xmajorticklabels(), fontsize = 1.3)
                # cbar = plt.colorbar(h2)
                # cbar.ax.tick_params(labelsize=10)
                # matplotlib.axes.Axes.tick_params(labelsize=10)
                # plt.tick_params(labelsize=10)
                # h2.figure.axes[-1].yaxis.tick_params(labelsize=10)
                # label.set_size(20)
                # ####

                # plt.setp(h2.ax_heatmap, facecolor="black")
                plt.setp(h2.ax_heatmap.yaxis.get_majorticklines(), color="white", linewidth=0.001)
                plt.title("                 {} ({}/{}; Observed/DB)".format(atf, target_RNA_num, len(target)), loc='left')
                output_fig = "{}_cluster.pdf".format(atf)
                # output_pickle = "H(11)_transcriptome_clustermap.pickle"
                h2.savefig(output_fig)
                # with open(output_pickle, "wb") as file_handle:
                #     pickle.dump(h2, file_handle)
    
    for aextra_data in extra_data:
        TFs_mRNAs.update({aextra_data: RNA_values["{}".format(aextra_data)]})

    # DF = pd.DataFrame.from_dict(TFs_proteins)
    DF = pd.DataFrame.from_dict(TFs_mRNAs)
    DF.index = ["TP{}".format(i+1) for i in range(7)]
    # DF.T.to_csv("H(7)_TFs_proteins_df.txt", sep="\t")
    DF.T.to_csv("H(7)_TFs_mRNA_df.txt", sep="\t")
    
    DF_with_npnan = pd.DataFrame.from_dict(TFs_proteins_with_npnan)
    DF_with_npnan.index = ["TP{}".format(i+1) for i in range(7)]
    DF_with_npnan.T.to_csv("H(7)_TFs_proteins_df_with_npnan.txt", sep="\t")
    mask = DF_with_npnan.T.isnull()
    
    my_cmap = sns.diverging_palette(h_neg=268, h_pos=54, s=100, l=54, as_cmap=True)
    divnorm = DivergingNorm(vmin=-2, vcenter=0, vmax=2)
    
    h2 = sns.clustermap(DF.T, method="ward", metric="euclidean", figsize=(22.25, 36), col_cluster=False, xticklabels=False, cmap="bwr", norm=divnorm, cbar_kws={"ticks":[-2,-1,0,1,2]}, mask=mask)
    # plt.title("HCA of Transcription Related Genes in Proteome Heat Shock Samples TP1~7", loc='left')
    plt.setp(h2.ax_heatmap, facecolor="black")
    plt.setp(h2.ax_heatmap.yaxis.get_majorticklines(), color="white", linewidth=0.001)
    output_fig = "TFs_proteins_HCA.pdf"
    # output_pickle = "H(11)_transcriptome_clustermap.pickle"
    h2.savefig(output_fig)
    # with open(output_pickle, "wb") as file_handle:
    #     pickle.dump(h2, file_handle)

    g2 = sns.clustermap(DF.T, method="ward", metric="euclidean", figsize=(22.25, 36), row_cluster=False, col_cluster=False, xticklabels=False, cmap="bwr", norm=divnorm, cbar_kws={"ticks":[-2,-1,0,1,2]})
    plt.setp(g2.ax_heatmap, facecolor="black")
    plt.setp(g2.ax_heatmap.yaxis.get_majorticklines(), color="white", linewidth=0.001)
    output_fig2 = "TFs_mRNAs_heatmap.pdf"
    g2.savefig(output_fig2)

    with open("garbages.txt", "w") as f:
        for iii in RNA_garbages.keys():
            print(RNA_garbages[iii], file=f)

    with open("notmatchTFs.txt", "w") as f:
        for avalue in notmatch:
            print(avalue, file=f)

    with open("no_protein.txt", "w") as f:
        for a_no_protein in no_protein:
            print(a_no_protein, file=f)

    with open("no_RNA.txt", "w") as f:
        for a_no_RNA in no_RNA:
            print(a_no_RNA, file=f)

    with open("Thesis_Table.txt", "w") as f:
        for a_Thesis_Table in Thesis_Table:
            print(a_Thesis_Table, file=f)

    with open("histogram.txt", "w") as f:
        for a_histogram in histogram:
            if a_histogram[1] == 0:
                continue
            else:
                print("\t".join(map(str, a_histogram)), file=f)

    with open("TFs_HCA.txt", "w") as f:
        for a_TFs_protein in TFs_proteins:
            # print("\t".join(map(str, a_TFs_protein)), file=f)
            print(a_TFs_protein, file=f)
    
if __name__=="__main__":
    main()
