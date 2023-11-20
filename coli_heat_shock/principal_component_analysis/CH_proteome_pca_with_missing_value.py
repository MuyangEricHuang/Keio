#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last update: 01/03/2022

from collections import defaultdict
import matplotlib.pyplot as plt
# import seaborn as sns; sns.set(color_codes=True, font_scale=0.01)
# import seaborn as sns; sns.set(color_codes=False, style="ticks", font_scale=0.9)
import seaborn as sns; sns.set(color_codes=False, style="ticks", font_scale=0.2)
import pandas as pd
import numpy as np
import scipy.stats as sp
import scipy.cluster.hierarchy as hierarchy
from sklearn.preprocessing import Imputer
from sklearn import preprocessing
from sklearn.decomposition import PCA
import pickle
import pprint
from ipywidgets import interact, FloatSlider
# import fastcluster

def main():
    input_file = "data/raw/proteome_expression_median_rmins.txt"
    protein_ids = defaultdict()
    protein_values = {}
    protein_values_with_npnan = {}
    max_amount = []

    with open(input_file, "r") as file_handle:
        for row_num, row in enumerate(file_handle):
            row = row.rstrip()
            col = row.split("\t")
            if row_num == 0:
                continue
            else:
                # uniprot_ac = "\t".join([col[0], col[3].split("#")[1], col[2]])
                uniprot_ac = col[3].split("#")[1]
                if "---" in row:
                    missing_flag = False
                    for i in range(7, 25):
                        if not col[i] == "---":
                            break
                        if i == 24:
                            missing_flag = True
                    if missing_flag:
                        continue

                protein_ids[uniprot_ac] = [col[0], col[1], col[2], col[3], col[4], col[5], col[6]]

                not_missing_values = []
                mask_position = []
                values_zscore = []
                not_missing_values_number = 0
                for index, one in enumerate(col[7:]):
                    if one != "---":
                        not_missing_values.append(float(one))
                    else:
                        mask_position.append(index)
                if not_missing_values:
                    if len(not_missing_values) == 1:
                        max_amount.append([col[7:]])
                        for one in col[7:]: 
                            if one != "---":
                                values_zscore.append(0)
                                not_missing_values_number += 1
                            else:
                                values_zscore.append(-2)
                    else:
                        zscore_not_missing_values = sp.stats.zscore(not_missing_values)
                        for one in col[7:]:
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
                else:
                    print(pro_uniprot_ac)
                    continue
                protein_values.update({uniprot_ac: values_zscore})
                protein_values_with_npnan.update({uniprot_ac: values_with_npnan})
        
        # with open("data/tmp/one_value_(CH).txt", "w") as f:
        #     for avalue in max_amount:
        #         print(avalue, file=f)
    
    # make DataFrame
    df = pd.DataFrame.from_dict(protein_values)
    # df.index = ["{0}{1}".format(status, i+1) for status in ["C", "H"] for i in range(7), "H8", "H9", "H10", "H11"]
    df.index = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H10", "H11"]
    df = df.T
    df.to_csv("data/tmp/CH_proteome_df.txt", sep="\t")
    # df.T.to_csv("data/tmp/CH_proteome_df.txt", sep="\t")

    df_with_npnan = pd.DataFrame.from_dict(protein_values_with_npnan)
    # df_with_npnan.index = ["{0}{1}".format(status, i+1) for status in ["C", "H"] for i in range(7), "H8", "H9", "H10", "H11"]
    df_with_npnan.index = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H10", "H11"]
    df_with_npnan = df_with_npnan.T
    df_with_npnan.to_csv("data/tmp/CH_proteome_df_with_npnan.txt", sep="\t")
    # df_with_npnan.T.to_csv("data/tmp/CH_proteome_df_with_npnan.txt", sep="\t")

    x = np.array(df.values)[:, :]
    # x = np.array(df_with_npnan.values)[:, :]
    # x_scaled = preprocessing.scale(x) # 正規化
    # 列に対して正規化を行う．

    print(len(x))

    pca = PCA(n_components=2)
    # 主成分空間に射影
    pca.fit(x)
    print("固有値:")
    print(pca.explained_variance_)
    print("固有ベクトル:")
    print(pca.components_)
    print("寄与率:")
    print(pca.explained_variance_ratio_)
    x_pca = pca.fit_transform(x)

    # h = plt.figure(figsize=[100, 61.80339887499])
    # h = plt.figure(figsize=[8, 8])
    h = plt.figure(figsize=[80, 80])

    dna_enzymes = get_dna_name_list()
    transcription_enzymes = get_transcription_name_list()
    rna_modification_enzymes = get_rna_modification_name_list()
    translation_enzymes = get_translation_name_list()
    aars = get_aars_name_list()
    cell_division_enzymes = get_cell_division_name_list()
    amino_acid_metabolism = get_amino_acid_name_list()
    carbohydrate_metabolism = get_carbohydrate_name_list()
    lipid_metabolism = get_lipid_name_list()
    nucleotide_metabolism = get_nucleotide_name_list()
    other_metabolism = get_other_name_list()
    signal_transduction = get_signal_name_list()
    response_to_stimulus = get_response_name_list()
    energy_metabolism = get_energy_name_list()
    protein_metabolism = get_pro_meta_name_list()
    protein_export = get_pro_exp_name_list()
    transport = get_transport_name_list()

    # 主成分空間でタンパク質名をプロット．
    plt.subplot(1, 2, 1)
    for ii in range(len(protein_values)):
        if df.index[ii] in dna_enzymes:
            plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='red', marker='o', alpha=0.5)
        elif df.index[ii] in transcription_enzymes:
            plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='orange', marker='o', alpha=0.5)
        elif df.index[ii] in rna_modification_enzymes:
            plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='yellow', marker='o', alpha=0.5)
        elif df.index[ii] in translation_enzymes:
            plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='green', marker='o', alpha=0.5)
        elif df.index[ii] in aars:
            plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='blue', marker='o', alpha=0.5)
        elif df.index[ii] in cell_division_enzymes:
            plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='purple', marker='o', alpha=0.5)
        elif df.index[ii] in amino_acid_metabolism:
            plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='red', marker='o', alpha=0.5)
        elif df.index[ii] in carbohydrate_metabolism:
            plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='orange', marker='^', alpha=0.5)
        elif df.index[ii] in lipid_metabolism:
            plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='yellow', marker='^', alpha=0.5)
        elif df.index[ii] in nucleotide_metabolism:
            plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='green', marker='^', alpha=0.5)
        elif df.index[ii] in other_metabolism:
            plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='blue', marker='^', alpha=0.5)
        elif df.index[ii] in signal_transduction:
            plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='red', marker='d', alpha=0.5)
        elif df.index[ii] in response_to_stimulus:
            plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='orange', marker='d', alpha=0.5)
        elif df.index[ii] in energy_metabolism:
            plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='yellow', marker='d', alpha=0.5)
        elif df.index[ii] in protein_metabolism:
            plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='green', marker='d', alpha=0.5)
        elif df.index[ii] in protein_export:
            plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='blue', marker='d', alpha=0.5)
        elif df.index[ii] in transport:
            plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='purple', marker='d', alpha=0.5)
        else:
            plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='black', marker='o', alpha=0.1)
        
        plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='black', marker='o', alpha=0.1)
        plt.annotate(df.index[ii], x_pca[ii]+[-0.0075, 0.013], alpha=1)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        plt.title("Proteins Principal Component Analysis")
        plt.xlabel("PC1 (37.95%)")
        plt.ylabel("PC2 (16.97%)")
        plt.grid(True)

    # 主成分空間でTPをプロット．
    plt.subplot(1, 2, 2)
    judge = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H10", "H11"]
    comps = PCA(n_components=2).fit(x).components_
    for ii in range(0, len(judge)):
        plt.plot(comps[0][:7], comps[1][:7], c="blue", marker='o')
        plt.plot(comps[0][7:18], comps[1][7:18], c="red", marker='s')
        plt.annotate(judge[ii], comps[:, ii])
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        plt.title("Time Points Principal Component Analysis")
        plt.xlabel("PC1 (37.95%)")
        plt.ylabel("PC2 (16.97%)")
        plt.grid(True)
    
    h.savefig("data/tmp/CH18_PCA_spstatsDone_scaleNone_pro.pdf")

    with open("data/tmp/CH_hikaku_pro_pdf.txt", "w") as f:
        for ii in x_pca:
            print(ii, file=f)

    h = plt.show()

    with open("data/tmp/CH_hikaku_pro_png.txt", "w") as f:
        for ii in x_pca:
            print(ii, file=f)

if __name__=="__main__":
    main()
