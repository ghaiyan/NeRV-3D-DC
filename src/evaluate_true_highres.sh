#!/bin/bash
#step1:define the parameters
#Set hic file name and directory
for chromosome in 20 21 22
do
    hicfilename="chr"${chromosome}"_5000"
    chrname="IMR90"
    for alpha in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8
    do
        mappingdir=/data1/ghy_data/IMR90/3DResults/NeRV-3D-DV/chr${chromosome}_5kb/${alpha}/400/
        mappingdir1=/data1/ghy_data/IMR90/3DResults/NeRV-3D-DV/chr${chromosome}_5kb/${alpha}/
        distfile=${mappingdir1}$hicfilename"_"$alpha".dist"
        #distfile="/data1/ghy_data/IMR90/3DResults/NeRV_3D/chr20_5000_0.3.dist"
        #generate the distance matrix, alpha=0.3 is ok
        nervOuput=$mappingdir${chrname}-chr${chromosome}-5kb-${alpha}-400.xyz
        evalfileDir=/data1/ghy_data/${chrname}/3DResults/NeRV-3D-DV/chr${chromosome}_5kb"/"$hicfilename"_400_evalMterics.txt"
        python -c "import evalMetrics;evalMetrics.evalMetrics('${distfile}','${nervOuput}','${evalfileDir}','${hicfilename}','${alpha}') "
    done
done

