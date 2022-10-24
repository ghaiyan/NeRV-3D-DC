#!/bin/bash
#step1:define the parameters
#Set hic file name and directory
for chromosome in 21
do
    hicfilename="chr"${chromosome}"_5000"
    chrname="IMR90"
    for alpha in 0.3 0.4 0.5
        do
        mappingdir=/data1/ghy_data/IMR90/3DResults/NeRV-3D-DV/chr${chromosome}_5kb/${alpha}/
        distfile=$mappingdir$hicfilename"_"$alpha".dist"
        #distfile="/data1/ghy_data/IMR90/3DResults/NeRV_3D/chr20_5000_0.3.dist"
        #generate the distance matrix, alpha=0.3 is ok
        for method in NeRV-TAD.xyz miniMDS.xyz Hierarchical.xyz 
        do
            methods=/home/ghaiyan/project/NeRV-3D/IMR90/chr${chromosome}_5kb/${method}
            evalfileDir=/data1/ghy_data/${chrname}/3DResults/NeRV-3D-DV/chr${chromosome}_5kb"/"$hicfilename"_evalMterics_methods.txt"
            python -c "import evalMetrics;evalMetrics.evalMetrics('${distfile}','${methods}','${evalfileDir}','${hicfilename}','${alpha}') "
        done
    done
done