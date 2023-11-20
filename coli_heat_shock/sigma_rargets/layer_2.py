#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last update: 08/27/2021

from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import DivergingNorm
import pandas as pd
import seaborn as sns; sns.set(color_codes=True, style="ticks", font_scale=.8)
import scipy.stats as sp
import json

def main():
    protein_data = []
    measured_data = []
    input_file1 = "proteome_expression_median.txt"
    input_file2 = "transcriptome_expression_-f2changed.txt"
    with open(input_file1, "r") as file_handle1:
        for row_num1, row1 in enumerate(file_handle1):
            row1 = row1.rstrip()
            col1 = row1.split("\t")
            if row_num1 == 0:
                continue
            else:
                protein_data.append(col1[3].split("#")[1])
    with open(input_file2, "r") as file_handle2:
        for row_num2, row2 in enumerate(file_handle2):
            row2 = row2.rstrip()
            col2 = row2.split("\t")
            if row_num2 == 0:
                continue
            else:
                if col2[0].split("_")[-1].split("-")[0] not in protein_data:
                    measured_data.append(col2[0].split("_")[-1].split("-")[0])

    TRGs = []
    with open("transcription_related_proteins.txt", "r") as file_handle3:
        for aTRG in file_handle3:
            aTRG = aTRG.rstrip()
            TRGs.append(aTRG)
    
    layer = ["layer_2.txt", "layer_3.txt", "layer_4.txt"]
    for list_num in range(0, 3):
        layer_data = []
        measured_data_num = 0
        TRG_num = 0
        with open("{}".format(layer[list_num]), "r") as f1:
            for layer_x in f1:
                layer_x = layer_x.rstrip()
                layer_data.append(layer_x)
            for alayer_data in layer_data:
                if alayer_data in measured_data:
                    measured_data_num += 1
                if alayer_data in TRGs:
                    TRG_num += 1
        with open("results_2.txt", "a") as f:
            print("{}".format(layer[list_num]) + " measured data is " + str(measured_data_num) + ", TRGs number is " + str(TRG_num), file=f)

if __name__=="__main__":
    main()
