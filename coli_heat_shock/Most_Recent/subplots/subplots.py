#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns; sns.set(color_codes=False, style="ticks", font_scale=0.1)
# import seaborn as sns; sns.set(color_codes=False, style="ticks", font_scale=0.3)
import pandas as pd
import numpy as np
import math
# import scipy.stats as stats
# 上2行はcopy.
import scipy.stats as sp
from sklearn.preprocessing import Imputer
from sklearn import preprocessing # 前処理用．
from sklearn.decomposition import PCA # 主成分分析用．
import pickle
import pprint ### 見やすくプリント．例えば数字が含まれているリストだったら改行しながらプリントされる．
from ipywidgets import interact, FloatSlider ### 色の指定に使用（特に分からない，自分で付け加えた）．

def main():
    gene_names = get_gene_names()
    protein_id_value_dict = get_protein_expression(gene_names)
    mRNA_id_value_dict = get_transcriptome_expression(gene_names)

    #define dictionary to covert "101110" => 46
    #                            "111111" => 64
    #                            "000001" =>  1
    up_down_dict = {}
    for i in range(64):
        key = str(bin(i))[2:].zfill(6)
        up_down_dict.update({key: i})

    fig, ax = plt.subplots(8, 8, figsize=(30, 30))
    protein_xaxis_pos = np.array([i for i in range(4)])
    mRNA_xaxis_pos = np.array([i+4 for i in range(4)])

    for uniprot_ac in protein_id_value_dict:
        if uniprot_ac not in mRNA_id_value_dict.keys():
            continue

        #log2 conversion
        protein_values = [math.log2(val) for val in protein_id_value_dict[uniprot_ac][7:11]]
        mRNA_values = [math.log2(val) for val in mRNA_id_value_dict[uniprot_ac][7:11]]

        #"101110" means protein{TP1-2: up, TP2-3: down, TP3-4: up}, mRNA{TP1-2: up, TP2-3: up, TP3-4: down}
        protein_binary_up_down_list = ["1" if protein_values[i]<protein_values[i+1] else "0" for i in range(3)]
        mRNA_binary_up_down_list = ["1" if mRNA_values[i]<mRNA_values[i+1] else "0" for i in range(3)]
        binary_up_down_string = "".join(protein_binary_up_down_list) + "".join(mRNA_binary_up_down_list)
        print(binary_up_down_string)
        subplot_index = up_down_dict[binary_up_down_string]

        #plot (color, marker, alpha, markersize, linestyle, linewidth...)
        ax[subplot_index%8, int(subplot_index/8)%8].plot(protein_xaxis_pos, protein_values, marker="o", color="red", linewidth=0.1)
        ax[subplot_index%8, int(subplot_index/8)%8].plot(mRNA_xaxis_pos, mRNA_values, marker="o", color="blue", linewidth=0.1)

        #config
        ax[subplot_index%8, int(subplot_index/8)%8].set_xticks([i for i in range(8)])
        ax[subplot_index%8, int(subplot_index/8)%8].set_xticklabels(["TP1", "TP2", "TP3", "TP4"]*2, fontsize=5)
        #ax[subplot_index%8, int(subplot_index/8)%8].set_ylim(-4, 4)

        # plt.title(jj, fontsize=2)
        #plt.title(jj, fontsize=90)
        #plt.xlabel("Time Points")
        #plt.ylabel("TPM(spstats)")
        #plt.xticks([num for num in range(14)], ["{0} TP{1}".format(status, i+1) for status in ["Control", "Heat_Shock"] for i in range(7)])
        # plt.legend((p1[0], p2[0], p3[0], p4[0]),("Protein Control", "Protein Heat Shock", "mRNA Control", "mRNA Heat Shock"), title="Label Name")
        # # plt.legend((p1[0], p2[0], p3[0], p4[0]), ("Protein Control", "Protein Heat Shock", "mRNA Control", "mRNA Heat Shock"), title="Label Name", prop={'size':12,})

        #plt.gca().spines['right'].set_visible(False)
        #plt.gca().spines['top'].set_visible(False)
        #plt.grid(True)

    # h = plt.show()
    plt.savefig("data/tmp/mm_subplots.pdf")
    # h.savefig("data/tmp/subplots_y.pdf")

