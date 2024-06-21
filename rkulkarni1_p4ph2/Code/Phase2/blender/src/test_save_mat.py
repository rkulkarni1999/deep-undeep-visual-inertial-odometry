import numpy as np
import scipy.io
scipy.io.savemat

yaw = np.array([1.2,3.4,2.4])

dict = {'yaw': yaw}
scipy.io.savemat("testout.mat", dict)


from scipy.io import loadmat
arr = np.genfromtxt('./helper/MP.csv', delimiter=',', skip_header=0)


print(arr.shape)
print(arr[8][1])
print((arr[8][1]).shape)

