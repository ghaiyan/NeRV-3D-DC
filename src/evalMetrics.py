#calculate the metrics of dRMSE, dPCC and dSCC
import math
import numpy as np
import pandas as pd

def calxyzDist(xyzDir):
    xyz = np.loadtxt(xyzDir)
    d = np.zeros((len(xyz), len(xyz)))
    for i in range(len(xyz)):
        for j in range(len(xyz)):
            if not np.isnan(xyz[i]).any() and not np.isnan(xyz[j]).any():
                d[i,j]=np.sqrt(np.sum((xyz[i] - xyz[j])**2))
    return d

def calcDistance(coord1, coord2):
    """Euclidean distance between coordinates"""
    return ((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2 +  (coord1[2] - coord2[2])**2)**(1./2)

def radius_of_gyration(coords):
    centroid = np.mean(coords, axis=0)
    dist_sum = sum([calcDistance(coord, centroid) for coord in coords])
    return dist_sum/len(coords)

#evaluate the metrics with calculated distance from Hi-C contact matrix
def evalMetrics(distDir,xyzDir,evalfileDir,hicfilename,alpha):
    d=calxyzDist(xyzDir)
    D = np.loadtxt(distDir)
    print(len(D),len(d))
    #dRMSE
    scaling_factor = radius_of_gyration(D)/radius_of_gyration(d)
    drms = 0
    for i in range(len(D)):
        for j in range(len(d)):
            drms = drms + (d[i,j] * scaling_factor-D[i,j])**2
    drms = drms / (len(D)**2)
    drms = math.sqrt(drms)
    drms=np.around(drms,2)
    print("dRMSE:",drms)

    # dPCC
    df = pd.DataFrame({'D':D.reshape(-1),'d':d.reshape(-1)})
    pcc=df.corr()
    pcc=np.array(pcc.iloc[[1],[0]])[0][0]
    pcc=np.around(pcc,3)
    print("dPCC:",pcc)
    
    #dSCC
    scc=df.corr('spearman')
    scc=np.array(scc.iloc[[1],[0]])[0][0]
    scc=np.around(scc,3)
    print("dSCC:",scc)
    with open(evalfileDir,'a+') as f:
            f.write("\t".join((str(hicfilename),str(alpha),str(drms),str(pcc),str(scc)))+'\n')
            f.close()
    return drms,pcc,scc

#evaluate the metrics with true xyz of simulated Hi-C
def evalTrue(truexyzDir,xyzDir,trueevalfileDir,hicfilename,alpha):
    d=calxyzDist(xyzDir)
    D = calxyzDist(truexyzDir)
    print(len(D),len(d))
    #dRMSE
    scaling_factor = radius_of_gyration(D)/radius_of_gyration(d)
    drms = 0
    for i in range(len(D)):
        for j in range(len(d)):
            drms = drms + (d[i,j] * scaling_factor-D[i,j])**2
    drms = drms / (len(D)**2)
    drms = math.sqrt(drms)
    print("dRMSE:",drms)

    # dPCC
    df = pd.DataFrame({'D':D.reshape(-1),'d':d.reshape(-1)})
    pcc=df.corr()
    pcc=np.array(pcc.iloc[[1],[0]])[0][0]
    pcc=np.around(pcc,3)
    print("dPCC:",pcc)
    
    #dSCC
    scc=df.corr('spearman')
    scc=np.array(scc.iloc[[1],[0]])[0][0]
    scc=np.around(scc,3)
    print("dSCC:",scc)

    with open(trueevalfileDir,'a+') as f:
            f.write("\t".join((str(hicfilename),str(alpha),str(drms),str(pcc),str(scc)))+'\n')
            f.close()
    return drms,pcc,scc
"""
true Hi-C data
#'_NeRV_chr19_50000_0.4','NeRV','LargeVis','3DMax','ShNeigh1','GEM','EVR'
#ShNeigh1 and LorDG:维数有问题,1121


for xyzname in ['miniMDS']:
    distDir1="/data1/ghy_data/GM12878/3DResults/NeRV_3D/chr19_50000_0.3.dist"
    distDir2="/data1/ghy_data/GM12878/3DResults/NeRV_3D/chr19_50000_0.4.dist"
    xyzDir="/home/ghaiyan/project/NeRV-3D/GM12878/chr19_50kb/"+xyzname+".xyz"
    evalfileDir="/home/ghaiyan/project/NeRV-3D/GM12878/chr19_50kb/evalueCompare_test.txt"
    hicfilename="/home/ghaiyan/project/NeRV-3D/chrtest/test.hic"
    trueevalfileDir="/home/ghaiyan/project/NeRV-3D/chrtest/evalueComparetrue_test.txt"
    truexyzDir="/home/ghaiyan/project/NeRV-3D/chrtest/test2000.xyz"
    alpha1=0.3
    alpha2=0.4
    evalMetrics(distDir1,xyzDir,evalfileDir,hicfilename,alpha1)
    evalMetrics(distDir2,xyzDir,evalfileDir,hicfilename,alpha2)
"""

"""
simulate Hi-C data evaluate
'_NeRV_test2000_0.9','NeRV','LargeVis','3DMax','ShNeigh1','miniMDS','ShRec3D','EVR','LorDG','GEM'

for xyzname in ['GEM']:
    distDir1="/home/ghaiyan/project/NeRV-3D/chrtest/NeRV_3d_test/test2000_0.3.dist"
    distDir2="/home/ghaiyan/project/NeRV-3D/chrtest/NeRV_3d_test/test2000_0.9.dist"
    xyzDir="/home/ghaiyan/project/NeRV-3D/chrtest/"+xyzname+".xyz"
    evalfileDir="/home/ghaiyan/project/NeRV-3D/chrtest/evalueCompare_test.txt"
    hicfilename="/home/ghaiyan/project/NeRV-3D/chrtest/test.hic"
    trueevalfileDir="/home/ghaiyan/project/NeRV-3D/chrtest/evalueComparetrue_test.txt"
    truexyzDir="/home/ghaiyan/project/NeRV-3D/chrtest/test2000.xyz"
    alpha1=0.3
    alpha2=0.9
    evalMetrics(distDir1,xyzDir,evalfileDir,hicfilename,alpha1)
    evalMetrics(distDir2,xyzDir,evalfileDir,hicfilename,alpha2)
    evalTrue(truexyzDir,xyzDir,trueevalfileDir,hicfilename,alpha1)
"""

"""
true Hi-C data in a high resolution 
"""

distDir1="/data1/ghy_data/IMR90/3DResults/NeRV_3D/chr20_5000_0.3.dist"
xyzDir="/data1/ghy_data/IMR90/3DResults/NeRV-3D-DV/chr20/5000/highresplusnan.xyz"
evalfileDir="/data1/ghy_data/IMR90/3DResults/NeRV-3D-DV/chr20/5000/evalueCompare_test.txt"
hicfilename="/home/ghaiyan/project/NeRV-3D/chrtest/test.hic"
alpha1=0.3
evalMetrics(distDir1,xyzDir,evalfileDir,hicfilename,alpha1)



