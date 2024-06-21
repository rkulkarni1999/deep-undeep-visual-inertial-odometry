import quad_dynamics as qd
import numpy as np
import math
import tello as tello

xyz = np.array([0.0, .0, .0])
vxyz = np.array([0.0, 0.0, 0.0])
quat = np.array([1.0, .0, .0, .0])
pqr = np.array([0.0, .0, .0])

X_row = np.concatenate((xyz, vxyz, quat, pqr))
# X0 = X_row.reshape((-1, 1))

U_row = np.array([0.0, 0.0, 0.0, 0.0], dtype="double")
U = U_row.reshape((-1,1))

from scipy.integrate import solve_ivp

sol = solve_ivp(qd.model_derivative, [0, 0.1], X_row, method='RK45', args=(U, tello))
print(sol.y[:, -1])