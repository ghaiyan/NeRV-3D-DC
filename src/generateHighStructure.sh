#!/bin/bash
#step1:define the parameters
#Set hic file name and directory
for chr in 19 21
do
    hicfilename="chr"${chr}"_5000"
    hicfileDir="/data1/ghy_data/GM12878/chr"${chr}"_5000.hic"
    alpha=0.3
    mappingdir="/data1/ghy_data/GM12878/3DResults/NeRV-3D-DV/chr"${chr}"_5kb/${bins}/"
    distfile=$mappingdir$hicfilename"_"$alpha".dist"
    bins=400
    #distfile="/data1/ghy_data/IMR90/3DResults/NeRV_3D/chr20_5000_0.3.dist"
    #generate the distance matrix, alpha=0.3 is ok
    mkdir -p /data1/ghy_data/GM12878/3DResults/NeRV-3D-DV/chr"${chr}"_5kb/${bins}
    #python -c "import distance; distance.contactToDist('${hicfilename}','${hicfileDir}',${alpha},'${mappingdir}')"
    generalFile=$mappingdir"genernal.xyz"
    mappingFile=$mappingdir"mapping.txt"
    #generate the mapping File
    #python -c "import generateMappingFile;generateMappingFile.generatemapping('${mappingdir}','${distfile}','${bins}')"


    #for a in {0..1000}
   # do
   #     echo $a
   #     ../NeRV/nerv --inputfile ${mappingdir}'tad'${a}.txt --outputdim 3 --outputfile ${mappingdir}'strtad'${a}.xyz
   # done
   #     ../NeRV/nerv --inputfile ${mappingdir}genernal.txt --outputdim 3 --outputfile ${mappingdir}genernal.xyz

    #map the structe to be high-reoslution structure 
    python -c "import MappingStructure;MappingStructure.mapStructure('${generalFile}','${mappingdir}','${mappingFile}','${bins}')"

    #rm ${mappingdir}tad*.txt
    #rm ${mappingdir}genernal.txt
    #rm ${mappingdir}strtad*.xyz
    #rm ${mappingdir}genernal.xyz
done