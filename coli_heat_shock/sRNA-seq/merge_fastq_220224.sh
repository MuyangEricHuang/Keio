#!/usr/bin/bash
# Last update: 02/24/2022
set -eu pipefail

out_dir="data/fastp_220224"
less Sequence/sRNA_H1/sRNA_H1_FRRN202412344-1a_HV72GDRXX_L1_2.fq.gz Sequence/sRNA_H1/sRNA_H1_FRRN202412344-1a_HVMVTDRXX_L1_2.fq.gz > ${out_dir}/Ec_sRNA_H1_2.fq
less Sequence/sRNA_H1/sRNA_H1_FRRN202412344-1a_HV72GDRXX_L1_1.fq.gz Sequence/sRNA_H1/sRNA_H1_FRRN202412344-1a_HVMVTDRXX_L1_1.fq.gz > ${out_dir}/Ec_sRNA_H1_1.fq
less Sequence/sRNA_H2/sRNA_H2_FRRN202412345-1a_HV72GDRXX_L1_2.fq.gz Sequence/sRNA_H2/sRNA_H2_FRRN202412345-1a_HVMVTDRXX_L2_2.fq.gz > ${out_dir}/Ec_sRNA_H2_2.fq
less Sequence/sRNA_H2/sRNA_H2_FRRN202412345-1a_HV72GDRXX_L1_1.fq.gz Sequence/sRNA_H2/sRNA_H2_FRRN202412345-1a_HVMVTDRXX_L2_1.fq.gz > ${out_dir}/Ec_sRNA_H2_1.fq
less Sequence/sRNA_H3/sRNA_H3_FRRN202412346-1a_HM7VMDRXX_L2_2.fq.gz > ${out_dir}/Ec_sRNA_H3_2.fq
less Sequence/sRNA_H3/sRNA_H3_FRRN202412346-1a_HM7VMDRXX_L2_1.fq.gz > ${out_dir}/Ec_sRNA_H3_1.fq
less Sequence/sRNA_H4/sRNA_H4_FRRN202412347-1a_HV72GDRXX_L1_2.fq.gz Sequence/sRNA_H4/sRNA_H4_FRRN202412347-1a_HVMVTDRXX_L2_2.fq.gz > ${out_dir}/Ec_sRNA_H4_2.fq
less Sequence/sRNA_H4/sRNA_H4_FRRN202412347-1a_HV72GDRXX_L1_1.fq.gz Sequence/sRNA_H4/sRNA_H4_FRRN202412347-1a_HVMVTDRXX_L2_1.fq.gz > ${out_dir}/Ec_sRNA_H4_1.fq
less Sequence/sRNA_H5/sRNA_H5_FRRN202412348-1a_HV72GDRXX_L1_2.fq.gz Sequence/sRNA_H5/sRNA_H5_FRRN202412348-1a_HVMVTDRXX_L2_2.fq.gz > ${out_dir}/Ec_sRNA_H5_2.fq
less Sequence/sRNA_H5/sRNA_H5_FRRN202412348-1a_HV72GDRXX_L1_1.fq.gz Sequence/sRNA_H5/sRNA_H5_FRRN202412348-1a_HVMVTDRXX_L2_1.fq.gz > ${out_dir}/Ec_sRNA_H5_1.fq
less Sequence/sRNA_H6/sRNA_H6_FRRN202412349-1a_HV72GDRXX_L1_2.fq.gz Sequence/sRNA_H6/sRNA_H6_FRRN202412349-1a_HVMVTDRXX_L2_2.fq.gz > ${out_dir}/Ec_sRNA_H6_2.fq
less Sequence/sRNA_H6/sRNA_H6_FRRN202412349-1a_HV72GDRXX_L1_1.fq.gz Sequence/sRNA_H6/sRNA_H6_FRRN202412349-1a_HVMVTDRXX_L2_1.fq.gz > ${out_dir}/Ec_sRNA_H6_1.fq
less Sequence/sRNA_H7/sRNA_H7_FRRN202412350-1a_HV72GDRXX_L1_2.fq.gz Sequence/sRNA_H7/sRNA_H7_FRRN202412350-1a_HVMVTDRXX_L1_2.fq.gz > ${out_dir}/Ec_sRNA_H7_2.fq
less Sequence/sRNA_H7/sRNA_H7_FRRN202412350-1a_HV72GDRXX_L1_1.fq.gz Sequence/sRNA_H7/sRNA_H7_FRRN202412350-1a_HVMVTDRXX_L1_1.fq.gz > ${out_dir}/Ec_sRNA_H7_1.fq