def get_gene_names():
    gene_names = []
    input_file = "data/raw/subplot_name.txt"
    with open(input_file) as file_handle:
        for row_index, row in enumerate(file_handle):
            row = row.rstrip()
            gene_names.append(row)
    return gene_names

def get_protein_expression(gene_names):
    protein_id_value_dict = {}
    input_file = "data/raw/ecoli_heat_proteome_average.txt"
    with open(input_file, "r") as file_handle:
        for row_index, row in enumerate(file_handle):
            row = row.rstrip()
            col = row.split("\t")
            if row_index == 0:
                continue
            elif col[2].split('#')[1] in gene_names:
                # col[num+11] != "---" and col[num+12] != "---":
                uniprot_ac = col[2].split("#")[1]
                if "---" in row:
                    missing_flag = False
                    for i in range(4, 18):
                        if not col[i] == "---":
                            break
                        if i == 17:
                            missing_flag = True
                    if missing_flag:
                        missing_flag = False
                        continue

                not_missing_values = []
                mask_position = []
                values = []
                for index, one in enumerate(col[4:]):
                    if one != "---":
                        not_missing_values.append(float(one))
                    else:
                        mask_position.append(index)
                if not_missing_values: # ここで全欠損の場合を除こうとした．not_missing_valueというリストが空だった場合，ifはFalseであることになり，以下は実行されない．
                    for one in col[4:]:
                        if one != "---":
                            values.append(float(one))
                        else:
                            continue
                    # values_zscore = sp.stats.zscore(values) # zscore化後のリスト．

                    value_with_npnan = []
                    j = 0
                    for one in range(14):
                        if one in mask_position:
                            value_with_npnan.append(100)
                        else:
                            # value_with_npnan.append(values_zscore[j])
                            value_with_npnan.append(values[j])
                            j += 1
                    protein_id_value_dict.update({uniprot_ac: value_with_npnan})

                # # b = float(col[num+12])/float(col[num+11])                
                # b = "\t".join(col[11:15])

    # make DataFrame
    pro_df = pd.DataFrame.from_dict(protein_id_value_dict)
    pro_df.index = ["{0}_TP{1}".format(status, i+1) for status in ["Control", "Heat_Shock"] for i in range(7)]
    pro_df = pro_df.T # Tは列と行の逆転を意味する．
    pro_df.to_csv("data/tmp/subplots_proteome_df.txt", sep="\t")

    return protein_id_value_dict

def get_transcriptome_expression(gene_names):
    mRNA_id_value_dict = {}
    input_file = "data/raw/transcriptome_expression.txt"
    with open(input_file, "r") as file_handle:
        for row_index, row in enumerate(file_handle):
            row = row.rstrip()
            col = row.split("\t")
            if row_index == 0:
                continue
            elif col[1].split("_")[-1] in gene_names:
                values = []
                garbages = []
                uniprot_ac = col[1].split("_")[-1]
                
                changing_flag = False
                if "0.00" in col[9:13]:
                    continue
                    for index, one in enumerate(col[2:]):
                        if not one == "0.00":
                            break
                        if index == 13:
                            changing_flag = True
                
                if changing_flag:
                    for i in range(2, 16):
                        garbages.append(float(col[i]))
                
                else:
                    for j in range(2, 16):
                        values.append(float(col[j]))
                    mRNA_id_value_dict.update({uniprot_ac: values})
                changing_flag = False

    tra_df = pd.DataFrame.from_dict(mRNA_id_value_dict)
    tra_df.index = ["{0}_TP{1}".format(status, i+1) for status in ["Control", "Heat_Shock"] for i in range(7)]
    tra_df = tra_df.T # Tは列と行の逆転を意味する．
    tra_df.to_csv("data/tmp/subplots_transcriptome_df.txt", sep="\t")

    return mRNA_id_value_dict

if __name__=="__main__":
    main()
