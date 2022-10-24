#!/bin/bash
#step1:define the parameters
#Set hic file name and directory
for chromosome in 20 21 22
do
    hicfilename="chr"${chromosome}"_5000"
    hicfileDir='/data1/ghy_data/IMR90/chr'${chromosome}'_5000.hic'

    for alpha in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9
    do
        mkdir -p /data1/ghy_data/IMR90/3DResults/NeRV-3D-DV/chr${chromosome}_5kb/$alpha
        mappingdir="/data1/ghy_data/IMR90/3DResults/NeRV-3D-DV/chr${chromosome}_5kb/"${alpha}/
        distfile=$mappingdir$hicfilename"_"$alpha".dist"
        #distfile="/data1/ghy_data/IMR90/3DResults/NeRV_3D/chr20_5000_0.3.dist"
        #generate the distance matrix, alpha=0.3 is ok
    rm /data1/ghy_data/IMR90/3DResults/NeRV-3D-DV/chr${chromosome}_5kb/${alpha}/_NeRV_${hicfilename}_${alpha}.dist
    done
done