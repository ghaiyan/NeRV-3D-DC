import numpy as np
import math
from scipy.spatial.transform import Rotation as R
#执行之前，需要test.sh,用NeRV-3D计算每个TADs结构
def mapStructure(genernalFile,tadDir,mappingFile,bins):
    genernal = np.loadtxt(genernalFile, skiprows=1)
    ratio=math.sqrt(int(bins))
    ratio=int(ratio)
    with open(tadDir+"highres.xyz", "w") as out:
        for i in range(math.ceil(len(genernal) / ratio)):
            file = tadDir+"strtad{}.xyz".format(i)
            tad = np.loadtxt(file, skiprows=1)
            inferredLow = np.zeros((math.ceil(len(tad) / ratio),3))
            for j in range(math.ceil(len(tad) / ratio)):
                inferredLow[j] = np.mean(tad[j*ratio:j*ratio+ratio,])
            trueLow = genernal[i*ratio:i*ratio+ratio,]

            # center
            trueLow = trueLow - np.mean(trueLow, axis=0)
            inferredLow = inferredLow - np.mean(inferredLow, axis=0)

            #rescale
            true_sum = sum([np.sqrt(np.sum(coord**2)) for coord in trueLow])
            inferred_sum = sum([np.sqrt(np.sum(coord**2)) for coord in inferredLow])
            scaling_factor = true_sum / inferred_sum
            inferredLow = inferredLow * scaling_factor

            # rotate
            estimated_rotation, rmsd = R.align_vectors(trueLow,inferredLow)
            a_transformed = estimated_rotation.apply(tad)
            a_transformed = a_transformed - np.mean(a_transformed, axis=0)
            true_sum = np.mean([np.sqrt(np.sum(coord**2)) for coord in trueLow])
            inferred_sum = np.mean([np.sqrt(np.sum(coord**2)) for coord in a_transformed])
            scaling_factor = true_sum / inferred_sum
            a_transformed = a_transformed * scaling_factor
            a_transformed = a_transformed + np.mean(genernal[i*ratio:i*ratio+ratio,], axis=0)
            for j in range(len(a_transformed)):
                out.write("\t".join(str(item) for item in a_transformed[j]) + "\n")
        out.close()
    map = np.loadtxt(mappingFile)
    xyz = np.loadtxt(tadDir+"highres.xyz")

    with open(tadDir+"highresplusnan.xyz", "w") as out:
        for i in range(len(map)):
            if np.isnan(map[i,1]):
                out.write("\t".join(("nan", "nan", "nan")) + "\n")
            else:
                out.write("\t".join(str(item) for item in xyz[int(map[i,1])]) + "\n")