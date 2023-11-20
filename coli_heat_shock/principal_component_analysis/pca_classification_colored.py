#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last update: 01/05/2022

from collections import defaultdict
import matplotlib.pyplot as plt
# import seaborn as sns; sns.set(color_codes=True, font_scale=0.01)
import seaborn as sns; sns.set(color_codes=False, style="ticks", font_scale=0.9)
# import seaborn as sns; sns.set(color_codes=False, style="ticks", font_scale=0.2)
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

    h = plt.figure(figsize=[8, 8])

    HSPs = get_HSPs_name_list()
    essential = get_essential_name_list()
    RNAPs = get_RNAPs_name_list()
    ribosomal_proteins = get_ribosomal_proteins_name_list()
    aaRS = get_aaRS_name_list()
    SFs = get_SFs_name_list()
    TFs = get_TFs_name_list()
    rna_modification_enzymes = get_rna_modification_name_list()
    dna_enzymes = get_dna_name_list()
    transcription_enzymes = get_transcription_name_list()
    translation_enzymes = get_translation_name_list()
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

    # # 主成分空間でタンパク質名をプロット．
    # plt.subplot(1, 2, 1)
    for ii in range(len(protein_values)):
        # if df.index[ii] in HSPs:
        #     plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='red', marker='o', alpha=0.5)
        #     plt.annotate(df.index[ii], x_pca[ii]+[-0.0075, 0.013], alpha=1)
        # if df.index[ii] in essential:
        #     plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='red', marker='^', alpha=0.5)
        #     plt.annotate(df.index[ii], x_pca[ii]+[-0.0075, 0.013], alpha=1)
        # if df.index[ii] in RNAPs:
        #     plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='orange', marker='o', alpha=0.5)
        #     plt.annotate(df.index[ii], x_pca[ii]+[-0.0075, 0.013], alpha=1)
        # if df.index[ii] in ribosomal_proteins:
        #     plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='yellow', marker='o', alpha=0.5)
        #     plt.annotate(df.index[ii], x_pca[ii]+[-0.0075, 0.013], alpha=1)
        # if df.index[ii] in aaRS:
        #     plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='green', marker='o', alpha=0.5)
        #     plt.annotate(df.index[ii], x_pca[ii]+[-0.0075, 0.013], alpha=1)
        if df.index[ii] in SFs:
            plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='blue', marker='o', alpha=0.5)
            plt.annotate(df.index[ii], x_pca[ii]+[-0.0075, 0.013], alpha=1)
        if df.index[ii] in TFs:
            plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='purple', marker='o', alpha=0.5)
            plt.annotate(df.index[ii], x_pca[ii]+[-0.0075, 0.013], alpha=1)
        # if df.index[ii] in rna_modification_enzymes:
        #     plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='red', marker='p', alpha=0.5)
        #     plt.annotate(df.index[ii], x_pca[ii]+[-0.0075, 0.013], alpha=1)
        # ==========
        # if df.index[ii] in dna_enzymes:
        #     plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='red', marker='o', alpha=0.5)
        #     plt.annotate(df.index[ii], x_pca[ii]+[-0.0075, 0.013], alpha=1)
        # if df.index[ii] in transcription_enzymes:
        #     plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='orange', marker='o', alpha=0.5)
        #     plt.annotate(df.index[ii], x_pca[ii]+[-0.0075, 0.013], alpha=1)
        # if df.index[ii] in rna_modification_enzymes:
        #     plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='#E60012', marker='o', alpha=0.5)
        #     plt.annotate(df.index[ii], x_pca[ii]+[-0.0075, 0.013], alpha=1)
        # if df.index[ii] in translation_enzymes:
        #     plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='green', marker='o', alpha=0.5)
        #     plt.annotate(df.index[ii], x_pca[ii]+[-0.0075, 0.013], alpha=1)
        # if df.index[ii] in ribosomal_protein:
        #     plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='#F39800', marker='o', alpha=0.5)
        #     plt.annotate(df.index[ii], x_pca[ii]+[-0.0075, 0.013], alpha=1)
        # if df.index[ii] in aars:
        #     plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='#FFF100', marker='o', alpha=0.5)
        #     plt.annotate(df.index[ii], x_pca[ii]+[-0.0075, 0.013], alpha=1)
        # if df.index[ii] in cell_division_enzymes:
        #     plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='purple', marker='o', alpha=0.5)
        #     plt.annotate(df.index[ii], x_pca[ii]+[-0.0075, 0.013], alpha=1)
        # if df.index[ii] in amino_acid_metabolism:
        #     plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='#009944', marker='^', alpha=0.5)
        #     plt.annotate(df.index[ii], x_pca[ii]+[-0.0075, 0.013], alpha=1)
        # if df.index[ii] in carbohydrate_metabolism:
        #     plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='#0068B7', marker='^', alpha=0.5)
        #     plt.annotate(df.index[ii], x_pca[ii]+[-0.0075, 0.013], alpha=1)
        # if df.index[ii] in lipid_metabolism:
        #     plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='yellow', marker='^', alpha=0.5)
        #     plt.annotate(df.index[ii], x_pca[ii]+[-0.0075, 0.013], alpha=1)
        # if df.index[ii] in nucleotide_metabolism:
        #     plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='green', marker='^', alpha=0.5)
        #     plt.annotate(df.index[ii], x_pca[ii]+[-0.0075, 0.013], alpha=1)
        # if df.index[ii] in other_metabolism:
        #     plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='blue', marker='^', alpha=0.5)
        #     plt.annotate(df.index[ii], x_pca[ii]+[-0.0075, 0.013], alpha=1)
        # if df.index[ii] in signal_transduction:
        #     plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='#1D2088', marker='d', alpha=0.5)
        #     plt.annotate(df.index[ii], x_pca[ii]+[-0.0075, 0.013], alpha=1)
        # if df.index[ii] in response_to_stimulus:
        #     plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='#920783', marker='d', alpha=0.5)
        #     plt.annotate(df.index[ii], x_pca[ii]+[-0.0075, 0.013], alpha=1)
        # if df.index[ii] in energy_metabolism:
        #     plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='yellow', marker='d', alpha=0.5)
        #     plt.annotate(df.index[ii], x_pca[ii]+[-0.0075, 0.013], alpha=1)
        # if df.index[ii] in protein_metabolism:
        #     plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='green', marker='d', alpha=0.5)
        #     plt.annotate(df.index[ii], x_pca[ii]+[-0.0075, 0.013], alpha=1)
        # if df.index[ii] in protein_export:
        #     plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='blue', marker='d', alpha=0.5)
        #     plt.annotate(df.index[ii], x_pca[ii]+[-0.0075, 0.013], alpha=1)
        # if df.index[ii] in transport:
        #     plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='purple', marker='d', alpha=0.5)
        #     plt.annotate(df.index[ii], x_pca[ii]+[-0.0075, 0.013], alpha=1)
        else:
            plt.plot(x_pca[ii, 0], x_pca[ii, 1], c='black', marker='o', alpha=0.1)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        plt.title("Principal Component Analysis of Sigma Factors and TFs")
        plt.xlabel("PC1 (37.95%)")
        plt.ylabel("PC2 (16.97%)")
        plt.grid(True)

    h = plt.show()

    # with open("data/tmp/TFs_hikaku_pro.txt", "w") as f:
    #     for ii in x_pca:
    #         print(ii, file=f)

