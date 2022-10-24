import os
import sys
import argparse
import math
import numpy as np
"""
convert tuple format Hi-C data into n*n matrix
"""

def tuple2matrix(in_dir,out_dir,resolution):
    for index in [22, 21, 19, 17, 16, 15, 14, 10, 9, 6, 5, 4, 3,1]:
        file_name = 'chr{}_kr_{}.hic'.format(index, resolution)
        file = open(os.path.join(in_dir, file_name), 'r')
        _list = file.readlines()

        min_num = max_num = int(int(_list[0].split()[0]) / 1000)
        for i in range(len(_list)):
            line = _list[i].split()
            x = int(int(line[0]) / 1000)
            y = int(int(line[1]) / 1000)
            min_num = min(min_num, x, y)
            max_num = max(max_num, x, y)

        matrix = np.zeros((max_num+1, max_num+1), dtype=np.uint16)

        for i in range(len(_list)):
            line = _list[i].split()
            x = int(int(line[0]) / 1000)
            y = int(int(line[1]) / 1000)
            z = float(line[2])
            z = 0 if math.isnan(z) else min(int(z), 65536)
            matrix[x, y] = matrix[y, x] = z

        prefix = 'chr{}_{}.hic'.format(index, resolution)
        np.savetxt(os.path.join(out_dir, prefix), matrix)

in_dir="/data2/ghy_data/ghy_data/1kb/GM12878/tuple/"
out_dir="/data2/ghy_data/ghy_data/1kb/GM12878/"
resolution=1000
tuple2matrix(in_dir,out_dir,resolution)