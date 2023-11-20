#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last update: 09/02/2021

from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import DivergingNorm
import pandas as pd
import seaborn as sns; sns.set(color_codes=True, style="ticks", font_scale=.8)
import scipy.stats as sp
import json

def main():
    input_file1 = "proteome_expression_median.txt"
    protein_data = []
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
                    for i in range(7, 25):
                        if not col1[i] == "---":
                            break
                        if i == 24:
                            missing_flag = True
                    if missing_flag:
                        continue
                    
                protein_data.append(pro_uniprot_ac)
        # print(len(protein_data))

    input_file2 = "transcriptome_expression_-f2changed.txt"
    RNA_data = []
    # ###
    # RNA_ids = defaultdict()
    # RNA_values = {}
    # ###
    with open(input_file2, "r") as file_handle2:
        for row_num2, row2 in enumerate(file_handle2):
            row2 = row2.rstrip()
            col2 = row2.split("\t")
            if row_num2 == 0:
                continue
            else:
                tra_uniprot_ac = col2[0].split("_")[-1].split("-")[0]
                # RNA_ids[tra_uniprot_ac] = [col2[0], col2[1]]
                changing_flag = False
                if "0.00" in row2:
                    for index, oneData in enumerate(col2[2:13]):
                        if not oneData == "0.00":
                            break
                        if index == 10:
                            changing_flag = True
                if changing_flag:
                    continue
                else:
                    RNA_data.append(tra_uniprot_ac)
    # ###
    #             RNA_value = []
    #             RNA_not_missing_value = []
    #             values_zscore = []
    #             for index, one in enumerate(col2[2:13]):
    #                 if one != "0.00":
    #                     RNA_not_missing_value.append(float(one))
    #                     RNA_value.append(float(one))
    #                 else:
    #                     RNA_value.append(float(one))
    #             if RNA_not_missing_value:
    #                 if len(RNA_not_missing_value) == 1:
    #                     for one in col2[2:13]:
    #                         if one != "0.00":
    #                             values_zscore.append(0)
    #                         else:
    #                             values_zscore.append(-2)
    #                 else:
    #                     values_zscore = sp.stats.zscore(RNA_value)
    #                 RNA_values.update({tra_uniprot_ac: values_zscore})
    # ###
    # df = pd.DataFrame.from_dict(RNA_values)
    # print(df)
    # ###

    input_file1 = "511145_v2020_sRDB18-13_dsRNA_regNetwork.json"
    Upstream_Table = []
    # JSONファイルからテキストストリームを生成．
    with open(input_file1, mode='rt', encoding='utf-8') as file:
        # 辞書オブジェクト(dictionary)を取得．
        data = json.load(file)
        upstream_tabel = [False, False, False]
        target = []
        for adata in data["elements"]["edges"]:
            if adata["data"]["target"] not in target:
               target.append(adata["data"]["target"])
            else:
                continue

        for atarget in target:
            upstream_tabel[0] = atarget
            source = []
            measured_num = 0
            for adata in data["elements"]["edges"]:
                if atarget in adata["data"]["target"]:
                    source.append(adata["data"]["source"])
                    if adata["data"]["source"] in protein_data and adata["data"]["source"] in RNA_data:
                        measured_num += 1
                else:
                    continue
            upstream_tabel[1] = len(source)
            upstream_tabel[2] = measured_num
            Upstream_Table.append("\t".join(map(str, upstream_tabel)))

    with open("upstream_table.txt", "w") as f:
        for a_upstream in Upstream_Table:
            print(a_upstream, file=f)
    
if __name__=="__main__":
    main()
