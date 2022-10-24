import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['pdf.fonttype']=42
mpl.rcParams['ps.fonttype']=42
import numpy as np

def plotmetric(metricsdir,metricsFileName):
    #metricsdir="/data1/ghy_data/GM12878/3DResults/NeRV_3D/chr19_50000_evalMterics.txt"
    #metricsFileName='chr19_50000_evalMterics'
    x=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8]
    rmse=np.loadtxt(metricsdir+'/'+metricsFileName+'.txt',usecols=(2,))
    pcc=np.loadtxt(metricsdir+'/'+metricsFileName+'.txt',usecols=(3,))
    scc=np.loadtxt(metricsdir+'/'+metricsFileName+'.txt',usecols=(4,))
    print(scc)
    x=np.arange(0.1,0.9,0.1)
    #plt.axes(yscale = "log")
    l1=plt.plot(x,rmse,'r--',label='RMSE')
    l2=plt.plot(x,pcc,'g--',label='PCC')
    l3=plt.plot(x,scc,'b--',label='SCC')
    

    plt.plot(x,rmse,'ro-',x,pcc,'g+-',x,scc,'b^-')

    plt.ylabel('metric value')
    plt.xlabel('alpha value')
    plt.legend()
    plt.savefig(metricsdir+'/'+metricsFileName+'_plot.pdf', format='pdf', bbox_inches='tight')
    plt.show()

metricsdir='/data1/ghy_data/IMR90/3DResults/NeRV-3D-DV/chr22_5kb'
metricsFileName='chr22_5000_400_evalMterics'
plotmetric(metricsdir,metricsFileName)
