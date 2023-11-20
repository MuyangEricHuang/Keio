#!/usr/bin/env python
# -*- coding: utf-8 -*-

def main():
    product_name_set = set([])
    in_file = "data/raw/network_tf_gene.txt"
    #ECK120015994    AcrR    ECK120002020    acrR    -       [AIBSCS, APIORCISFBSCS, BCE, BPP, GEA]  Strong  
    with open(in_file, "r") as file_handle:
        for row in file_handle:
            row = row.rstrip()
            if row.startswith("#"):
                continue
            col = row.split("\t")
            product_name = col[1]
            product_name_set.add(product_name)

    product_name_list = list(product_name_set)
    product_count_dict = {one: 0 for one in product_name_list}
    in_file = "data/raw/network_tf_tf.txt"
    #AcrR    acrR    -       [AIBSCS, APIORCISFBSCS, BCE, BPP, GEA]  Strong  
    with open(in_file, "r") as file_handle:
        for row in file_handle:
            row = row.strip()
            if row.startswith("#"):
                continue
            col = row.split("\t")
            product_name = col[0]
            if product_name in product_name_set:
                print(row, "IN_SET", sep="\t")
                product_count_dict[product_name]+=1
            else:
                print(row, "NOTIN_SET", sep="\t")
                #print(product_name, product_count_dict[product_name], sep="\t")

    #for product_name in product_name_list:
    #    print(product_name, product_count_dict[product_name], sep="\t")

if __name__=="__main__":
    main()