def get_HSPs_name_list():
    HSPs_list = []
    input_file = "data/raw/HSPs_cp_tr.txt"
    with open(input_file, "r") as file_handle:
        for row in file_handle:
            gene_name = ""
            row = row.rstrip()
            for char in row:
                gene_name+=char
                if char.isupper():
                    break
            HSPs_list.append(gene_name)
    with open("data/tmp/HSPs.txt", "w") as f:
        for ao in HSPs_list:
            print(ao, file=f)
    return HSPs_list

def get_essential_name_list():
    essential_list = []
    input_file = "data/raw/essential_genes_tr.txt"
    with open(input_file, "r") as file_handle:
        for row in file_handle:
            gene_name = ""
            row = row.rstrip()
            for char in row:
                gene_name+=char
                if char.isupper():
                    break
            essential_list.append(gene_name)
    with open("data/tmp/essential_genes.txt", "w") as f:
        for ao in essential_list:
            print(ao, file=f)
    return essential_list

def get_RNAPs_name_list():
    RNAPs_list = []
    input_file = "data/raw/RNA_polymerase.txt"
    with open(input_file, "r") as file_handle:
        for row in file_handle:
            gene_name = ""
            row = row.rstrip()
            for char in row:
                gene_name+=char
                if char.isupper():
                    break
            RNAPs_list.append(gene_name)
    with open("data/tmp/RNA_polymerase.txt", "w") as f:
        for ao in RNAPs_list:
            print(ao, file=f)
    return RNAPs_list

def get_ribosomal_proteins_name_list():
    ribosomal_proteins_list = []
    input_file = "data/raw/ribosomal_proteins_cp_tr.txt"
    with open(input_file, "r") as file_handle:
        for row in file_handle:
            gene_name = ""
            row = row.rstrip()
            for char in row:
                gene_name+=char
                if char.isupper():
                    break
            ribosomal_proteins_list.append(gene_name)
    with open("data/tmp/ribosomal_proteins.txt", "w") as f:
        for ao in ribosomal_proteins_list:
            print(ao, file=f)
    return ribosomal_proteins_list

