#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last update: 08/27/2021

from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.colors import DivergingNorm
import seaborn as sns; sns.set(color_codes=True, font_scale=0.1)
import pandas as pd
import numpy as np
import scipy.stats as sp
# import scipy.cluster.hierarchy as hierarchy
# from sklearn.preprocessing import Imputer
# import pickle
# import pprint
# from ipywidgets import interact, FloatSlider
# import fastcluster

def main():
    # input_file1 = "data/raw/transcription_related_proteins.txt"
    input_file1 = "data/raw/ribosomal_proteins_cp_tr.txt"
    # input_file1 = "data/raw/aaRS_cp_tr.txt"
    protein_data = []
    proteins = {}
    proteins_with_npnan = {}
    # mRNA = {}
    # mRNA_with_npnan = {}
    
    with open(input_file1, "r") as file_handle1:
        for oneLine in file_handle1:
            oneLine = oneLine.rstrip()
            protein_data.append(oneLine)
    # with open("data/tmp/TRGs.txt", "w") as f:
    with open("data/tmp/ribosomal_proteins.txt", "w") as f:
    # with open("data/tmp/aaRS.txt", "w") as f:
        for ao in protein_data:
            print(ao, file=f)

    input_file2 = "data/raw/essential_genes_list_cp_tr.txt"
    EGs_data = []
    with open(input_file2, "r") as file_handle2:
        for oneEG in file_handle2:
            oneEG = oneEG.rstrip()
            EGs_data.append(oneEG)
    
    input_file3 = "data/raw/proteome_expression_median.txt"
    protein_ids = defaultdict()
    protein_values = {}
    protein_values_with_npnan = {}
    uniprot_ac = []

    dna_enzymes = get_dna_name_list()
    transcription_enzymes = get_transcription_name_list()
    rna_modification_enzymes = get_rna_modification_name_list()
    translation_enzymes = get_translation_name_list()
    ribosomal_protein = get_ribosomal_name_list()
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
    metabolism = get_metabolism_list()

    with open(input_file3, "r") as file_handle3:
        for row_num1, row1 in enumerate(file_handle3):
            row1 = row1.rstrip()
            col1 = row1.split("\t")
            if row_num1 == 0:
                continue
            else:
                # uniprot_ac = col[0]
                # if col[2].split("#")[1] in dna_enzymes:
                #     uniprot_ac = "\t".join([col[0], col[2].split("#")[1], col[1]])
                # if col[2].split("#")[1] in transcription_enzymes:
                #     uniprot_ac = "\t".join([col[0], col[2].split("#")[1], col[1]])
                # if col[2].split("#")[1] in rna_modification_enzymes:
                #     uniprot_ac = "\t".join([col[0], col[2].split("#")[1], col[1]])
                # if col[2].split("#")[1] in translation_enzymes:
                #     uniprot_ac = "\t".join([col[0], col[2].split("#")[1], col[1]])
                # if col[2].split("#")[1] in ribosomal_protein:
                #     uniprot_ac = "\t".join([col[0], col[2].split("#")[1], col[1]])
                # if col[2].split("#")[1] in aars:
                #     uniprot_ac = "\t".join([col[0], col[2].split("#")[1], col[1]])
                # if col[2].split("#")[1] in cell_division_enzymes:
                #     uniprot_ac = "\t".join([col[0], col[2].split("#")[1], col[1]])
                # if col[2].split("#")[1] in amino_acid_metabolism:
                #     uniprot_ac = "\t".join([col[0], col[2].split("#")[1], col[1]])
                # if col[2].split("#")[1] in carbohydrate_metabolism:
                #     uniprot_ac = "\t".join([col[0], col[2].split("#")[1], col[1]])
                # if col[2].split("#")[1] in lipid_metabolism:
                #     uniprot_ac = "\t".join([col[0], col[2].split("#")[1], col[1]])
                # if col[2].split("#")[1] in nucleotide_metabolism:
                #     uniprot_ac = "\t".join([col[0], col[2].split("#")[1], col[1]])
                # if col[2].split("#")[1] in other_metabolism:
                #     uniprot_ac = "\t".join([col[0], col[2].split("#")[1], col[1]])
                # if col[2].split("#")[1] in signal_transduction:
                #     uniprot_ac = "\t".join([col[0], col[2].split("#")[1], col[1]])
                # if col[2].split("#")[1] in response_to_stimulus:
                #     uniprot_ac = "\t".join([col[0], col[2].split("#")[1], col[1]])
                # if col[2].split("#")[1] in energy_metabolism:
                #     uniprot_ac = "\t".join([col[0], col[2].split("#")[1], col[1]])
                # if col[2].split("#")[1] in protein_metabolism:
                #     uniprot_ac = "\t".join([col[0], col[2].split("#")[1], col[1]])
                # if col[2].split("#")[1] in protein_export:
                #     uniprot_ac = "\t".join([col[0], col[2].split("#")[1], col[1]])
                # if col[2].split("#")[1] in transport:
                #     uniprot_ac = "\t".join([col[0], col[2].split("#")[1], col[1]])
                # if col[2].split("#")[1] in metabolism:
                #     uniprot_ac = "\t".join([col[0], col[2].split("#")[1], col[1]])
                # else:
                #     uniprot_ac = row_num
                if col1[3].split("#")[1] in EGs_data:
                    pro_uniprot_ac = col1[3].split("#")[1]
                    # pro_uniprot_ac = col1[2]
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
    
    input_file3 = "data/raw/transcriptome_expression_-f2changed.txt"
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
                        zscore_not_missing_values = sp.stats.zscore(RNA_value)
                        # for one in range(11):
                        for one in range(7):
                            values_zscore.append(zscore_not_missing_values[one])

                    RNA_values.update({tra_uniprot_ac: values_zscore})
        # print(RNA_values)
        # print(protein_garbages)

    pro_num = 0
    for aprotein_key in protein_values.keys():
        if aprotein_key in protein_data:
            proteins.update({aprotein_key: protein_values["{}".format(aprotein_key)]})
            proteins_with_npnan.update({aprotein_key: protein_values_with_npnan["{}".format(aprotein_key)]})
        else:
            proteins.update({pro_num: protein_values["{}".format(aprotein_key)]})
            proteins_with_npnan.update({pro_num: protein_values_with_npnan["{}".format(aprotein_key)]})
            pro_num += 1
    
    for aprotein_data in protein_data:
        if aprotein_data in protein_values:
            proteins.update({aprotein_data: protein_values["{}".format(aprotein_data)]})
            proteins_with_npnan.update({aprotein_data: protein_values_with_npnan["{}".format(aprotein_data)]})
            if aprotein_data in RNA_values:
                mRNA.update({aprotein_data: RNA_values["{}".format(aprotein_data)]})
                mRNA_with_npnan.update({aprotein_data: RNA_values["{}".format(aprotein_data)]})
            else:
                mRNA.update({pro_num: [0,0,0,0,0,0,0]})
                mRNA_with_npnan.update({pro_num: [np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]})
                pro_num += 1
        else:
            proteins.update({pro_num: protein_values["{}".format(aprotein_data)]})
            proteins_with_npnan.update({pro_num: protein_values_with_npnan["{}".format(aprotein_data)]})
            if aprotein_data in RNA_values:
                mRNA.update({aprotein_data: RNA_values["{}".format(aprotein_data)]})
                mRNA_with_npnan.update({aprotein_data: RNA_values["{}".format(aprotein_data)]})
                pro_num += 1
            else:
                mRNA.update({pro_num: [0,0,0,0,0,0,0]})
                mRNA_with_npnan.update({pro_num: [np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]})
                pro_num += 1

    DF = pd.DataFrame.from_dict(proteins)
    DF.index = ["H{}".format(i+1) for i in range(7)]
    DF.T.to_csv("data/tmp/_proteome_df_(protein_classification_shown).txt", sep="\t")
    
    DF_with_npnan = pd.DataFrame.from_dict(proteins_with_npnan)
    DF_with_npnan.index = ["H{}".format(i+1) for i in range(7)]
    DF_with_npnan.T.to_csv("data/tmp/_proteome_df_with_npnan_(protein_classification_shown).txt", sep="\t")
    mask1 = DF_with_npnan.T.isnull()

    # print(DF.T)
    # print(mask1)
    
    # cmap = sns.diverging_palette(240, 10, s=90, l=50, n=5, center="light", as_cmap=True) # color map https://qiita.com/SaitoTsutomu/items/c79c9973a92e1e2c77a7
    my_cmap = sns.diverging_palette(h_neg=268, h_pos=54, s=100, l=54, as_cmap=True)
    divnorm = DivergingNorm(vmin=-2, vcenter=0, vmax=2)
    colors = ["black" if gene_id in protein_data else "white" for gene_id in DF.columns]
    karakuri = 0
    for gene_id in DF.columns:
        if gene_id in protein_data:
            karakuri += 1
    print(karakuri)
    h2 = sns.clustermap(DF.T, method="ward", metric="euclidean", figsize=(61.805, 100), col_cluster=False, row_colors=colors, cmap="bwr", norm=divnorm, cbar_kws={"ticks":[-2,-1,0,1,2]}, mask=mask1)
    # plt.title("HCA of Transcription Related Genes in Proteome Heat Shock Samples TP1~7", loc='left')
    plt.setp(h2.ax_heatmap, facecolor="black")
    plt.setp(h2.ax_heatmap.xaxis.get_majorticklabels(), rotation=90)
    plt.setp(h2.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
    plt.setp(h2.ax_heatmap.yaxis.get_majorticklines(), color="white", linewidth=0.001)
    output_fig = "data/tmp/_HCA_(protein_classification_shown).pdf"
    # output_pickle = "H(11)_transcriptome_clustermap.pickle"
    h2.savefig(output_fig)
    # with open(output_pickle, "wb") as file_handle:
    #     pickle.dump(h2, file_handle)

def get_aars_name_list():
    aars_list = []
    input_file = "data/raw/aaRS_list.txt"
    with open(input_file, "r") as file_handle:
        for row in file_handle:
            gene_name = ""
            row = row.rstrip()
            for char in row:
                gene_name+=char
                if char.isupper():
                    break
            aars_list.append(gene_name)
    with open("data/tmp/aaRS.txt", "w") as f:
        for ao in aars_list:
            print(ao, file=f)
    return aars_list

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

def get_rna_modification_name_list():
    rna_modification_list = []
    input_file = "data/raw/rna_modification_and_processing_list.txt"
    with open(input_file, "r") as file_handle:
        for row in file_handle:
            gene_name = ""
            row = row.rstrip()
            for char in row:
                gene_name+=char
                if char.isupper():
                    break
            rna_modification_list.append(gene_name)
    with open("data/tmp/rna_modification_and_processing.txt", "w") as f:
        for ao in rna_modification_list:
            print(ao, file=f)
    return rna_modification_list

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

def get_ribosomal_name_list():
    ribosomal_list = []
    input_file = "data/raw/ribosomal_list.txt"
    with open(input_file, "r") as file_handle:
        for row in file_handle:
            gene_name = ""
            row = row.rstrip()
            for char in row:
                gene_name+=char
                if char.isupper():
                    break
            ribosomal_list.append(gene_name)
    with open("data/tmp/ribosomal.txt", "w") as f:
        for ao in ribosomal_list:
            print(ao, file=f)
    return ribosomal_list

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

def get_metabolism_list():
    metabolism_list = []
    input_file = "data/raw/metabolism_list.txt"
    with open(input_file, "r") as file_handle:
        for row in file_handle:
            gene_name = ""
            row = row.rstrip()
            for char in row:
                gene_name+=char
                if char.isupper():
                    break
            metabolism_list.append(gene_name)
    with open("data/tmp/metabolism.txt", "w") as f:
        for ao in metabolism_list:
            print(ao, file=f)
    return metabolism_list

if __name__=="__main__":
    main()
