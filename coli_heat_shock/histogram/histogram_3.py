#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last update: 09/03/2021

# %matplotlib inline
import matplotlib as mpl
mpl.use('Agg')

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

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

input_file2 = "transcriptome_expression_-f2changed.txt"
RNA_data = []
with open(input_file2, "r") as file_handle2:
    for row_num2, row2 in enumerate(file_handle2):
        row2 = row2.rstrip()
        col2 = row2.split("\t")
        if row_num2 == 0:
            continue
        else:
            tra_uniprot_ac = col2[0].split("_")[-1].split("-")[0]
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

a_list = []
non_list = []
a = open("upstream_table.txt", "r")
for aline in a:
    aline = aline.rstrip()
    al = aline.split("\t")
    if al[0] in protein_data and al[0] in RNA_data:
        a_list.append(float(al[1]))
    else:
        non_list.append(float(al[1]))

print(len(aline))
print(len(a_list))
print(len(non_list))

labels = ['Measured', 'DB']
plt.hist([a_list, non_list], bins=18, range=(0.00, 18.00), align="mid", histtype="barstacked", stacked=True, color=['black', 'gray'], label=labels)
plt.legend()
plt.title("Number of Upstream Gene")
plt.xlabel("Upstream Gene Number")
plt.ylabel("Downstream Gene Number")
plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18])
plt.yticks([0, 100, 200, 300, 400, 500, 600, 700])
plt.savefig("histogram.pdf")
plt.figure()
a_list = []
a.close()
