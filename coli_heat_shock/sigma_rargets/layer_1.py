#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last update: 08/26/2021

from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import DivergingNorm
import pandas as pd
import seaborn as sns; sns.set(color_codes=True, style="ticks", font_scale=.8)
import scipy.stats as sp
import json

def main():
    used_file = "used_layer.txt"
    used_data = []
    with open(used_file, "r") as used_handle:
        for usedLayer in used_handle:
            usedLayer = usedLayer.rstrip()
            usedlayer = usedLayer.split("\t")
            used_data.append(usedlayer[0])

    # layer_file = "layer_1.txt"
    # layer_file = "layer_2.txt"
    # layer_file = "layer_3_su.txt"
    layer_file = "layer_4_su.txt"
    layer_data = []
    with open(layer_file, "r") as layer_handle:
        for oneLayer in layer_handle:
            oneLayer = oneLayer.rstrip()
            onelayer = oneLayer.split("\t")
            layer_data.append(onelayer[0])

    input_file4 = "511145_v2020_sRDB18-13_dsRNA_regNetwork.json"
    plus_num = 0
    minus_num = 0
    space = 0
    space_data = []
    # JSONファイルからテキストストリームを生成．
    with open(input_file4, mode='rt', encoding='utf-8') as file:
        # 辞書オブジェクト(dictionary)を取得．
        data = json.load(file)
        target = []
        for alayer_data in layer_data:
            # JSONデータから必要な箇所を出力．
            for adata in data["elements"]["edges"]:
                if alayer_data in adata["data"]["source"]:
                    if adata["data"]["target"] not in used_data:
                        target.append(adata["data"]["target"])
                        if "+" in adata["data"]["Effect"]:
                            plus_num += 1
                            if "-" in adata["data"]["Effect"]:
                                minus_num += 1
                        elif "-" in adata["data"]["Effect"]:
                            minus_num += 1
                        else:
                            space += 1
                            space_data.append([adata["data"]["source"], adata["data"]["target"], adata["data"]["Effect"]])
                else:
                    continue
    
    # # with open("layer_2.txt", "w") as f:
    # # with open("layer_3.txt", "w") as f:
    # # with open("layer_4.txt", "w") as f:
    # with open("layer_5.txt", "w") as f:
    #     for atarget in target:
    #         print(atarget, file=f)

    print(space_data)
    
    with open("results_1.txt", "a") as f:
        print(layer_file + " + effect " + str(plus_num) + ", - effect " + str(minus_num) + ", " + str(space) + " genes don't have data." , file=f)

if __name__=="__main__":
    main()
