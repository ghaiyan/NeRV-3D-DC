#!/bin/bash
#step1:define the parameters
#Set hic file name and directory
cell="GM12878"
for chromosome in 22 21 19 17 16 15 14 10 9 6 5 4 3 1
do
    hicfilename="chr"${chromosome}"_1000"
    hicfileDir=/data2/ghy_data/ghy_data/1kb/GM12878/chr${chromosome}_1000.hic
    for alpha in 0.4
    do
        bins=900
        mkdir -p /data2/ghy_data/ghy_data/1kb/${cell}/NeRV-3D-DC/chr${chromosome}/$alpha/${bins}
        mappingdir1=/data2/ghy_data/ghy_data/1kb/${cell}/NeRV-3D-DC/chr${chromosome}/$alpha/${bins}/
        distfile=$mappingdir1$hicfilename"_"$alpha".dist"
        #distfile="/data1/ghy_data/IMR90/3DResults/NeRV_3D/chr20_5000_0.3.dist"
        #generate the distance matrix, alpha=0.3 is ok
        generalFile=$mappingdir1"genernal.xyz"
        mappingFile=$mappingdir1"mapping.txt"
        python -c "import distance; distance.contactToDist('${hicfilename}','${hicfileDir}',${alpha},'${mappingdir1}')"

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
        nervOuput=${mappingdir1}highresplusnan.xyz
        evalfileDir=${mappingdir1}${cell}_chr${chromosome}_evalMterics.txt
        python -c "import evalMetrics;evalMetrics.evalMetrics('${distfile}','${nervOuput}','${evalfileDir}','${hicfilename}','${alpha}') "
    done
done