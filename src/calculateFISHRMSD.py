import pandas as pd
import numpy as np
from scipy.spatial.transform import Rotation as R
def calcluteFISHRMSDeval(mappingFile,sheet_name,FishFile,xyzFile,evalFile,res):
    """
    dir="/home/ghaiyan/project/NeRV-3D/IMR90/"
    mapping = pd.read_excel(dir+"mapping.xls", sheet_name='Chr22')
    fish = pd.read_excel(dir+"chr22.xls")
    xyz = np.loadtxt(dir+"chr22_5kb/NeRV-TAD.xyz")
    evalFishDir="/home/ghaiyan/project/NeRV-3D/IMR90/Chr22_Fish_eval.txt"
    res = 5000
    """
    mapping=pd.read_excel(mappingFile,sheet_name=sheet_name)
    fish = pd.read_excel(FishFile)
    xyz = np.loadtxt(xyzFile)
    num = len(mapping)
    rep = int(len(fish) / len(mapping))
    res=int(res)

    # 计算模型的对应位置值
    model = np.zeros((num,3))
    for i in range(num):
        start = int(mapping.loc[i,"Start genomic coordinate"] / res)
        end =  int(mapping.loc[i,"End genomic coordinate",] / res)
        model[i] = pd.DataFrame(xyz[start:end,]).mean(axis=0)

    # fish的真实数据多次测量的每次误差
    for i in range(rep):
        serial = i + 1
        data = fish.loc[fish['Serial # of the imaged chromosome'] == serial,["x(um)","y(um)","z(um)"]]
        data = np.array(data)

        # 删除模型或FISH中没有的点们
        data_new = []
        model_new = []
        for i in range(num):
            if not (np.isnan(model[i,0]) or np.isnan(data[i,0])):
                data_new.append(data[i])
                model_new.append(model[i])

        # center
        data_new = data_new - np.mean(data_new, axis=0)
        model_new = model_new - np.mean(model_new, axis=0)

        # rescale
        data_sum = sum([np.sqrt(np.sum(coord**2)) for coord in data_new])
        model_sum = sum([np.sqrt(np.sum(coord**2)) for coord in model_new])
        scaling_factor = data_sum / model_sum
        model_new = np.array(model_new) * scaling_factor

        # rotate
        estimated_rotation, rmsd = R.align_vectors(data_new,model_new)
        print (rmsd)
        with open(evalFile,'a+') as f:
                f.write(str(rmsd)+'\n')
                f.close()