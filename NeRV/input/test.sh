#!/bin/bash
for a in {0..100}
do
    ../nerv --inputfile tad$a.txt --outputdim 3 --outputfile strtad$a.xyz
done
../nerv --inputfile genernal.txt --outputdim 3 --outputfile genernal.xyz
mv strtad*.xyz ../../biye/IMR90/chr22_5kb/structure
mv genernal.xyz ../../biye/IMR90/chr22_5kb/structure
rm tad*.txt
rm genernal.txt