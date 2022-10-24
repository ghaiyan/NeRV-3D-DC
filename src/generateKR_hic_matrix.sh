#!/bin/bash
juicer='/data2/ghy_data/ghy_data/juicer'
cellline='GM12878'
rawdatapath=/data1/lmh_data/MINE/source/${cellline}
norm_kr_contact=/data2/ghy_data/ghy_data/1kb/GM12878
for j in {1..22}
do
#java -jar $juicer/juicer_tools_1.22.01.jar  dump observed KR $rawdatapath/4DNFI1UEG1HD.hic  ${j} ${j}   BP 1000 ${norm_kr_contact}/chr${j}_kr_1000.hic
#java -jar /home/software/juicer/CPU/juicer_tools.jar  eigenvector -p KR inter_30.hic ${j} BP 100000 ${1}_chr${j}_pc1_100k.txt
#java -jar /home/software/juicer/CPU/juicer_tools.jar  dump observed NONE inter_30.hic  ${j} ${j}   BP 50000 ${1}_chr${j}_raw_50k.txt
done