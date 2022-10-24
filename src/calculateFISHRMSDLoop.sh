#!/bin/bash
#step1:define the parameters
#Set hic file name and directory
mappingFile="/home/ghaiyan/project/NeRV-3D/IMR90/mapping.xls"
res=5000
for chromosome in 20 21 22
do
    chrname="IMR90"
    sheet_name=chr${chromosome}
    FishFile=/home/ghaiyan/project/NeRV-3D/IMR90/chr${chromosome}.xls
    for alpha in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8
    do
    mappingdir=/data1/ghy_data/IMR90/3DResults/NeRV-3D-DV/chr${chromosome}_5kb/${alpha}/400/
    #distfile="/data1/ghy_data/IMR90/3DResults/NeRV_3D/chr20_5000_0.3.dist"
    #generate the distance matrix, alpha=0.3 is ok
    evalFile=${mappingdir}chr${chromosome}_${alpha}_400_Fish_eval.txt
    xyzFile=${mappingdir}${chrname}-chr${chromosome}-5kb-${alpha}-400.xyz

    python -c "import calculateFISHRMSD;calculateFISHRMSD.calcluteFISHRMSDeval('${mappingFile}','${sheet_name}','${FishFile}','${xyzFile}','${evalFile}','${res}') "
    done
done