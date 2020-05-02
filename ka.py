import numpy as np
from numpy.random import default_rng

rng = default_rng()
tmp = rng.choice(356, size=356, replace=False)
arr=np.genfromtxt("C:\dataset\\n2vf.csv",delimiter=",")
arr1=arr[tmp,:]
lable=arr1[:,32]
train_lable=lable[:300]
test_lable=lable[300:]
np.savetxt("train_lable.csv",train_lable,delimiter=",",fmt='%.2f')
np.savetxt("test_lable.csv",test_lable,delimiter=",",fmt='%.2f')
train_data=arr1[:300,:32]
test_data=arr1[300:,:32]
np.savetxt("total.csv",arr1,delimiter=",",fmt='%.2f')
np.savetxt("train_data.csv",train_data,delimiter=",",fmt='%.2f')
np.savetxt("test_data.csv",test_data,delimiter=",",fmt='%.2f')

