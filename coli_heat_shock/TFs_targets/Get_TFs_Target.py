#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last update: 06/18/2021

from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import DivergingNorm
import pandas as pd
import seaborn as sns; sns.set(color_codes=True, style="ticks", font_scale=.8)
import scipy.stats as sp
import json

def main():
    input_file1 = "transcript_sort_uniq.txt"
    tf_data = []
    with open(input_file1, "r") as file_handle1:
        for oneLine in file_handle1:
            oneLine = oneLine.rstrip()
            onetf = oneLine.split("\t")
            tf_data.append(onetf[0])

    TRGs_data = []
    input_file2 = "TRGs_157.txt"
    with open(input_file2, "r") as file_handle2:
        for oneline in file_handle2:
            oneline = oneline.rstrip()
            oneTRG = oneline.split("\t")
            TRGs_data.append(oneTRG[0])

    for num in range(1, 7):
        input_file3 = "group_{}.txt".format(num)
        group_num = []
        with open(input_file3, "r") as file_handle3:
            for a_group_num_gene in file_handle3:
                a_group_num_gene = a_group_num_gene.rstrip()
                group_num.append(a_group_num_gene)
    
        input_file4 = "511145_v2020_sRDB18-13_dsRNA_regNetwork.json"
        # JSONファイルからテキストストリームを生成．
        with open(input_file4, mode='rt', encoding='utf-8') as file:
            # 辞書オブジェクト(dictionary)を取得．
            data = json.load(file)
            number = 0
            if number == 0:
                TFs_targets = []
                for atf in tf_data:
                    # JSONデータから必要な箇所を出力．
                    for adata in data["elements"]["edges"]:
                        if atf in adata["data"]["source"]:
                            TFs_targets.append(adata["data"]["target"])
                        else:
                            continue
                with open("TFs_target(325).txt", "w") as f1:
                    for a_TFs_target in TFs_targets:
                        print(a_TFs_target, file=f1)

                TRGs_targets = []
                for aTRG in TRGs_data:
                    # JSONデータから必要な箇所を出力．
                    for adata in data["elements"]["edges"]:
                        if aTRG in adata["data"]["source"]:
                            TRGs_targets.append(adata["data"]["target"])
                        else:
                            continue
                with open("TRGs_target(157).txt", "w") as f2:
                    for a_TRGs_target in TRGs_targets:
                        print(a_TRGs_target, file=f2)
                number = 1
            group_targets = []
            for agroup in group_num:
                # JSONデータから必要な箇所を出力．
                for adata in data["elements"]["edges"]:
                    if agroup in adata["data"]["source"]:
                        group_targets.append(adata["data"]["target"])
                    else:
                        continue
            with open("group_{}_targets.txt".format(num), "w") as f3:
                for a_group_target in group_targets:
                    print(a_group_target, file=f3)
        
if __name__=="__main__":
    main()
