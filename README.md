# NeRV-3D-DC
NeRV-3D-DC: A Nonlinear Dimensionality Reduction visualization method for 3D Chromosome Structure Reconstruction with high Resolution Hi-C Data
# python environment
python 3.8.10
numpy
pandas
matplotlib
xlrd
openpyxl

## Data used in the experiment
../chrtest:simulation data and results

../GM12878:results of 50kb and 5kb resolution in real Hi-C data

../IMR90:results of 50kb and 5kb resolution in real Hi-C data
## generate simulation strcture
run 'generate_test_structer.ipynb'

## generate Hi-C contact matrix
run functions of "normalize.py"

or 

bash generateKR_hic_matrix.sh

then

python tuple2matrix(in_dir,out_dir,resolution)
## reconstrcute the simulation structure
change the directory of the input Hi-C contact file and output file, and the conversion factor alpha.

bash generateStructue.sh

## reconstrcute the 3D structure from true Hi-C contact matrix (low resolution Hi-C)

change the directory of the input Hi-C contact file and output file, and the conversion factor alpha.

bash generateStructuetruehic.sh

## reconstrcute the 3D structure from true Hi-C contact matrix （high resolution Hi-C data)
bash generateHighStructure.sh

## plot the strcuture you have generated
run 'plot3D.ipynb'

## evalute the quality of the 3D structure generated by different methods
python evalMetrics.py

before running, please modify the dirctores of your structure files.

## plot the comparsion of metrics
python plotmetrics.py

or

run 'plotmetric.ipynb' 

## evaluate the 3D strcuture with avaliable FISH data
run calculateFISHRMSDLoop.sh

Or run evaluate_with_FISH.ipynb







