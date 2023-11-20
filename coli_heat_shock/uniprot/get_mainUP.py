#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last update: 03/07/2022
import glob

def main():
    load_other_data = []
    input_file1 = "duplicate_su.txt"
    with open(input_file1, "r") as file_handle1:
        for row1 in file_handle1:
            row1 = row1.rstrip()
            load_other_data.append(row1)
   
    # print(len(load_other_data))
    # print(load_other_data[:5])
    load_main_UPID = []
    input_file2 = "all_gene_name_data_edit_fin_new.txt"
    with open(input_file2, "r") as file_handle2:
        for row2 in file_handle2:
            row2 = row2.rstrip()
            col2 = row2.split("\t")
            for a_col2 in col2:
                if a_col2 in load_other_data:
                    # print("A")
                    for a_other_data in load_other_data:
                        if a_col2 == a_other_data:
                            # print("B")
                            load_main_UPID.append([col2[2], a_col2])
                            break
                        # elif a_other_data == load_other_data[-1]:
                        #     print(a_col2)
    
    # print(load_main_UPID)

    with open("mainUP_left_duplicate_right.txt", "w") as f:
        for aline in load_main_UPID:
            print("\t".join(map(str, aline)), file=f)
            # print("\t".join(set(str, load_main_UPID)), file=f)

if __name__=="__main__":
    main()
