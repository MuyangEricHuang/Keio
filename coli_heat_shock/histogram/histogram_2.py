#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last update: 04/15/2021

# %matplotlib inline
import matplotlib as mpl
mpl.use('Agg')

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

a_list = []

a = open("upstream_tabel_sort_uniq.txt", "r")
for aline in a:
    aline = aline.rstrip()
    al = aline.split("\t")
    a_list.append(float(al[1]))
    # a_list.append(float(al[2]))

plt.hist(a_list, bins=18, range=(0.00, 18.00))
# plt.hist(a_list, bins=np.logspace(0, 4, 50), range=(0.00, 1700.00))
# plt.xlim(0, 2000)

plt.title("Number of Upstream Gene (DB)")
# plt.title("Number of Upstream Gene (Measured)")
plt.xlabel("Upstream Gene Number")
plt.ylabel("Downstream Gene Number")
plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18])
plt.yticks([0, 100, 200, 300, 400, 500, 600, 700])
plt.savefig("histogram.pdf")
plt.figure()
a_list = []
a.close()
