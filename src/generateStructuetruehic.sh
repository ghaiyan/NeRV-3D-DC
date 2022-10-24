#!/bin/bash
cd /home/ghaiyan/project/3d/src/
echo `pwd`
#Set hic file name and directory
hicfilename="chr20_5000"
#set the metrics file name compared with the distance matrix
metricsFileName1="chr20_5000_evalMterics"
hicfileDir="/data1/ghy_data/IMR90/chr20_5000.hic"
#alpha=0.3
distfileDir="/data1/ghy_data/IMR90/3DResults/NeRV_3D"

for alpha in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0 1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 2.0
do
    distfile=$distfileDir"/"$hicfilename"_"$alpha".dist"
    evalfileDir=$distfileDir"/"$hicfilename"_evalMterics.txt"
    
    nervinput=$distfileDir"/_NeRV_$hicfilename"'_'"$alpha.dist"
    nervOuput=$distfileDir"/_NeRV_$hicfilename"'_'"$alpha.xyz"

    python -c "import distance; distance.contactToDist('${hicfilename}','${hicfileDir}',${alpha},'${distfileDir}')"
    ../NeRV/nerv --inputfile $nervinput --outputdim 3 --outputfile $nervOuput
    python -c "import NervOutput; NervOutput.del_firstline('${nervOuput}')"
    python -c "import dumplicatedxyz;dumplicatedxyz.replacenan('${nervOuput}')"
    python -c "import evalMetrics;evalMetrics.evalMetrics('${distfile}','${nervOuput}','${evalfileDir}','${hicfilename}','${alpha}') "
done
#plot the metrics
python -c "import plotmetrics; plotmetrics.plotmetric(distfileDir,metricsFileName1)"