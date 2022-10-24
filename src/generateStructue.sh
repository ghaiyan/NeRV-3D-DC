#!/bin/bash
cd /home/ghaiyan/project/3d/src/
echo `pwd`
#Set hic file name and directory
hicfilename="test2000"
#set the metrics file name compared with the distance matrix
metricsFileName1="test2000_evalMterics"
#set the metrics file name compareed with the true xyz file from simulated Hi-C
metricsFileName2="test2000_evaltrueMterics"
hicfileDir="/home/ghaiyan/project/3d/chrtest/test.hic"
#alpha=0.3
distfileDir="/home/ghaiyan/project/3d/chrtest/NeRV_3d_test"
truexyzDir="/home/ghaiyan/project/3d/chrtest/test2000.xyz"
for alpha in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0 1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 2.0
do
    distfile=$distfileDir"/"$hicfilename"_"$alpha".dist"
    evalfileDir=$distfileDir"/"$hicfilename"_evalMterics.txt"
    trueevalfileDir=$distfileDir"/"$hicfilename"_evaltrueMterics.txt"
    nervinput=$distfileDir"/_NeRV_$hicfilename"'_'"$alpha.dist"
    nervOuput=$distfileDir"/_NeRV_$hicfilename"'_'"$alpha.xyz"
    #calculate the distance
    python -c "import distance; distance.contactToDist('${hicfilename}','${hicfileDir}',${alpha},'${distfileDir}')"
    #calculate the 3d structure
    ../NeRV/nerv --inputfile $nervinput --outputdim 3 --outputfile $nervOuput
    #calculate the output structure
    python -c "import NervOutput; NervOutput.del_firstline('${nervOuput}')"
    python -c "import dumplicatedxyz;dumplicatedxyz.replacenan('${nervOuput}')"
    #calculate the metrics
    python -c "import evalMetrics;evalMetrics.evalMetrics('${distfile}','${nervOuput}','${evalfileDir}','${hicfilename}','${alpha}') "
    python -c "import evalMetrics;evalMetrics.evalTrue('${truexyzDir}','${nervOuput}','${trueevalfileDir}','${hicfilename}','${alpha}') "
done
#plot the metrics
python -c "import plotmetrics; plotmetrics.plotmetric(distfileDir,metricsFileName1)"
python -c "import plotmetrics; plotmetrics.plotmetric(distfileDir,metricsFileName2)"