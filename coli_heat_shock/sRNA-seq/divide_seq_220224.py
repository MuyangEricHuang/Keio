#!/usr/bin/env python                                                                                                                             
# -*- coding: utf-8 -*-
# Last update: 02/24/2022

import sys

def main():
    divide_num = int(sys.argv[1]) #30
    in_file = str(sys.argv[2]) #data/fwdrev_220224/Ec_sRNA_H1_fwd.coverage.bg
    with open(in_file, "r") as file_handle:
        #Chromosome      0       152     0
        #Chromosome      152     193     8
        current_range = 0
        current_height = 0
        for row in file_handle:
            row = row.rstrip()
            col =row.split("\t")
            start = int(col[0])
            end = int(col[1])
            height = int(float(col[2]))
            if (divide_num*2 - current_range) < (end - start):
                current_height += height * (divide_num*2 - current_range)
                current_range = (end - start) - (divide_num*2 - current_range)
            else:
                current_height += height * (end - start)
                current_range += end - start

            while divide_num*2 < current_range:
                if (divide_num*2 - current_range) < (end - start):
                    current_height += height * (divide_num*2 - current_range)
                    current_range = (end - start) - (divide_num*2 - current_range)
                else:
                    current_height += height * (end - start)
                    current_range += end - start

    out_file = ".txt"
    with open(out_file, "w") as file_handle:
        for one in print_list:
            print(one, file=file_handle)

if __name__=="__main__":
    main()
