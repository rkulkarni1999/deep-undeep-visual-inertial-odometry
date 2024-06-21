import numpy as np
import math
import control
kp = 2.0
ki = 1.0
kd = 2.0
tau = 0.02
dt = 0.005
pid = control.pid(kp, ki, kd, tau, dt)

print('pid ', pid.step(0, 0))
print('pid ', pid.step(2, 0))

pid2 = control.pid(kp, ki, kd, tau, dt, 3)

print(pid2.step(np.array([1,2,3]), np.array([2,3,4])))