def get_aaRS_name_list():
    aaRS_list = []
    input_file = "data/raw/aaRS_cp_tr.txt"
    with open(input_file, "r") as file_handle:
        for row in file_handle:
            gene_name = ""
            row = row.rstrip()
            for char in row:
                gene_name+=char
                if char.isupper():
                    break
            aaRS_list.append(gene_name)
    with open("data/tmp/aaRS.txt", "w") as f:
        for ao in aaRS_list:
            print(ao, file=f)
    return aaRS_list

def get_SFs_name_list():
    SFs_list = []
    input_file = "data/raw/SFs_tr_cut.txt"
    with open(input_file, "r") as file_handle:
        for row in file_handle:
            gene_name = ""
            row = row.rstrip()
            for char in row:
                gene_name+=char
                if char.isupper():
                    break
            SFs_list.append(gene_name)
    with open("data/tmp/SFs.txt", "w") as f:
        for ao in SFs_list:
            print(ao, file=f)
    return SFs_list

def get_TFs_name_list():
    TFs_list = []
    input_file = "data/raw/TRGs_tr.txt"
    with open(input_file, "r") as file_handle:
        for row in file_handle:
            gene_name = ""
            row = row.rstrip()
            for char in row:
                gene_name+=char
                if char.isupper():
                    break
            TFs_list.append(gene_name)
    with open("data/tmp/TFs.txt", "w") as f:
        for ao in TFs_list:
            print(ao, file=f)
    return TFs_list

def get_rna_modification_name_list():
    rna_modification_list = []
    input_file = "data/raw/RNA_modification_tr.txt"
    with open(input_file, "r") as file_handle:
        for row in file_handle:
            gene_name = ""
            row = row.rstrip()
            for char in row:
                gene_name+=char
                if char.isupper():
                    break
            rna_modification_list.append(gene_name)
    with open("data/tmp/rRNA_modification_enzymes.txt", "w") as f:
        for ao in rna_modification_list:
            print(ao, file=f)
    return rna_modification_list

def get_dna_name_list():
    dna_list = []
    input_file = "data/raw/DNA_list.txt"
    with open(input_file, "r") as file_handle:
        for row in file_handle:
            gene_name = ""
            row = row.rstrip()
            for char in row:
                gene_name+=char
                if char.isupper():
                    break
            dna_list.append(gene_name)
    with open("data/tmp/DNA.txt", "w") as f:
        for ao in dna_list:
            print(ao, file=f)
    return dna_list

def get_transcription_name_list():
    transcription_list = []
    input_file = "data/raw/transcription_list.txt"
    with open(input_file, "r") as file_handle:
        for row in file_handle:
            gene_name = ""
            row = row.rstrip()
            for char in row:
                gene_name+=char
                if char.isupper():
                    break
            transcription_list.append(gene_name)
    with open("data/tmp/transcription.txt", "w") as f:
        for ao in transcription_list:
            print(ao, file=f)
    return transcription_list

def get_translation_name_list():
    translation_list = []
    input_file = "data/raw/translation_list.txt"
    with open(input_file, "r") as file_handle:
        for row in file_handle:
            gene_name = ""
            row = row.rstrip()
            for char in row:
                gene_name+=char
                if char.isupper():
                    break
            translation_list.append(gene_name)
    with open("data/tmp/translation.txt", "w") as f:
        for ao in translation_list:
            print(ao, file=f)
    return translation_list

def get_cell_division_name_list():
    cell_division_list = []
    input_file = "data/raw/cell_cycle_list.txt"
    with open(input_file, "r") as file_handle:
        for row in file_handle:
            gene_name = ""
            row = row.rstrip()
            for char in row:
                gene_name+=char
                if char.isupper():
                    break
            cell_division_list.append(gene_name)
    with open("data/tmp/cell_cycle.txt", "w") as f:
        for ao in cell_division_list:
            print(ao, file=f)
    return cell_division_list

    ##########

def get_amino_acid_name_list():
    amino_list = []
    input_file = "data/raw/amino_acid_metabolism_list.txt"
    with open(input_file, "r") as file_handle:
        for row in file_handle:
            gene_name = ""
            row = row.rstrip()
            for char in row:
                gene_name+=char
                if char.isupper():
                    break
            amino_list.append(gene_name)
    with open("data/tmp/amino_acid_metabolism.txt", "w") as f:
        for ao in amino_list:
            print(ao, file=f)
    return amino_list

