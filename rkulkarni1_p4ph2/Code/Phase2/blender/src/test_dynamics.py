import quad_dynamics as qd
import numpy as np
import math
import tello as tello

xyz = np.array([0.0, .0, .0])
vxyz = np.array([0.0, 0.0, 0.0])
quat = np.array([1.0, .0, .0, .0])
pqr = np.array([0.0, .0, .0])

X_row = np.concatenate((xyz, vxyz, quat, pqr))
X = X_row.reshape((-1, 1))

Fb = np.array([0.0, 0.0, 0.0])
Fb.reshape((-1, 1))
Mb = np.array([0.0, 0.0, 0.0])
Mb.reshape((-1, 1))

X_dot = qd.derivative_rigidBody(X, Fb, Mb, tello)
print('X_dot', X_dot)

T_prop = np.array([0.22, 0.2, 0.20, 0.22])
torq_prop = np.array([0.0, 0.0, 0.1, 0.1])
X_dot = qd.quad_dynamics_der(X, T_prop, torq_prop, tello)
print('X_dot from quad dynamics\n', X_dot)

U_row = np.array([0.5, 0.4, 0.4, 0.5], dtype="double")
U = U_row.reshape((-1,1))

X_dot = qd.model_derivative(0, X, U, tello)
np.set_printoptions(suppress=True)
print('X_dot from full system dynamics\n', X_dot)

# Main loop should contain

"""

Physics - time will be from physics dynamics
1. Propagates physics by 5 ms (major step)
2. Position, velocity,... controller runs at every step 5 ms
4. IMU - run at the same rate as phyics
5. set position, orientation and perform camera rendering at 60 FPS (once every 16.6 ms of physics, render camera )
6.  - Guidance, motion planning - Go point - students just set the setpoints for position and yaw
7. Saving images to file or viewing on a imshow window

Blender stuff:
1. Some mechanism to stop simulation 
2. How to import external py files into blender script
Camera - one scene camera, front view, down camera

"""