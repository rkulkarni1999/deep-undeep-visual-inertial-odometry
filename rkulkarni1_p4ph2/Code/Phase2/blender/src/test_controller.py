import quad_dynamics as qd
import numpy as np
import math
import tello as tello
import control
import time

from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt 

# Initial condition
xyz = np.array([0.0, .0, .0])
vxyz = np.array([0.0, 0.0, 0.0])
quat = np.array([1.0, .0, .0, .0])
pqr = np.array([0.0, .0, .0])

X_row = np.concatenate((xyz, vxyz, quat, pqr))

# Simulation
t = 0.0
dt = 0.005
tend = 5
qc = control.quad_control()

start = time.time()
while t<=tend:
    WP = np.array([0.9, -0.7, -2, 0.3])
    U = qc.step(X_row, WP)
    # U = np.array([0.0, 0.0, 0.0, 0.0])
    # implement RK4 later. scipy does not have fixed step solvers. Using explicit euler integrator for now. 
    X_row = X_row + dt*qd.model_derivative(t, X_row, U, tello)
    # sol = solve_ivp(qd.model_derivative, [0, dt], X_row, method='LSODA', args=(U, tello), min_step=0.002, max_step=dt)
    t += dt

stop = time.time()

print('time taken to simulate ', tend, ' is ', stop-start)
print('final state is\n', X_row)
print('final control inputs ', U)