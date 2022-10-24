#!/usr/bin/python
import numpy as np
import numpy as np
import heapq
import argparse
import math
from scipy.sparse.csgraph import floyd_warshall
from scipy.sparse import csr_matrix
import sys
def contactToDist(hicfilename,hicfiledir,alpha,distfileDir):
    """Convert contact matrix to distance matrix."""
    contactMat=np.loadtxt(hicfiledir)
    distMat = np.zeros_like(contactMat)#same demension matrix with zero
    numRows = len(contactMat) #aquire the length of matrix
    for i in range(numRows):#calculate the distance matrix
        for j in range(numRows):
            if contactMat[i,j] != 0 and i != j:
                distMat[i,j] = contactMat[i,j]**(-alpha)#alpha transformer
            if distMat[i,j] > 100:#why 100?
                distMat[i,j] = 0
    newDistMat = csr_matrix(distMat)
    pathMat = floyd_warshall(csgraph=newDistMat, directed=False) #calculate the shortest path of undirected graph
    where_are_inf = np.isinf(pathMat)#identify whether there are infs ,then set to be zero
    pathMat[where_are_inf] = 0
    np.savetxt(distfileDir+"/{}_{}.dist".format(hicfilename,alpha),pathMat)
    np.savetxt(distfileDir+"/_NeRV_{}_{}.dist".format(hicfilename,alpha),pathMat)
    with open(distfileDir+"/_NeRV_{}_{}.dist".format(hicfilename,alpha),'r+') as f:
        content=f.read()
        f.seek(0,0)
        f.write(str(numRows)+'\n'+content)
        f.close()
    return pathMat

if __name__ == "__main__":
    contactToDist()
