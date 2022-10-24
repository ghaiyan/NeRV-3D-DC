import sys
import numpy as np
from scipy.sparse.csgraph import floyd_warshall
from scipy.sparse import csr_matrix
from decimal import *


class ChromParameters(object):
    """Basic information on chromosome, inferred from input file"""

    def __init__(self, minPos, maxPos, res, name):
        self.minPos = minPos  # minimum genomic coordinate
        self.maxPos = maxPos  # maximum genomic coordinate
        self.res = res  # resolution (bp)
        self.name = name  # e.g. "chr22"

    def getLength(self):
        """Number of possible loci"""
        return int((self.maxPos - self.minPos)/self.res) + 1

    def getAbsoluteIndex(self, genCoord):
        """Converts genomic coordinate into absolute index. Absolute indexing includes empty (zero) points."""
        if genCoord < self.minPos or genCoord > self.maxPos + self.res:
            return None
        else:
            return int((genCoord - self.minPos)/self.res)

    def getGenCoord(self, abs_index):
        """Converts absolute index into genomic coordinate"""
        return self.minPos + self.res * abs_index

    def reduceRes(self, resRatio):
        """Creates low-res version of this chromosome"""
        lowRes = self.res * resRatio
        # approximate at low resolution
        lowMinPos = (self.minPos/lowRes)*lowRes
        lowMaxPos = (self.maxPos/lowRes)*lowRes
        return ChromParameters(lowMinPos, lowMaxPos, lowRes, self.name)

    def get_res_string(self):
        res_kb = int(self.res/1000)
        return str(res_kb) + "kb"


def chromFromBed(path, minPos=None, maxPos=None):
    """Initialize ChromParams from intrachromosomal file in BED format"""
    overall_minPos = sys.float_info.max
    overall_maxPos = 0
    print("Scanning {}".format(path))
    with open(path) as infile:
        for i, line in enumerate(infile):
            line = line.strip().split()
            if minPos is None or maxPos is None:
                pos1 = int(line[1])
                pos2 = int(line[4])
                if minPos is None:
                    curr_minPos = min((pos1, pos2))
                    if curr_minPos < overall_minPos:
                        overall_minPos = curr_minPos
                if maxPos is None:
                    curr_maxPos = max((pos1, pos2))
                    if curr_maxPos > overall_maxPos:
                        overall_maxPos = curr_maxPos
            if i == 0:
                name = line[0]
                res = (int(line[2]) - pos1)
        infile.close()
    minPos = int(np.floor(float(overall_minPos)/res)) * res  # round
    maxPos = int(np.ceil(float(overall_maxPos)/res)) * res
    return ChromParameters(minPos, maxPos, res, name)


def matrixFromBed(chrom, path, parent):
    """Contact Matrix from intrachromosomal BED file."""
    start = chrom.minPos
    end = chrom.maxPos
    length = chrom.getLength()
    matrix = np.zeros((length, length))

    # add loci
    with open(path) as listFile:
        for line in listFile:
            line = line.strip().split()
            pos1 = int(line[1])
            pos2 = int(line[4])
            if pos1 >= start and pos1 <= end and pos2 >= start and pos2 <= end:
                abs_index1 = chrom.getAbsoluteIndex(pos1)
                abs_index2 = chrom.getAbsoluteIndex(pos2)
                matrix[abs_index1][abs_index2] = Decimal(line[6])
                matrix[abs_index2][abs_index1] = Decimal(line[6])
        listFile.close()
    np.savetxt("{}{}_{}.hic".format(parent, chrom.name, chrom.res), matrix)
    return matrix

def matrixFromTuple(chrom, path, parent):
    """Contact Matrix from Tuple format file (n*3)."""
    start = chrom.minPos
    end = chrom.maxPos
    length = chrom.getLength()
    matrix = np.zeros((length, length))

    # add loci
    with open(path) as listFile:
        for line in listFile:
            line = line.strip().split()
            pos1 = int(line[0])
            pos2 = int(line[1])
            if pos1 >= start and pos1 <= end and pos2 >= start and pos2 <= end:
                abs_index1 = chrom.getAbsoluteIndex(pos1)
                abs_index2 = chrom.getAbsoluteIndex(pos2)
                matrix[abs_index1][abs_index2] = Decimal(line[6])
                matrix[abs_index2][abs_index1] = Decimal(line[6])
        listFile.close()
    np.savetxt("{}{}_{}.hic".format(parent, chrom.name, chrom.res), matrix)
    return matrix

def rawmatrix(chrom):
    length = chrom.getLength()
    res_string = chrom.get_res_string()
    name = chrom.name
    rawmatrix = np.zeros((length, length))
    rawpath = "../{}_{}/{}_{}.RAWobserved".format(name, res_string, name, res_string)
    with open(rawpath) as raw:
        for line in raw:
            line = line.split()
            loc1 = int(line[0])
            loc2 = int(line[1])
            rawmatrix[chrom.getAbsoluteIndex(loc1)][chrom.getAbsoluteIndex(loc2)] = float(line[2])
            rawmatrix[chrom.getAbsoluteIndex(loc2)][chrom.getAbsoluteIndex(loc1)] = float(line[2])
    raw.close()
    np.savetxt("{}_{}_raw.hic".format(chrom.name, chrom.res), rawmatrix)

def contactToDist(contactMat, alpha, chrom, path):
    """Convert contact matrix to distance matrix."""
    distMat = np.zeros_like(contactMat)
    numRows = len(contactMat)
    for i in range(numRows):
        for j in range(numRows):
            if contactMat[i,j] != 0 and i != j:
                distMat[i,j] = contactMat[i,j]**(-alpha)
            if distMat[i,j] > 100:
                distMat[i,j] = 0
    newDistMat = csr_matrix(distMat)
    pathMat = floyd_warshall(csgraph=newDistMat, directed=False)
    where_are_inf = np.isinf(pathMat)
    pathMat[where_are_inf] = 0
    np.savetxt("{}{}_{}.dist".format(path, chrom.name, chrom.res), pathMat)
    return pathMat