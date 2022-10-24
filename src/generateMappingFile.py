import numpy as np
#generate the mapping file of local loci and general locis
import math
def get_tads(id,mappingdir,data,bins):
    """
    id:the number of TADs
    mappingdir：the diretory to save the results
    data：the distance data
    bins:the number of bins you want to divide,for example bins=100
    """

    # 域内的点,每个子域有100个点
    start = id *bins
    end = (id + 1) *bins

    if end > len(data):
        end = len(data)
    # 用于输入的文件
    file =mappingdir+ "tad{}.txt".format(id)
    with open(file, "w") as out:
        out.write(str(end - start) + "\n")
        for i in range(start,end):
            out.write("\t".join(str(item) for item in data[i,start:end]) + "\n")
        out.close()

def generatemapping(mappingdir,distFile,bins):
    """
    mappingdir:the diretory to save the results
    distFile: the distance file of Hi-C data in low-resoliton, such as 25kb
    bins:the number of bins you want to divide,for example bins=100
    """
    #mappingdir="/data1/ghy_data/IMR90/3DResults/NeRV-3D-DV/25000/"
    matrix = np.loadtxt(distFile) #"/IMR90/chr21/chr21_25000.dist"
    j = 0
    data_index=[]
    with open(mappingdir+"mapping.txt", "w") as out:
        for i in range(len(matrix)):
            if not (matrix[i] == 0).all():
                out.write("\t".join((str(i),str(j))) + "\n")
                data_index.append(i)
                j = j + 1
            else:
                out.write("\t".join((str(i),'nan')) + "\n")
    l = len(data_index)
    data = np.zeros((l,l))
    for i in range(l):
        for j in range(l):
            data[i,j] = matrix[data_index[i],data_index[j]]

    np.savetxt(mappingdir+"data.txt",data)
    data = np.loadtxt(mappingdir+"data.txt")

    #generate the global distance file in low reslotion
    ratio=math.sqrt(int(bins))
    ratio=int(ratio)
    overlap=data[::ratio,::ratio]
    file = mappingdir+"genernal.txt" 
    with open(file, "w") as out:
        out.write(str(len(overlap)) + "\n")
        for i in range(len(overlap)):
            out.write("\t".join(str(item) for item in overlap[i]) + "\n")
        out.close()
    #generate the contact files of TADs
    for i in range(math.ceil(len(data)/int(bins))):
        get_tads(i,mappingdir,data,int(bins))