def get_carbohydrate_name_list():
    carbohydrate_list = []
    input_file = "data/raw/carbohydrate_metabolism_list.txt"
    with open(input_file, "r") as file_handle:
        for row in file_handle:
            gene_name = ""
            row = row.rstrip()
            for char in row:
                gene_name+=char
                if char.isupper():
                    break
            carbohydrate_list.append(gene_name)
    with open("data/tmp/carbohydrate_metabolism.txt", "w") as f:
        for ao in carbohydrate_list:
            print(ao, file=f)
    return carbohydrate_list

def get_lipid_name_list():
    lipid_list = []
    input_file = "data/raw/lipid_metabolism_list.txt"
    with open(input_file, "r") as file_handle:
        for row in file_handle:
            gene_name = ""
            row = row.rstrip()
            for char in row:
                gene_name+=char
                if char.isupper():
                    break
            lipid_list.append(gene_name)
    with open("data/tmp/aaRS.txt", "w") as f:
        for ao in lipid_list:
            print(ao, file=f)
    return lipid_list

def get_nucleotide_name_list():
    nucleotide_list = []
    input_file = "data/raw/nucleotide_metabolism_list.txt"
    with open(input_file, "r") as file_handle:
        for row in file_handle:
            gene_name = ""
            row = row.rstrip()
            for char in row:
                gene_name+=char
                if char.isupper():
                    break
            nucleotide_list.append(gene_name)
    with open("data/tmp/nucleotide_metabolism.txt", "w") as f:
        for ao in nucleotide_list:
            print(ao, file=f)
    return nucleotide_list

def get_other_name_list():
    other_list = []
    input_file = "data/raw/other_metabolism_list.txt"
    with open(input_file, "r") as file_handle:
        for row in file_handle:
            gene_name = ""
            row = row.rstrip()
            for char in row:
                gene_name+=char
                if char.isupper():
                    break
            other_list.append(gene_name)
    with open("data/tmp/other_metabolism.txt", "w") as f:
        for ao in other_list:
            print(ao, file=f)
    return other_list

def get_signal_name_list():
    signal_list = []
    input_file = "data/raw/signal_transduction_list.txt"
    with open(input_file, "r") as file_handle:
        for row in file_handle:
            gene_name = ""
            row = row.rstrip()
            for char in row:
                gene_name+=char
                if char.isupper():
                    break
            signal_list.append(gene_name)
    with open("data/tmp/signal_transduction.txt", "w") as f:
        for ao in signal_list:
            print(ao, file=f)
    return signal_list

def get_response_name_list():
    response_list = []
    input_file = "data/raw/response_to_stimulus_list.txt"
    with open(input_file, "r") as file_handle:
        for row in file_handle:
            gene_name = ""
            row = row.rstrip()
            for char in row:
                gene_name+=char
                if char.isupper():
                    break
            response_list.append(gene_name)
    with open("data/tmp/response_to_stimulus.txt", "w") as f:
        for ao in response_list:
            print(ao, file=f)
    return response_list

def get_energy_name_list():
    energy_list = []
    input_file = "data/raw/energy_metabolism_list.txt"
    with open(input_file, "r") as file_handle:
        for row in file_handle:
            gene_name = ""
            row = row.rstrip()
            for char in row:
                gene_name+=char
                if char.isupper():
                    break
            energy_list.append(gene_name)
    with open("data/tmp/energy_metabolism.txt", "w") as f:
        for ao in energy_list:
            print(ao, file=f)
    return energy_list

def get_pro_meta_name_list():
    pro_meta_list = []
    input_file = "data/raw/protein_processing_list.txt"
    with open(input_file, "r") as file_handle:
        for row in file_handle:
            gene_name = ""
            row = row.rstrip()
            for char in row:
                gene_name+=char
                if char.isupper():
                    break
            pro_meta_list.append(gene_name)
    with open("data/tmp/protein_processing.txt", "w") as f:
        for ao in pro_meta_list:
            print(ao, file=f)
    return pro_meta_list

def get_pro_exp_name_list():
    pro_exp_list = []
    input_file = "data/raw/protein_export_list.txt"
    with open(input_file, "r") as file_handle:
        for row in file_handle:
            gene_name = ""
            row = row.rstrip()
            for char in row:
                gene_name+=char
                if char.isupper():
                    break
            pro_exp_list.append(gene_name)
    with open("data/tmp/protein_export.txt", "w") as f:
        for ao in pro_exp_list:
            print(ao, file=f)
    return pro_exp_list

def get_transport_name_list():
    transport_list = []
    input_file = "data/raw/transport_list.txt"
    with open(input_file, "r") as file_handle:
        for row in file_handle:
            gene_name = ""
            row = row.rstrip()
            for char in row:
                gene_name+=char
                if char.isupper():
                    break
            transport_list.append(gene_name)
    with open("data/tmp/transport.txt", "w") as f:
        for ao in transport_list:
            print(ao, file=f)
    return transport_list

if __name__=="__main__":
    main()
