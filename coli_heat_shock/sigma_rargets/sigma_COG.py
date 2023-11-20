#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last update: 09/02/2021

from collections import defaultdict
from inspect import TPFLAGS_IS_ABSTRACT
import matplotlib.pyplot as plt
from matplotlib.colors import DivergingNorm
import seaborn as sns; sns.set(color_codes=True, style="ticks", font_scale=2.58)
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
    file_list = ["rpoD_cluster_1_tr", "rpoD_cluster_2_tr", "rpoD_cluster_3_tr", "rpoH_cluster_1_tr", "rpoH_cluster_2_tr", "rpoE_cluster_1_tr", "rpoE_cluster_2_tr", "rpoE_cluster_3_tr", "rpoE_cluster_4_tr", "rpoS_cluster_1_tr", "rpoS_cluster_2_tr", "rpoN_cluster_1_tr", "rpoN_cluster_2_tr"]
    input_file1 = "gene_with_cog_sort_k2_uniq.txt"
    cog = []
    with open(input_file1, "r") as file_handle1:
        for a_line in file_handle1:
            a_line = a_line.rstrip()
            # a_cog = a_line.split("\t")
            cog.append(a_line)
    for afile_list in file_list:
        input_file2 = "../{}.txt".format(afile_list)
        group_num = []
        group_num_cog = []
        with open(input_file2, "r") as file_handle2:
            for a_group_num_gene in file_handle2:
                a_group_num_gene = a_group_num_gene.rstrip()
                group_num.append(a_group_num_gene)
            
            for aLine in cog:
                a_COG = aLine.split("\t")
                for a_gene in group_num:
                    if a_gene in a_COG[0]:
                        group_num_cog+=list(a_COG[1].split(";")[-1])
                        # break
            with open("{}_cog.txt".format(afile_list), "w") as f3:
                for a_group_num_cog in group_num_cog:
                    print(a_group_num_cog, file=f3)

if __name__=="__main__":
    main()
