import numpy as np
import re
np.set_printoptions(suppress=True)

np.set_printoptions(precision=3) #设精度为3
test=np.loadtxt("test.hic")
test1=np.array(test)
print(test1.shape)
np.savetxt("test.hic",test1,fmt='%.03f')