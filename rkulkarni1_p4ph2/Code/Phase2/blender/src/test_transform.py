

import numpy as np
import math
from pyquaternion import Quaternion

theta = 30*math.pi/180
quat = Quaternion(math.cos(theta/2), 0, 0, math.sin(theta/2))

print(quat)

print(quat.yaw_pitch_roll)

print(quat.rotation_matrix)

print(quat.rotation_matrix.T@np.array([1, 0, 0]))