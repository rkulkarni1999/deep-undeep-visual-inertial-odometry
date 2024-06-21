import numpy as np

# Rotation matrices
R0 = np.array([[1, 0, 0],
               [0, 1, 0],
               [0, 0, 1]])
R1 = np.array([[0, 0, 1],
               [0, 1, 0],
               [-1, 0, 0]])
R2 = np.array([[0, 0, -1],
               [0, -1, 0],
               [-1, 0, 0]])


# Compute delta R from {1} to {2}
delta_R_0_to_1 = np.linalg.inv(R0) @ R1
delta_R_1_to_2 = np.linalg.inv(R1) @ R2

# Angular velocity calculation function
def angular_velocity_from_rotation(delta_R):
    omega_x = (delta_R[2, 1] - delta_R[1, 2]) / 2
    omega_y = (delta_R[0, 2] - delta_R[2, 0]) / 2
    omega_z = (delta_R[1, 0] - delta_R[0, 1]) / 2
    return np.array([omega_x, omega_y, omega_z])



# Angular velocities
omega_World_to_1 = angular_velocity_from_rotation(delta_R_0_to_1) 
omega_1_to_2 = angular_velocity_from_rotation(delta_R_1_to_2)

# Print results
print("Angular Velocity from World to {1} (rad/s):", omega_World_to_1)
print("Angular Velocity from {1} to {2} (rad/s):", omega_1_to_2)
