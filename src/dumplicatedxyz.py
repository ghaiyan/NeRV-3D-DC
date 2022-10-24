import numpy as np
import pandas as pd

def replacenan(xyzFile):
    xyz = pd.read_csv(xyzFile,engine='python',header=None)
    result=xyz.duplicated()
    if len(xyz[result])!=0:
        rep=xyz[result]
        repvalue1=rep.iloc[[0],[0]]
        print(repvalue1)
        nprepvalue1=np.array(repvalue1)
        print('nprepvalue1[0]',nprepvalue1[0])
        xyz[xyz==nprepvalue1[0]]='nan nan nan'
        np.savetxt(xyzFile,xyz,fmt = '%s')
    return xyz