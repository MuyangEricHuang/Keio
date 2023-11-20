#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last update: 09/01/2021

# %matplotlib inline
import matplotlib as mpl
mpl.use('Agg')

import numpy as np
import matplotlib.pyplot as plt

a_list = []

a = open("histogram.txt", "r")
for aline in a:
    al = aline.split("\t")
    a_list.append(float(al[1]))
plt.hist(a_list, bins=340, range=(0.00, 1700.00))
plt.title("Number of Targets")
plt.xlabel("Targets Gene Number")
plt.ylabel("TFs Gene Number (171 in Total)")
plt.xticks([10, 250, 500, 750, 1000, 1250, 1500, 1750])
plt.yticks([0, 10, 20, 30, 40, 50, 60])
plt.savefig("histogram.pdf")
plt.figure()
a_list = []
a.close()
