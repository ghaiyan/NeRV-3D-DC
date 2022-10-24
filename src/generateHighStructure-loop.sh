#!/bin/bash
#step1:define the parameters
#Set hic file name and directory
cell="IMR90"
for chromosome in 20 21 22
do
    hicfilename="chr"${chromosome}"_5000"
    hicfileDir='/data1/ghy_data/IMR90/chr'${chromosome}'_5000.hic'

    for alpha in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9
    do
        bins=400
        mkdir -p /data1/ghy_data/${cell}/3DResults/NeRV-3D-DV/chr${chromosome}_5kb/$alpha/${bins}
        mappingdir="/data1/ghy_data/${cell}/3DResults/NeRV-3D-DV/chr${chromosome}_5kb/"${alpha}/
        mappingdir1="/data1/ghy_data/${cell}/3DResults/NeRV-3D-DV/chr${chromosome}_5kb/"${alpha}/${bins}/
        distfile=$mappingdir$hicfilename"_"$alpha".dist"
        #distfile="/data1/ghy_data/IMR90/3DResults/NeRV_3D/chr20_5000_0.3.dist"
        #generate the distance matrix, alpha=0.3 is ok
        generalFile=$mappingdir1"genernal.xyz"
        mappingFile=$mappingdir1"mapping.txt"
        #python -c "import distance; distance.contactToDist('${hicfilename}','${hicfileDir}',${alpha},'${mappingdir}')"

        #generate the mapping File
        python -c "import generateMappingFile;generateMappingFile.generatemapping('${mappingdir1}','${distfile}','${bins}')"


        for a in {0..1000}
        do
        echo $a
        ../NeRV/nerv --inputfile ${mappingdir1}'tad'${a}.txt --outputdim 3 --outputfile ${mappingdir1}'strtad'${a}.xyz
        done
        ../NeRV/nerv --inputfile ${mappingdir1}genernal.txt --outputdim 3 --outputfile ${mappingdir1}genernal.xyz

        #map the structe to be high-reoslution structure 
        python -c "import MappingStructure;MappingStructure.mapStructure('${generalFile}','${mappingdir1}','${mappingFile}','${bins}')"

        rm ${mappingdir1}tad*.txt
        rm ${mappingdir1}genernal.txt
        rm ${mappingdir1}strtad*.xyz
        rm ${mappingdir1}genernal.xyz
    done
done